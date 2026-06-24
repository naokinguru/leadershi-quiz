import base64
import hashlib
import hmac
import json
import os

import requests
from flask import Flask, abort, request
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

QUESTIONS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "questions.txt")
LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET", "")
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN", "")

user_states = {}

WELCOME_MESSAGE = (
    "リーダーシップクイズへようこそ！\n"
    "メッセージを送るとクイズが始まります。"
)


def load_questions():
    questions = []
    with open(QUESTIONS_FILE, encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            question, answer, option_a, option_b, option_c = line.split(",")
            questions.append(
                {
                    "question": question,
                    "answer": answer.upper(),
                    "options": {
                        "A": option_a,
                        "B": option_b,
                        "C": option_c,
                    },
                }
            )
    return questions


def format_question(num, question_data, total):
    return (
        f"第{num + 1}問 / {total}問\n\n"
        f"{question_data['question']}\n\n"
        f"A. {question_data['options']['A']}\n"
        f"B. {question_data['options']['B']}\n"
        f"C. {question_data['options']['C']}\n\n"
        "A / B / C で答えてください"
    )


def verify_line_signature(body, signature):
    if not LINE_CHANNEL_SECRET or not signature:
        return False

    hash_value = hmac.new(
        LINE_CHANNEL_SECRET.encode("utf-8"),
        body,
        hashlib.sha256,
    ).digest()
    expected = base64.b64encode(hash_value).decode()
    return hmac.compare_digest(expected, signature)


def reply_message(reply_token, text):
    if not LINE_CHANNEL_ACCESS_TOKEN:
        return

    requests.post(
        "https://api.line.me/v2/bot/message/reply",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
        },
        json={
            "replyToken": reply_token,
            "messages": [{"type": "text", "text": text}],
        },
        timeout=10,
    )


def handle_text_message(user_id, text, reply_token):
    questions = load_questions()
    if not questions:
        reply_message(reply_token, "問題が見つかりませんでした。")
        return

    answer = text.strip().upper()
    state = user_states.get(user_id)

    if answer in ("A", "B", "C") and state is not None:
        current_index = state["index"]
        current_question = questions[current_index]
        if answer == current_question["answer"]:
            state["score"] += 1
            reply_text = "正解！\n\n"
        else:
            reply_text = f"不正解... 正解は {current_question['answer']} です。\n\n"

        state["index"] += 1

        if state["index"] >= len(questions):
            reply_text += f"クイズ終了！\n{state['score']} / {len(questions)} 問正解！"
            del user_states[user_id]
        else:
            reply_text += format_question(
                state["index"], questions[state["index"]], len(questions)
            )
    else:
        user_states[user_id] = {"index": 0, "score": 0}
        reply_text = (
            "リーダーシップクイズを始めます！\n\n"
            + format_question(0, questions[0], len(questions))
        )

    reply_message(reply_token, reply_text)


@app.route("/")
def index():
    return "LINE Bot is running. Webhook URL: /webhook", 200


@app.route("/health")
def health():
    return "ok", 200


@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data()

    if not verify_line_signature(body, signature):
        abort(400)

    events = json.loads(body.decode("utf-8")).get("events", [])
    for event in events:
        event_type = event.get("type")
        reply_token = event.get("replyToken")

        if event_type == "follow" and reply_token:
            reply_message(reply_token, WELCOME_MESSAGE)
            continue

        if event_type != "message":
            continue
        if event.get("message", {}).get("type") != "text":
            continue

        user_id = event.get("source", {}).get("userId")
        text = event.get("message", {}).get("text", "")

        if user_id and reply_token:
            handle_text_message(user_id, text, reply_token)

    return "OK", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

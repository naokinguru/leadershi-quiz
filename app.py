import os

from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "leadership-quiz-secret"

QUESTIONS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "questions.txt")


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


@app.route("/")
def index():
    session["score"] = 0
    return redirect(url_for("question", num=0))


@app.route("/question/<int:num>")
def question(num):
    questions = load_questions()
    if num >= len(questions):
        return redirect(url_for("result"))

    current = questions[num]
    return render_template(
        "question.html",
        question=current,
        num=num + 1,
        total=len(questions),
    )


@app.route("/answer/<int:num>", methods=["POST"])
def answer(num):
    questions = load_questions()
    if num >= len(questions):
        return redirect(url_for("result"))

    user_answer = request.form.get("answer", "").upper()
    if user_answer == questions[num]["answer"]:
        session["score"] = session.get("score", 0) + 1

    return redirect(url_for("question", num=num + 1))


@app.route("/result")
def result():
    questions = load_questions()
    score = session.get("score", 0)
    total = len(questions)
    return render_template("result.html", score=score, total=total)


if __name__ == "__main__":
    app.run(debug=True)

questions = [
    {
        "question": "良いリーダーが最も大切にすべきことは？",
        "options": ["A. 自分の意見を押し通す", "B. チームの意見を聞く", "C. 仕事をすべて一人でこなす"],
        "answer": "B",
    },
    {
        "question": "チームメンバーが失敗したとき、リーダーとして最初にすべきことは？",
        "options": ["A. 責める", "B. 無視する", "C. 原因を一緒に考える"],
        "answer": "C",
    },
    {
        "question": "リーダーシップの説明として正しいものは？",
        "options": ["A. 人を動かして目標に向かう力", "B. いつも一番忙しい人", "C. 命令だけを出す人"],
        "answer": "A",
    },
]

score = 0

print("=== リーダーシップクイズ ===\n")

for i, q in enumerate(questions, start=1):
    print(f"第{i}問: {q['question']}")
    for option in q["options"]:
        print(option)

    answer = input("答えを入力してください (A/B/C): ").strip().upper()

    if answer == q["answer"]:
        print("正解！\n")
        score += 1
    else:
        print(f"不正解... 正解は {q['answer']} です。\n")

print(f"結果: {score} / {len(questions)} 問正解！")

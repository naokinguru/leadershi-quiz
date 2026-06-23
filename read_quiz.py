print("=== リーダーシップクイズ ===\n")

score = 0
total = 0

with open("questions.txt", encoding="utf-8") as file:
    for line in file:
        line = line.strip()
        if not line:
            continue

        total += 1
        question, answer, option_a, option_b, option_c = line.split(",")

        print(f"第{total}問: {question}")
        print(f"A. {option_a}")
        print(f"B. {option_b}")
        print(f"C. {option_c}")

        user_answer = input("答えを入力してください (A/B/C): ").strip().upper()

        if user_answer == answer.upper():
            print("正解！\n")
            score += 1
        else:
            print(f"不正解... 正解は {answer.upper()} です。\n")

print(f"結果: {score} / {total} 問正解！")

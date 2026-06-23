name = input("名前を入力してください: ")

messages = [
    f"Hello, {name}!",
    f"{name}, have a great day!",
    f"{name}さん、こんにちは！",
    f"{name}さん、今日もよい一日を！",
]

for message in messages:
    print(message)

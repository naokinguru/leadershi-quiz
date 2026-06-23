def say_hello(name):
    print(f"こんにちは！{name}さん！")


def check_time_greeting(hour):
    if hour < 12:
        print("おはようございます")
    elif hour < 18:
        print("こんにちは")
    else:
        print("こんばんは")


say_hello("Naoki")

print("--- check_time_greeting テスト ---")
print("9時:", end=" ")
check_time_greeting(9)

print("13時:", end=" ")
check_time_greeting(13)

print("20時:", end=" ")
check_time_greeting(20)

import random

def custom_ai_response(diff):
    if diff == 0:
        return "🎉 You nailed it! Absolute legend!"
    elif diff <= 5:
        return "🔥 So close! I can feel the heat from here!"
    elif diff <= 10:
        return "🌡️ You're warm, but not burning yet. Keep trying!"
    elif diff <= 20:
        return "😐 Meh, you're kinda lukewarm. You can do better."
    elif diff <= 30:
        return "🥶 Getting chilly... you might wanna turn up the brainpower."
    else:
        return "❄️ Bro... you're basically in Antarctica right now."

def hot_cold_ai_game():
    secret_number = random.randint(1, 100)
    attempts = 0

    print("🤖 Hey! I'm thinking of a number between 1 and 100.")
    print("Try to guess it. I'll tell you how you're doing... in my own special way 😎")

    while True:
        try:
            guess = int(input("Your guess: "))
            attempts += 1
            diff = abs(secret_number - guess)

            response = custom_ai_response(diff)
            print(response)

            if guess == secret_number:
                print(f"You found it in {attempts} tries! GG!")
                break
        except ValueError:
            print("⚠️ That's not a number. Try again.")

hot_cold_ai_game()

import random
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load your API key from .env
load_dotenv()
client = OpenAI()

def get_temperature_label(diff):
    if diff == 0:
        return "correct"
    elif diff <= 2:
        return "on fire"
    elif diff <= 5:
        return "hot"
    elif diff <= 10:
        return "warm"
    elif diff <= 20:
        return "cool"
    elif diff <= 30:
        return "cold"
    elif diff <= 50:
        return "freezing"
    else:
        return "lost"


def get_gpt_feedback(diff, guess):
    temp = get_temperature_label(diff)

    try:
        response = client.chat.completions.create(
            model="gpt-4.1", 
            messages=[
                {
                    "role": "system",
                    "content": "You're a sarcastic AI in a number guessing game. Respond with personality. NEVER reveal the number or use any actual numerical distance. React based on the temperature level only (hot, warm, cold, etc)."
                },
                {
                    "role": "user",
                    "content": f"The player's guess was a {temp} guess. Say something funny or roasty."
                }
            ],
            max_tokens=25,
            temperature=1.9,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"(OpenAI error: {e})"

def hot_cold_ai_game():
    secret_number = random.randint(1, 100)
    attempts = 0

    print("🤖 I'm thinking of a number between 1 and 100.")
    print("Guess it! I'll give you feedback in my own spicy way...")

    while True:
        try:
            guess = int(input("Your guess: "))
            attempts += 1
            diff = abs(secret_number - guess)

            if guess == secret_number:
                print("🎯 You got it! Took you long enough 😏")
                print(f"(You won in {attempts} tries)")
                break

            ai_comment = get_gpt_feedback(diff, guess)
            print(ai_comment)

        except ValueError:
            print("⚠️ Not a valid number. Try again.")
        except KeyboardInterrupt:
            print("\n👋 Peace out!")
            break

hot_cold_ai_game()

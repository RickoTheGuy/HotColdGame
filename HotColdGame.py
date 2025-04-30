import random
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load your API key from .env
load_dotenv()
client = OpenAI()

def get_gpt_feedback(diff, guess):
    prompt = f"I guessed {guess}, and I was {diff} away from the correct number. Roast me."

    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You're a sarcastic AI bot in a number guessing game. Reply with funny, creative, or savage comebacks."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50,
            temperature=0.9,
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

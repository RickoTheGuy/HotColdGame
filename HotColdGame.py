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

def get_ai_intro():
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You're a sarcastic AI game host. Write a short, funny introduction "
                        "to a number guessing game between 1 and 100. Be rude, clever, and under 30 words. "
                        "Do NOT reveal the number."
                    )
                }
            ],
            max_tokens=75,
            temperature=1.3,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return "(Intro error: couldn't generate intro)"

def get_gpt_feedback(diff, guess, retries=1):
    temp = get_temperature_label(diff)

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You're a sarcastic, rude AI in a number guessing game. Your job is to insult the player "
                        "based on how close or far their guess was. Never reveal numbers. Use temperature labels like "
                        "'cold', 'hot', 'lost', etc. Be clever, disrespectful, and short. No more than 1 sentence."
                    )
                },
                {
                    "role": "user",
                    "content": f"The player's guess was labeled '{temp}'. Roast them accordingly."
                }
            ],
            max_tokens=40,
            temperature=1.5,
        )

        msg = response.choices[0].message.content.strip()

        if msg.endswith(("...", ",", "and", "but")) and retries > 0:
            print("🛠️ Message cut off, retrying...")
            return get_gpt_feedback(diff, guess, retries=retries - 1)

        return msg

    except Exception as e:
        return f"(OpenAI error: {e})"

def get_ai_outro(attempts):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"You're a sarcastic AI game host. The player guessed the number in {attempts} attempts. "
                        "Roast them one last time. Short, savage, under 30 words. Be smug."
                    )
                }
            ],
            max_tokens=50,
            temperature=1.3,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return "(Outro error: couldn't generate outro)"

def get_cheat_roast():
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You're a sarcastic AI. The player is suddenly guessing too well. "
                        "Call them out for cheating in a petty, funny, disrespectful way. Short and brutal."
                    )
                }
            ],
            max_tokens=40,
            temperature=1.2,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return "(Couldn't accuse the cheater in time...)"

def is_suspect_guess_pattern(last_guesses, diff):
    if len(last_guesses) < 3:
        return False
    guess_range = max(last_guesses) - min(last_guesses)
    if guess_range <= 5 or diff <= 2:
        return True
    return False

def hot_cold_ai_game():
    secret_number = random.randint(1, 100)
    attempts = 0
    last_guesses = []

    print(get_ai_intro())

    while True:
        try:
            guess = int(input("Your guess: "))
            attempts += 1
            diff = abs(secret_number - guess)

            last_guesses.append(guess)
            if len(last_guesses) > 3:
                last_guesses.pop(0)

            print(f"🧠 Attempt #{attempts}:")

            if guess == secret_number:
                print(get_ai_outro(attempts))
                break

            if is_suspect_guess_pattern(last_guesses, diff):
                print(get_cheat_roast())

            ai_comment = get_gpt_feedback(diff, guess)
            print(ai_comment)

        except ValueError:
            print("⚠️ That wasn’t even a number. You trying to lose on purpose?")
        except KeyboardInterrupt:
            print("\n👋 Rage quitting? Figures. I expected better. No I didn’t.")
            break

hot_cold_ai_game()

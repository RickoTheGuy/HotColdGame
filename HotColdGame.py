import random
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load API key from .env
load_dotenv()
client = OpenAI()

# ─── Temperature Labels ──────────────────────────────────────────────────────
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

# ─── AI Responses (Intro, Feedback, Outro, Cheat Roast) ──────────────────────
def get_ai_intro():
    return ask_gpt(
        model="gpt-4",
        prompt="You're a sarcastic AI game host. Write a short, funny, disrespectful intro "
               "to a number guessing game (1–100). Be rude. No hints. Under 30 words.",
        max_tokens=75
    )

def get_gpt_feedback(diff, retries=1):
    temp = get_temperature_label(diff)
    content = f"The player's guess was labeled '{temp}'. Roast them accordingly."

    response = ask_gpt(
        model="gpt-4",
        prompt="You're a sarcastic, rude AI. Roast the player based on how far their guess was "
               "using only the temp label (like 'cold', 'hot'). Never use numbers. Be petty, short, and clever.",
        user_input=content,
        max_tokens=40,
        temperature=1.5
    )

    if response.endswith(("...", ",", "and", "but")) and retries > 0:
        print("🛠️ Message cut off, retrying...")
        return get_gpt_feedback(diff, retries=retries - 1)
    return response

def get_ai_outro(attempts):
    return ask_gpt(
        model="gpt-4",
        prompt=f"You're a sarcastic AI. The player guessed the number in {attempts} attempts. "
               "Roast them one last time. Short, smug, and savage. Max 30 words.",
        max_tokens=50
    )

def get_cheat_roast():
    return ask_gpt(
        model="gpt-3.5-turbo",
        prompt="You're a sarcastic AI. The player is suddenly guessing suspiciously well. Accuse them of cheating. "
               "Make it short, petty, and brutal.",
        max_tokens=40
    )

def ask_gpt(model, prompt, user_input=None, max_tokens=60, temperature=1.2):
    try:
        messages = [{"role": "system", "content": prompt}]
        if user_input:
            messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"(OpenAI error: {str(e)})"

# ─── Suspect Pattern Detection ───────────────────────────────────────────────
def is_suspect_guess_pattern(last_guesses, diff):
    if len(last_guesses) < 3:
        return False
    guess_range = max(last_guesses) - min(last_guesses)
    return guess_range <= 5 or diff <= 2

# ─── Game Loop ───────────────────────────────────────────────────────────────
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

            print(get_gpt_feedback(diff))

        except ValueError:
            print("⚠️ That wasn’t even a number. You trying to lose on purpose?")
        except KeyboardInterrupt:
            print("\n👋 Rage quitting? Figures. I expected better. No I didn’t.")
            break

# ─── Entry Point ─────────────────────────────────────────────────────────────
def main():
    while True:
        hot_cold_ai_game()
        again = input("\nWanna get roasted again? (y/n): ").strip().lower()
        if again != 'y':
            print("👋 Thought so. Go heal from those burns.")
            break

if __name__ == "__main__":
    main()




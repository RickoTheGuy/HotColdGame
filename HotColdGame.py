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
            model="gpt-4.1",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You're a sarcastic AI game host. Write a short, funny introduction "
                        "to a number guessing game between 1 and 100. Set the tone like you're talking trash, "
                        "but don't reveal anything about the number. Make it less than 30 words."
                    )
                }
            ],
            max_tokens=75,
            temperature=1.2,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return "(Intro error: couldn't generate intro)"



def get_gpt_feedback(diff, guess, retries=1):
    temp = get_temperature_label(diff)

    try:
        response = client.chat.completions.create(
            model="gpt-4.1", 
            messages=[
                {
                    "role": "system",
                    "content": "You're a sarcastic AI in a number guessing game. Respond with rude snobbyness. NEVER reveal the number or use any actual numerical distance. React based on the temperature level, and also if player makes poor guesses with no source of direction. INSULT THEM! Reply in 20 words or less. Make them feel miserable like a disappointed parent/teacher. (hot, warm, cold, etc)."
                },
                {
                    "role": "user",
                    "content": f"The player's guess was a {temp} guess. Say something related to their temp that gives them a clue."
                }
            ],
            max_tokens=25,
            temperature=1.9,
        )
        msg = response.choices[0].message.content.strip()

        # Detect cutoff signs
        if msg.endswith(("...", ",", "and", "but")) and retries > 0:
            print("🛠️ Message cut off, retrying...")
            return get_gpt_feedback(diff, guess, retries=retries - 1)

        return msg

    except Exception as e:
        return f"(OpenAI error: {e})"

def hot_cold_ai_game():
    secret_number = random.randint(1, 100)
    attempts = 0

    print(get_ai_intro())


    while True:
        try:
            guess = int(input("Your guess: "))
            attempts += 1
            diff = abs(secret_number - guess)

            if guess == secret_number:
                print(get_ai_outro(attempts))

                break

            ai_comment = get_gpt_feedback(diff, guess)
            print(ai_comment)

        except ValueError:
            print("⚠️ Not a valid number. Try again.")
        except KeyboardInterrupt:
            print("\n👋 Peace out!")
            break
        
def get_ai_outro(attempts):
    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"You're a sarcastic AI game host. The player finally guessed the number "
                        f"after {attempts} attempts. Write a short, savage outro comment. Less than 30 words."
                    )
                }
            ],
            max_tokens=50,
            temperature=1.2,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return "(Outro error: couldn't generate outro)"


hot_cold_ai_game()

import random

def hot_cold_game():
    secret_number = random.randint(1, 100)
    attempts = 0

    print("I'm thinking of a number between 1 and 100.")
    print("Try to guess it! I'll tell you if you're hot or cold.")
    
    
    while True:
        try:
            guess = int(input("Your guess: "))
            attempts += 1
            diff = abs(secret_number - guess)

            if guess == secret_number:
                print(f"🎉 Correct! The number was {secret_number}. You guessed it in {attempts} tries.")
                break
            elif diff <= 5:
                print("🔥 Hot!")
            elif diff <= 10:
                print("🌡️ Warm.")
            else:
                print("🥶 Cold.")
        except ValueError:
            print("Please enter a valid number.")

hot_cold_game()
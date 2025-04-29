import random

def hot_cold_game():
    secret_number = random.randint(1, 100)
    attempts = 0

    print("I'm thinking of a number between 1 and 100.")
    print("Try to guess it! I'll tell you if you're hot or cold.")
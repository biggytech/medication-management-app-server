import random


def get_random_verification_code():
    number = random.randint(1000, 9999)

    return str(number)

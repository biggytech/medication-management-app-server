import random
import string

def get_random_email():
    return ''.join(random.choice(string.ascii_letters) for _ in range(7)) + "@random-email.com"

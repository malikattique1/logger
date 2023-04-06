
import random
import string


def generate_username():
    letters = string.ascii_letters
    digits = string.digits
    username = random.choice(letters) + random.choice(digits)
    for i in range(5):
        username += random.choice(letters + digits)
    return username

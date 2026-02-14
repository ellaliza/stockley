import string
from random import random, randint

def generate_sku() -> str:
    letters = string.ascii_uppercase
    sku = ""
    while True:
        idx = randint(0, len(letters) - 1)
        sku += letters[idx]
        if len(sku) == 5:
            sku += (str(random() * 100000))[0:5]
            return sku
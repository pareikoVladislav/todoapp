import random


def create_default_description():
    random_value = random.randint(1, 1_000_000)
    return f"THIS IS A DEFAULT '{random_value}' DESCRIPTION!!!!!"

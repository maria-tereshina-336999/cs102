"""This script creates a greeting message"""


def get_greeting(name: str) -> str:
    """Returns greeting"""
    return "Hello, " + name + "!"


if __name__ == "__main__":
    MESSAGE = get_greeting("World")
    print(MESSAGE)

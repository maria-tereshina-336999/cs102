"""Encrypts and decrypts text using a Vigenere cipher"""


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    k = 0
    while len(keyword) < len(plaintext):
        keyword += keyword[k % len(keyword)]
        k += 1
    for i, symb in enumerate(plaintext):
        key = keyword[i]
        shift = 0
        if key.isalpha():
            key = key.lower()
            shift = ord(key) - ord("a")
        else:
            raise Exception("Key must contain only letters; other symbol occurred")
        if symb.isalpha():
            if symb.isupper():
                ciphertext += chr((ord(symb) - ord("A") + shift) % 26 + ord("A"))
            else:
                ciphertext += chr((ord(symb) - ord("a") + shift) % 26 + ord("a"))
        else:
            ciphertext += symb
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    k = 0
    while len(keyword) < len(ciphertext):
        keyword += keyword[k % len(keyword)]
        k += 1
    for i, symb in enumerate(ciphertext):
        key = keyword[i]
        shift = 0
        if key.isalpha():
            key = key.lower()
            shift = ord(key) - ord("a")
        else:
            raise Exception("Key must contain only letters; other symbol occurred")
        if symb.isalpha():
            if symb.isupper():
                plaintext += chr((ord(symb) - ord("A") - shift) % 26 + ord("A"))
            else:
                plaintext += chr((ord(symb) - ord("a") - shift) % 26 + ord("a"))
        else:
            plaintext += symb
    return plaintext

"""encrypts and decrypts text using a Caesar cipher"""


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for symb in plaintext:
        if symb.isalpha():
            if symb.isupper():
                ciphertext += chr((ord(symb) - ord("A") + shift) % 26 + ord("A"))
            else:
                ciphertext += chr((ord(symb) - ord("a") + shift) % 26 + ord("a"))
        else:
            ciphertext += symb
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for symb in ciphertext:
        if symb.isalpha():
            if symb.isupper():
                plaintext += chr((ord(symb) - ord("A") - shift) % 26 + ord("A"))
            else:
                plaintext += chr((ord(symb) - ord("a") - shift) % 26 + ord("a"))
        else:
            plaintext += symb
    return plaintext

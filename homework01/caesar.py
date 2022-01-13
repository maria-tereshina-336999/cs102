import typing as tp


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
    alpha_s = [chr(x) for x in range(ord("a"), ord("z") + 1)]
    alpha_c = [chr(x) for x in range(ord("A"), ord("Z") + 1)]
    for symb in plaintext:
        if symb in alpha_s:
            ciphertext += alpha_s[(alpha_s.index(symb) + shift) % len(alpha_s)]
        elif symb in alpha_c:
            ciphertext += alpha_c[(alpha_c.index(symb) + shift) % len(alpha_c)]
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
    alpha_s = [chr(x) for x in range(ord("a"), ord("z") + 1)]
    alpha_c = [chr(x) for x in range(ord("A"), ord("Z") + 1)]
    for symb in ciphertext:
        if symb in alpha_s:
            plaintext += alpha_s[(alpha_s.index(symb) - shift) % len(alpha_s)]
        elif symb in alpha_c:
            plaintext += alpha_c[(alpha_c.index(symb) - shift) % len(alpha_c)]
        else:
            plaintext += symb
    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    return best_shift

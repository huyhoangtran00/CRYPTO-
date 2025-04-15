import random
from sympy import primitive_root, randprime


def vigenere_encrypt_with_int_key(plaintext, key):
    # Convert all letters to uppercase for simplicity
    plaintext = plaintext.upper()

    # Convert the integer key into a list of its digits
    key_digits = [int(digit) for digit in str(key)]

    ciphertext = []

    # Encrypt each character of the plaintext
    for i, char in enumerate(plaintext):
        if char.isalpha():  # Ensure only alphabetic characters are encrypted
            # Find the position in the alphabet (A=0, B=1, ..., Z=25)
            p_val = ord(char) - ord("A")

            # Get the corresponding digit from the key, using modulo to cycle through if necessary
            k_val = key_digits[i % len(key_digits)]

            # Vigenère cipher encryption formula: (p_val + k_val) % 26
            c_val = (p_val + k_val) % 26

            # Convert back to character and add to the result
            ciphertext.append(chr(c_val + ord("A")))
        else:
            ciphertext.append(char)  # Non-alphabet characters remain unchanged

    # Return the encrypted text as a string
    return "".join(ciphertext)


def main():
    x = "HELLO"
    bound = 1000
    p_modulor = randprime(10**bound, 10 ** (bound + 1) - 1)
    # p_modulor = 73132144049
    secret_A = random.randint(10**bound, 10 ** (bound + 1) - 1)
    # secret_A = 72031240573
    secret_B = random.randint(10**bound, 10 ** (bound + 1) - 1)
    # secret_B = 41744673185
    g_primitive_root = 3
    print("modulor:", p_modulor)
    print(f"Secret_A: {secret_A}, Secret_B: { secret_B}")

    print("g_primitive_root:", g_primitive_root)

    # p, g, public_B
    public_A = pow(g_primitive_root, secret_A, p_modulor)
    public_B = pow(g_primitive_root, secret_B, p_modulor)

    print(f"public_A: {public_A}, public_B: { public_B}")
    key_A = pow(public_B, secret_A, p_modulor)
    key_B = pow(public_A, secret_B, p_modulor)
    print(f"private key: ", key_A)
    print(key_A == key_B)
    print(vigenere_encrypt_with_int_key(x, key_A))


main()

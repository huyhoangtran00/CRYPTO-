from algorithms.helper import *
import gmpy2
import concurrent.futures
import math
from dataclasses import dataclass


@dataclass
class RSA:
    p: int
    q: int
    n: int
    public_key: int
    secret_key: int


# Helper function to convert integer to string using custom decryption

def choose_e(phi):
    e = phi - 1
    if math.gcd(phi, e) == 1:
        return e
    else:
        for candidate in range(phi, 2, -2):  # Start from 3, check odd numbers
            if math.gcd(phi, candidate) == 1:
                return candidate
        raise ValueError("Could not find a suitable 'e' that is coprime to phi.")


def get_decryption_key(e, phi):
    return pow(e, -1, phi)


def enc(p, e, n):
    return pow(p, e, n)


def dec(c, d, n):
    return pow(c, d, n)


def rsa_encrypt(message):
    bound = 1024 #8192
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_p = executor.submit(generate_n_bit_prime, bound)
        future_q = executor.submit(generate_n_bit_prime, bound)
        p = gmpy2.mpz(future_p.result())
        q = gmpy2.mpz(future_q.result())

    n = gmpy2.mpz(gmpy2.mul(p, q))
    phi = gmpy2.mul((p - 1), (q - 1))
    e = gmpy2.mpz(choose_e(phi))

    plaintext = int_encrypt(message)
    encrypted = enc(plaintext, e, n)
    d = gmpy2.mpz(get_decryption_key(e, phi))
    public_key = (int(e), int(n))
    decrypted = rsa_decrypt(encrypted, d, n)
    private_key = (int(d), int(n))
    
    return encrypted, private_key, public_key, decrypted

def rsa_decrypt(encrypted, private_key, n):
    decrypted_num = dec(encrypted, private_key, n)
    return decrypt_to_str(decrypted_num)


def rsa_signature(message):
    bound = 1024 #8192
    p = gmpy2.mpz(generate_n_bit_prime(bound))
    q = gmpy2.mpz(generate_n_bit_prime(bound))

    n = gmpy2.mul(p, q)
    phi = gmpy2.mul((p - 1), (q - 1))
    e = choose_e(phi)

    plaintext = int_encrypt(message)
    d = get_decryption_key(e, phi)
    signature = enc(plaintext, d, n)
    private_key = (int(d), int(n))
    public_key = (int(e), int(n))
    return signature, private_key, public_key


def rsa_verify(message, signature, public_key):
    plaintext = int_encrypt(message)
    e, n = public_key
    decrypted_signature = dec(signature, e, n)

    return plaintext == decrypted_signature




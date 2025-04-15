# p: 6 chu so nguyen tu => Tim phan tu nguyen thuy
# a: 5 chu so

from hashlib import sha256
from algorithms.helper import *
import requests

elgamal_bits = 2048


class ElGamal:
    def __init__(self, p, q, a, k):
        self.p = p  # prime number self.a = a  # random number
        self.alpha = primitive_root(p, q)
        self.beta = pow(self.alpha, a, p)
        self.a = a
        self.k = k

    def encrypt(self, message: int) -> (int, int):
        c_1 = pow(self.alpha, self.k, self.p)
        c_2 = (message * pow(self.beta, self.k, self.p)) % self.p
        return (c_1, c_2, self.alpha)

    def decrypt(self, c_1, c_2) -> str:
        temp = pow(pow(c_1, self.a, self.p), -1, self.p) % self.p
        return decrypt_to_str(c_2 * (temp) % self.p)


def primitive_root(p, q):
    for i in range(2, p):
        if is_primitive_root(i, p, q):
            return i


def is_primitive_root(a, p, q):
    if pow(a, 2, p) == 1:
        return False

    if pow(a, p, q) == 1:
        return False

    return True


def generate_safe_prime(bit_size):
    response = requests.get(f"https://2ton.com.au/getprimes/random/{bit_size}")

    p, q = 0, 0
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON data
        safe_primes_data = response.json()

        p = int(safe_primes_data["p"]["base10"])
        q = int(safe_primes_data["q"]["base10"])
    else:
        print(f"Error: {response.status_code}")

    return p, q


def generate_keys(key_size: int):
    # generate safe prime
    p, q = generate_safe_prime(key_size)
    a = generate_random_number(p)
    k = generate_random_number(p)

    return p, q, a, k


class SigningElGamal(ElGamal):
    def sign(self, message: int) -> (int, int):
        sig_1 = pow(self.alpha, self.k, self.p)
        sig_2 = ((message - self.a * sig_1) * pow(self.k, -1, self.p - 1)) % (
            self.p - 1
        )

        return (sig_1, sig_2)

    def verify(self, message: int, sig_1, sig_2) -> bool:
        lhs = pow(self.beta, sig_1, self.p) * pow(sig_1, sig_2, self.p) % self.p
        rhs = pow(self.alpha, message, self.p)
        print("Elgamal parameters:")
        print("alpha: ", self.alpha)
        print("beta: ", self.beta)
        print("p: ", self.p)
        return lhs == rhs


def elgamal_cryptography(message_str):
    p, q, a, k = generate_keys(elgamal_bits)
    elgamal = ElGamal(p, q, a, k)
    message = int_encrypt(message_str)
    c_1, c_2, alpha = elgamal.encrypt(message)
    decrypted = elgamal.decrypt(c_1, c_2)
    return c_1, c_2, p, a, alpha, decrypted


def elgamal_signature(message_str):
    p, q, a, k = generate_keys(elgamal_bits)
    signed_elgamal = SigningElGamal(p, q, a, k)
    message = int_encrypt(message_str)
    sig_1, sig_2 = signed_elgamal.sign(message)
    verify = signed_elgamal.verify(message, sig_1, sig_2)
    return sig_1, sig_2, signed_elgamal.alpha, signed_elgamal.beta, signed_elgamal.p


def elgamal_encrypt(message: int, alpha: int, beta: int, p: int, k: int) -> (int, int):
    """
    Hàm mã hóa thông điệp với hệ mật ElGamal.

    Args:
        message (int): Thông điệp cần mã hóa.
        alpha (int): Số gốc nguyên thủy (primitive root) của hệ mật.
        beta (int): Khóa công khai.
        p (int): Số nguyên tố lớn.
        k (int): Số ngẫu nhiên dùng trong quá trình mã hóa.

    Returns:
        (int, int): Cặp mã hóa (c1, c2).
    """
    c_1 = pow(alpha, k, p)
    c_2 = (message * pow(beta, k, p)) % p
    return c_1, c_2


def elgamal_decrypt(c_1: int, c_2: int, a: int, p: int) -> str:
    """
    Hàm giải mã thông điệp với hệ mật ElGamal.

    Args:
        c_1 (int): Phần đầu của cặp mã hóa.
        c_2 (int): Phần thứ hai của cặp mã hóa.
        alpha (int): Số gốc nguyên thủy (primitive root).
        a (int): Khóa bí mật.
        p (int): Số nguyên tố lớn.

    Returns:
        int: Thông điệp gốc.
    """
    temp = pow(pow(c_1, a, p), -1, p)  # Inverse of alpha^a mod p
    decrypted = (c_2 * temp) % p
    return decrypt_to_str(decrypted)


def elgamal_sign(message: int, alpha: int, a: int, k: int, p: int) -> (int, int):
    """
    Hàm ký thông điệp với hệ mật ElGamal.

    Args:
        message (int): Thông điệp cần ký.
        alpha (int): Số gốc nguyên thủy.
        a (int): Khóa bí mật của người ký.
        k (int): Số ngẫu nhiên dùng trong quá trình ký.
        p (int): Số nguyên tố lớn.

    Returns:
        (int, int): Cặp chữ ký (sig_1, sig_2).
    """
    sig_1 = pow(alpha, k, p)
    sig_2 = ((message - a * sig_1) * pow(k, -1, p - 1)) % (p - 1)
    return sig_1, sig_2


def elgamal_verify(
    message_str: str, sig_1: int, sig_2: int, alpha: int, beta: int, p: int
) -> bool:
    """
    Hàm xác minh chữ ký của thông điệp trong hệ mật ElGamal.

    Args:
        message (int): Thông điệp cần xác minh.
        sig_1 (int): Phần đầu của chữ ký.
        sig_2 (int): Phần thứ hai của chữ ký.
        alpha (int): Số gốc nguyên thủy.
        beta (int): Khóa công khai.
        p (int): Số nguyên tố lớn.

    Returns:
        bool: Trả về True nếu chữ ký hợp lệ, False nếu không hợp lệ.
    """
    message = int_encrypt(message_str)
    lhs = (pow(beta, sig_1, p) * pow(sig_1, sig_2, p)) % p
    rhs = pow(alpha, message, p)
    return lhs == rhs

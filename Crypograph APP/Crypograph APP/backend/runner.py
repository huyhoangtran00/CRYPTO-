"""
File to run algorithms
"""

from algorithms.rsa import *
from algorithms.elgamal import *
from algorithms.ECElGamal import *
from algorithms.helper import *


# RSA
async def run_rsa_enc(message: str):
    # Chạy tệp module1.py và truyền input_value cho nó
    encrypted, private_key, public_key, decrypted = rsa_encrypt(message)
    return {
        "encrypted": str(encrypted),
        "private_key": str(private_key),
        "public_key": str(public_key),
        "decrypted": str(decrypted),
    }


async def run_rsa_dec(encrypted: int, private_key: int, n: int):
    # Chạy tệp module1.py và truyền input_value cho nó
    decrypted = rsa_decrypt(encrypted, private_key, n)
    return {"decrypted": str(decrypted)}


async def run_rsa_sig(message: str):
    # Chạy tệp module1.py và truyền input_value cho nó
    signature, private_key, public_key = rsa_signature(message)
    return {
        "signature": str(signature),
        "private_key (d, n)": str(private_key),
        "public_key (e, n)": str(public_key),
    }


async def run_rsa_ver(message: str, encrypted: int, public_key):
    # Chạy tệp module1.py và truyền input_value cho nó
    verify = rsa_verify(message, encrypted, public_key)
    return {"Verified": verify}


# ElGamal
async def run_elgamal_enc(message: str):
    c_1, c_2, p, a, alpha, decrypted = elgamal_cryptography(message)
    return {
        "encrypted": f"({c_1}, {c_2})",
        "private_key(p, a)": f"({p}, {a})",
        "public_key(p, alpha)": f"({p}, {alpha})",
        "decrypted": str(decrypted),
    }


async def run_elgamal_sig(message: str):
    sig_1, sig_2, alpha, beta, p = elgamal_signature(message)
    return {
        "signature": f"({sig_1}, {sig_2})",
        "alpha": str(alpha),
        "beta": str(beta),
        "p": str(p),
    }


async def run_elgamal_dec(c_1: int, c_2: int, a: int, p: int):
    decrypted = elgamal_decrypt(c_1, c_2, a, p)
    return {"decrypted": str(decrypted)}


async def run_elgamal_ver(
    message: str, sig_1: int, sig_2: int, alpha: int, beta: int, p: int
):
    verify = elgamal_verify(message, sig_1, sig_2, alpha, beta, p)
    return {"verify": str(verify)}


# Elliptic vs ECDSA
async def run_ecelgamal_enc(message: str):
    # Chuyển đổi message thành điểm trên đường cong (giả định về cách ánh xạ message thành tọa độ)
    point_1, point_2 = message_to_point(message)
    plain_point = (point_1, point_2)  # Giả sử điểm hợp lệ

    # Tạo khóa riêng và khóa công khai
    private_key = random.randint(1, n - 1)
    public_key = scalar_mult(private_key, G)

    # Mã hóa điểm thông điệp với khóa công khai
    c_1, c_2 = encrypt(plain_point, public_key)

    # Giải mã để kiểm tra tính đúng đắn
    decrypted_point = decrypt((c_1, c_2), private_key)

    return {
        "message_to_point": f"{point_1},{point_2}",
        "encrypted": f"{c_1}, {c_2}",
        "private_key": f"{private_key}",
        "public_key": f"{public_key}",
        "decrypted": str(decrypted_point),
    }


# Hàm ký số ECDSA với đầu vào là thông điệp cần ký
async def run_ecelgamal_sig(message: str, private_key: int):
    # Tạo khóa riêng và khóa công khai
    public_key = scalar_mult(private_key, G)

    # Ký số
    sig_1, sig_2 = ecdsa_sign(message, private_key)

    # Xác minh chữ ký để kiểm tra tính đúng đắn
    verify = ecdsa_verify(message, (sig_1, sig_2), public_key)

    return {
        "signature(r,s)": f"({sig_1}, {sig_2})",
        "public_key(x,y)": f"{public_key}",
        "verify": str(verify),
    }


# Hàm giải mã ElGamal với đầu vào là cặp mã và khóa riêng
async def run_ecelgamal_dec(ciphertext, private_key):
    # Giải mã cặp mã hóa ElGamal
    c_1, c_2 = ciphertext
    decrypted_point = decrypt((c_1, c_2), private_key)
    return {"decrypted_point": str(decrypted_point)}


# Hàm xác minh chữ ký ECDSA với đầu vào là thông điệp, chữ ký và khóa công khai
async def run_ecelgamal_ver(message: str, signature, public_key):
    # Xác minh chữ ký với thông điệp và khóa công khai
    verify = ecdsa_verify(message, signature, public_key)
    return {"verify": str(verify)}


async def check_prime_aks(n: int):
    return aks_prime_test(n)

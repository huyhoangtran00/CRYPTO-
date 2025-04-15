import hashlib
import random
from curves import SECP521r1


p, a, b, G, n = SECP521r1()


def mod_inverse(k, p):
    return pow(k, p - 2, p)


def point_add(p1, p2):
    """Cộng hai điểm trên đường cong"""
    if p1 == (0, 0):
        return p2
    if p2 == (0, 0):
        return p1

    x1, y1 = p1
    x2, y2 = p2

    if x1 == x2 and y1 == y2:
        # Tính m = (3 * x1^2 + a) / (2 * y1) với 2 * y1 đã được modulo p
        m = (3 * x1**2 + a) * mod_inverse(2 * y1 % p, p) % p
    else:
        # Tính m = (y2 - y1) / (x2 - x1)
        m = (y2 - y1) * mod_inverse((x2 - x1) % p, p) % p

    x3 = (m**2 - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p
    return (x3, y3)


def point_multiply(k, P):
    """Nhân một điểm với một số nguyên"""
    R = (0, 0)
    while k:
        if k & 1:
            R = point_add(R, P)
        P = point_add(P, P)
        k >>= 1
    return R


def ecdsa_sign(private_key, message):
    """Ký một thông điệp bằng ECDSA"""
    # Bước 1: Hash thông điệp
    message_hash = int(hashlib.sha256(message.encode()).hexdigest(), 16)
    while True:
        # Bước 2: Chọn số ngẫu nhiên k trong khoảng (1, n-1)
        k = random.randint(1, n - 1)

        # Bước 3: Tính R = k * G
        R = point_multiply(k, G)
        r = R[0] % n
        if r == 0:
            continue

        # Bước 4: Tính s
        k_inv = mod_inverse(k, n)
        s = (k_inv * (message_hash + private_key * r)) % n
        if s == 0:
            continue

        return (r, s)


def ecdsa_verify(public_key, message, signature):
    """Xác minh chữ ký bằng ECDSA"""
    r, s = signature

    # Bước 1: Hash thông điệp
    message_hash = int(hashlib.sha256(message.encode()).hexdigest(), 16)

    # Bước 2: Tính w = s^(-1) mod n
    w = mod_inverse(s, n)

    # Bước 3: Tính u1 và u2
    u1 = (message_hash * w) % n
    u2 = (r * w) % n

    # Bước 4: Tính điểm P = u1 * G + u2 * public_key
    P1 = point_multiply(u1, G)
    P2 = point_multiply(u2, public_key)
    P = point_add(P1, P2)

    # Bước 5: Kiểm tra r == x(P) mod n
    if P == (0, 0):
        return False  # Kiểm tra điểm vô cùng
    R = P[0] % n
    print("R: ", R.bit_length(), "   r: ", r.bit_length())
    return R == r

    #
    # a = 0
    # b = 7
    # p = 43


print("p: ", p.bit_length())
print("a: ", a.bit_length())
print("b: ", b.bit_length())
print(f"G:  ({G[0].bit_length()}, {G[1].bit_length()})")
print("n: ", n.bit_length())


private_key = random.randint(1, n - 1)
public_key = point_multiply(private_key, G)

message = "Hello, Duc Anh!"
signature = ecdsa_sign(private_key, message)

print("Private Key:", private_key.bit_length())
print(f"Public Key: ({public_key[0].bit_length()}, {public_key[1].bit_length()})")
print("Message:", message)
print(f"Signature: {signature[0].bit_length()}, {signature[1].bit_length()}")

# Xác minh chữ ký
is_valid = ecdsa_verify(public_key, message, signature)
print("Signature valid:", is_valid)

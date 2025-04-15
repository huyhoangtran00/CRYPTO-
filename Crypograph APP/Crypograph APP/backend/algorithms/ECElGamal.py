import hashlib
import random
from algorithms.curves import SECP521r1

# Khởi tạo các tham số đường cong SECP521r1
p, a, b, G, n = SECP521r1()

def mod_sqrt(a, p):
    """Tính căn bậc hai modulo p (nếu có) sử dụng thuật toán Tonelli-Shanks"""
    # Trả về căn bậc hai của a mod p, nếu có
    if pow(a, (p - 1) // 2, p) != 1:
        return None  # Không có căn bậc hai (a không phải là một số chính phương mod p)
    # Trường hợp p ≡ 3 (mod 4) thì có thể tính trực tiếp
    if p % 4 == 3:
        return pow(a, (p + 1) // 4, p)
    
    # Thuật toán Tonelli-Shanks
    s = 0
    q = p - 1
    while q % 2 == 0:
        s += 1
        q //= 2
    z = 2
    while pow(z, (p - 1) // 2, p) == 1:
        z += 1
    m = s
    c = pow(z, q, p)
    t = pow(a, q, p)
    r = pow(a, (q + 1) // 2, p)
    while t != 0 and t != 1:
        t2i = t
        i = 0
        for i in range(1, m):
            t2i = pow(t2i, 2, p)
            if t2i == 1:
                break
        b = pow(c, 2 ** (m - i - 1), p)
        m = i
        c = pow(b, 2, p)
        t = (t * b * b) % p
        r = (r * b) % p
    return r if t == 1 else None

def message_to_point(message):
    # Băm thông điệp
    hashed_message = hashlib.sha512(message.encode()).hexdigest()
    
    # Lấy 128 ký tự hex đầu tiên (64 byte) và chuyển thành số nguyên
    x = int(hashed_message[:128], 16)  # Dùng 128 ký tự hex (64 byte)

    # Tính toán giá trị phải của phương trình đường cong elliptic: x^3 + ax + b mod p
    rhs = (x**3 + a * x + b) % p

    # Tính căn bậc hai modulo p
    y = mod_sqrt(rhs, p)
    
    # Nếu không có căn bậc hai, thử với giá trị x khác (tăng x)
    attempts = 0
    while y is None and attempts < 100:
        x += 1  # Tăng x để thử lại
        rhs = (x**3 + a * x + b) % p
        y = mod_sqrt(rhs, p)
        attempts += 1
    
    if y is None:
        raise ValueError("Không thể tìm thấy một điểm hợp lệ trên đường cong.")
    
    # Đảm bảo y có giá trị dương
    if y % 2 == 1:
        y = p - y
    
    return (x, y)

# Hàm tính nghịch đảo modulo sử dụng thuật toán Euclid mở rộng
def mod_inv(x, p):
    if x == 0:
        raise ZeroDivisionError("Không tồn tại nghịch đảo")
    lm, hm = 1, 0
    low, high = x % p, p
    while low > 1:
        ratio = high // low
        nm, new = hm - lm * ratio, high - low * ratio
        lm, low, hm, high = nm, new, lm, low
    return lm % p

# Phép cộng điểm trên đường cong elliptic
def point_add(P, Q):
    if P is None:
        return Q
    if Q is None:
        return P
    if P == Q:
        if P[1] == 0:
            return None  # Điểm tại vô cực
        l = (3 * P[0] * P[0] + a) * mod_inv(2 * P[1], p) % p
    else:
        l = (Q[1] - P[1]) * mod_inv(Q[0] - P[0], p) % p
    x = (l * l - P[0] - Q[0]) % p
    y = (l * (P[0] - x) - P[1]) % p
    return (x, y)

# Phép nhân điểm (nhân đôi và cộng - Double and Add)
def scalar_mult(k, P):
    R = None
    while k:
        if k & 1:
            R = point_add(R, P)
        P = point_add(P, P)
        k >>= 1
    return R

# Mã hóa ElGamal trên đường cong elliptic
def encrypt(plain_point, public_key):
    k = random.randint(1, n - 1)
    C1 = scalar_mult(k, G)  # Điểm công khai
    shared_secret = scalar_mult(k, public_key)
    C2 = point_add(plain_point, shared_secret)  # Tạo điểm mã hóa
    return (C1, C2)

# Giải mã ElGamal trên đường cong elliptic
def decrypt(ciphertext, private_key):
    C1, C2 = ciphertext
    shared_secret = scalar_mult(private_key, C1)
    neg_shared_secret = (shared_secret[0], -shared_secret[1] % p)  # Điểm đối
    plain_point = point_add(C2, neg_shared_secret)
    return plain_point

# Tạo chữ ký số ECDSA
def ecdsa_sign(message, private_key):
    z = int(hashlib.sha256(message.encode()).hexdigest(), 16)  # Băm thành số nguyên
    while True:
        k = random.randint(1, n - 1)
        R = scalar_mult(k, G)
        r = R[0] % n
        if r == 0:
            continue
        k_inv = mod_inv(k, n)
        s = (k_inv * (z + r * private_key)) % n
        if s != 0:
            break
    return (r, s)

# Xác minh chữ ký số ECDSA
def ecdsa_verify(message, signature, public_key):
    r, s = signature
    if not (1 <= r < n and 1 <= s < n):
        return False
    z = int(hashlib.sha256(message.encode()).hexdigest(), 16)
    w = mod_inv(s, n)
    u1 = (z * w) % n
    u2 = (r * w) % n
    P = point_add(scalar_mult(u1, G), scalar_mult(u2, public_key))
    return P is not None and (P[0] % n) == r

# Chạy thử mã hóa/giải mã và ký/xác minh
def main():
    # Tạo khóa riêng và khóa công khai
    private_key = random.randint(1, n - 1)
    public_key = scalar_mult(private_key, G)

    # Điểm để mã hóa (ví dụ dữ liệu hoặc thông điệp dưới dạng tọa độ trên đường cong)
    plain_point = (123456, 789012)  # Đây là ví dụ, điểm cần nằm trên đường cong elliptic

    print("Public key:", public_key)

    # Mã hóa và giải mã
    ciphertext = encrypt(plain_point, public_key)
    decrypted_point = decrypt(ciphertext, private_key)

    print("Original point:", plain_point)
    print("Ciphertext:", ciphertext)
    print("Decrypted point:", decrypted_point)

    # Kiểm tra mã hóa/giải mã thành công
    if plain_point == decrypted_point:
        print("Decryption successful!")
    else:
        print("Decryption failed!")

    # Ký và xác minh thông điệp
    message = "Hello, Elliptic Curve!"
    signature = ecdsa_sign(message, private_key)
    is_valid = ecdsa_verify(message, signature, public_key)

    print("Message:", message)
    print("Signature:", signature)
    print("Signature valid:", is_valid)


if __name__ == "__main__":
    main()

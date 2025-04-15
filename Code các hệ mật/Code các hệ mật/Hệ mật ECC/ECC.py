import random
import gmpy2
from gmpy2 import mpz

# Sử dụng các giá trị lớn hơn ở dạng hex
p = mpz("AADD9DB8DBE9C48B3FD4E6AE33C9FC07CB308DB3B3C9D20ED6639CCA703308717D4D9B009BC66842AECDA12AE6A380E62881FF2F2D82C68528AA6056583A48F3", 16)
a = mpz("7830A3318B603B89E2327145AC234CC594CBDD8D3DF91610A83441CAEA9863BC2DED5D5AA8253AA10A2EF1C98B9AC8B57F1117A72BF2C7B9E7C1AC4D77FC94CA", 16)
b = mpz("3DF91610A83441CAEA9863BC2DED5D5AA8253AA10A2EF1C98B9AC8B57F1117A72BF2C7B9E7C1AC4D77FC94CADC083E67984050B75EBAE5DD2809BD638016F723", 16)
G = (mpz("81AEE4BDD82ED9645A21322E9C4C6A9385ED9F70B5D916C1B43B62EEF4D0098EFF3B1F78E2D0D48D50D1687B93B97D5F7C6D5047406A5E688B352209BCB9F822", 16),
     mpz("7DDE385D566332ECC0EABFA9CF7822FDF209F70024A57B1AA000C55B881F8111B2DCDE494A5F485E5BCA4BD88A2763AED1CA2B2FA8F0540678CD1E0F3AD80892", 16))
message = "20160091143476977738780"

def mod_inv(x, p):
    return gmpy2.invert(x, p)

def point_add(P, Q, a, p):
    if P == "O":
        return Q
    if Q == "O":
        return P
    (x1, y1), (x2, y2) = P, Q
    if x1 == x2 and y1 == (-y2) % p:
        return "O"
    
    if P == Q:
        m = (3 * x1**2 + a) * mod_inv(2 * y1, p) % p
    else:
        m = (y2 - y1) * mod_inv(x2 - x1, p) % p
    
    x3 = (m**2 - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p
    return (x3, y3)
# Phép nhân vô hướng (dP) sử dụng phương pháp Double-and-Add -> bạn Hoàng Bắc Giang đã giải thích quá hay kkk
def scalar_mult(d, P, a, p):
    Q = "O"
    while d > 0:
        if d % 2 == 1:
            Q = point_add(Q, P, a, p)
        P = point_add(P, P, a, p)
        d //= 2
    return Q

def generate_keys(G, a, p):
    private_key = mpz(random.randint(1, int(p - 1)))
    public_key = scalar_mult(private_key, G, a, p)
    return private_key, public_key

def map_integer_to_point(m, a, b, p):
    x = m
    while True:
        rhs = (x**3 + a * x + b) % p
        y = mod_sqrt(rhs, p)
        if y is not None:
            
            return (x, y)
        x = (x + 1) % p

def mod_sqrt(a, p):
    if gmpy2.legendre(a, p) != 1:
        return None
    return gmpy2.powmod(a, (p + 1) // 4, p) if p % 4 == 3 else None

def encrypt(m, G, public_key, a, b, p):
    M = map_integer_to_point(m, a, b, p)
    k = mpz(random.randint(1, int(p - 1)))
    M1 = scalar_mult(k, G, a, p)
    M2 = point_add(M, scalar_mult(k, public_key, a, p), a, p)
    return M1, M2, M

def decrypt(M1, M2, private_key, a, p):
    S = scalar_mult(private_key, M1, a, p)
    S_neg = (S[0], -S[1] % p)
    M = point_add(M2, S_neg, a, p)
    return M

# Số nguyên `m` cần mã hóa
m = mpz(message, 10)
private_key, public_key = generate_keys(G, a, p)
M1, M2, (x_anh_xa_tu_eliptc, y_anh_xa_tu_eliptc) = encrypt(m, G, public_key, a, b, p)
decrypted_M = decrypt(M1, M2, private_key, a, p)

print("Khóa riêng:", private_key)
print("Khóa công khai:", str(public_key[0]), str(public_key[1]))
print("Thông điệp đã mã hóa (M1, M2):", (str(M1[0]), str(M1[1])), (str(M2[0]), str(M2[1])))
print("Thông điệp giải mã dưới dạng điểm:", (str(decrypted_M[0]), str(decrypted_M[1])))
with open("ecc_result.txt",  "w", encoding="utf-8") as file:
    file.write("message: " + message + "\n")
    file.write("\n")
    file.write("message được ánh xạ sang đường cong eliptic:" + "\n")
    file.write("x: " + str(x_anh_xa_tu_eliptc) + "\n")
    file.write("y: " + str(y_anh_xa_tu_eliptc) + "\n")
    file.write("\n")
    file.write("p: " + str(p) + "\n")
    file.write("a: " +  str(a) + "\n")
    file.write("b: " + str(b) + "\n")
    file.write("\n")
    file.write("Ta được đường cong eliptic:" "y^2 = x^3 + " + str(a) + "x + " + str(b) + "mod (" + str(p) + ")\n")
    file.write("\n")
    file.write("Điểm sinh G" + "\n")
    file.write("x: " + str(G[0]) + "\n")
    file.write("y: " + str(G[1]) + "\n")
    file.write("\n")

    file.write("Khóa riêng: " + str(private_key) + "\n")
    file.write("Khóa công khai: "  + "\n")
    file.write("x: " + str(public_key[0]) + "\n")
    file.write("y: " + str(public_key[1]) + "\n")
    file.write("\n")
    file.write("Thông điệp đã mã hóa (M1, M2): "  +"\n")
    file.write("M1: " + str(M1[0]) + " " + str(M1[1]) + "\n")
    file.write("M2: " + str(M2[0]) + " " + str(M2[1]) + "\n")
    file.write("Thông điệp giải mã dưới dạng điểm: " + "\n")
    file.write("x: " + str(decrypted_M[0]) + "\n")
    file.write("y: " + str(decrypted_M[1]) + "\n")

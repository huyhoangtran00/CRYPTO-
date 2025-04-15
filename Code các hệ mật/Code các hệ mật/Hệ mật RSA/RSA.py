import sys
import time
import gmpy2
from gmpy2 import mpz
from algorithm import Alogrithm  # Giữ nguyên nếu bạn vẫn cần hàm text_to_numbers từ Alogrithm

class RSA:
    # Hàm sinh khóa RSA
    @staticmethod
    def generate_rsa_keys(digit_count):
        # Số bit cần thiết cho số nguyên có 'digit_count' chữ số thập phân
        bit_count = int(digit_count * 3.32)  # Đổi từ chữ số thập phân sang bit
        
        # Sử dụng gmpy2 để tạo số nguyên tố ngẫu nhiên
        rand_state = gmpy2.random_state()  # Tạo trạng thái ngẫu nhiên
        p = gmpy2.next_prime(gmpy2.mpz_urandomb(rand_state, bit_count))
        q = gmpy2.next_prime(gmpy2.mpz_urandomb(rand_state, bit_count))
        n = p * q
        phi_n = (p - 1) * (q - 1)
        e = 65537
        d = gmpy2.invert(e, phi_n)  # Nghịch đảo modulo

        print(f"p = {p}")
        print(f"q = {q}")
        print(f"n = {n}")
        print(f"phi_n = {phi_n}")
        print(f"e = {e}")
        print(f"d = {d}")

        return (e, n), (d, n)

    @staticmethod
    def encrypt(plaintext, public_key):
        e, n = public_key
        numbers = mpz(Alogrithm.text_to_numbers(plaintext))
        ciphertext = gmpy2.powmod(numbers, e, n)  # Sử dụng powmod để tính (numbers^e) % n
        return str(ciphertext)

    @staticmethod
    def decrypt(ciphertext, private_key):
        d, n = private_key
        decrypted_number = gmpy2.powmod(mpz(ciphertext), d, n)  # Sử dụng powmod để tính (ciphertext^d) % n
        return decrypted_number

    @staticmethod
    def sig(plaintext, public_key):
        a, n = public_key
        numbers = mpz(Alogrithm.text_to_numbers(plaintext))
        signature = gmpy2.powmod(numbers, a, n)  # Sử dụng powmod cho chữ ký
        return str(signature)

    @staticmethod
    def ver(signature, private_key, h_x):
        b, n = private_key
        decrypted_signature = gmpy2.powmod(mpz(signature), b, n)
        return str(decrypted_signature) == h_x


# Redirect output to file with UTF-8 encoding
with open("rsa.txt", "w", encoding="utf-8") as f:
    sys.stdout = f  # Redirect output to the file

    start_time = time.time()

    x = "hoangvaduong"
    print(f"x = {Alogrithm.text_to_numbers(x)}")

    public_key, private_key = RSA.generate_rsa_keys(70000)  # Thay đổi 'digit_count' nếu cần

    print("Sau khi mã hóa:")
    cipher_text = RSA.encrypt(x, public_key)
    print(cipher_text)
    plain_text = RSA.decrypt(cipher_text, private_key)
    print(f"Sau khi giải mã:\n{plain_text}")

    h_x = Alogrithm.text_to_numbers(x)

    print("===================================================================")
    print("Chữ ký là:")
    print(cipher_text)
    ver_sig = RSA.ver(cipher_text, private_key, h_x)

    print("Xác minh chữ ký:")

    if ver_sig:
        print("Chữ ký hợp lệ")
    else:
        print("Chữ ký không hợp lệ")

    end_time = time.time()
    print(f"Thời gian chạy là {end_time - start_time}")

sys.stdout = sys.__stdout__  # Reset stdout về mặc định

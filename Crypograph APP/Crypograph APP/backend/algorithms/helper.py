from sympy import randprime
from sympy import isprime, factorint, Poly
from sympy import prime
import random
import math

# Kiểm tra số nguyên tố với AKS
def aks_prime_test(n):
    # Bước 1: Kiểm tra điều kiện cơ bản
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    # Bước 2: Tính m (m là giá trị nhỏ nhất sao cho m*m >= log^2(n))
    m = int(math.floor(math.exp(math.log(n) ** 2 / math.log(math.log(n)))))

    # Bước 3: Kiểm tra nếu n không chia hết cho các số nguyên tố nhỏ hơn hoặc bằng m
    for i in range(2, m + 1):
        if n % i == 0:
            return False

    # Bước 4: Kiểm tra các điều kiện đồng dư
    r = 2
    while True:
        r += 1
        if r > math.log(n) ** 2:
            break
        if n % r == 0:
            return False

    # Bước 5: Kiểm tra sự đồng nhất của các đa thức
    for i in range(2, m + 1):
        poly = Poly(x ** i - 1, x)
        if poly.coeff(0) != 0:
            return False

    return True


def generate_prime(digit_bound):
    upper_bound = 2  # Smallest 6-digit number
    lower_bound = digit_bound
    prime_number = randprime(lower_bound, upper_bound)
    return prime_number


def generate_n_bit_prime(n):
    lower_bound = 1 << (n - 1)  # Smallest n-bit number (e.g., 2^(n-1))
    upper_bound = (1 << n) - 1  # Largest n-bit number (e.g., 2^n - 1)
    return randprime(lower_bound, upper_bound)


def int_encrypt(x):
    X = 0
    base = 256  # Sử dụng hệ cơ số 256 cho ký tự ASCII
    for i in range(len(x)):
        X += ord(x[i]) * (base ** (len(x) - i - 1))
    return X

def decrypt_to_str(n):
    result = []
    base = 256
    while n > 0:
        remainder = n % base  # Get the remainder in base 256 (for a-z)
        char = chr(remainder)  # Convert remainder to uppercase letter
        result.append(char)
        n = n // base  # Move to the next "digit"
    return "".join(result[::-1])  # Reverse the list and join to get the string


def generate_random_number(bound):
    # Generate a random integer with 'bound' digits
    lower_bound = 1  # Smallest number with 'bound' digits
    upper_bound = bound - 1  # Largest number with 'bound' digits
    a = random.randint(lower_bound, upper_bound)
    return a
def split_key(key: str):
    filtered_key = ''.join([char for char in key if char.isdigit() or char == ','])
    result = filtered_key.split(",")
    return int(result[0]), int(result[1])

import sys
import random
import math
import sys
import sympy

sys.set_int_max_str_digits(10000000)


def generate_random_number(digits):
    return random.randint(10 ** (digits - 1), 10**digits - 1)


# Function to generate two coprime numbers, one with 1000 digits and another with 999 digits
def generate_coprime_numbers(num2):
    while True:
        num1 = generate_random_number(9)  # Generate a 1000-digit number

        # Check if the two numbers are coprime
        if math.gcd(num1, num2) == 1:
            return num1


def extended_euclide(a, b):
    # Generate the coprime numbers
    a = a
    b = b
    # a = num1
    # b = num2
    x_2 = 1
    x_1 = 0
    y_2 = 0
    y_1 = 1
    x = 0
    y = 0
    r = 0
    q = 0
    while b != 0:
        q = a // b
        r = a % b
        x = x_2 - q * x_1
        y = y_2 - q * y_1
        a = b
        b = r
        x_2 = x_1
        x_1 = x
        y_2 = y_1
        y_1 = y

    return x_2


def main():
    a, b = int(sys.argv[1]), int(sys.argv[2])
    print(extended_euclide(a, b))

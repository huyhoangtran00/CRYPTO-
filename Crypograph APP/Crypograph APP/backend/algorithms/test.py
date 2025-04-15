from sympy import randprime, factorint, primitive_root


def generate_prime(digit_bound):
    upper_bound = 10**digit_bound  # Smallest 6-digit number
    lower_bound = 10 ** (digit_bound - 1)  # Largest 6-digit number
    prime_number = randprime(lower_bound, upper_bound)
    return prime_number


def find_primitive_roots(p):
    euler_quotient = p - 1

    factors = factorint(euler_quotient)

    for g in range(2, p):
        is_primitive_root = True
        for q in factors.keys():
            if pow(g, euler_quotient // q, p) == 1:
                is_primitive_root = False
                break
        if is_primitive_root:
            return g
    return None


print(primitive_root(generate_prime(100)))

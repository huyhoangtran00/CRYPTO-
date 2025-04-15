from math import isqrt, gcd, log, ceil, log2
import random
from sympy import randprime


def is_perfect_power(n):
    """Check if n is a perfect power."""
    if n < 1:
        return False
    for b in range(2, isqrt(n) + 2):
        a = int(round(n ** (1.0 / b)))
        if a**b == n:
            return True
    return False


def find_r(n):
    """Find the smallest r such that the order of n modulo r is greater than log2(n)^2."""
    max_k = ceil((log2(n)) ** 2)
    for r in range(2, n):
        if gcd(n, r) == 1:
            order = 1
            power = n % r
            while power != 1:
                power = (power * n) % r
                order += 1
                if order > max_k:
                    return r
    return n


def poly_expansion(x, a, n, r, mod):
    """Expands (x + a)^n modulo x^r - 1 and mod."""
    coeffs = [0] * r
    coeffs[0] = 1  # Start with (x + a)^0 = 1

    for _ in range(n):
        new_coeffs = [0] * r
        for i in range(r):
            new_coeffs[i] = (coeffs[i] * a) % mod
            if i + 1 < r:
                new_coeffs[i + 1] = (new_coeffs[i + 1] + coeffs[i]) % mod
            else:
                new_coeffs[0] = (new_coeffs[0] + coeffs[i]) % mod
        coeffs = new_coeffs
    return coeffs


def aks_primality_test(n):
    """AKS primality test to determine if n is prime."""
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False

    # Step 1: Check if n is a perfect power
    if is_perfect_power(n):
        return False

    # Step 2: Find the smallest r
    r = find_r(n)

    # Step 3: Check for GCD conditions
    for a in range(2, min(r, n)):
        d = gcd(a, n)
        if d > 1:
            return False

    # Step 4: If n <= r, then n is prime
    if n <= r:
        return True

    # Step 5: Polynomial congruence check
    log_n = log2(n)
    a_upper = isqrt(int(2 * log_n)) + 1

    for a in range(1, a_upper + 1):
        lhs = poly_expansion(1, a, n, r, n)
        rhs = [0] * r
        rhs[n % r] = 1  # Corresponds to x^n % (x^r - 1)
        rhs[0] = (rhs[0] + a) % n

        if lhs != rhs:
            return False

    return True


def generate_n_bit_prime(n):
    """Generate a random n-bit prime number using the AKS primality test."""
    if n < 2:
        raise ValueError("Number of bits must be at least 2")

    lower_bound = 1 << (n - 1)
    upper_bound = (1 << n) - 1

    while True:
        # Generate a random n-bit odd number
        candidate = random.randint(lower_bound, upper_bound)
        candidate |= 1  # Ensure it's odd

        if aks_primality_test(candidate):
            return candidate


# Example usage
# if __name__ == "__main__":
#     bit_length = 10
#     prime = generate_n_bit_prime(bit_length)
#     print(f"Generated {bit_length}-bit prime: {prime}")

bound = 50
randprimer = randprime(2**bound, 2 ** (bound + 1))
print(randprimer)
print(aks_primality_test(randprimer))

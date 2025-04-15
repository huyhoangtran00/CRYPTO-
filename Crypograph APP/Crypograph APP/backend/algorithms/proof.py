import random
from sympy import isprime, mod_inverse


# Function to compute modular square root using Tonelli-Shanks algorithm (for odd n)
def modular_sqrt(a, p):
    """Returns x such that x^2 ≡ a (mod p), or None if no solution exists."""
    assert pow(a, (p - 1) // 2, p) == 1, "a is not a quadratic residue modulo p"

    # Case 1: simple case
    if pow(a, (p + 1) // 4, p) ** 2 % p == a:
        return pow(a, (p + 1) // 4, p)

    # Tonelli-Shanks algorithm
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
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
        b = pow(c, 1 << (m - i - 1), p)
        m = i
        c = pow(b, 2, p)
        t = t * b * b % p
        r = r * b % p

    return r if t == 1 else None


# Function to check if a number is a quadratic residue modulo n
def is_quadratic_residue(x, n):
    """Returns True if x is a quadratic residue modulo n, False otherwise."""
    if n <= 1:
        return False
    return pow(x, (n - 1) // 2, n) == 1


# Key generation: generating two large primes and computing n
def generate_key(bits):
    p = q = 0
    while not isprime(p):
        p = random.getrandbits(bits)  # 512-bit prime
    while not isprime(q) or q == p:
        q = random.getrandbits(bits)  # 512-bit prime
    n = p * q
    return p, q, n


# Step 1: Prover (P) generates the interaction
def prover_step1(n, x, u):
    v = random.randint(1, n - 1)
    y = pow(v, 2, n)
    return y, v


# Step 2: Verifier (V) sends challenge i (0 or 1)
def verifier_step2():
    return random.choice([0, 1])


# Step 3: Prover (P) calculates z and sends it to V
def prover_step3(u, v, i, n):
    z = (u**i * v) % n
    return z


# Step 4: Verifier (V) checks if the condition holds
def verifier_step4(z, y, x, i, n):
    if i == 0:
        return pow(z, 2, n) == x
    else:
        return pow(z, 2, n) == y


# Interactive proof protocol: multiple rounds
def interactive_proof(x, u, n, rounds=10):
    for _ in range(rounds):
        y, v = prover_step1(n, x, u)
        i = verifier_step2()
        z = prover_step3(u, v, i, n)
        if not verifier_step4(z, y, x, i, n):
            print("Verification failed!")
            return False
    print("Proof accepted!")
    return True


# Example usage:
if __name__ == "__main__":
    # Generate key (p, q, n)
    p, q, n = generate_key(13)

    print(f"p: {p}, q: {q}, n:{n}")
    # Given x, check if it's a quadratic residue
    x = random.randint(1, n - 1)
    while not is_quadratic_residue(x, n):
        x = random.randint(1, n - 1)

    # Find a quadratic root of x (u such that u^2 ≡ x mod n)
    u = modular_sqrt(x, n)
    if u is None:
        print(f"No square root found for x = {x} mod n")
    else:
        print(
            f"x = {x} is a quadratic residue, and u = {u} is a square root of x mod n."
        )

        # Run the interactive proof
        interactive_proof(x, u, n, rounds=10)

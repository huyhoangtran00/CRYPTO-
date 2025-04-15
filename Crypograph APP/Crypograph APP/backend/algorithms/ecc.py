from mpmath.libmp.libmpf import math
from sympy import isprime, factorint, mod_inverse, randprime, sqrt
from helper import generate_prime
import gmpy2
from concurrent.futures import ThreadPoolExecutor


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"


class EllipticCurve:
    def __init__(self, p, a, b):
        self.p = p  # Prime modulus
        self.a = a
        self.b = b

    def subtract_points(self, P, Q):
        """Subtract point Q from point P on the elliptic curve."""
        # To subtract Q, add the inverse of Q
        Q_inverse = Point(Q.x, -Q.y % self.p)
        return self.add_points(P, Q_inverse)

    def add_points(self, P, Q):
        """Add two points P and Q on the elliptic curve."""
        if P is None:
            return Q
        if Q is None:
            return P

        # Convert points to gmpy2.mpz
        P_x = gmpy2.mpz(P.x)
        P_y = gmpy2.mpz(P.y)
        Q_x = gmpy2.mpz(Q.x)
        Q_y = gmpy2.mpz(Q.y)

        if P_x == Q_x and P_y == Q_y:
            # Use precomputed inverses if available or memoize them
            inv_2P_y = gmpy2.invert(2 * P_y, self.p)
            m = (3 * P_x**2 + self.a) * inv_2P_y % self.p
        else:
            inv_Qx_minus_Px = gmpy2.invert(Q_x - P_x, self.p)
            m = (Q_y - P_y) * inv_Qx_minus_Px % self.p

        x_r = (m**2 - P_x - Q_x) % self.p
        y_r = (m * (P_x - x_r) - P_y) % self.p

        return Point(int(x_r), int(y_r))


def modular_square_root(a, p):
    # Tonelli-Shanks algorithm for finding a square root modulo p
    if pow(a, (p - 1) // 2, p) != 1:
        return None  # No square root exists if not a quadratic residue
    if p % 4 == 3:
        return pow(a, (p + 1) // 4, p)
    # Implement the general Tonelli-Shanks here for other cases
    # (the full implementation is a bit longer)


# Thông số của đường cong elliptic


def main():

    p = 2**255 - 19
    a, b = 486662, 1  # Curve parameters
    print(f"Parameters: a = {a}, b = {b}, p = {p}")

    curve = EllipticCurve(p, a, b)


main()

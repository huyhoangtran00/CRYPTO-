import math


class MasseyOmura:
    def __init__(self, p) -> None:
        self.public_p = p
        self.secret_key = None
        self.public_key = None

    def generate_key(self) -> None:
        phi = self.public_p - 1

        for e_key in range(2, phi):
            if math.gcd(e_key, phi) == 1:
                d = pow(e_key, -1, phi)
                self.public_key = e_key
                self.secret_key = d
                break

    def encrypt(self, message) -> int:
        return pow(message, self.public_key, self.public_p)

    def decrypt(self, cipher) -> int:
        return pow(cipher, self.secret_key, self.public_p)


class EllipticMasseyOmura(MasseyOmura):
    def __init__(self, p) -> None:
        super().__init__(p)


massey = MasseyOmura(18810230123021)
massey.generate_key()
c = massey.encrypt(123)
print(c)
print(massey.decrypt(c))

import random


class FeigeFiatShamir:
    def __init__(self, p, q, rounds=5):
        # Modulus N is the product of two primes p and q
        self.N = p * q
        # Secret key (s) and public key (v)
        self.s = random.randint(1, self.N - 1)
        self.v = pow(self.s, 2, self.N)
        # Number of rounds for verification
        self.rounds = rounds

    def run_protocol(self):
        # Run multiple rounds of the protocol
        for i in range(self.rounds):
            print(f"\nRound {i+1}")

            # Prover sends commitment
            commitment = self.commit()
            print("Commitment (x):", commitment)

            # Verifier sends challenge
            challenge = self.challenge()
            print("Challenge (c):", challenge)

            # Prover sends response based on challenge
            response = self.respond()
            print("Response:", response)

            # Verifier checks the response
            if not self.verify(response):
                print("Verification failed: Prover is not authenticated.")
                return False
        print("Verification successful: Prover is authenticated.")
        return True

    def commit(self):
        # Prover generates a random commitment r and computes x = r^2 mod N
        self.r = random.randint(1, self.N - 1)
        self.x = pow(self.r, 2, self.N)
        return self.x

    def challenge(self):
        # Verifier sends a random bit c (0 or 1)
        self.c = random.randint(0, 1)
        return self.c

    def respond(self):
        # Prover computes response based on the challenge c
        if self.c == 0:
            return self.r  # If c = 0, response is r
        else:
            return (self.r * self.s) % self.N  # If c = 1, response is r * s mod N

    def verify(self, response):
        # Verifier checks if the response is valid
        if self.c == 0:
            return pow(response, 2, self.N) == self.x
        else:
            return pow(response, 2, self.N) == (self.x * self.v) % self.N


# Example usage:
p = 883  # Example prime p
q = 911  # Example prime q
rounds = 5  # Number of rounds for the protocol

ffs = FeigeFiatShamir(p, q, rounds)
ffs.run_protocol()

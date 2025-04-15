# Run this in SageMath
from sage.all import EllipticCurve, GF
# Define the prime field and the elliptic curve parameters
p = int("AADD9DB8DBE9C48B3FD4E6AE33C9FC07CB308DB3B3C9D20ED6639CCA703308717D4D9B009BC66842AECDA12AE6A380E62881FF2F2D82C68528AA6056583A48F3", 16)
A = int("7830A3318B603B89E2327145AC234CC594CBDD8D3DF91610A83441CAEA9863BC2DED5D5AA8253AA10A2EF1C98B9AC8B57F1117A72BF2C7B9E7C1AC4D77FC94CA", 16)
B = int("3DF91610A83441CAEA9863BC2DED5D5AA8253AA10A2EF1C98B9AC8B57F1117A72BF2C7B9E7C1AC4D77FC94CADC083E67984050B75EBAE5DD2809BD638016F723", 16)

# Define the finite field and elliptic curve
F = GF(p)  # Finite field of prime order p
E = EllipticCurve(F, [A, B])

# Count the number of points on the elliptic curve using Schoof's algorithm
num_points = E.cardinality()
print("Số điểm trên đường cong là:", num_points)
    
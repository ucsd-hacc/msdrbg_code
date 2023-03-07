# Verify SUS Parameters
N = int("0x"
    "f17351a63a5b2042c08e423466bf654be5f59bcefd173ee4ba4d5c129439ed36"
    "6da97ce83550e2a8139bb93a909107060c755eedf3784c725e57f6207ae2a7a4"
    "4dbdaa96e1db5c169a4a31a2543290260cb9688e27f6f424d79f140e978f6117"
    "adad579a05b7ce76b932e5aff3c7461fdac9c08112e7f9e51a64e0ba949bcf3f",
    16)

p = int("0x"
    "00027c0ef9a55007e7f9f77963a9fb5f6d87b4e39a83a4ac2ddccee72a70ddfe"
    "b8277ade35ca7ff44f9a96a191fdb7adda2508ab2a4b212a8e7e3cf43a4760df",
    16)
q = int("0x"
    "0000612dbd55fd70051f60effe91db4427fb1939872660e8d161f23c193be198"
    "a9dda8a6e6613634f176a41cbd8f789ea23a2eb19d07bc0c2fe67d152e388fb8"
    "62f57da1",
    16)
e = 17

from math import gcd
phi_N = (p - 1) * (q - 1) // gcd(p-1, q-1)
val = pow(e, 200, phi_N) - pow(e, 180, phi_N) + pow(e, 20, phi_N) - 1
assert val % phi_N == 0

# Apply RSA PRG update function
import random
states = [random.randrange(N)]
for _ in range(200): states += [pow(states[-1], e, N)]

# Check relations
assert (states[200] * states[20] - states[180] * states[0]) % N == 0
print("The SUS parameters verify successfully")

# Verify eSP Parameters
N = int("0x"
    "fa4351292767d540d8dd2ef15b39b02e29b56ad2125add6964203eb0029ba7aa8d44c8e5"
    "65df7818f6eb959c37f83349ec4b1514ed42741b8e772028db779f5e362234b782b9064c"
    "ef07dead66bced100eb71cc8bf7f1325959eb304e90ecf6e53c4eff9708ebd3c7641ea2b"
    "aed50fbc679b4f0e06ad60b8e70c7836a5f99e1571be6194afe04c81a6eef8281bb43b99"
    "f17ee715e5f1a95e36aee8c4eb8757aa8ff108acdf29136cf543bb8831074b71fc63cc44"
    "4ca4d3d7811b6cdca33ec889dddc77828510ff0d10ac07b0f691ce2995a72137abf32816"
    "eed9cd322075e7450326ff2fba0b65c19c477d61407eccf48f5857b5ff95cf4c63702b9f"
    "09f9ca83", 16)
p = int("0x"
    "9da439c726a6c69087a81e49644d5e2d28937de5ba08c475a615813025318e2ae05f3174"
    "8f685c68f02b6883f10d407012970b50b28da780a6b157b7c80011a3857a877d56b5a8d4"
    "fc0a96bf62b7ec86d735de29628e230665356f535df7664723659f8f88847baaf9526393"
    "a521", 16)
q = int("0x"
    "1966956586a77b7e1fda36f722223a66b161f10027c53b2b39fde757e01fa6ef8b79e62e"
    "0b423546ebc2473011c3a79b4379788fff85eb743bfdbfe1d679511042295e5c6a5cf634"
    "b650bf83a997ecef1abef4467e02103de493f1f269bdb9088c6bc0f114971d05c983f499"
    "a48551bdeb901d3bc3290fbbf49368e5d9495b3922bdc03a9ec38e49aee6f0cedc78a1e2"
    "c5723", 16)
e = 5
c_q = 187
l = 504

assert pow(e, l, p - 1) == 1
assert pow(e, l, q - 1) == c_q

# Apply RSA PRG update function
import random
states = [random.randrange(N)]
for _ in range(l): states += [pow(states[-1], e, N)]

# Check relations
assert states[0] % p == states[l] % p
assert pow(states[0], c_q, q) == states[l] % q
print("The eSP parameters verify successfully")

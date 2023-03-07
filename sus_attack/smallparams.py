from sage.all import Integer, polygen, ZZ

"""
Small parameters for testing.
lg N: 147
lg p: 97
lg q: 50

backdoor nvars: 4
f(e) == 0 mod phi(p), not mod phi(N)
"""

e = 39
p = 108990479000505473112019722211 # 97 bits
q = 854194422016787 # 50 bits
N = p*q # 147 bits
k = 135 # unknown size: 12 bits

e,p,q,N,k = Integer(e),Integer(p),Integer(q),Integer(N),Integer(k)

x = polygen(ZZ)
f = x**20 + x**13 - x**9 - x**8
relation_coeffs = [(20,1),(13,1),(9,-1),(8,-1)]

hints = {'diylll': False}

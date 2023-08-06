from libc.math cimport sqrt
import numpy as np


cpdef int is_prime(int p):
    assert p > 1
    cdef int i
    cdef int n = int(sqrt(p))
    for i in range(2,n+1):
        if p % i == 0:
            return 0
    return 1


cpdef int random_prime(int low, int high):
    cdef int p
    while 1:
        p = np.random.randint(low,high)
        if is_prime(p):
            break
    return p
            

cpdef int gcd(int a, int b):
    while a:
        a, b = b % a, a
    return b


cpdef int inverse_mod_p(int a, int p):
    cdef int b = p
    cdef int x = 1
    cdef int y = 0

    assert a > 0 and a < p
    while a > 0:
        a, b, x, y = b % a, a, y - (b/a)*x, x
    assert b == 1    #b=gcd(a,p)
    return y % p


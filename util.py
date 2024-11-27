import math
import cmath
import numpy as np
import random

def randlist(max_index):
    _list = []
    for i in range(0, max_index):
        _list.append(random.randrange(-1, 1, 1))
    return _list
rand_bit_list = randlist(1000)

pi = cmath.pi
e = cmath.e
exp = cmath.exp
def ln(x):
    return cmath.log(x)
ru = random.uniform
fac=math.factorial
sq = math.sqrt
ceil = math.ceil
floor = math.floor
phi = (1+sq(5))/2

def isPrime(n) :
 
    if (n < 2) :
        return False
    for i in range(2, n + 1) :
        if (i * i <= n and n % i == 0) :
            return False
    return True
 
def mobius(N) :
    if (N == 1) :
        return 1
    p = 0
    for i in range(1, N + 1) :
        if (N % i == 0 and
                isPrime(i)) :
            if (N % (i * i) == 0) :
                return 0
            else :
                p = p + 1
    if(p % 2 != 0) :
        return -1
    else :
        return 1
#https://rosettacode.org/wiki/M%C3%B6bius_function#Python mobius and isprime funcs
def prime_sieve(end):
    end = end+1
    integers = np.arange(0, end)
    composite_integers  = np.array([0, 1])
    for i in range(2, ceil(sq(end))):
        if i not in composite_integers:
            mult_range = np.arange(i**2, end, i)
            composite_integers = np.union1d(composite_integers, mult_range)
    integers = np.delete(integers, composite_integers)
    return integers



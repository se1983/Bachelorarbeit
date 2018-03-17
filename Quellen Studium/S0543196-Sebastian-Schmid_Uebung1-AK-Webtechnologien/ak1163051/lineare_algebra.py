# %load ./ak1163051/lineare_algebra.py
""" Some functions for basic linear algebra operations based on python lists. """

from random import randint


def vector_add(a, b):
    assert len(a) == len(b)
    return [x + b[i] for i, x in enumerate(a)]


def vector_sub(a, b):
    return [x - b[i] for i, x in enumerate(a)]


def vector_scalar_mul(r, a):
    return [r * x for x in a]


def vector_dot(a, b):
    assert len(a) == len(b)
    return sum(a[i] * x for i, x in enumerate(b))


def create_random_matrix(n, m):
    return [[randint(0, 255) for _n in range(n)] for _m in range(m)]


def matrix_vector_mul(mat, vec):
    E = []
    for c in mat: 
        E.append([r*vec[i] for i, r in enumerate(c)])
    return E
        
    
def matrix_transpose(a):
    if not isinstance(a[0], list):
        return a
    s = len(a[0])
    return [[row[i] for row in a] for i in range(s)]
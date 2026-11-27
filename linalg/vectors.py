"""Vector operations (Phase 1, Days 2–14).

Rule: never call np.linalg in this file. np.linalg is only used in tests, as the reference.
"""

import numpy as np


def as_vector(x):
    """Day 2: convert a list or array into a 1D float array.

     Raise ValueError if the input is not 1-dimensional.

    >>> as_vector([1, 2, 3])
    array([1., 2., 3.])
    """
    x = np.asarray(x, dtype = float)
    if x.ndim != 1:
        raise ValueError("Input must be 1-dimensional")
    return x


def is_zero_vector(v, tol=1e-10):
    """Day 3: return True if every entry of v is within tol of zero.

    Floats carry tiny rounding errors, so never test with == 0.
    Remember Day 2, Task 3.3: compare the *absolute value* with tol.

    >>> is_zero_vector([1e-12, -3e-11])
    True
    >>> is_zero_vector([0.0, 0.001])
    False
    """
    v = as_vector(v)
    return np.all(np.abs(v) < tol)


def vectors_close(u, v, tol=1e-10):
    """Day 3: return True if u and v have the same length and every pair of
    entries differs by less than tol.

    Raise ValueError if the lengths differ (comparing a 2D vector with a 3D
    vector is a bug in the caller, not a False answer).

    >>> vectors_close([0.1 + 0.2, 1.0], [0.3, 1.0])
    True
    """
    u = as_vector(u)
    v = as_vector(v)
    if u.shape != v.shape:
        raise ValueError("Vectors must have the same length")
    return np.all(np.abs(u - v) < tol)


def add(u, v):
    """Day 5: return the vector u + v, built with a for loop.

    Add the entries one by one: result[i] = u[i] + v[i].
    Do not write u + v on whole arrays here (that is what the tests compare against).
    Raise ValueError if the lengths differ.

    >>> add([1, 2], [3, -1])
    array([4., 1.])
    """
    u = as_vector(u)
    v = as_vector(v)
    if u.shape != v.shape:
        raise ValueError("Vectors must have the same length")
    result = np.zeros(len(u))
    for i in range(len(u)):
        result[i] = u[i] + v[i]
    return result



def scale(k, v):
    """Day 5: return the vector k * v (k is a number), built with a for loop.

    Multiply the entries one by one: result[i] = k * v[i].

    >>> scale(3, [1, 2])
    array([3., 6.])
    """
    v = as_vector(v)
    result = np.zeros(len(v))
    for i in range(len(v)):
        result[i] = k * v[i]
    return result
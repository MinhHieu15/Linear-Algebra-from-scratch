"""Tests for linalg/vectors.py, checked against NumPy.
"""

import numpy as np
import pytest

from linalg.vectors import add, as_vector, is_zero_vector, scale, vectors_close

DAY5 = pytest.mark.skip(reason="Day 5: delete the @DAY5 lines when done")




def test_as_vector_from_list():
    v = as_vector([1, 2, 3])
    assert v.dtype == float
    np.testing.assert_array_equal(v, np.array([1.0, 2.0, 3.0]))


def test_as_vector_rejects_2d():
    with pytest.raises(ValueError):
        as_vector([[1, 2], [3, 4]])

def test_as_vector_rejects_scalar():
    with pytest.raises(ValueError):
        as_vector(2)


def test_is_zero_vector_true_for_exact_zeros():
    assert is_zero_vector([0, 0, 0])



def test_is_zero_vector_true_for_tiny_values():
    assert is_zero_vector([1e-12, -3e-11])



def test_is_zero_vector_false_for_small_but_real_values():
    assert not is_zero_vector([0.0, 0.001])



def test_vectors_close_ignores_rounding():
    assert vectors_close([0.1 + 0.2, 1.0], [0.3, 1.0])



def test_vectors_close_false_when_different():
    assert not vectors_close([1.0, 2.0], [1.0, 2.1])


 
def test_vectors_close_matches_numpy():
    rng = np.random.default_rng(0)
    u = rng.normal(size=5)
    for v in (u + 1e-12, u + 1e-3):
        assert vectors_close(u, v) == np.allclose(u, v, rtol=0, atol=1e-10)



def test_vectors_close_rejects_different_lengths():
    with pytest.raises(ValueError):
        vectors_close([1, 2], [1, 2, 3])


def test_is_zero_vector_false_for_negative_values():
    assert not is_zero_vector([-5., 0.0])


# ---- Day 5: add and scale ----


def test_add_small_example():
    np.testing.assert_array_equal(add([1, 2], [3, -1]), np.array([4.0, 1.0]))



def test_add_matches_numpy():
    rng = np.random.default_rng(5)
    u = rng.normal(size=6)
    v = rng.normal(size=6)
    np.testing.assert_allclose(add(u, v), u + v)



def test_add_rejects_different_lengths():
    with pytest.raises(ValueError):
        add([1, 2], [1, 2, 3])



def test_scale_small_example():
    np.testing.assert_array_equal(scale(3, [1, 2]), np.array([3.0, 6.0]))



def test_scale_matches_numpy():
    rng = np.random.default_rng(5)
    v = rng.normal(size=6)
    for k in (2.5, -1.0, 0.0):
        np.testing.assert_allclose(scale(k, v), k * v)



def test_scale_does_not_change_input():
    v = np.array([1.0, 2.0, 3.0])
    scale(10, v)
    np.testing.assert_array_equal(v, np.array([1.0, 2.0, 3.0]))

def test_add_opposite_gives_zero():
    v = np.array([1.5, -2.0, 3.0])
    is_zero_vector(add(v, scale(-1,v)))

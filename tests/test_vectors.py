"""Tests for linalg/vectors.py, checked against NumPy.

Day 2: delete the pytestmark line below once as_vector is written.
"""

import numpy as np
import pytest

from linalg.vectors import as_vector, is_zero_vector, vectors_close




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


# ---- Day 3: delete each @DAY3 line once the function is written ----

DAY3 = pytest.mark.skip(reason="Day 3 not done yet")


@DAY3
def test_is_zero_vector_true_for_exact_zeros():
    assert is_zero_vector([0, 0, 0])


@DAY3
def test_is_zero_vector_true_for_tiny_values():
    assert is_zero_vector([1e-12, -3e-11])


@DAY3
def test_is_zero_vector_false_for_small_but_real_values():
    assert not is_zero_vector([0.0, 0.001])


@DAY3
def test_vectors_close_ignores_rounding():
    assert vectors_close([0.1 + 0.2, 1.0], [0.3, 1.0])


@DAY3
def test_vectors_close_false_when_different():
    assert not vectors_close([1.0, 2.0], [1.0, 2.1])


@DAY3
def test_vectors_close_matches_numpy():
    rng = np.random.default_rng(0)
    u = rng.normal(size=5)
    for v in (u + 1e-12, u + 1e-3):
        assert vectors_close(u, v) == np.allclose(u, v, rtol=0, atol=1e-10)


@DAY3
def test_vectors_close_rejects_different_lengths():
    with pytest.raises(ValueError):
        vectors_close([1, 2], [1, 2, 3])

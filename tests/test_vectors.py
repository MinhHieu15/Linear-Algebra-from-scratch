"""Test cho linalg/vectors.py, đối chiếu với NumPy.

Ngày 2: xóa dòng pytestmark bên dưới sau khi viết xong as_vector.
"""

import numpy as np
import pytest

from linalg.vectors import as_vector

pytestmark = pytest.mark.skip(reason="Ngày 2 chưa làm")


def test_as_vector_from_list():
    v = as_vector([1, 2, 3])
    assert v.dtype == float
    np.testing.assert_array_equal(v, np.array([1.0, 2.0, 3.0]))


def test_as_vector_rejects_2d():
    with pytest.raises(ValueError):
        as_vector([[1, 2], [3, 4]])

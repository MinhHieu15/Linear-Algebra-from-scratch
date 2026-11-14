"""Test khởi động: đảm bảo môi trường và package import được, để CI xanh từ Ngày 1."""

import numpy as np

import linalg


def test_numpy_works():
    assert np.array([1, 2, 3]).sum() == 6


def test_package_imports():
    assert linalg.__doc__

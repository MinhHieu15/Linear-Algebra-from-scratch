"""Smoke tests: make sure the environment and package import, so CI is green from Day 1."""

import numpy as np

import linalg


def test_numpy_works():
    assert np.array([1, 2, 3]).sum() == 6


def test_package_imports():
    assert linalg.__doc__

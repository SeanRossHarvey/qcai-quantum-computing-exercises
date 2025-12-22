"""
pytest configuration file with shared fixtures for quantum computing tests.
"""

import pytest
import numpy as np
from qiskit_aer import AerSimulator


@pytest.fixture(scope="session")
def simulator():
    """Reusable quantum simulator instance for all tests."""
    return AerSimulator()


@pytest.fixture(scope="session")
def statevector_simulator():
    """Reusable statevector simulator for tests requiring quantum state information."""
    return AerSimulator(method='statevector')


@pytest.fixture(scope="session")
def random_seed():
    """Fixed random seed for reproducible tests."""
    seed = 42
    np.random.seed(seed)
    return seed


@pytest.fixture
def tolerance():
    """Numerical tolerance for floating point comparisons."""
    return 1e-10


@pytest.fixture
def measurement_shots():
    """Standard number of shots for measurement tests."""
    return 10000


@pytest.fixture
def chi_squared_significance():
    """Significance level for chi-squared statistical tests."""
    return 0.01

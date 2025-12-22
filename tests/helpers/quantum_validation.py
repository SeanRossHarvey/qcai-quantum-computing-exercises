"""
Utilities for statistical validation of quantum measurement outcomes.
"""

from typing import Dict
import numpy as np
from scipy import stats


def validate_measurement_distribution(
    counts: Dict[str, int],
    expected_probs: Dict[str, float],
    shots: int,
    significance: float = 0.01
) -> bool:
    """
    Validate measurement distribution using chi-squared test.

    Performs a statistical test to determine if observed measurement counts
    are consistent with expected probability distribution.

    Args:
        counts: Measured counts from quantum simulation
        expected_probs: Expected probability distribution (values sum to 1.0)
        shots: Total number of measurement shots
        significance: Significance level for hypothesis test (default 0.01)

    Returns:
        True if distribution matches expectation (p-value > significance)

    Example:
        >>> counts = {'00': 505, '11': 495}
        >>> expected = {'00': 0.5, '11': 0.5}
        >>> validate_measurement_distribution(counts, expected, 1000)
        True
    """
    # Ensure all expected states are represented
    all_states = set(expected_probs.keys())

    # Extract observed and expected counts
    observed = np.array([counts.get(state, 0) for state in all_states])
    expected = np.array([expected_probs[state] * shots for state in all_states])

    # Perform chi-squared test
    chi2_stat, p_value = stats.chisquare(observed, expected)

    return p_value > significance


def validate_statevector(
    actual: np.ndarray,
    expected: np.ndarray,
    tolerance: float = 1e-10
) -> bool:
    """
    Validate that a statevector matches expected value (up to global phase).

    Quantum states that differ only by a global phase are physically equivalent.
    This function checks if two statevectors represent the same quantum state.

    Args:
        actual: Actual statevector from simulation
        expected: Expected statevector
        tolerance: Numerical tolerance for comparison

    Returns:
        True if statevectors match (up to global phase)

    Example:
        >>> actual = np.array([1, 0]) / np.sqrt(2) * np.exp(1j * np.pi/4)
        >>> expected = np.array([1, 0]) / np.sqrt(2)
        >>> validate_statevector(actual, expected)
        True
    """
    # Flatten arrays if needed
    actual = np.asarray(actual).flatten()
    expected = np.asarray(expected).flatten()

    # Check dimensions match
    if actual.shape != expected.shape:
        return False

    # Calculate inner product (overlap)
    inner_product = np.abs(np.vdot(actual, expected))

    # If |⟨ψ₁|ψ₂⟩| = 1, states are equivalent up to global phase
    return np.isclose(inner_product, 1.0, atol=tolerance)


def calculate_fidelity(
    state1: np.ndarray,
    state2: np.ndarray
) -> float:
    """
    Calculate fidelity between two quantum states.

    Fidelity measures how "close" two quantum states are, with F=1 indicating
    identical states and F=0 indicating orthogonal states.

    Args:
        state1: First quantum state (statevector)
        state2: Second quantum state (statevector)

    Returns:
        Fidelity value between 0 and 1

    Example:
        >>> state1 = np.array([1, 0])
        >>> state2 = np.array([1, 0])
        >>> calculate_fidelity(state1, state2)
        1.0
    """
    # Flatten and normalize
    state1 = np.asarray(state1).flatten()
    state2 = np.asarray(state2).flatten()

    state1 = state1 / np.linalg.norm(state1)
    state2 = state2 / np.linalg.norm(state2)

    # Fidelity is |⟨ψ₁|ψ₂⟩|²
    overlap = np.abs(np.vdot(state1, state2))
    return overlap ** 2


def check_probability_distribution(
    probs: Dict[str, float],
    tolerance: float = 1e-10
) -> bool:
    """
    Verify that probabilities form a valid probability distribution.

    Checks that all probabilities are non-negative and sum to 1.

    Args:
        probs: Dictionary of state labels to probabilities
        tolerance: Tolerance for sum check

    Returns:
        True if valid probability distribution

    Example:
        >>> probs = {'00': 0.5, '11': 0.5}
        >>> check_probability_distribution(probs)
        True
    """
    # Check all probabilities are non-negative
    if any(p < 0 for p in probs.values()):
        return False

    # Check probabilities sum to 1
    total = sum(probs.values())
    return np.isclose(total, 1.0, atol=tolerance)


def calculate_measurement_error(
    counts: Dict[str, int],
    expected_probs: Dict[str, float]
) -> float:
    """
    Calculate the total variation distance between measured and expected distributions.

    Args:
        counts: Measured counts
        expected_probs: Expected probability distribution

    Returns:
        Total variation distance (0 = perfect match, higher = more error)

    Example:
        >>> counts = {'00': 510, '11': 490}
        >>> expected = {'00': 0.5, '11': 0.5}
        >>> error = calculate_measurement_error(counts, expected)
        >>> error < 0.1  # Small error
        True
    """
    total_counts = sum(counts.values())

    # Calculate observed probabilities
    observed_probs = {
        state: count / total_counts
        for state, count in counts.items()
    }

    # Calculate total variation distance
    all_states = set(expected_probs.keys()) | set(observed_probs.keys())
    tvd = 0.5 * sum(
        abs(observed_probs.get(state, 0) - expected_probs.get(state, 0))
        for state in all_states
    )

    return tvd


def is_entangled_state(statevector: np.ndarray, tolerance: float = 1e-10) -> bool:
    """
    Heuristic check if a two-qubit statevector represents an entangled state.

    Note: This is a simplified check that works for two-qubit systems. For
    more complex cases, proper entanglement measures should be used.

    Args:
        statevector: Two-qubit statevector (length 4)
        tolerance: Numerical tolerance

    Returns:
        True if state appears to be entangled

    Example:
        >>> bell_state = np.array([1, 0, 0, 1]) / np.sqrt(2)
        >>> is_entangled_state(bell_state)
        True
    """
    statevector = np.asarray(statevector).flatten()

    # Only works for two-qubit systems
    if len(statevector) != 4:
        raise ValueError("This function only works for two-qubit systems")

    # Reshape to 2x2 matrix
    matrix = statevector.reshape((2, 2))

    # Calculate Schmidt coefficients via SVD
    singular_values = np.linalg.svd(matrix, compute_uv=False)

    # If more than one non-zero Schmidt coefficient, state is entangled
    non_zero_sv = np.sum(singular_values > tolerance)

    return non_zero_sv > 1

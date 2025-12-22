"""
Tests for Task 2: Linear Algebra Foundations

These tests validate the NumPy-based linear algebra operations
students implement in Task 2.
"""

import pytest
import numpy as np


class TestQuantumStates:
    """Test quantum state creation and properties."""

    def test_state_zero_creation(self):
        """Test creation of |0⟩ state."""
        state_0 = np.array([[1], [0]])

        assert state_0.shape == (2, 1), "Should be column vector (2,1)"
        assert np.isclose(np.linalg.norm(state_0), 1.0), "State must be normalised"
        assert state_0[0, 0] == 1, "First component should be 1"
        assert state_0[1, 0] == 0, "Second component should be 0"

    def test_state_one_creation(self):
        """Test creation of |1⟩ state."""
        state_1 = np.array([[0], [1]])

        assert state_1.shape == (2, 1), "Should be column vector (2,1)"
        assert np.isclose(np.linalg.norm(state_1), 1.0), "State must be normalised"
        assert state_1[0, 0] == 0, "First component should be 0"
        assert state_1[1, 0] == 1, "Second component should be 1"

    def test_superposition_state(self):
        """Test creation of superposition state."""
        plus_state = np.array([[1], [1]]) / np.sqrt(2)

        assert plus_state.shape == (2, 1), "Should be column vector"
        assert np.isclose(np.linalg.norm(plus_state), 1.0), "Must be normalised"

        # Check equal amplitudes
        assert np.isclose(np.abs(plus_state[0, 0]), 1/np.sqrt(2))
        assert np.isclose(np.abs(plus_state[1, 0]), 1/np.sqrt(2))


class TestQuantumGates:
    """Test quantum gate matrix definitions."""

    def test_pauli_x_gate_structure(self):
        """Test Pauli-X gate matrix structure."""
        pauli_x = np.array([[0, 1], [1, 0]])

        assert pauli_x.shape == (2, 2), "Should be 2×2 matrix"
        assert pauli_x[0, 0] == 0, "Top-left should be 0"
        assert pauli_x[0, 1] == 1, "Top-right should be 1"
        assert pauli_x[1, 0] == 1, "Bottom-left should be 1"
        assert pauli_x[1, 1] == 0, "Bottom-right should be 0"

    def test_pauli_x_gate_unitary(self):
        """Test that Pauli-X gate is unitary."""
        pauli_x = np.array([[0, 1], [1, 0]])

        # Check X†X = I
        x_dagger = pauli_x.conj().T
        product = np.dot(x_dagger, pauli_x)
        identity = np.eye(2)

        assert np.allclose(product, identity), "X†X must equal identity"

    def test_pauli_x_gate_self_inverse(self):
        """Test that X² = I."""
        pauli_x = np.array([[0, 1], [1, 0]])
        x_squared = np.dot(pauli_x, pauli_x)

        assert np.allclose(x_squared, np.eye(2)), "X² should equal identity"

    def test_hadamard_gate_structure(self):
        """Test Hadamard gate matrix structure."""
        hadamard = np.array([[1, 1], [1, -1]]) / np.sqrt(2)

        assert hadamard.shape == (2, 2), "Should be 2×2 matrix"

        # Check values
        expected_val = 1 / np.sqrt(2)
        assert np.isclose(hadamard[0, 0], expected_val)
        assert np.isclose(hadamard[0, 1], expected_val)
        assert np.isclose(hadamard[1, 0], expected_val)
        assert np.isclose(hadamard[1, 1], -expected_val)

    def test_hadamard_gate_unitary(self):
        """Test that Hadamard gate is unitary."""
        hadamard = np.array([[1, 1], [1, -1]]) / np.sqrt(2)

        # Check H†H = I
        h_dagger = hadamard.conj().T
        product = np.dot(h_dagger, hadamard)

        assert np.allclose(product, np.eye(2)), "H†H must equal identity"

    def test_hadamard_gate_self_inverse(self):
        """Test that H² = I."""
        hadamard = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
        h_squared = np.dot(hadamard, hadamard)

        assert np.allclose(h_squared, np.eye(2)), "H² should equal identity"

    def test_identity_matrix(self):
        """Test identity matrix creation."""
        identity = np.eye(2)

        assert identity.shape == (2, 2), "Should be 2×2"
        assert identity[0, 0] == 1 and identity[1, 1] == 1, "Diagonal should be 1"
        assert identity[0, 1] == 0 and identity[1, 0] == 0, "Off-diagonal should be 0"


class TestGateApplications:
    """Test application of gates to quantum states."""

    def test_pauli_x_flips_state_0(self):
        """Test X|0⟩ = |1⟩."""
        pauli_x = np.array([[0, 1], [1, 0]])
        state_0 = np.array([[1], [0]])

        result = np.dot(pauli_x, state_0)
        expected = np.array([[0], [1]])

        assert np.allclose(result, expected), "X should flip |0⟩ to |1⟩"

    def test_pauli_x_flips_state_1(self):
        """Test X|1⟩ = |0⟩."""
        pauli_x = np.array([[0, 1], [1, 0]])
        state_1 = np.array([[0], [1]])

        result = np.dot(pauli_x, state_1)
        expected = np.array([[1], [0]])

        assert np.allclose(result, expected), "X should flip |1⟩ to |0⟩"

    def test_hadamard_creates_plus_state(self):
        """Test H|0⟩ = |+⟩."""
        hadamard = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
        state_0 = np.array([[1], [0]])

        result = np.dot(hadamard, state_0)
        expected = np.array([[1], [1]]) / np.sqrt(2)

        assert np.allclose(result, expected), "H|0⟩ should create |+⟩"

    def test_hadamard_creates_minus_state(self):
        """Test H|1⟩ = |-⟩."""
        hadamard = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
        state_1 = np.array([[0], [1]])

        result = np.dot(hadamard, state_1)
        expected = np.array([[1], [-1]]) / np.sqrt(2)

        assert np.allclose(result, expected), "H|1⟩ should create |-⟩"

    def test_hadamard_probability_amplitudes(self):
        """Test that H|0⟩ creates equal superposition."""
        hadamard = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
        state_0 = np.array([[1], [0]])

        result = np.dot(hadamard, state_0)

        prob_0 = np.abs(result[0, 0])**2
        prob_1 = np.abs(result[1, 0])**2

        assert np.isclose(prob_0, 0.5), "Should have 50% probability for |0⟩"
        assert np.isclose(prob_1, 0.5), "Should have 50% probability for |1⟩"
        assert np.isclose(prob_0 + prob_1, 1.0), "Probabilities must sum to 1"

    def test_identity_preserves_states(self):
        """Test that identity gate leaves states unchanged."""
        identity = np.eye(2)
        state_0 = np.array([[1], [0]])
        state_1 = np.array([[0], [1]])

        result_0 = np.dot(identity, state_0)
        result_1 = np.dot(identity, state_1)

        assert np.allclose(result_0, state_0), "I|0⟩ should equal |0⟩"
        assert np.allclose(result_1, state_1), "I|1⟩ should equal |1⟩"


class TestGateSequences:
    """Test sequential application of multiple gates."""

    def test_x_then_h_creates_minus_state(self):
        """Test that X→H creates |-⟩ state."""
        pauli_x = np.array([[0, 1], [1, 0]])
        hadamard = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
        state_0 = np.array([[1], [0]])

        # Apply X then H
        result = np.dot(hadamard, np.dot(pauli_x, state_0))
        expected = np.array([[1], [-1]]) / np.sqrt(2)

        assert np.allclose(result, expected), "X→H should create |-⟩"

    def test_h_then_x_creates_different_state(self):
        """Test that H→X creates different state than X→H."""
        pauli_x = np.array([[0, 1], [1, 0]])
        hadamard = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
        state_0 = np.array([[1], [0]])

        # X→H
        result_xh = np.dot(hadamard, np.dot(pauli_x, state_0))

        # H→X
        result_hx = np.dot(pauli_x, np.dot(hadamard, state_0))

        # These should be different (gate order matters)
        assert not np.allclose(result_xh, result_hx), "Gate order should matter"

    def test_gate_composition(self):
        """Test that gate composition equals sequential application."""
        pauli_x = np.array([[0, 1], [1, 0]])
        hadamard = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
        state_0 = np.array([[1], [0]])

        # Method 1: Sequential application
        result1 = np.dot(hadamard, np.dot(pauli_x, state_0))

        # Method 2: Composed gate
        composed = np.dot(hadamard, pauli_x)
        result2 = np.dot(composed, state_0)

        assert np.allclose(result1, result2), "Both methods should give same result"


class TestInnerProducts:
    """Test inner product calculations."""

    def test_orthogonal_basis_states(self):
        """Test that |0⟩ and |1⟩ are orthogonal."""
        state_0 = np.array([[1], [0]])
        state_1 = np.array([[0], [1]])

        inner_product = np.vdot(state_0.flatten(), state_1.flatten())

        assert np.isclose(inner_product, 0), "⟨0|1⟩ should be 0"

    def test_state_with_itself(self):
        """Test that ⟨ψ|ψ⟩ = 1 for normalised states."""
        state_0 = np.array([[1], [0]])

        inner_product = np.vdot(state_0.flatten(), state_0.flatten())

        assert np.isclose(inner_product, 1), "⟨0|0⟩ should be 1"

    def test_plus_state_overlap(self):
        """Test overlap between |+⟩ and |0⟩."""
        state_0 = np.array([[1], [0]])
        plus_state = np.array([[1], [1]]) / np.sqrt(2)

        inner_product = np.vdot(plus_state.flatten(), state_0.flatten())

        # |⟨+|0⟩| = 1/√2
        expected = 1 / np.sqrt(2)
        assert np.isclose(np.abs(inner_product), expected), "Overlap should be 1/√2"

    def test_probability_from_inner_product(self):
        """Test that |⟨ψ|φ⟩|² gives measurement probability."""
        plus_state = np.array([[1], [1]]) / np.sqrt(2)
        state_0 = np.array([[1], [0]])

        inner_product = np.vdot(plus_state.flatten(), state_0.flatten())
        probability = np.abs(inner_product)**2

        assert np.isclose(probability, 0.5), "Measurement probability should be 50%"


class TestTensorProducts:
    """Test tensor product calculations for multi-qubit systems."""

    def test_tensor_product_00(self):
        """Test |0⟩ ⊗ |0⟩ = |00⟩."""
        state_0 = np.array([[1], [0]])

        result = np.kron(state_0, state_0)
        expected = np.array([[1], [0], [0], [0]])

        assert result.shape == (4, 1), "Two-qubit state should be 4D"
        assert np.allclose(result, expected), "Should produce |00⟩"

    def test_tensor_product_01(self):
        """Test |0⟩ ⊗ |1⟩ = |01⟩."""
        state_0 = np.array([[1], [0]])
        state_1 = np.array([[0], [1]])

        result = np.kron(state_0, state_1)
        expected = np.array([[0], [1], [0], [0]])

        assert np.allclose(result, expected), "Should produce |01⟩"

    def test_tensor_product_10(self):
        """Test |1⟩ ⊗ |0⟩ = |10⟩."""
        state_0 = np.array([[1], [0]])
        state_1 = np.array([[0], [1]])

        result = np.kron(state_1, state_0)
        expected = np.array([[0], [0], [1], [0]])

        assert np.allclose(result, expected), "Should produce |10⟩"

    def test_tensor_product_11(self):
        """Test |1⟩ ⊗ |1⟩ = |11⟩."""
        state_1 = np.array([[0], [1]])

        result = np.kron(state_1, state_1)
        expected = np.array([[0], [0], [0], [1]])

        assert np.allclose(result, expected), "Should produce |11⟩"

    def test_tensor_product_superposition(self):
        """Test tensor product with superposition states."""
        plus_state = np.array([[1], [1]]) / np.sqrt(2)
        state_0 = np.array([[1], [0]])

        result = np.kron(plus_state, state_0)

        # |+⟩ ⊗ |0⟩ = (|00⟩ + |10⟩)/√2
        expected = np.array([[1], [0], [1], [0]]) / np.sqrt(2)

        assert np.allclose(result, expected), "Should produce (|00⟩ + |10⟩)/√2"

    def test_tensor_product_normalisation(self):
        """Test that tensor product preserves normalisation."""
        plus_state = np.array([[1], [1]]) / np.sqrt(2)

        result = np.kron(plus_state, plus_state)
        norm = np.linalg.norm(result)

        assert np.isclose(norm, 1.0), "Tensor product must preserve normalisation"


class TestEigenvalues:
    """Test eigenvalue and eigenvector calculations."""

    def test_eigenvalue_decomposition(self):
        """Test eigenvalue decomposition of given matrix."""
        matrix = np.array([[3, 1], [1, 2]])

        eigenvalues, eigenvectors = np.linalg.eig(matrix)

        assert len(eigenvalues) == 2, "Should have 2 eigenvalues for 2×2 matrix"
        assert eigenvectors.shape == (2, 2), "Should have 2 eigenvectors"

    def test_eigenvalue_equation(self):
        """Test that A|λ⟩ = λ|λ⟩ for all eigenpairs."""
        matrix = np.array([[3, 1], [1, 2]])
        eigenvalues, eigenvectors = np.linalg.eig(matrix)

        for i in range(len(eigenvalues)):
            eigenvector = eigenvectors[:, i]
            eigenvalue = eigenvalues[i]

            left_side = matrix @ eigenvector
            right_side = eigenvalue * eigenvector

            assert np.allclose(left_side, right_side), f"Eigenvalue equation failed for pair {i}"

    def test_eigenvalues_are_real(self):
        """Test that eigenvalues of symmetric matrix are real."""
        matrix = np.array([[3, 1], [1, 2]])
        eigenvalues, _ = np.linalg.eig(matrix)

        # For symmetric (Hermitian) matrices, eigenvalues should be real
        for eigenvalue in eigenvalues:
            assert np.isclose(eigenvalue.imag, 0), "Eigenvalues should be real for symmetric matrix"

    def test_pauli_x_eigenvalues(self):
        """Test eigenvalues of Pauli-X gate are ±1."""
        pauli_x = np.array([[0, 1], [1, 0]])
        eigenvalues, _ = np.linalg.eig(pauli_x)

        eigenvalues_sorted = sorted(eigenvalues)
        expected = [-1, 1]

        assert np.allclose(eigenvalues_sorted, expected), "X eigenvalues should be ±1"


class TestIntegration:
    """Integration tests combining multiple concepts."""

    def test_complete_workflow(self):
        """Test a complete workflow: state creation, gate application, measurement."""
        # Create initial state
        state_0 = np.array([[1], [0]])

        # Create gates
        hadamard = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
        pauli_x = np.array([[0, 1], [1, 0]])

        # Apply gate sequence
        state_after_h = np.dot(hadamard, state_0)
        state_after_x = np.dot(pauli_x, state_after_h)

        # Calculate measurement probabilities
        prob_0 = np.abs(state_after_x[0, 0])**2
        prob_1 = np.abs(state_after_x[1, 0])**2

        # Verify properties
        assert np.isclose(np.linalg.norm(state_after_x), 1.0), "State must remain normalised"
        assert np.isclose(prob_0 + prob_1, 1.0), "Probabilities must sum to 1"

    def test_bell_state_preparation(self):
        """Test preparation of Bell state using tensor products and gates."""
        # Create |00⟩
        state_0 = np.array([[1], [0]])
        state_00 = np.kron(state_0, state_0)

        # Create H ⊗ I gate
        hadamard = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
        identity = np.eye(2)
        h_tensor_i = np.kron(hadamard, identity)

        # Apply to get (|00⟩ + |10⟩)/√2
        result = h_tensor_i @ state_00
        expected = np.array([[1], [0], [1], [0]]) / np.sqrt(2)

        assert np.allclose(result, expected), "Should create correct superposition"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

"""
Tests for Task 1: Quantum Entanglement and Measurement Statistics

These tests validate Bell state creation, measurement statistics,
and proper use of Qiskit 1.x API.
"""

import pytest
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector, Operator


class TestBellStateCircuit:
    """Test Bell state circuit construction."""

    def test_bell_state_circuit_structure(self):
        """Test that Bell state circuit has correct structure."""
        # Create Bell state circuit
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure([0, 1], [0, 1])

        # Check circuit properties
        assert qc.num_qubits == 2, "Should have 2 qubits"
        assert qc.num_clbits == 2, "Should have 2 classical bits"
        assert qc.depth() >= 2, "Should have at least depth 2 (H + CX)"

    def test_bell_state_gates_present(self):
        """Test that Bell state circuit contains H and CX gates."""
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure([0, 1], [0, 1])

        # Extract gate names (excluding measurements)
        gate_names = [inst.operation.name for inst in qc.data
                     if inst.operation.name != 'measure']

        assert 'h' in gate_names, "Circuit should contain Hadamard gate"
        assert 'cx' in gate_names, "Circuit should contain CNOT gate"

    def test_bell_state_gate_order(self):
        """Test that gates are in correct order (H before CX)."""
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure([0, 1], [0, 1])

        gate_names = [inst.operation.name for inst in qc.data
                     if inst.operation.name != 'measure']

        # H should come before CX
        h_index = gate_names.index('h')
        cx_index = gate_names.index('cx')
        assert h_index < cx_index, "Hadamard should come before CNOT"

    def test_bell_state_qubit_targeting(self):
        """Test that gates target correct qubits."""
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure([0, 1], [0, 1])

        # Check H gate targets qubit 0
        for inst in qc.data:
            if inst.operation.name == 'h':
                assert inst.qubits[0].index == 0, "H should target qubit 0"

        # Check CX gate has correct control and target
        for inst in qc.data:
            if inst.operation.name == 'cx':
                assert inst.qubits[0].index == 0, "CX control should be qubit 0"
                assert inst.qubits[1].index == 1, "CX target should be qubit 1"


class TestBellStateStatevector:
    """Test Bell state using statevector simulation (without measurement)."""

    def test_bell_state_amplitudes(self):
        """Test that Bell state has correct amplitudes."""
        # Create Bell state without measurement
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)

        # Get statevector
        statevector = Statevector.from_instruction(qc)
        amplitudes = statevector.data

        # Expected Bell state: (|00⟩ + |11⟩)/√2
        expected = np.array([1, 0, 0, 1]) / np.sqrt(2)

        assert np.allclose(amplitudes, expected), "Should produce correct Bell state"

    def test_bell_state_entangled(self):
        """Test that Bell state is entangled (not separable)."""
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)

        statevector = Statevector.from_instruction(qc)

        # Bell state should not be separable
        # Check using Schmidt decomposition (via helpers)
        from tests.helpers.quantum_validation import is_entangled_state

        assert is_entangled_state(statevector.data), "Bell state should be entangled"

    def test_bell_state_normalization(self):
        """Test that Bell state is properly normalized."""
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)

        statevector = Statevector.from_instruction(qc)

        # Check normalization: ⟨ψ|ψ⟩ = 1
        norm_squared = np.sum(np.abs(statevector.data)**2)
        assert np.isclose(norm_squared, 1.0), "State must be normalized"


class TestMeasurementStatistics:
    """Test measurement statistics and probabilities."""

    @pytest.fixture
    def simulator(self):
        """Provide AerSimulator instance."""
        return AerSimulator()

    @pytest.fixture
    def bell_circuit(self):
        """Provide Bell state circuit with measurements."""
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure([0, 1], [0, 1])
        return qc

    def test_bell_state_measurement_outcomes(self, simulator, bell_circuit):
        """Test that only |00⟩ and |11⟩ outcomes occur."""
        transpiled = transpile(bell_circuit, simulator)
        job = simulator.run(transpiled, shots=1000)
        counts = job.result().get_counts()

        # Should only have |00⟩ and |11⟩
        valid_outcomes = {'00', '11'}
        for outcome in counts.keys():
            assert outcome in valid_outcomes, f"Unexpected outcome: {outcome}"

    def test_bell_state_probability_distribution(self, simulator, bell_circuit):
        """Test that probabilities are approximately 50-50."""
        transpiled = transpile(bell_circuit, simulator)
        job = simulator.run(transpiled, shots=10000)  # More shots for better statistics
        counts = job.result().get_counts()

        count_00 = counts.get('00', 0)
        count_11 = counts.get('11', 0)
        total = count_00 + count_11

        prob_00 = count_00 / total
        prob_11 = count_11 / total

        # Should be close to 0.5 each (within 3 sigma: ~0.015 for 10000 shots)
        assert 0.47 < prob_00 < 0.53, f"P(00) should be ~0.5, got {prob_00}"
        assert 0.47 < prob_11 < 0.53, f"P(11) should be ~0.5, got {prob_11}"

    def test_no_invalid_outcomes(self, simulator, bell_circuit):
        """Test that |01⟩ and |10⟩ never occur."""
        transpiled = transpile(bell_circuit, simulator)
        job = simulator.run(transpiled, shots=1000)
        counts = job.result().get_counts()

        # These should have zero counts
        assert counts.get('01', 0) == 0, "Should not measure |01⟩"
        assert counts.get('10', 0) == 0, "Should not measure |10⟩"

    def test_statistical_validation(self, simulator, bell_circuit):
        """Test measurement distribution using chi-squared test."""
        from tests.helpers.quantum_validation import validate_measurement_distribution

        transpiled = transpile(bell_circuit, simulator)
        job = simulator.run(transpiled, shots=10000)
        counts = job.result().get_counts()

        # Expected 50-50 distribution
        expected_probs = {'00': 0.5, '11': 0.5}

        # Chi-squared test should pass
        is_valid = validate_measurement_distribution(
            counts, expected_probs, shots=10000, significance=0.01
        )

        assert is_valid, "Measurement distribution should match theoretical prediction"


class TestQiskitAPIUsage:
    """Test proper use of Qiskit 1.x API."""

    def test_aer_simulator_creation(self):
        """Test creating AerSimulator (Qiskit 1.x)."""
        simulator = AerSimulator()

        assert simulator is not None, "Should create simulator"
        assert hasattr(simulator, 'run'), "Simulator should have run method"

    def test_transpile_function(self):
        """Test using transpile function."""
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure([0, 1], [0, 1])

        simulator = AerSimulator()
        transpiled = transpile(qc, simulator)

        assert transpiled is not None, "Transpile should return circuit"
        assert transpiled.num_qubits == 2, "Transpiled circuit should preserve qubits"

    def test_simulation_workflow(self):
        """Test complete Qiskit 1.x simulation workflow."""
        # Create circuit
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure([0, 1], [0, 1])

        # Qiskit 1.x workflow
        simulator = AerSimulator()
        transpiled = transpile(qc, simulator)
        job = simulator.run(transpiled, shots=100)
        result = job.result()
        counts = result.get_counts()

        # Should get valid results
        assert isinstance(counts, dict), "Should return counts dictionary"
        assert len(counts) > 0, "Should have measurement outcomes"
        assert sum(counts.values()) == 100, "Should have 100 total counts"


class TestCircuitVariations:
    """Test variations and edge cases."""

    def test_bell_state_with_different_initial_state(self):
        """Test Bell state starting from |11⟩."""
        qc = QuantumCircuit(2)
        qc.x(0)  # |0⟩ → |1⟩
        qc.x(1)  # |0⟩ → |1⟩
        qc.h(0)
        qc.cx(0, 1)

        statevector = Statevector.from_instruction(qc)

        # Should produce (|01⟩ + |10⟩)/√2
        expected = np.array([0, 1, 1, 0]) / np.sqrt(2)
        assert np.allclose(statevector.data, expected), "Should produce Ψ+ Bell state"

    def test_hadamard_on_different_qubit(self):
        """Test applying Hadamard to qubit 1 instead."""
        qc = QuantumCircuit(2)
        qc.h(1)  # Hadamard on qubit 1
        qc.cx(1, 0)  # CX with control=1, target=0

        statevector = Statevector.from_instruction(qc)

        # Should still create entanglement (different Bell state)
        from tests.helpers.quantum_validation import is_entangled_state
        assert is_entangled_state(statevector.data), "Should still be entangled"

    def test_multiple_measurements(self):
        """Test that multiple measurements give consistent statistics."""
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure([0, 1], [0, 1])

        simulator = AerSimulator()
        transpiled = transpile(qc, simulator)

        # Run multiple times
        all_prob_00 = []
        for _ in range(10):
            job = simulator.run(transpiled, shots=1000)
            counts = job.result().get_counts()
            prob_00 = counts.get('00', 0) / 1000
            all_prob_00.append(prob_00)

        # Mean should be close to 0.5
        mean_prob = np.mean(all_prob_00)
        assert 0.45 < mean_prob < 0.55, "Average probability should be ~0.5"

        # Standard deviation should be reasonable (< 5%)
        std_prob = np.std(all_prob_00)
        assert std_prob < 0.05, "Standard deviation should be small"


class TestCircuitEquivalence:
    """Test circuit equivalence using helpers."""

    def test_bell_circuits_functionally_equivalent(self):
        """Test that two Bell state circuits are equivalent."""
        from tests.helpers.circuit_comparison import circuits_equivalent

        # Circuit 1
        qc1 = QuantumCircuit(2)
        qc1.h(0)
        qc1.cx(0, 1)

        # Circuit 2 (same as circuit 1)
        qc2 = QuantumCircuit(2)
        qc2.h(0)
        qc2.cx(0, 1)

        assert circuits_equivalent(qc1, qc2), "Identical circuits should be equivalent"

    def test_different_circuits_not_equivalent(self):
        """Test that different circuits are not equivalent."""
        from tests.helpers.circuit_comparison import circuits_equivalent

        # Bell state
        qc1 = QuantumCircuit(2)
        qc1.h(0)
        qc1.cx(0, 1)

        # Just Hadamard (separable state)
        qc2 = QuantumCircuit(2)
        qc2.h(0)

        assert not circuits_equivalent(qc1, qc2), "Different circuits should not be equivalent"


class TestStatisticalProperties:
    """Test statistical properties of quantum measurements."""

    def test_measurement_uncertainty(self):
        """Test that measurement uncertainty matches theoretical prediction."""
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure([0, 1], [0, 1])

        simulator = AerSimulator()
        transpiled = transpile(qc, simulator)

        # Collect data from multiple runs
        deviations = []
        for _ in range(20):
            job = simulator.run(transpiled, shots=1000)
            counts = job.result().get_counts()
            prob_00 = counts.get('00', 0) / 1000
            deviation = abs(prob_00 - 0.5)
            deviations.append(deviation)

        # Mean deviation should be small
        mean_deviation = np.mean(deviations)
        assert mean_deviation < 0.03, "Mean deviation should be < 3%"

        # Most deviations should be within expected range
        within_range = sum(1 for d in deviations if d < 0.03)
        assert within_range >= 15, "Most runs should be within expected range"

    def test_correlation_perfect(self):
        """Test that Bell state shows perfect correlation."""
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure([0, 1], [0, 1])

        simulator = AerSimulator()
        transpiled = transpile(qc, simulator)
        job = simulator.run(transpiled, shots=1000)
        counts = job.result().get_counts()

        # Calculate correlation
        # Both qubits should always have same value
        correlated = counts.get('00', 0) + counts.get('11', 0)
        uncorrelated = counts.get('01', 0) + counts.get('10', 0)

        assert correlated == 1000, "All measurements should be correlated"
        assert uncorrelated == 0, "No uncorrelated measurements"


class TestIntegration:
    """Integration tests combining multiple aspects."""

    def test_complete_bell_state_workflow(self):
        """Test complete workflow from circuit creation to analysis."""
        # Create circuit
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure([0, 1], [0, 1])

        # Simulate
        simulator = AerSimulator()
        transpiled = transpile(qc, simulator)
        job = simulator.run(transpiled, shots=1000)
        result = job.result()
        counts = result.get_counts()

        # Analyze
        count_00 = counts.get('00', 0)
        count_11 = counts.get('11', 0)
        prob_00 = count_00 / 1000
        prob_11 = count_11 / 1000

        # All checks
        assert qc.num_qubits == 2, "Circuit structure correct"
        assert '00' in counts or '11' in counts, "Valid outcomes present"
        assert 0.4 < prob_00 < 0.6, "Probability in expected range"
        assert 0.4 < prob_11 < 0.6, "Probability in expected range"
        assert np.isclose(prob_00 + prob_11, 1.0, atol=0.01), "Probabilities sum to 1"

    def test_separable_vs_entangled_comparison(self):
        """Test distinguishing separable from entangled states."""
        # Entangled (Bell state)
        qc_ent = QuantumCircuit(2)
        qc_ent.h(0)
        qc_ent.cx(0, 1)
        sv_ent = Statevector.from_instruction(qc_ent)

        # Separable
        qc_sep = QuantumCircuit(2)
        qc_sep.h(0)
        sv_sep = Statevector.from_instruction(qc_sep)

        from tests.helpers.quantum_validation import is_entangled_state

        assert is_entangled_state(sv_ent.data), "Bell state should be entangled"
        assert not is_entangled_state(sv_sep.data), "Product state should not be entangled"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

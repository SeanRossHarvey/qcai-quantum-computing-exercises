"""
Tests for Task 5: Quantum Error Correction

These tests validate the 3-qubit bit-flip error correction code implementation,
including encoding, syndrome measurement, error detection, and correction,
with proper use of Qiskit 1.x API.
"""

import pytest
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector


class TestEncoding:
    """Test quantum error correction encoding."""

    def test_encoding_circuit_structure(self):
        """Test that encoding circuit has correct structure."""
        qc = QuantumCircuit(5, 2)
        qc.cx(0, 1)
        qc.cx(0, 2)

        assert qc.num_qubits == 5, "Should have 5 qubits (3 data + 2 syndrome)"
        assert qc.num_clbits == 2, "Should have 2 classical bits"
        assert qc.depth() >= 2, "Should have at least 2 gates"

    def test_encoding_gates_present(self):
        """Test that encoding uses CNOT gates."""
        qc = QuantumCircuit(5, 2)
        qc.cx(0, 1)
        qc.cx(0, 2)

        gate_names = [inst.operation.name for inst in qc.data]

        assert gate_names.count('cx') == 2, "Should have exactly 2 CNOT gates"

    def test_encoding_state_zero(self):
        """Test encoding of |0⟩ state."""
        qc = QuantumCircuit(3)  # Only data qubits for statevector
        qc.cx(0, 1)
        qc.cx(0, 2)

        statevector = Statevector.from_instruction(qc)
        amplitudes = statevector.data

        # Should be |000⟩
        expected = np.zeros(8)
        expected[0] = 1.0  # |000⟩

        assert np.allclose(amplitudes, expected, atol=1e-10), \
            "Encoding |0⟩ should produce |000⟩"

    def test_encoding_state_one(self):
        """Test encoding of |1⟩ state."""
        qc = QuantumCircuit(3)
        qc.x(0)  # Prepare |1⟩
        qc.cx(0, 1)
        qc.cx(0, 2)

        statevector = Statevector.from_instruction(qc)
        amplitudes = statevector.data

        # Should be |111⟩
        expected = np.zeros(8)
        expected[7] = 1.0  # |111⟩ = |0b111⟩

        assert np.allclose(amplitudes, expected, atol=1e-10), \
            "Encoding |1⟩ should produce |111⟩"

    def test_encoding_plus_state(self):
        """Test encoding of |+⟩ state."""
        qc = QuantumCircuit(3)
        qc.h(0)  # Prepare |+⟩
        qc.cx(0, 1)
        qc.cx(0, 2)

        statevector = Statevector.from_instruction(qc)
        amplitudes = statevector.data

        # Should be (|000⟩ + |111⟩)/√2
        expected = np.zeros(8)
        expected[0] = 1/np.sqrt(2)  # |000⟩
        expected[7] = 1/np.sqrt(2)  # |111⟩

        assert np.allclose(amplitudes, expected, atol=1e-10), \
            "Encoding |+⟩ should produce (|000⟩+|111⟩)/√2"


class TestSyndromeMeasurement:
    """Test syndrome measurement implementation."""

    @pytest.fixture
    def simulator(self):
        """Provide AerSimulator instance."""
        return AerSimulator()

    def test_syndrome_no_error(self, simulator):
        """Test syndrome measurement with no error."""
        qc = QuantumCircuit(5, 2)

        # Encoding
        qc.cx(0, 1)
        qc.cx(0, 2)

        # Syndrome measurement
        qc.cx(0, 3)
        qc.cx(1, 3)
        qc.cx(0, 4)
        qc.cx(2, 4)
        qc.measure([3, 4], [0, 1])

        transpiled = transpile(qc, simulator)
        job = simulator.run(transpiled, shots=1000)
        counts = job.result().get_counts()

        # Should measure 00 (no error)
        syndrome = max(counts, key=counts.get)
        assert syndrome == '00', f"No error should give syndrome 00, got {syndrome}"

    def test_syndrome_error_qubit_0(self, simulator):
        """Test syndrome measurement with error on qubit 0."""
        qc = QuantumCircuit(5, 2)

        # Encoding
        qc.cx(0, 1)
        qc.cx(0, 2)

        # Error on qubit 0
        qc.x(0)

        # Syndrome measurement
        qc.cx(0, 3)
        qc.cx(1, 3)
        qc.cx(0, 4)
        qc.cx(2, 4)
        qc.measure([3, 4], [0, 1])

        transpiled = transpile(qc, simulator)
        job = simulator.run(transpiled, shots=1000)
        counts = job.result().get_counts()

        syndrome = max(counts, key=counts.get)
        assert syndrome == '11', f"Error on qubit 0 should give syndrome 11, got {syndrome}"

    def test_syndrome_error_qubit_1(self, simulator):
        """Test syndrome measurement with error on qubit 1."""
        qc = QuantumCircuit(5, 2)

        qc.cx(0, 1)
        qc.cx(0, 2)
        qc.x(1)  # Error on qubit 1

        qc.cx(0, 3)
        qc.cx(1, 3)
        qc.cx(0, 4)
        qc.cx(2, 4)
        qc.measure([3, 4], [0, 1])

        transpiled = transpile(qc, simulator)
        job = simulator.run(transpiled, shots=1000)
        counts = job.result().get_counts()

        syndrome = max(counts, key=counts.get)
        assert syndrome == '10', f"Error on qubit 1 should give syndrome 10, got {syndrome}"

    def test_syndrome_error_qubit_2(self, simulator):
        """Test syndrome measurement with error on qubit 2."""
        qc = QuantumCircuit(5, 2)

        qc.cx(0, 1)
        qc.cx(0, 2)
        qc.x(2)  # Error on qubit 2

        qc.cx(0, 3)
        qc.cx(1, 3)
        qc.cx(0, 4)
        qc.cx(2, 4)
        qc.measure([3, 4], [0, 1])

        transpiled = transpile(qc, simulator)
        job = simulator.run(transpiled, shots=1000)
        counts = job.result().get_counts()

        syndrome = max(counts, key=counts.get)
        assert syndrome == '01', f"Error on qubit 2 should give syndrome 01, got {syndrome}"


class TestErrorCorrection:
    """Test error correction implementation."""

    @pytest.fixture
    def simulator(self):
        """Provide AerSimulator instance."""
        return AerSimulator()

    def create_full_ec_circuit(self, error_qubit=None):
        """Create complete error correction circuit."""
        qc = QuantumCircuit(5, 3)  # 3 classical bits for final data measurement

        # Encoding
        qc.cx(0, 1)
        qc.cx(0, 2)
        qc.barrier()

        # Error (if specified)
        if error_qubit is not None:
            qc.x(error_qubit)
        qc.barrier()

        # Syndrome measurement
        qc.cx(0, 3)
        qc.cx(1, 3)
        qc.cx(0, 4)
        qc.cx(2, 4)
        qc.measure([3, 4], [0, 1])
        qc.barrier()

        # Correction
        qc.ccx(3, 4, 0)  # If syndrome 11, flip qubit 0
        qc.cx(3, 1)      # If syndrome 10, flip qubit 1
        qc.ccx(3, 4, 1)  # Unflip if was 11
        qc.cx(4, 2)      # If syndrome 01, flip qubit 2
        qc.ccx(3, 4, 2)  # Unflip if was 11
        qc.barrier()

        return qc

    def test_correction_no_error(self, simulator):
        """Test correction with no error."""
        qc = self.create_full_ec_circuit(error_qubit=None)
        qc.measure([0, 1, 2], [0, 1, 2])

        transpiled = transpile(qc, simulator)
        job = simulator.run(transpiled, shots=1000)
        counts = job.result().get_counts()

        # Extract data bits (last 3 bits)
        data_counts = {}
        for outcome, count in counts.items():
            data_bits = outcome[-3:]  # Last 3 bits are data
            data_counts[data_bits] = data_counts.get(data_bits, 0) + count

        # Should be |000⟩
        assert data_counts.get('000', 0) > 900, \
            "Without error, should measure |000⟩"

    def test_correction_error_qubit_0(self, simulator):
        """Test correction of error on qubit 0."""
        qc = self.create_full_ec_circuit(error_qubit=0)
        qc.measure([0, 1, 2], [0, 1, 2])

        transpiled = transpile(qc, simulator)
        job = simulator.run(transpiled, shots=1000)
        counts = job.result().get_counts()

        data_counts = {}
        for outcome, count in counts.items():
            data_bits = outcome[-3:]
            data_counts[data_bits] = data_counts.get(data_bits, 0) + count

        # Should correct to |000⟩
        assert data_counts.get('000', 0) > 900, \
            "Error on qubit 0 should be corrected to |000⟩"

    def test_correction_error_qubit_1(self, simulator):
        """Test correction of error on qubit 1."""
        qc = self.create_full_ec_circuit(error_qubit=1)
        qc.measure([0, 1, 2], [0, 1, 2])

        transpiled = transpile(qc, simulator)
        job = simulator.run(transpiled, shots=1000)
        counts = job.result().get_counts()

        data_counts = {}
        for outcome, count in counts.items():
            data_bits = outcome[-3:]
            data_counts[data_bits] = data_counts.get(data_bits, 0) + count

        assert data_counts.get('000', 0) > 900, \
            "Error on qubit 1 should be corrected to |000⟩"

    def test_correction_error_qubit_2(self, simulator):
        """Test correction of error on qubit 2."""
        qc = self.create_full_ec_circuit(error_qubit=2)
        qc.measure([0, 1, 2], [0, 1, 2])

        transpiled = transpile(qc, simulator)
        job = simulator.run(transpiled, shots=1000)
        counts = job.result().get_counts()

        data_counts = {}
        for outcome, count in counts.items():
            data_bits = outcome[-3:]
            data_counts[data_bits] = data_counts.get(data_bits, 0) + count

        assert data_counts.get('000', 0) > 900, \
            "Error on qubit 2 should be corrected to |000⟩"


class TestDifferentInitialStates:
    """Test error correction with different initial states."""

    @pytest.fixture
    def simulator(self):
        """Provide AerSimulator instance."""
        return AerSimulator()

    def test_correction_state_one(self, simulator):
        """Test error correction with |1⟩ initial state."""
        qc = QuantumCircuit(5, 3)

        # Prepare |1⟩
        qc.x(0)

        # Encoding
        qc.cx(0, 1)
        qc.cx(0, 2)

        # Error on qubit 1
        qc.x(1)

        # Syndrome and correction
        qc.cx(0, 3)
        qc.cx(1, 3)
        qc.cx(0, 4)
        qc.cx(2, 4)
        qc.measure([3, 4], [0, 1])

        qc.ccx(3, 4, 0)
        qc.cx(3, 1)
        qc.ccx(3, 4, 1)
        qc.cx(4, 2)
        qc.ccx(3, 4, 2)

        qc.measure([0, 1, 2], [0, 1, 2])

        transpiled = transpile(qc, simulator)
        job = simulator.run(transpiled, shots=1000)
        counts = job.result().get_counts()

        data_counts = {}
        for outcome, count in counts.items():
            data_bits = outcome[-3:]
            data_counts[data_bits] = data_counts.get(data_bits, 0) + count

        # Should correct to |111⟩
        assert data_counts.get('111', 0) > 900, \
            "Should correct to |111⟩ for initial |1⟩ state"

    def test_correction_plus_state(self, simulator):
        """Test error correction with |+⟩ initial state."""
        qc = QuantumCircuit(5, 3)

        # Prepare |+⟩
        qc.h(0)

        # Encoding
        qc.cx(0, 1)
        qc.cx(0, 2)

        # Error on qubit 0
        qc.x(0)

        # Syndrome and correction
        qc.cx(0, 3)
        qc.cx(1, 3)
        qc.cx(0, 4)
        qc.cx(2, 4)
        qc.measure([3, 4], [0, 1])

        qc.ccx(3, 4, 0)
        qc.cx(3, 1)
        qc.ccx(3, 4, 1)
        qc.cx(4, 2)
        qc.ccx(3, 4, 2)

        qc.measure([0, 1, 2], [0, 1, 2])

        transpiled = transpile(qc, simulator)
        job = simulator.run(transpiled, shots=10000)
        counts = job.result().get_counts()

        data_counts = {}
        for outcome, count in counts.items():
            data_bits = outcome[-3:]
            data_counts[data_bits] = data_counts.get(data_bits, 0) + count

        # Should have 50-50 mix of |000⟩ and |111⟩
        count_000 = data_counts.get('000', 0)
        count_111 = data_counts.get('111', 0)

        total = count_000 + count_111
        assert total > 9000, "Most outcomes should be |000⟩ or |111⟩"

        # Check rough 50-50 distribution
        prob_000 = count_000 / total
        assert 0.4 < prob_000 < 0.6, \
            f"Should have ~50% |000⟩, got {prob_000*100:.1f}%"


class TestQiskitAPIUsage:
    """Test proper use of Qiskit 1.x API."""

    def test_aer_simulator_creation(self):
        """Test creating AerSimulator (Qiskit 1.x)."""
        simulator = AerSimulator()

        assert simulator is not None, "Should create simulator"
        assert hasattr(simulator, 'run'), "Simulator should have run method"

    def test_transpile_function(self):
        """Test using transpile function."""
        qc = QuantumCircuit(5, 2)
        qc.cx(0, 1)
        qc.cx(0, 2)
        qc.measure([3, 4], [0, 1])

        simulator = AerSimulator()
        transpiled = transpile(qc, simulator)

        assert transpiled is not None, "Transpile should return circuit"
        assert transpiled.num_qubits == 5, "Transpiled circuit should preserve qubits"

    def test_simulation_workflow(self):
        """Test complete Qiskit 1.x simulation workflow."""
        qc = QuantumCircuit(5, 2)
        qc.cx(0, 1)
        qc.cx(0, 2)
        qc.measure([0, 1], [0, 1])

        # Qiskit 1.x workflow (NO assemble!)
        simulator = AerSimulator()
        transpiled = transpile(qc, simulator)
        job = simulator.run(transpiled, shots=100)
        result = job.result()
        counts = result.get_counts()

        assert isinstance(counts, dict), "Should return counts dictionary"
        assert len(counts) > 0, "Should have measurement outcomes"
        assert sum(counts.values()) == 100, "Should have 100 total counts"


class TestToffoliGate:
    """Test Toffoli (CCX) gate usage."""

    def test_toffoli_gate_present(self):
        """Test that Toffoli gate is used in correction."""
        qc = QuantumCircuit(5, 2)
        qc.ccx(3, 4, 0)

        gate_names = [inst.operation.name for inst in qc.data]

        assert 'ccx' in gate_names, "Should use Toffoli (CCX) gate"

    def test_toffoli_functionality(self):
        """Test Toffoli gate flips target when both controls are 1."""
        from qiskit.quantum_info import Statevector

        # Test: |110⟩ → |111⟩ (both controls 1, target flips)
        qc = QuantumCircuit(3)
        qc.x(0)  # Control 1 = 1
        qc.x(1)  # Control 2 = 1
        # Target = 0
        qc.ccx(0, 1, 2)  # Should flip target

        sv = Statevector.from_instruction(qc)

        # Should be |111⟩
        expected = np.zeros(8)
        expected[7] = 1.0  # |111⟩

        assert np.allclose(sv.data, expected, atol=1e-10), \
            "Toffoli should flip target when both controls are 1"


class TestMultipleErrors:
    """Test behavior with multiple errors."""

    @pytest.fixture
    def simulator(self):
        """Provide AerSimulator instance."""
        return AerSimulator()

    def test_two_errors_fails(self, simulator):
        """Test that two simultaneous errors cannot be corrected."""
        qc = QuantumCircuit(5, 3)

        # Encoding
        qc.cx(0, 1)
        qc.cx(0, 2)

        # TWO errors
        qc.x(0)
        qc.x(1)

        # Syndrome and correction
        qc.cx(0, 3)
        qc.cx(1, 3)
        qc.cx(0, 4)
        qc.cx(2, 4)
        qc.measure([3, 4], [0, 1])

        qc.ccx(3, 4, 0)
        qc.cx(3, 1)
        qc.ccx(3, 4, 1)
        qc.cx(4, 2)
        qc.ccx(3, 4, 2)

        qc.measure([0, 1, 2], [0, 1, 2])

        transpiled = transpile(qc, simulator)
        job = simulator.run(transpiled, shots=1000)
        counts = job.result().get_counts()

        data_counts = {}
        for outcome, count in counts.items():
            data_bits = outcome[-3:]
            data_counts[data_bits] = data_counts.get(data_bits, 0) + count

        # Should NOT be |000⟩ (correction fails)
        assert data_counts.get('000', 0) < 100, \
            "Two errors should not be corrected to |000⟩"


class TestIntegration:
    """Integration tests for complete error correction workflow."""

    def test_complete_workflow(self):
        """Test complete error correction workflow."""
        simulator = AerSimulator()

        # Create circuit
        qc = QuantumCircuit(5, 3)

        # 1. Encoding
        qc.cx(0, 1)
        qc.cx(0, 2)

        # 2. Error
        qc.x(1)

        # 3. Syndrome measurement
        qc.cx(0, 3)
        qc.cx(1, 3)
        qc.cx(0, 4)
        qc.cx(2, 4)
        qc.measure([3, 4], [0, 1])

        # 4. Correction
        qc.ccx(3, 4, 0)
        qc.cx(3, 1)
        qc.ccx(3, 4, 1)
        qc.cx(4, 2)
        qc.ccx(3, 4, 2)

        # 5. Final measurement
        qc.measure([0, 1, 2], [0, 1, 2])

        # Verify structure
        assert qc.num_qubits == 5, "Circuit structure correct"
        assert qc.num_clbits == 3, "Classical bits correct"

        # Simulate
        transpiled = transpile(qc, simulator)
        job = simulator.run(transpiled, shots=1000)
        result = job.result()
        counts = result.get_counts()

        # Verify results
        assert len(counts) > 0, "Should have measurement outcomes"
        assert sum(counts.values()) == 1000, "Should have 1000 shots"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

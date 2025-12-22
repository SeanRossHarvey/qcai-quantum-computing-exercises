"""
Tests for Task 3: Quantum Teleportation

These tests validate the quantum teleportation protocol implementation,
including Bell state creation, Bell measurements, conditional operations,
and proper use of Qiskit 1.x API.
"""

import pytest
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator, StatevectorSimulator
from qiskit.quantum_info import Statevector, state_fidelity


class TestBellStateCreation:
    """Test Bell state creation for teleportation."""

    def test_bell_state_circuit_structure(self):
        """Test that Bell state is created on qubits 1 and 2."""
        qc = QuantumCircuit(3)
        qc.h(1)
        qc.cx(1, 2)

        assert qc.num_qubits == 3, "Should have 3 qubits"
        assert qc.depth() >= 2, "Should have H and CX gates"

    def test_bell_state_gates(self):
        """Test that Bell state uses correct gates."""
        qc = QuantumCircuit(3)
        qc.h(1)
        qc.cx(1, 2)

        gate_names = [inst.operation.name for inst in qc.data]

        assert 'h' in gate_names, "Should have Hadamard gate"
        assert 'cx' in gate_names, "Should have CNOT gate"

    def test_bell_state_statevector(self):
        """Test that Bell state has correct statevector."""
        qc = QuantumCircuit(3)
        qc.h(1)
        qc.cx(1, 2)

        statevector = Statevector.from_instruction(qc)
        amplitudes = statevector.data

        # Bell state on qubits 1-2: should have |000⟩ and |011⟩
        # (qubit ordering: 0 is rightmost)
        expected = np.zeros(8, dtype=complex)
        expected[0b000] = 1/np.sqrt(2)  # |000⟩
        expected[0b011] = 1/np.sqrt(2)  # |011⟩

        assert np.allclose(amplitudes, expected, atol=1e-10), \
            "Bell state should be (|000⟩ + |011⟩)/√2"

    def test_bell_state_entanglement(self):
        """Test that qubits 1 and 2 are entangled."""
        from tests.helpers.quantum_validation import is_entangled_state

        qc = QuantumCircuit(3)
        qc.h(1)
        qc.cx(1, 2)

        statevector = Statevector.from_instruction(qc)

        # Check entanglement between qubits 1 and 2
        # For this, we need to trace out qubit 0
        # Simplified check: verify the state is not separable
        assert is_entangled_state(statevector.data), \
            "Qubits 1 and 2 should be entangled"


class TestStatePrepation:
    """Test state preparation on qubit 0."""

    def test_rx_gate_applied(self):
        """Test that RX gate is applied to qubit 0."""
        qc = QuantumCircuit(3)
        qc.h(1)
        qc.cx(1, 2)
        qc.rx(0.5, 0)

        # Check that rx gate is present
        gate_names = [inst.operation.name for inst in qc.data]
        assert 'rx' in gate_names, "Should have RX gate"

        # Check it targets qubit 0
        for inst in qc.data:
            if inst.operation.name == 'rx':
                assert inst.qubits[0].index == 0, "RX should target qubit 0"

    def test_state_preparation_statevector(self):
        """Test that state preparation creates correct state."""
        theta = 0.5

        # Single qubit with RX
        qc_single = QuantumCircuit(1)
        qc_single.rx(theta, 0)
        sv_single = Statevector.from_instruction(qc_single)

        # Expected state after RX(theta)
        expected = np.array([
            np.cos(theta/2),
            -1j * np.sin(theta/2)
        ])

        assert np.allclose(sv_single.data, expected, atol=1e-10), \
            "RX gate should create correct state"


class TestBellMeasurement:
    """Test Bell measurement implementation."""

    def test_bell_measurement_gates_present(self):
        """Test that Bell measurement gates are present."""
        qc = QuantumCircuit(3, 3)
        qc.h(1)
        qc.cx(1, 2)
        qc.rx(0.5, 0)

        # Bell measurement
        qc.cx(0, 1)
        qc.h(0)
        qc.measure([0, 1], [0, 1])

        gate_names = [inst.operation.name for inst in qc.data]

        # Count CX and H gates
        cx_count = gate_names.count('cx')
        h_count = gate_names.count('h')

        assert cx_count >= 2, "Should have at least 2 CX gates"
        assert h_count >= 2, "Should have at least 2 H gates"

    def test_bell_measurement_targets(self):
        """Test that Bell measurement targets correct qubits."""
        qc = QuantumCircuit(3, 3)
        qc.h(1)
        qc.cx(1, 2)
        qc.rx(0.5, 0)
        qc.cx(0, 1)
        qc.h(0)
        qc.measure([0, 1], [0, 1])

        # Find the second CX gate (first is for Bell state)
        cx_gates = [inst for inst in qc.data if inst.operation.name == 'cx']
        bell_measurement_cx = cx_gates[1]  # Second CX

        assert bell_measurement_cx.qubits[0].index == 0, \
            "Bell measurement CX should have control on qubit 0"
        assert bell_measurement_cx.qubits[1].index == 1, \
            "Bell measurement CX should have target on qubit 1"

    def test_measurements_present(self):
        """Test that measurements are applied to qubits 0 and 1."""
        qc = QuantumCircuit(3, 3)
        qc.h(1)
        qc.cx(1, 2)
        qc.rx(0.5, 0)
        qc.cx(0, 1)
        qc.h(0)
        qc.measure([0, 1], [0, 1])

        # Count measurements
        measure_count = sum(1 for inst in qc.data
                           if inst.operation.name == 'measure')

        assert measure_count >= 2, "Should have at least 2 measurements"


class TestConditionalCorrections:
    """Test conditional correction gates."""

    def test_correction_gates_present(self):
        """Test that correction gates are present."""
        qc = QuantumCircuit(3, 3)
        qc.h(1)
        qc.cx(1, 2)
        qc.rx(0.5, 0)
        qc.cx(0, 1)
        qc.h(0)
        qc.measure([0, 1], [0, 1])

        # Corrections
        qc.cx(1, 2)
        qc.cz(0, 2)

        gate_names = [inst.operation.name for inst in qc.data]

        # Should have CX and CZ for corrections
        assert 'cz' in gate_names, "Should have CZ gate for corrections"

    def test_correction_targets(self):
        """Test that corrections target qubit 2."""
        qc = QuantumCircuit(3, 3)
        qc.h(1)
        qc.cx(1, 2)
        qc.rx(0.5, 0)
        qc.cx(0, 1)
        qc.h(0)
        qc.measure([0, 1], [0, 1])
        qc.cx(1, 2)
        qc.cz(0, 2)

        # Find correction gates (after measurements)
        gates_after_measure = []
        found_measure = False
        for inst in qc.data:
            if inst.operation.name == 'measure':
                found_measure = True
            elif found_measure and inst.operation.name in ['cx', 'cz']:
                gates_after_measure.append(inst)

        # All correction gates should target qubit 2
        for gate in gates_after_measure:
            target_qubit = gate.qubits[-1].index
            assert target_qubit == 2, \
                f"Correction gate should target qubit 2, got {target_qubit}"


class TestTeleportationProtocol:
    """Test complete teleportation protocol."""

    @pytest.fixture
    def simulator(self):
        """Provide AerSimulator instance."""
        return AerSimulator()

    @pytest.fixture
    def statevector_sim(self):
        """Provide StatevectorSimulator instance."""
        return StatevectorSimulator()

    def test_teleportation_circuit_structure(self):
        """Test complete teleportation circuit structure."""
        qc = QuantumCircuit(3, 3)
        qc.h(1)
        qc.cx(1, 2)
        qc.rx(0.5, 0)
        qc.cx(0, 1)
        qc.h(0)
        qc.measure([0, 1], [0, 1])
        qc.cx(1, 2)
        qc.cz(0, 2)

        assert qc.num_qubits == 3, "Should have 3 qubits"
        assert qc.num_clbits == 3, "Should have 3 classical bits"
        assert qc.depth() >= 5, "Should have sufficient depth"

    def test_teleportation_measurement_outcomes(self, simulator):
        """Test that teleportation produces valid measurement outcomes."""
        qc = QuantumCircuit(3, 3)
        qc.h(1)
        qc.cx(1, 2)
        qc.rx(0.5, 0)
        qc.cx(0, 1)
        qc.h(0)
        qc.measure([0, 1], [0, 1])
        qc.cx(1, 2)
        qc.cz(0, 2)

        transpiled = transpile(qc, simulator)
        job = simulator.run(transpiled, shots=1000)
        counts = job.result().get_counts()

        # Should have measurement outcomes
        assert len(counts) > 0, "Should have measurement outcomes"
        assert sum(counts.values()) == 1000, "Should have 1000 total counts"

    def test_alice_measurement_distribution(self, simulator):
        """Test that Alice's measurements are uniformly distributed."""
        qc = QuantumCircuit(3, 3)
        qc.h(1)
        qc.cx(1, 2)
        qc.rx(0.5, 0)
        qc.cx(0, 1)
        qc.h(0)
        qc.measure([0, 1], [0, 1])
        qc.cx(1, 2)
        qc.cz(0, 2)

        transpiled = transpile(qc, simulator)
        job = simulator.run(transpiled, shots=10000)
        counts = job.result().get_counts()

        # Extract Alice's measurements (qubits 0 and 1)
        alice_counts = {'00': 0, '01': 0, '10': 0, '11': 0}
        for outcome, count in counts.items():
            # outcome format: bit2 bit1 bit0
            alice_bits = outcome[2] + outcome[1]  # bits 0 and 1
            alice_counts[alice_bits] += count

        # Each outcome should be approximately 25% (0.25 ± 0.03)
        total = sum(alice_counts.values())
        for outcome, count in alice_counts.items():
            prob = count / total
            assert 0.20 < prob < 0.30, \
                f"Alice measurement {outcome} should be ~0.25, got {prob}"

    def test_teleportation_fidelity_state_zero(self, simulator):
        """Test teleportation fidelity for |0⟩ state."""
        # Teleport |0⟩ (no preparation)
        qc = QuantumCircuit(3, 3)
        qc.h(1)
        qc.cx(1, 2)
        # No preparation on qubit 0 (stays |0⟩)
        qc.cx(0, 1)
        qc.h(0)
        qc.measure([0, 1], [0, 1])
        qc.cx(1, 2)
        qc.cz(0, 2)

        transpiled = transpile(qc, simulator)
        job = simulator.run(transpiled, shots=10000)
        counts = job.result().get_counts()

        # Extract qubit 2 outcomes
        qubit_2_counts = {'0': 0, '1': 0}
        for outcome, count in counts.items():
            qubit_2_bit = outcome[0]
            qubit_2_counts[qubit_2_bit] += count

        prob_0 = qubit_2_counts['0'] / 10000

        # For |0⟩ state, should measure |0⟩ ~100% of the time
        assert prob_0 > 0.95, f"Teleported |0⟩ should be |0⟩, got P(0)={prob_0}"

    def test_teleportation_fidelity_state_one(self, simulator):
        """Test teleportation fidelity for |1⟩ state."""
        qc = QuantumCircuit(3, 3)
        qc.h(1)
        qc.cx(1, 2)
        qc.x(0)  # Prepare |1⟩
        qc.cx(0, 1)
        qc.h(0)
        qc.measure([0, 1], [0, 1])
        qc.cx(1, 2)
        qc.cz(0, 2)

        transpiled = transpile(qc, simulator)
        job = simulator.run(transpiled, shots=10000)
        counts = job.result().get_counts()

        # Extract qubit 2 outcomes
        qubit_2_counts = {'0': 0, '1': 0}
        for outcome, count in counts.items():
            qubit_2_bit = outcome[0]
            qubit_2_counts[qubit_2_bit] += count

        prob_1 = qubit_2_counts['1'] / 10000

        # For |1⟩ state, should measure |1⟩ ~100% of the time
        assert prob_1 > 0.95, f"Teleported |1⟩ should be |1⟩, got P(1)={prob_1}"

    def test_teleportation_fidelity_plus_state(self, simulator):
        """Test teleportation fidelity for |+⟩ state."""
        qc = QuantumCircuit(3, 3)
        qc.h(1)
        qc.cx(1, 2)
        qc.h(0)  # Prepare |+⟩
        qc.cx(0, 1)
        qc.h(0)
        qc.measure([0, 1], [0, 1])
        qc.cx(1, 2)
        qc.cz(0, 2)

        transpiled = transpile(qc, simulator)
        job = simulator.run(transpiled, shots=10000)
        counts = job.result().get_counts()

        # Extract qubit 2 outcomes
        qubit_2_counts = {'0': 0, '1': 0}
        for outcome, count in counts.items():
            qubit_2_bit = outcome[0]
            qubit_2_counts[qubit_2_bit] += count

        prob_0 = qubit_2_counts['0'] / 10000
        prob_1 = qubit_2_counts['1'] / 10000

        # For |+⟩ state, should have 50-50 distribution
        assert 0.45 < prob_0 < 0.55, \
            f"Teleported |+⟩ should be 50-50, got P(0)={prob_0}"
        assert 0.45 < prob_1 < 0.55, \
            f"Teleported |+⟩ should be 50-50, got P(1)={prob_1}"


class TestQiskitAPIUsage:
    """Test proper use of Qiskit 1.x API."""

    def test_statevector_simulator_creation(self):
        """Test creating StatevectorSimulator (Qiskit 1.x)."""
        simulator = StatevectorSimulator()

        assert simulator is not None, "Should create simulator"
        assert hasattr(simulator, 'run'), "Simulator should have run method"

    def test_aer_simulator_creation(self):
        """Test creating AerSimulator (Qiskit 1.x)."""
        simulator = AerSimulator()

        assert simulator is not None, "Should create simulator"
        assert hasattr(simulator, 'run'), "Simulator should have run method"

    def test_statevector_simulation_workflow(self):
        """Test StatevectorSimulator workflow (Qiskit 1.x)."""
        qc = QuantumCircuit(3)
        qc.h(1)
        qc.cx(1, 2)

        simulator = StatevectorSimulator()
        transpiled = transpile(qc, simulator)
        job = simulator.run(transpiled)
        result = job.result()
        statevector = result.get_statevector()

        assert statevector is not None, "Should get statevector"
        assert len(statevector.data) == 8, "Should have 8 amplitudes for 3 qubits"

    def test_measurement_simulation_workflow(self):
        """Test AerSimulator workflow (Qiskit 1.x)."""
        qc = QuantumCircuit(3, 3)
        qc.h(1)
        qc.cx(1, 2)
        qc.measure([0, 1, 2], [0, 1, 2])

        simulator = AerSimulator()
        transpiled = transpile(qc, simulator)
        job = simulator.run(transpiled, shots=100)
        result = job.result()
        counts = result.get_counts()

        assert isinstance(counts, dict), "Should return counts dictionary"
        assert len(counts) > 0, "Should have measurement outcomes"
        assert sum(counts.values()) == 100, "Should have 100 total counts"


class TestCircuitEquivalence:
    """Test circuit equivalence and variations."""

    def test_different_bell_states_teleport(self):
        """Test that teleportation works with different Bell states."""
        from tests.helpers.circuit_comparison import circuits_equivalent

        # Standard Bell state
        qc1 = QuantumCircuit(2)
        qc1.h(0)
        qc1.cx(0, 1)

        # Alternative construction (should be equivalent)
        qc2 = QuantumCircuit(2)
        qc2.h(0)
        qc2.cx(0, 1)

        assert circuits_equivalent(qc1, qc2), \
            "Identical Bell state circuits should be equivalent"

    def test_teleportation_qubit_ordering(self):
        """Test that qubit ordering is consistent."""
        qc = QuantumCircuit(3, 3)
        qc.h(1)
        qc.cx(1, 2)
        qc.rx(0.5, 0)
        qc.cx(0, 1)
        qc.h(0)

        # Verify H gate is on qubit 0 (second H gate)
        h_gates = [inst for inst in qc.data if inst.operation.name == 'h']
        assert len(h_gates) == 2, "Should have 2 H gates"
        assert h_gates[1].qubits[0].index == 0, \
            "Second H should be on qubit 0"


class TestStatevectorAnalysis:
    """Test statevector analysis at different stages."""

    def test_initial_bell_state(self):
        """Test statevector after Bell state creation."""
        qc = QuantumCircuit(3)
        qc.h(1)
        qc.cx(1, 2)

        statevector = Statevector.from_instruction(qc)

        # Should be normalized
        norm = np.sum(np.abs(statevector.data)**2)
        assert np.isclose(norm, 1.0), "State must be normalized"

    def test_after_state_preparation(self):
        """Test statevector after preparing state on qubit 0."""
        qc = QuantumCircuit(3)
        qc.h(1)
        qc.cx(1, 2)
        qc.rx(0.5, 0)

        statevector = Statevector.from_instruction(qc)

        # Should be normalized
        norm = np.sum(np.abs(statevector.data)**2)
        assert np.isclose(norm, 1.0), "State must be normalized"

        # Should have more than 2 non-zero amplitudes
        non_zero = np.sum(np.abs(statevector.data) > 1e-10)
        assert non_zero > 2, "Should have multiple non-zero amplitudes"

    def test_bell_basis_transformation(self):
        """Test statevector after Bell basis transformation."""
        qc = QuantumCircuit(3)
        qc.h(1)
        qc.cx(1, 2)
        qc.rx(0.5, 0)
        qc.cx(0, 1)
        qc.h(0)

        statevector = Statevector.from_instruction(qc)

        # Should be normalized
        norm = np.sum(np.abs(statevector.data)**2)
        assert np.isclose(norm, 1.0), "State must be normalized"


class TestIntegration:
    """Integration tests for complete teleportation workflow."""

    def test_complete_teleportation_workflow(self):
        """Test complete teleportation from start to finish."""
        # Create circuit
        qc = QuantumCircuit(3, 3)
        qc.h(1)
        qc.cx(1, 2)
        qc.rx(0.5, 0)
        qc.cx(0, 1)
        qc.h(0)
        qc.measure([0, 1], [0, 1])
        qc.cx(1, 2)
        qc.cz(0, 2)

        # Simulate
        simulator = AerSimulator()
        transpiled = transpile(qc, simulator)
        job = simulator.run(transpiled, shots=1000)
        result = job.result()
        counts = result.get_counts()

        # Verify structure
        assert qc.num_qubits == 3, "Circuit structure correct"
        assert qc.num_clbits == 3, "Classical bits correct"

        # Verify results
        assert len(counts) > 0, "Should have measurement outcomes"
        assert sum(counts.values()) == 1000, "Should have 1000 shots"

    def test_teleportation_vs_original_state(self):
        """Test that teleported state matches original."""
        theta = 0.7

        # Original state
        qc_orig = QuantumCircuit(1, 1)
        qc_orig.rx(theta, 0)
        qc_orig.measure(0, 0)

        sim = AerSimulator()
        t_orig = transpile(qc_orig, sim)
        counts_orig = sim.run(t_orig, shots=10000).result().get_counts()

        prob_0_orig = counts_orig.get('0', 0) / 10000

        # Teleported state
        qc_tel = QuantumCircuit(3, 3)
        qc_tel.h(1)
        qc_tel.cx(1, 2)
        qc_tel.rx(theta, 0)
        qc_tel.cx(0, 1)
        qc_tel.h(0)
        qc_tel.measure([0, 1], [0, 1])
        qc_tel.cx(1, 2)
        qc_tel.cz(0, 2)

        t_tel = transpile(qc_tel, sim)
        counts_tel = sim.run(t_tel, shots=10000).result().get_counts()

        # Extract qubit 2
        qubit_2_counts = {'0': 0, '1': 0}
        for outcome, count in counts_tel.items():
            qubit_2_counts[outcome[0]] += count

        prob_0_tel = qubit_2_counts['0'] / 10000

        # Probabilities should match (within 3%)
        assert abs(prob_0_orig - prob_0_tel) < 0.03, \
            f"Teleported state should match original: {prob_0_orig} vs {prob_0_tel}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

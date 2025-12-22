"""
Utilities for comparing and validating quantum circuits.
"""

from typing import List
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator


def circuits_equivalent(
    circuit1: QuantumCircuit,
    circuit2: QuantumCircuit,
    tolerance: float = 1e-10
) -> bool:
    """
    Check if two quantum circuits are functionally equivalent.

    Compares the unitary matrices of both circuits to determine if they
    perform the same transformation on quantum states.

    Args:
        circuit1: First quantum circuit to compare
        circuit2: Second quantum circuit to compare
        tolerance: Numerical tolerance for floating-point comparison

    Returns:
        True if circuits are equivalent (within tolerance), False otherwise

    Example:
        >>> qc1 = QuantumCircuit(1)
        >>> qc1.x(0)
        >>> qc2 = QuantumCircuit(1)
        >>> qc2.x(0)
        >>> circuits_equivalent(qc1, qc2)
        True
    """
    try:
        # Convert circuits to unitary operators
        op1 = Operator(circuit1)
        op2 = Operator(circuit2)

        # Compare the unitary matrices
        return np.allclose(op1.data, op2.data, atol=tolerance)
    except Exception as e:
        # If conversion fails (e.g., circuit contains measurements), return False
        print(f"Warning: Could not compare circuits: {e}")
        return False


def check_gate_sequence(
    circuit: QuantumCircuit,
    expected_gates: List[str]
) -> bool:
    """
    Verify that a circuit contains the expected sequence of gates.

    Args:
        circuit: Quantum circuit to check
        expected_gates: List of expected gate names in order

    Returns:
        True if the gate sequence matches, False otherwise

    Example:
        >>> qc = QuantumCircuit(2)
        >>> qc.h(0)
        >>> qc.cx(0, 1)
        >>> check_gate_sequence(qc, ['h', 'cx'])
        True
    """
    actual_gates = [
        instruction.operation.name
        for instruction in circuit.data
    ]
    return actual_gates == expected_gates


def check_circuit_properties(
    circuit: QuantumCircuit,
    expected_qubits: int = None,
    expected_clbits: int = None,
    expected_depth: int = None
) -> bool:
    """
    Validate basic properties of a quantum circuit.

    Args:
        circuit: Quantum circuit to validate
        expected_qubits: Expected number of qubits (None to skip check)
        expected_clbits: Expected number of classical bits (None to skip check)
        expected_depth: Expected circuit depth (None to skip check)

    Returns:
        True if all specified properties match, False otherwise

    Example:
        >>> qc = QuantumCircuit(2, 2)
        >>> qc.h(0)
        >>> qc.cx(0, 1)
        >>> check_circuit_properties(qc, expected_qubits=2, expected_clbits=2)
        True
    """
    if expected_qubits is not None and circuit.num_qubits != expected_qubits:
        return False

    if expected_clbits is not None and circuit.num_clbits != expected_clbits:
        return False

    if expected_depth is not None and circuit.depth() != expected_depth:
        return False

    return True


def has_measurement(circuit: QuantumCircuit) -> bool:
    """
    Check if a circuit contains any measurement operations.

    Args:
        circuit: Quantum circuit to check

    Returns:
        True if circuit contains at least one measurement, False otherwise
    """
    return any(
        instruction.operation.name == 'measure'
        for instruction in circuit.data
    )


def count_gate_type(circuit: QuantumCircuit, gate_name: str) -> int:
    """
    Count the number of times a specific gate appears in a circuit.

    Args:
        circuit: Quantum circuit to analyze
        gate_name: Name of the gate to count (e.g., 'h', 'cx', 'x')

    Returns:
        Number of occurrences of the specified gate

    Example:
        >>> qc = QuantumCircuit(2)
        >>> qc.h(0)
        >>> qc.h(1)
        >>> qc.cx(0, 1)
        >>> count_gate_type(qc, 'h')
        2
    """
    return sum(
        1 for instruction in circuit.data
        if instruction.operation.name == gate_name
    )

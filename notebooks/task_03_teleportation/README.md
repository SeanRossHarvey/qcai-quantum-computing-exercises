# Task 3: Quantum Teleportation

**Difficulty**: Intermediate
**Prerequisites**: Task 1 (Entanglement), basic quantum gates
**Estimated Time**: 60-75 minutes

## Learning Objectives

By completing this task, you will:

- ✅ Understand the quantum teleportation protocol
- ✅ Implement entanglement-based quantum communication
- ✅ Work with 3-qubit quantum systems
- ✅ Perform Bell measurements
- ✅ Apply conditional quantum operations
- ✅ Visualise statevectors using Qiskit tools
- ✅ Use `StatevectorSimulator` for quantum state analysis

## Overview

Quantum teleportation is a protocol for transmitting quantum information using entanglement and classical communication. It demonstrates that quantum information can be transferred without physically moving the quantum system itself.

### The Teleportation Protocol

**Setup**:
- **Alice** has a qubit in an unknown state $|\psi\rangle$ that she wants to send to **Bob**
- Alice and Bob share an entangled Bell pair

**Protocol**:
1. Create Bell state between qubits 1 and 2 (shared by Alice and Bob)
2. Prepare the state $|\psi\rangle$ on qubit 0 (Alice's qubit to teleport)
3. Alice performs a Bell measurement on qubits 0 and 1
4. Alice sends her measurement results to Bob (classical communication)
5. Bob applies corrections to qubit 2 based on Alice's results
6. Qubit 2 now contains the state $|\psi\rangle$

### Key Insight

The original state on qubit 0 is **destroyed** during measurement (no-cloning theorem), but the information is **transferred** to qubit 2 through entanglement.

## Mathematical Background

### Initial State to Teleport

We'll use a general single-qubit state:

$$|\psi\rangle = \cos(\theta/2)|0\rangle + e^{i\phi}\sin(\theta/2)|1\rangle$$

For simplicity, we often use states created by rotation gates like $R_X(\theta)$:

$$R_X(\theta) = \begin{pmatrix} \cos(\theta/2) & -i\sin(\theta/2) \\ -i\sin(\theta/2) & \cos(\theta/2) \end{pmatrix}$$

### Bell State

The shared entangled state between Alice and Bob:

$$|\Phi^+\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)$$

### Complete Protocol State Evolution

**Initial state** (3 qubits):

$$|\psi_0\rangle = |\psi\rangle_0 \otimes |\Phi^+\rangle_{12}$$

**After Bell measurement** (qubits 0 and 1):

The measurement projects onto one of four Bell states, collapsing qubit 2 into a state related to $|\psi\rangle$.

**After corrections**:

Qubit 2 is in state $|\psi\rangle$ (exact copy of original).

## Qiskit 1.x Implementation

### ❌ Old API (Pre-1.0)

```python
from qiskit import QuantumCircuit, Aer, transpile, assemble

# Old statevector simulator
simulator = Aer.get_backend('statevector_simulator')
tqc = transpile(qc, simulator)
qobj = assemble(tqc)  # Deprecated!
result = simulator.run(qobj).result()
statevector = result.get_statevector()
```

### ✅ Modern Qiskit 1.x Pattern

```python
from qiskit import QuantumCircuit, transpile
from qiskit_aer import StatevectorSimulator, AerSimulator
from qiskit.visualization import plot_bloch_multivector, plot_state_qsphere

# For statevector analysis
statevector_sim = StatevectorSimulator()
qc_no_measure = QuantumCircuit(3)  # No classical bits
# ... build circuit ...
transpiled = transpile(qc_no_measure, statevector_sim)
job = statevector_sim.run(transpiled)
result = job.result()
statevector = result.get_statevector()

# For measurement outcomes
simulator = AerSimulator()
qc = QuantumCircuit(3, 3)  # With classical bits
# ... build circuit with measurements ...
transpiled = transpile(qc, simulator)
job = simulator.run(transpiled, shots=1000)
result = job.result()
counts = result.get_counts()
```

**Key Changes**:
- Import from `qiskit_aer`, not `qiskit`
- Use `StatevectorSimulator()` instead of `Aer.get_backend('statevector_simulator')`
- **Remove `assemble()`** - deprecated in Qiskit 1.x
- Use `simulator.run(transpiled_circuit)` directly

## Circuit Structure

```
Qubit 0: |ψ⟩ ─────────────●───H───M───────────┐
                          │       │           │
Qubit 1: |0⟩ ───H───●─────X───────M───●───────┼───
                    │             │   │       │
Qubit 2: |0⟩ ───────X─────────────────X───●───●───
                                          │
                                       (CZ if needed)
```

**Gates**:
1. Hadamard on qubit 1
2. CNOT(1, 2) - creates Bell state
3. Prepare state on qubit 0 (e.g., $R_X(0.5)$)
4. CNOT(0, 1) - entangle with Bell pair
5. Hadamard on qubit 0 - complete Bell measurement
6. Measure qubits 0 and 1
7. Conditional X on qubit 2 (if qubit 1 measured |1⟩)
8. Conditional Z on qubit 2 (if qubit 0 measured |1⟩)

## Key Concepts

### Bell Measurement

A measurement in the Bell basis projects two qubits onto one of four maximally entangled states. Implemented by:
- CNOT(0, 1)
- H(0)
- Measure both qubits

### Classical Corrections

Based on measurement outcomes:
- If qubit 1 is |1⟩: apply X gate to qubit 2
- If qubit 0 is |1⟩: apply Z gate to qubit 2

In Qiskit, use `.c_if()` for classical control:
```python
qc.x(2).c_if(creg[1], 1)  # Apply X if classical bit 1 is 1
qc.z(2).c_if(creg[0], 1)  # Apply Z if classical bit 0 is 1
```

### No-Cloning Theorem

Quantum teleportation does **not** violate the no-cloning theorem because:
- The original state on qubit 0 is **destroyed** by measurement
- Only one copy of $|\psi\rangle$ exists at any time
- Classical information must be sent (cannot transmit information faster than light)

## Visualisations

Qiskit provides several statevector visualisation tools:

```python
from qiskit.visualization import (
    plot_bloch_multivector,  # Bloch sphere for each qubit
    plot_state_qsphere,      # Q-sphere representation
    plot_state_city,         # City plot (bar chart)
    plot_state_paulivec      # Pauli vector representation
)

# Example
plot_bloch_multivector(statevector)
```

## Common Pitfalls

### 1. Qubit Ordering
**Issue**: Qiskit uses **little-endian** ordering (qubit 0 is rightmost in ket notation).

```python
# State |001⟩ means:
# Qubit 0 = |1⟩
# Qubit 1 = |0⟩
# Qubit 2 = |0⟩
```

### 2. Measurement Before Corrections
**Issue**: Must measure qubits 0 and 1 **before** applying corrections to qubit 2.

### 3. StatevectorSimulator vs AerSimulator
**Issue**: Cannot get measurement counts from `StatevectorSimulator`.

**Solution**:
- Use `StatevectorSimulator` for state analysis (no measurements)
- Use `AerSimulator` for measurement outcomes

### 4. Teleportation ≠ Faster-than-Light Communication
**Issue**: Classical communication is required (measurement results must be sent).

## Testing Your Implementation

Run the test suite:

```bash
# Test Task 3 specifically
pytest tests/test_task_03.py -v

# Run with detailed output
pytest tests/test_task_03.py -v -s
```

### Expected Test Results

- ✅ Circuit has 3 qubits and 3 classical bits
- ✅ Bell state created correctly
- ✅ Bell measurement implemented
- ✅ Conditional operations present
- ✅ Statevector calculations correct
- ✅ Teleportation preserves quantum state

## Files

- `task_03_starter.ipynb` - Exercises with hints and guidance
- `task_03_solution.ipynb` - Complete implementation with explanations
- `../../tests/test_task_03.py` - Automated test suite

## Next Steps

1. Complete exercises in `task_03_starter.ipynb`
2. Compare with `task_03_solution.ipynb`
3. Run tests: `pytest tests/test_task_03.py`
4. Proceed to Task 4 (Playing Card Magic Trick)

## References

- **Original Paper**: C. H. Bennett et al., "Teleporting an unknown quantum state via dual classical and Einstein-Podolsky-Rosen channels" (1993)
- **Qiskit Documentation**: [Quantum Teleportation Tutorial](https://qiskit.org/textbook/ch-algorithms/teleportation.html)
- **API Migration**: See `docs/QISKIT_MIGRATION.md`

## Help

If you encounter issues:
1. Check `docs/TROUBLESHOOTING.md`
2. Verify installation: `python scripts/verify_installation.py`
3. Review API migration: `docs/QISKIT_MIGRATION.md`

---

**Remember**: Quantum teleportation requires both quantum entanglement **and** classical communication!

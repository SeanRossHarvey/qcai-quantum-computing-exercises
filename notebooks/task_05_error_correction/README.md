# Task 5: Quantum Error Correction

**Quick Launch:**
[![Open Starter in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SeanRossHarvey/qcai-quantum-computing-exercises/blob/main/notebooks/task_05_error_correction/task_05_starter.ipynb)
[![Open Solution in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SeanRossHarvey/qcai-quantum-computing-exercises/blob/main/notebooks/task_05_error_correction/task_05_solution.ipynb)

**Difficulty**: Advanced
**Prerequisites**: Task 1 (Entanglement), Task 3 (Teleportation), multi-qubit gates
**Estimated Time**: 75-90 minutes

## Learning Objectives

By completing this task, you will:

- ✅ Understand quantum error correction principles
- ✅ Implement the 3-qubit bit-flip code
- ✅ Encode quantum information with redundancy
- ✅ Detect and correct single-qubit errors
- ✅ Use Toffoli (CCX) gates for error correction
- ✅ Compare error-free and error-prone scenarios
- ✅ Visualise error correction in action

## Overview

Quantum error correction is essential for building reliable quantum computers. Unlike classical bits, quantum states cannot be copied (no-cloning theorem), making error correction challenging. This task implements the **3-qubit bit-flip code**, the simplest quantum error correction scheme.

### The Problem: Bit-Flip Errors

A **bit-flip error** is when a qubit spontaneously flips from |0⟩ to |1⟩ or vice versa (equivalent to an X gate being applied randomly).

**Classical Solution**: Use redundancy - encode 0 as 000 and 1 as 111. If one bit flips, use majority voting.

**Quantum Challenge**: Cannot simply "copy" a quantum state due to the no-cloning theorem.

**Quantum Solution**: Use entanglement to create redundancy while preserving quantum information.

## The 3-Qubit Bit-Flip Code

### Encoding

Encode a single logical qubit into three physical qubits:

$$|0_L\rangle = |000\rangle$$
$$|1_L\rangle = |111\rangle$$

For a general state $|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$:

$$|\psi_L\rangle = \alpha|000\rangle + \beta|111\rangle$$

**Implementation**:
```python
# Start with |ψ⟩|0⟩|0⟩
qc.cx(0, 1)  # Entangle qubit 0 with qubit 1
qc.cx(0, 2)  # Entangle qubit 0 with qubit 2
# Result: α|000⟩ + β|111⟩
```

### Error Detection

After potential errors, measure **syndrome qubits** to detect which qubit (if any) has flipped.

**Syndrome Measurement**:
- Compare qubits 0 and 1 (store result in ancilla 3)
- Compare qubits 0 and 2 (store result in ancilla 4)

**Syndrome Table**:
| Qubit Flipped | Syndrome (q3, q4) | Meaning |
|---------------|-------------------|---------|
| None | 00 | No error |
| Qubit 0 | 11 | Both checks fail |
| Qubit 1 | 10 | First check fails |
| Qubit 2 | 01 | Second check fails |

### Error Correction

Based on the syndrome measurement, apply X gate to the flipped qubit:

```python
# If syndrome is 11 (qubit 0 flipped)
qc.ccx(3, 4, 0)  # Toffoli: flip qubit 0 if both 3 and 4 are 1

# If syndrome is 10 (qubit 1 flipped)
qc.cx(3, 1)  # Flip qubit 1 if qubit 3 is 1 (and qubit 4 is 0)

# If syndrome is 01 (qubit 2 flipped)
qc.cx(4, 2)  # Flip qubit 2 if qubit 4 is 1 (and qubit 3 is 0)
```

## Qiskit 1.x Implementation

### ❌ Old API (Pre-1.0)

```python
from qiskit import QuantumCircuit, Aer, transpile, assemble

simulator = Aer.get_backend('qasm_simulator')
tqc = transpile(qc, simulator)
qobj = assemble(tqc)  # Deprecated!
result = simulator.run(qobj).result()
```

### ✅ Modern Qiskit 1.x Pattern

```python
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# Create simulator
simulator = AerSimulator()

# Build circuit
qc = QuantumCircuit(5, 2)  # 3 data + 2 syndrome, 2 classical bits
# ... build circuit ...

# Transpile and run (NO assemble!)
transpiled = transpile(qc, simulator)
job = simulator.run(transpiled, shots=1000)
result = job.result()
counts = result.get_counts()
```

**Key Changes**:
- Import from `qiskit_aer`, not `qiskit`
- Use `AerSimulator()` instead of `Aer.get_backend('qasm_simulator')`
- **Remove `assemble()`** - deprecated in Qiskit 1.x
- Use `simulator.run(transpiled_circuit)` directly

## Circuit Structure

### Full Error Correction Circuit

```
Qubit 0: |ψ⟩ ───●───●───────[ERROR?]───●───────M──
                │   │                   │
Qubit 1: |0⟩ ───X───┼───────[ERROR?]───┼───●───M──
                    │                   │   │
Qubit 2: |0⟩ ───────X───────[ERROR?]───┼───┼───M──
                                        │   │
Qubit 3: |0⟩ ─────────────────────────-X───●───●───M
                                            │   │
Qubit 4: |0⟩ ───────────────────────────────X───●───M
                                                │
                                             [CORRECTION]
```

**Stages**:
1. **Encoding**: Create |ψ_L⟩ = α|000⟩ + β|111⟩
2. **Error**: Apply X gate to one qubit (simulate bit flip)
3. **Syndrome Measurement**: Detect which qubit flipped
4. **Correction**: Apply X to flipped qubit based on syndrome

## Key Concepts

### 1. Syndrome Measurement

**Syndrome** = pattern of measurement results that indicates the error type/location without revealing the quantum state itself.

**Crucial Property**: Measuring the syndrome doesn't collapse the encoded state $|\psi_L\rangle$. We measure **correlations** between qubits, not the qubits themselves.

### 2. Toffoli (CCX) Gate

The **Toffoli gate** (CCX) is a three-qubit gate that flips the target if both controls are 1:

$$\text{CCX}|a\rangle|b\rangle|c\rangle = |a\rangle|b\rangle|c \oplus (a \land b)\rangle$$

**In Qiskit**:
```python
qc.ccx(control1, control2, target)
```

**Use in Error Correction**: Toffoli applies correction only when both syndrome bits match a specific pattern.

### 3. No-Cloning Theorem

The no-cloning theorem states that **arbitrary quantum states cannot be copied**. Error correction doesn't violate this because:
- We don't copy $|\psi\rangle$ - we **encode** it into an entangled state
- The encoding uses entanglement, not cloning
- Only one copy of the quantum information exists (spread across 3 qubits)

### 4. Limitation: Single Errors Only

The 3-qubit code corrects **one** bit-flip error. If two or more qubits flip:
- Syndrome measurement gives wrong diagnosis
- Correction fails or makes it worse

**For multiple errors**: Need more sophisticated codes (5-qubit, 7-qubit Steane code, surface codes, etc.)

## Common Pitfalls

### 1. Incorrect Syndrome Interpretation

**Issue**: Mismatching syndrome patterns to qubit errors.

**Solution**: Remember the syndrome table:
- `00` → No error
- `11` → Qubit 0 flipped
- `10` → Qubit 1 flipped
- `01` → Qubit 2 flipped

### 2. Forgetting to Reset Syndrome Qubits

**Issue**: Using syndrome qubits with leftover states.

**Solution**: Initialize syndrome qubits to |0⟩ before syndrome measurement.

### 3. Measuring Data Qubits Too Early

**Issue**: Measuring data qubits before correction destroys quantum information.

**Solution**: Only measure syndrome qubits during error correction. Measure data qubits after correction is complete.

### 4. Using `assemble()` in Qiskit 1.x

**Issue**: Code uses deprecated `assemble()` function.

**Solution**: Remove `assemble()` calls - use `transpile()` then `run()` directly.

## Testing Your Implementation

Run the test suite:

```bash
# Test Task 5 specifically
pytest tests/test_task_05.py -v

# Run with detailed output
pytest tests/test_task_05.py -v -s
```

### Expected Test Results

- ✅ Encoding creates correct logical states
- ✅ Syndrome measurement detects errors
- ✅ Correction recovers original state
- ✅ Works for arbitrary input states
- ✅ Qiskit 1.x API used correctly

## Files

- `task_05_starter.ipynb` - Exercises with hints and guidance
- `task_05_solution.ipynb` - Complete implementation with explanations
- `../../tests/test_task_05.py` - Automated test suite

## Extension Ideas

- Implement phase-flip error correction
- Combine bit-flip and phase-flip codes (Shor code)
- Explore the 5-qubit perfect code
- Simulate multiple error scenarios
- Implement error correction with noise models

## Error Correction in Practice

**Real quantum computers** use much more sophisticated codes:
- **Surface codes**: 2D lattice, distance-3 → 9 qubits per logical qubit
- **Topological codes**: Robust against local noise
- **Fault-tolerant operations**: Errors during correction don't cascade

**Key Insight**: Quantum error correction is **overhead** - we need many physical qubits to encode one logical qubit. Current research aims to reduce this overhead.

## Help

If you encounter issues:
1. Check `docs/TROUBLESHOOTING.md`
2. Verify Qiskit 1.x installation: `python scripts/verify_installation.py`
3. Review API migration: `docs/QISKIT_MIGRATION.md`
4. Check syndrome measurement logic carefully

---

**Remember**: Error correction doesn't prevent errors - it detects and fixes them! Quantum computers will always have errors; error correction makes them manageable.

# Qiskit API Migration Guide: 0.x → 1.x

This guide provides comprehensive information for migrating code from Qiskit 0.x (pre-1.0) to Qiskit 1.x, focusing on the changes relevant to the QCAI exercises.

## Overview

Qiskit 1.0 introduced significant API changes to improve consistency, performance, and maintainability. The most impactful changes affect:
- Simulator backends (Aer)
- Circuit execution workflow
- Import statements
- Deprecated functions

**All exercises in this repository use Qiskit 1.x API.**

---

## Quick Migration Checklist

- [ ] Update imports: `from qiskit_aer import AerSimulator`
- [ ] Replace `Aer.get_backend()` with direct simulator classes
- [ ] Remove all `assemble()` function calls
- [ ] Replace `execute()` with `transpile() + run()`
- [ ] Update virtual environment: `pip install qiskit>=1.0.0 qiskit-aer>=0.13.0`
- [ ] Test with verification script: `python scripts/verify_installation.py`

---

## Key Changes Summary

| Component | Qiskit 0.x | Qiskit 1.x |
|-----------|------------|------------|
| **Aer Import** | `from qiskit import Aer` | `from qiskit_aer import AerSimulator` |
| **Get Backend** | `Aer.get_backend('qasm_simulator')` | `AerSimulator()` |
| **Execute** | `execute(qc, backend, shots=1000)` | `backend.run(transpiled, shots=1000)` |
| **Assemble** | `qobj = assemble(transpiled)` | *Removed - not needed* |
| **Run** | `backend.run(qobj)` | `backend.run(transpiled)` |

---

## Detailed Migration Examples

### 1. Imports

#### OLD (Qiskit 0.x)
```python
from qiskit import QuantumCircuit, Aer, execute, transpile, assemble
from qiskit.visualization import plot_histogram
```

#### NEW (Qiskit 1.x)
```python
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator, StatevectorSimulator
from qiskit.visualization import plot_histogram
```

**Key Changes**:
- `Aer` → Import specific simulators from `qiskit_aer`
- `execute` and `assemble` → Removed
- `transpile` → Still in `qiskit`
- `QuantumCircuit` → Still in `qiskit`

---

### 2. Simulator Creation

#### OLD (Qiskit 0.x)
```python
# QASM simulator (measurement-based)
qasm_simulator = Aer.get_backend('qasm_simulator')

# Statevector simulator (wavefunction)
statevector_simulator = Aer.get_backend('statevector_simulator')

# Unitary simulator
unitary_simulator = Aer.get_backend('unitary_simulator')
```

#### NEW (Qiskit 1.x)
```python
from qiskit_aer import AerSimulator, StatevectorSimulator, UnitarySimulator

# Measurement-based simulation
simulator = AerSimulator()

# Statevector simulation
statevector_sim = StatevectorSimulator()

# Unitary simulation
unitary_sim = UnitarySimulator()
```

**Key Changes**:
- Direct class instantiation instead of string-based backend lookup
- Import from `qiskit_aer` package
- No need for `get_backend()` method

---

### 3. Circuit Execution Workflow

#### OLD (Qiskit 0.x) - Method 1: execute()
```python
from qiskit import QuantumCircuit, Aer, execute

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=1000)
result = job.result()
counts = result.get_counts()
```

#### NEW (Qiskit 1.x)
```python
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

simulator = AerSimulator()
transpiled_qc = transpile(qc, simulator)
job = simulator.run(transpiled_qc, shots=1000)
result = job.result()
counts = result.get_counts()
```

**Key Changes**:
- `execute()` → `transpile()` + `simulator.run()`
- `Aer.get_backend()` → `AerSimulator()`
- More explicit workflow

---

#### OLD (Qiskit 0.x) - Method 2: transpile + assemble
```python
from qiskit import QuantumCircuit, Aer, transpile, assemble

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

backend = Aer.get_backend('qasm_simulator')
transpiled_qc = transpile(qc, backend)
qobj = assemble(transpiled_qc, backend, shots=1000)  # ❌ Deprecated
result = backend.run(qobj).result()
counts = result.get_counts()
```

#### NEW (Qiskit 1.x)
```python
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

simulator = AerSimulator()
transpiled_qc = transpile(qc, simulator)
# NO assemble() call!
result = simulator.run(transpiled_qc, shots=1000).result()
counts = result.get_counts()
```

**Key Changes**:
- **Remove `assemble()`** completely
- Pass `shots` to `run()` method instead
- `backend.run(transpiled)` directly

---

### 4. Statevector Simulation

#### OLD (Qiskit 0.x)
```python
from qiskit import QuantumCircuit, Aer, execute

qc = QuantumCircuit(2)  # No classical bits
qc.h(0)
qc.cx(0, 1)

backend = Aer.get_backend('statevector_simulator')
job = execute(qc, backend)
result = job.result()
statevector = result.get_statevector()
```

#### NEW (Qiskit 1.x)
```python
from qiskit import QuantumCircuit, transpile
from qiskit_aer import StatevectorSimulator

qc = QuantumCircuit(2)  # No classical bits
qc.h(0)
qc.cx(0, 1)

statevector_sim = StatevectorSimulator()
transpiled_qc = transpile(qc, statevector_sim)
job = statevector_sim.run(transpiled_qc)
result = job.result()
statevector = result.get_statevector()
```

**Key Changes**:
- `StatevectorSimulator()` class instead of string lookup
- Same `transpile() + run()` workflow
- Import from `qiskit_aer`

---

### 5. Alternative: Statevector from Instruction

#### OLD (Qiskit 0.x)
```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

# This works in both versions
statevector = Statevector.from_instruction(qc)
```

#### NEW (Qiskit 1.x)
```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

# Still works the same way
statevector = Statevector.from_instruction(qc)
```

**Note**: `Statevector.from_instruction()` works in both versions and doesn't require migration.

---

## Task-Specific Migration Examples

### Task 1: Quantum Entanglement

#### OLD
```python
from qiskit import QuantumCircuit, Aer, execute

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

simulator = Aer.get_backend('qasm_simulator')
job = execute(qc, simulator, shots=1000)
counts = job.result().get_counts()
```

#### NEW
```python
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

simulator = AerSimulator()
transpiled = transpile(qc, simulator)
job = simulator.run(transpiled, shots=1000)
counts = job.result().get_counts()
```

---

### Task 3: Quantum Teleportation

#### OLD
```python
from qiskit import QuantumCircuit, Aer, transpile, assemble

qc = QuantumCircuit(3, 3)
# ... build teleportation circuit ...

simulator = Aer.get_backend('statevector_simulator')
tqc = transpile(qc, simulator)
qobj = assemble(tqc)  # ❌ Remove this
result = simulator.run(qobj).result()
statevector = result.get_statevector()
```

#### NEW
```python
from qiskit import QuantumCircuit, transpile
from qiskit_aer import StatevectorSimulator

qc = QuantumCircuit(3, 3)
# ... build teleportation circuit ...

simulator = StatevectorSimulator()
transpiled = transpile(qc, simulator)
result = simulator.run(transpiled).result()
statevector = result.get_statevector()
```

---

### Task 5: Quantum Error Correction

#### OLD
```python
from qiskit import QuantumCircuit, Aer, transpile, assemble

qc = QuantumCircuit(5, 2)
# ... build error correction circuit ...

backend = Aer.get_backend('qasm_simulator')
transpiled = transpile(qc, backend)
qobj = assemble(transpiled, shots=1000)
result = backend.run(qobj).result()
counts = result.get_counts()
```

#### NEW
```python
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

qc = QuantumCircuit(5, 2)
# ... build error correction circuit ...

simulator = AerSimulator()
transpiled = transpile(qc, simulator)
result = simulator.run(transpiled, shots=1000).result()
counts = result.get_counts()
```

---

## Common Migration Errors

### Error 1: `AttributeError: module 'qiskit' has no attribute 'Aer'`

**Cause**: Using Qiskit 0.x import with Qiskit 1.x installation.

**Fix**:
```python
# Change this:
from qiskit import Aer
simulator = Aer.get_backend('qasm_simulator')

# To this:
from qiskit_aer import AerSimulator
simulator = AerSimulator()
```

---

### Error 2: `NameError: name 'assemble' is not defined`

**Cause**: Trying to use deprecated `assemble()` function.

**Fix**:
```python
# Remove this line:
qobj = assemble(transpiled_circuit)

# And change:
result = backend.run(qobj).result()

# To:
result = backend.run(transpiled_circuit, shots=1000).result()
```

---

### Error 3: `ModuleNotFoundError: No module named 'qiskit_aer'`

**Cause**: `qiskit-aer` package not installed.

**Fix**:
```bash
pip install qiskit-aer
```

---

### Error 4: `TypeError: run() missing 1 required positional argument`

**Cause**: Trying to pass `qobj` to `run()` in Qiskit 1.x.

**Fix**:
```python
# Change this:
result = simulator.run(qobj).result()

# To this:
result = simulator.run(transpiled_circuit).result()
```

---

## Verification After Migration

### 1. Check Imports
```python
# This should work:
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator, StatevectorSimulator

print("Imports successful!")
```

### 2. Test Basic Circuit
```python
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

simulator = AerSimulator()
transpiled = transpile(qc, simulator)
job = simulator.run(transpiled, shots=100)
result = job.result()
counts = result.get_counts()

print("Circuit execution successful!")
print(counts)
```

### 3. Run Verification Script
```bash
python scripts/verify_installation.py
```

Expected output:
```
[OK] Python 3.10.x
[OK] qiskit: 1.0.x
[OK] qiskit_aer: 0.13.x
[OK] Successfully created and simulated a quantum circuit
[SUCCESS] All checks passed!
```

---

## Best Practices for Qiskit 1.x

### 1. Always Transpile
```python
# Good practice:
transpiled = transpile(qc, simulator)
result = simulator.run(transpiled, shots=1000).result()

# Avoid:
result = simulator.run(qc, shots=1000).result()  # May work but not optimal
```

### 2. Use Explicit Simulator Classes
```python
# Good:
from qiskit_aer import AerSimulator
simulator = AerSimulator()

# Avoid:
# (Old style, no longer works)
```

### 3. Keep Circuit and Classical Registers Separate
```python
# Good:
qc = QuantumCircuit(3, 3)  # Clear: 3 qubits, 3 classical bits

# Less clear:
qc = QuantumCircuit(3)  # Only qubits, no classical bits
```

### 4. Specify Shots Explicitly
```python
# Good:
result = simulator.run(transpiled, shots=1000).result()

# Avoid relying on defaults:
result = simulator.run(transpiled).result()  # Uses default shots
```

---

## Migration Workflow

For migrating existing Qiskit 0.x code:

### Step 1: Update Dependencies
```bash
pip install --upgrade qiskit qiskit-aer
```

### Step 2: Fix Imports
```python
# Find and replace:
from qiskit import Aer, execute, assemble
# With:
from qiskit_aer import AerSimulator, StatevectorSimulator
```

### Step 3: Update Simulator Creation
```python
# Find:
simulator = Aer.get_backend('qasm_simulator')
# Replace:
simulator = AerSimulator()

# Find:
simulator = Aer.get_backend('statevector_simulator')
# Replace:
simulator = StatevectorSimulator()
```

### Step 4: Remove assemble()
```python
# Find:
qobj = assemble(transpiled, ...)
result = simulator.run(qobj).result()

# Replace:
result = simulator.run(transpiled, shots=1000).result()
```

### Step 5: Replace execute()
```python
# Find:
result = execute(qc, backend, shots=1000).result()

# Replace:
transpiled = transpile(qc, backend)
result = backend.run(transpiled, shots=1000).result()
```

### Step 6: Test Thoroughly
```bash
pytest  # Run all tests
python scripts/verify_installation.py
```

---

## Additional Resources

### Official Documentation
- [Qiskit 1.0 Migration Guide](https://qiskit.org/documentation/migration_guides/qiskit_1.0.html)
- [Qiskit Documentation](https://qiskit.org/documentation/)
- [Qiskit Aer Documentation](https://qiskit.org/ecosystem/aer/)

### What's New in Qiskit 1.x
- Improved performance
- More consistent API
- Better error messages
- Simplified simulator access
- Removed deprecated functions

### Breaking Changes Summary
- **Removed**: `execute()`, `assemble()`, `Aer.get_backend()`
- **Changed**: Simulator imports moved to `qiskit_aer`
- **Improved**: Transpilation and execution workflow

---

## Quick Reference Card

```python
# === IMPORTS ===
# OLD: from qiskit import Aer, execute, assemble
# NEW: from qiskit_aer import AerSimulator, StatevectorSimulator

# === SIMULATOR CREATION ===
# OLD: simulator = Aer.get_backend('qasm_simulator')
# NEW: simulator = AerSimulator()

# === EXECUTION ===
# OLD: job = execute(qc, backend, shots=1000)
# NEW: transpiled = transpile(qc, backend)
#      job = backend.run(transpiled, shots=1000)

# === NO ASSEMBLE ===
# OLD: qobj = assemble(transpiled, shots=1000)
#      result = backend.run(qobj).result()
# NEW: result = backend.run(transpiled, shots=1000).result()
```

---

**Remember**: All exercises in this repository use Qiskit 1.x API. If you encounter old Qiskit 0.x code elsewhere, use this guide to migrate it to the modern API.

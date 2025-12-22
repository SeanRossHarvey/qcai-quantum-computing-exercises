# Troubleshooting Guide

This guide provides solutions to common issues you might encounter while working with the QCAI Quantum Computing exercises.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Qiskit Errors](#qiskit-errors)
- [Jupyter Notebook Issues](#jupyter-notebook-issues)
- [Circuit Errors](#circuit-errors)
- [Measurement and Simulation Issues](#measurement-and-simulation-issues)
- [Test Failures](#test-failures)
- [Performance Issues](#performance-issues)
- [API Migration Issues](#api-migration-issues)

---

## Installation Issues

### Problem: `pip install` fails with dependency conflicts

**Symptoms**:
```
ERROR: Could not find a version that satisfies the requirement qiskit>=1.0.0
```

**Solutions**:

1. **Ensure Python 3.10+**:
   ```bash
   python --version  # Should be 3.10.0 or higher
   ```

2. **Upgrade pip**:
   ```bash
   python -m pip install --upgrade pip
   ```

3. **Use a virtual environment**:
   ```bash
   python -m venv qcai_env
   # Windows:
   qcai_env\Scripts\activate
   # macOS/Linux:
   source qcai_env/bin/activate

   pip install -r requirements.txt
   ```

4. **Install dependencies individually**:
   ```bash
   pip install qiskit>=1.0.0
   pip install qiskit-aer>=0.13.0
   pip install numpy matplotlib jupyter pytest
   ```

---

### Problem: ModuleNotFoundError for `qiskit_aer`

**Symptoms**:
```python
ModuleNotFoundError: No module named 'qiskit_aer'
```

**Cause**: Qiskit 1.x split Aer into a separate package.

**Solution**:
```bash
pip install qiskit-aer
```

**Verification**:
```python
from qiskit_aer import AerSimulator
print("Success!")
```

---

### Problem: Verification script fails

**Symptoms**:
```
python scripts/verify_installation.py
[FAIL] Qiskit functionality test failed
```

**Solutions**:

1. **Run with verbose output**:
   ```bash
   python scripts/verify_installation.py
   ```
   Read the error messages carefully.

2. **Check Python version**:
   ```python
   import sys
   print(sys.version)
   # Should be 3.10+
   ```

3. **Check Qiskit version**:
   ```python
   import qiskit
   print(qiskit.__version__)
   # Should be 1.0.0 or higher
   ```

4. **Reinstall Qiskit**:
   ```bash
   pip uninstall qiskit qiskit-aer
   pip install qiskit qiskit-aer
   ```

---

## Qiskit Errors

### Problem: `AttributeError: module 'qiskit' has no attribute 'Aer'`

**Symptoms**:
```python
simulator = qiskit.Aer.get_backend('qasm_simulator')
AttributeError: module 'qiskit' has no attribute 'Aer'
```

**Cause**: Using old Qiskit 0.x API with Qiskit 1.x.

**Solution**: Migrate to Qiskit 1.x API:
```python
# OLD (Qiskit 0.x)
from qiskit import Aer
simulator = Aer.get_backend('qasm_simulator')

# NEW (Qiskit 1.x)
from qiskit_aer import AerSimulator
simulator = AerSimulator()
```

See `docs/QISKIT_MIGRATION.md` for complete migration guide.

---

### Problem: `assemble()` is not defined or deprecated

**Symptoms**:
```python
qobj = assemble(transpiled_circuit)
NameError: name 'assemble' is not defined
```

**Cause**: `assemble()` was removed in Qiskit 1.x.

**Solution**: Remove `assemble()` calls:
```python
# OLD (Qiskit 0.x)
transpiled = transpile(qc, simulator)
qobj = assemble(transpiled)
result = simulator.run(qobj).result()

# NEW (Qiskit 1.x)
transpiled = transpile(qc, simulator)
result = simulator.run(transpiled).result()
```

---

### Problem: `execute()` function not working

**Symptoms**:
```python
from qiskit import execute
ModuleNotFoundError: cannot import name 'execute'
```

**Cause**: `execute()` was deprecated and removed in Qiskit 1.x.

**Solution**: Use `transpile() + run()` workflow:
```python
# OLD
result = execute(qc, simulator, shots=1000).result()

# NEW
transpiled = transpile(qc, simulator)
job = simulator.run(transpiled, shots=1000)
result = job.result()
```

---

## Jupyter Notebook Issues

### Problem: Jupyter notebook server won't start

**Symptoms**:
```
jupyter notebook
Command 'jupyter' not found
```

**Solutions**:

1. **Install Jupyter**:
   ```bash
   pip install jupyter notebook
   ```

2. **Check installation**:
   ```bash
   jupyter --version
   ```

3. **Use alternative startup**:
   ```bash
   python -m notebook
   ```

---

### Problem: Kernel keeps dying or restarting

**Symptoms**:
- Kernel crashes when running certain cells
- "Kernel Restarting" message appears

**Solutions**:

1. **Restart kernel and run all cells**:
   - Kernel → Restart & Run All

2. **Check for memory issues**:
   - Reduce `shots` parameter
   - Close other applications

3. **Update packages**:
   ```bash
   pip install --upgrade qiskit qiskit-aer
   ```

4. **Check for infinite loops** in code

---

### Problem: Plots not displaying in Jupyter

**Symptoms**:
- `plt.show()` doesn't display plots
- Empty output cells

**Solutions**:

1. **Enable matplotlib inline**:
   ```python
   %matplotlib inline
   import matplotlib.pyplot as plt
   ```

2. **Try different backend**:
   ```python
   %matplotlib notebook
   ```

3. **Explicit display**:
   ```python
   from IPython.display import display
   fig = plt.figure()
   # ... plotting code ...
   display(fig)
   ```

---

## Circuit Errors

### Problem: Circuit depth is 0 or unexpected

**Symptoms**:
```python
qc.depth()  # Returns 0 when gates were added
```

**Cause**: Gates added to wrong circuit or circuit was overwritten.

**Solution**:

1. **Check circuit object**:
   ```python
   print(qc)  # Should show gates
   qc.draw()  # Visual verification
   ```

2. **Verify gates were added**:
   ```python
   qc = QuantumCircuit(2)
   qc.h(0)
   qc.cx(0, 1)
   print(f"Depth: {qc.depth()}")  # Should be 2
   ```

---

### Problem: "Qubit index out of range"

**Symptoms**:
```python
qc.cx(0, 3)
QiskitError: "Qubit index 3 out of range for 2-qubit circuit"
```

**Cause**: Trying to apply gate to non-existent qubit.

**Solution**:

1. **Check circuit size**:
   ```python
   print(f"Circuit has {qc.num_qubits} qubits")
   ```

2. **Create circuit with enough qubits**:
   ```python
   qc = QuantumCircuit(4)  # Create 4 qubits
   qc.cx(0, 3)  # Now valid
   ```

3. **Remember**: Qubits are zero-indexed (0, 1, 2, ...)

---

### Problem: Classical register dimension mismatch

**Symptoms**:
```python
qc.measure([0, 1, 2], [0, 1])
QiskitError: "Different number of qubits and classical bits"
```

**Cause**: Measuring more qubits than classical bits available.

**Solution**:

1. **Match dimensions**:
   ```python
   qc = QuantumCircuit(3, 3)  # 3 qubits, 3 classical bits
   qc.measure([0, 1, 2], [0, 1, 2])  # OK
   ```

2. **Or measure fewer qubits**:
   ```python
   qc = QuantumCircuit(3, 2)
   qc.measure([0, 1], [0, 1])  # Measure only 2 qubits
   ```

---

## Measurement and Simulation Issues

### Problem: No measurement results (empty counts)

**Symptoms**:
```python
counts = result.get_counts()
print(counts)  # {}
```

**Cause**: No measurement gates in circuit.

**Solution**:

1. **Add measurements**:
   ```python
   qc.measure_all()  # Measure all qubits
   # OR
   qc.measure([0, 1], [0, 1])  # Measure specific qubits
   ```

2. **Verify measurements present**:
   ```python
   qc.draw()  # Should show measurement symbols
   ```

---

### Problem: Statevector simulator gives measurement counts

**Symptoms**:
- Using StatevectorSimulator but expecting measurement statistics
- Confusion between statevector and measurement simulations

**Solution**:

**For statevector** (no measurements):
```python
from qiskit_aer import StatevectorSimulator

qc = QuantumCircuit(2)  # NO classical bits
qc.h(0)
qc.cx(0, 1)
# NO measurements

sim = StatevectorSimulator()
statevector = sim.run(transpile(qc, sim)).result().get_statevector()
```

**For measurement counts**:
```python
from qiskit_aer import AerSimulator

qc = QuantumCircuit(2, 2)  # WITH classical bits
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])  # WITH measurements

sim = AerSimulator()
counts = sim.run(transpile(qc, sim), shots=1000).result().get_counts()
```

---

### Problem: Unexpected measurement outcomes

**Symptoms**:
- Getting |01⟩ and |10⟩ when expecting only |00⟩ and |11⟩
- Measurement statistics don't match theory

**Debugging Steps**:

1. **Check qubit ordering**:
   - Qiskit uses little-endian: `|q2 q1 q0⟩`
   - Rightmost bit is qubit 0

2. **Verify circuit**:
   ```python
   qc.draw()  # Visual inspection
   print(qc)  # Text representation
   ```

3. **Check for errors in circuit construction**:
   ```python
   # Example: Bell state
   qc = QuantumCircuit(2, 2)
   qc.h(0)  # Superposition on qubit 0
   qc.cx(0, 1)  # Entangle with qubit 1
   qc.measure([0, 1], [0, 1])
   ```

4. **Print measurements**:
   ```python
   for outcome, count in counts.items():
       print(f"|{outcome}⟩: {count}")
   ```

---

## Test Failures

### Problem: Tests fail with "ModuleNotFoundError"

**Symptoms**:
```bash
pytest
ModuleNotFoundError: No module named 'tests.helpers'
```

**Cause**: Python can't find test helper modules.

**Solution**:

1. **Run from repository root**:
   ```bash
   cd qcai-quantum-computing-exercises
   pytest
   ```

2. **Add to Python path**:
   ```bash
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   pytest
   ```

---

### Problem: Tests fail due to statistical variation

**Symptoms**:
```
AssertionError: Probability should be 0.5, got 0.472
```

**Cause**: Quantum measurements are probabilistic.

**Solutions**:

1. **This is normal** for small shot counts
2. **Increase shots** in tests (if you modify them)
3. **Check tolerance** in test assertions
4. **Re-run tests** - statistical fluctuations are expected

---

### Problem: Notebooks fail nbmake tests

**Symptoms**:
```bash
pytest --nbmake notebooks/**/*.ipynb
FAILED: Kernel died during execution
```

**Solutions**:

1. **Run notebooks manually first**:
   ```bash
   jupyter notebook
   # Execute each notebook
   ```

2. **Check for infinite loops or crashes**

3. **Increase timeout**:
   ```bash
   pytest --nbmake --nbmake-timeout=300 notebooks/**/*.ipynb
   ```

---

## Performance Issues

### Problem: Simulation takes too long

**Symptoms**:
- Circuits with many qubits running forever
- High memory usage

**Solutions**:

1. **Reduce shot count**:
   ```python
   shots = 100  # Instead of 10000
   ```

2. **Reduce circuit size**:
   - Use fewer qubits if possible
   - Simplify circuit depth

3. **Use appropriate simulator**:
   ```python
   # For small circuits (< 20 qubits):
   from qiskit_aer import AerSimulator
   sim = AerSimulator()

   # For statevector only (no shots):
   from qiskit_aer import StatevectorSimulator
   sim = StatevectorSimulator()
   ```

---

## API Migration Issues

### Full migration checklist

If you have old Qiskit code to migrate:

- [ ] Replace `from qiskit import Aer` with `from qiskit_aer import AerSimulator`
- [ ] Replace `Aer.get_backend(...)` with `AerSimulator()` or `StatevectorSimulator()`
- [ ] Remove all `assemble()` calls
- [ ] Replace `execute(...)` with `transpile() + run()`
- [ ] Update simulator imports to `qiskit_aer`
- [ ] Test with `python scripts/verify_installation.py`

See `docs/QISKIT_MIGRATION.md` for detailed guide.

---

## General Debugging Tips

### 1. Print Everything
```python
print(f"Circuit depth: {qc.depth()}")
print(f"Num qubits: {qc.num_qubits}")
print(f"Num clbits: {qc.num_clbits}")
print(qc)  # Text representation
```

### 2. Visualise Circuits
```python
qc.draw(output='mpl')
plt.show()
```

### 3. Check Intermediate Results
```python
# After each step
statevector = Statevector.from_instruction(qc)
print(statevector)
```

### 4. Simplify and Isolate
- Start with minimal circuit
- Add complexity incrementally
- Test after each addition

### 5. Use Version Control
```bash
git diff  # See what changed
git checkout -- file.py  # Revert changes
```

---

## Getting Additional Help

### Documentation
- Main README: `README.md`
- Learning path: `docs/LEARNING_PATH.md`
- API migration: `docs/QISKIT_MIGRATION.md`
- Task READMEs in each `notebooks/task_XX_name/` directory

### Qiskit Resources
- [Qiskit Documentation](https://qiskit.org/documentation/)
- [Qiskit Textbook](https://qiskit.org/textbook/)
- [Qiskit GitHub Issues](https://github.com/Qiskit/qiskit/issues)

### Community
- Qiskit Slack workspace
- Quantum Computing Stack Exchange
- GitHub discussions

### Verification
Run the verification script to check your setup:
```bash
python scripts/verify_installation.py
```

---

## Still Stuck?

1. **Check all error messages carefully**
2. **Search error messages online**
3. **Review relevant task README**
4. **Compare your code with solution notebook**
5. **Run tests to see what's expected**
6. **Create minimal reproducible example**

**Remember**: Quantum computing is complex. Take breaks, experiment, and learn from errors!

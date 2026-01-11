# Task 1: Quantum Entanglement and Measurement Statistics

**Quick Launch:**
[![Open Starter in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SeanRossHarvey/qcai-quantum-computing-exercises/blob/main/notebooks/task_01_entanglement/task_01_starter.ipynb)
[![Open Solution in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SeanRossHarvey/qcai-quantum-computing-exercises/blob/main/notebooks/task_01_entanglement/task_01_solution.ipynb)

## Overview

This task introduces quantum computing through hands-on experience with quantum entanglement - one of the most fascinating phenomena in quantum mechanics. You'll create and simulate quantum circuits using Qiskit, observe measurement statistics, and visualise the correlations that arise from entanglement.

## Learning Objectives

By completing this task, you will:

- Create quantum circuits using Qiskit 1.x
- Understand and implement the Hadamard gate for creating superposition
- Use CNOT gates to create entangled states (Bell states)
- Perform quantum measurements and interpret results
- Analyse measurement statistics and quantum correlations
- Visualise probability distributions from quantum circuits
- Understand the difference between classical and quantum correlations

## Prerequisites

**Required Knowledge:**
- Basic Python programming
- Basic understanding of probability and statistics
- Familiarity with NumPy and Matplotlib (helpful)

**Prior Tasks:**
- Task 2 (recommended but not required) - provides mathematical foundation

**Required Libraries:**
- Qiskit 1.x (quantum circuit framework)
- Qiskit Aer (quantum simulator)
- Matplotlib (visualisation)
- NumPy (numerical operations)

## Estimated Time

- **Beginner**: 45-60 minutes
- **With quantum computing background**: 30-45 minutes

## Key Concepts

### 1. Quantum Superposition

Unlike classical bits (0 or 1), qubits can exist in a **superposition** of both states simultaneously:

$$|\\psi\\rangle = \\alpha|0\\rangle + \\beta|1\\rangle$$

where $|\\alpha|^2 + |\\beta|^2 = 1$.

The **Hadamard gate** creates superposition:

$$H|0\\rangle = \\frac{1}{\\sqrt{2}}(|0\\rangle + |1\\rangle) = |+\\rangle$$

### 2. Quantum Entanglement

**Entanglement** is a quantum phenomenon where two qubits become correlated in ways impossible classically. A **Bell state** is a maximally entangled two-qubit state:

$$|\\Phi^+\\rangle = \\frac{1}{\\sqrt{2}}(|00\\rangle + |11\\rangle)$$

Properties:
- Measuring one qubit instantaneously determines the other
- Perfect correlation: if qubit 0 is |0⟩, qubit 1 is also |0⟩
- Cannot be described as independent qubits (non-separable)

### 3. Creating Bell States

**Circuit:**
```
q0: ─H─●─
       │
q1: ───X─
```

**Steps:**
1. Start with |00⟩ (both qubits in state |0⟩)
2. Apply Hadamard to qubit 0: creates $(|0\\rangle + |1\\rangle) \\otimes |0\\rangle$
3. Apply CNOT (qubit 0 controls, qubit 1 target): creates Bell state

**Mathematical evolution:**
$$|00\\rangle \\xrightarrow{H \\otimes I} \\frac{1}{\\sqrt{2}}(|00\\rangle + |10\\rangle) \\xrightarrow{CNOT} \\frac{1}{\\sqrt{2}}(|00\\rangle + |11\\rangle)$$

### 4. CNOT Gate

The **Controlled-NOT (CNOT)** gate is a two-qubit gate:
- If control qubit is |0⟩: target unchanged
- If control qubit is |1⟩: target flipped (NOT applied)

**Truth table:**
- |00⟩ → |00⟩
- |01⟩ → |01⟩
- |10⟩ → |11⟩ (target flipped)
- |11⟩ → |10⟩ (target flipped)

### 5. Quantum Measurement

**Key properties:**
- Measurement is **probabilistic**: outcomes determined by $|\\alpha|^2$, $|\\beta|^2$
- Measurement **collapses** superposition to a definite state
- **Born rule**: Probability of outcome $i$ is $P(i) = |\\langle i|\\psi\\rangle|^2$

**For Bell state:**
- 50% probability of measuring |00⟩
- 50% probability of measuring |11⟩
- 0% probability of measuring |01⟩ or |10⟩
- Perfect correlation: both qubits always give same result

### 6. Measurement Statistics

Due to probabilistic nature, we need multiple measurements (**shots**) to estimate probabilities:

- Run circuit many times (e.g., 1000 shots)
- Count frequency of each outcome
- Frequency approximates true probability
- Statistical fluctuations decrease with more shots: $\\sigma \\propto 1/\\sqrt{N}$

**Example:**
- 1000 shots → might see 487 instances of |00⟩, 513 of |11⟩
- Estimated probabilities: 48.7% and 51.3%
- True probabilities: 50% and 50%
- Deviation: $\\approx 1.6\\%$ (statistical fluctuation)

## Qiskit 1.x API Changes

This task uses **Qiskit 1.x**, which has important API changes from pre-1.0 versions:

### ✅ Modern Qiskit 1.x Pattern

```python
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# Create simulator
simulator = AerSimulator()

# Create and run circuit
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

# Transpile and run
transpiled = transpile(qc, simulator)
job = simulator.run(transpiled, shots=1000)
result = job.result()
counts = result.get_counts()
```

### ❌ Old Pre-1.0 Pattern (Deprecated)

```python
from qiskit import Aer, execute  # Don't use

simulator = Aer.get_backend('qasm_simulator')  # Old way
job = execute(qc, simulator, shots=1000)  # Deprecated
```

**Key differences:**
- Import from `qiskit_aer` not `qiskit`
- Use `AerSimulator()` not `Aer.get_backend()`
- Use `transpile() + simulator.run()` not `execute()`
- No `assemble()` needed in 1.x

## Exercise Structure

This task includes the following exercises:

1. **Setup and Imports** - Import Qiskit 1.x libraries
2. **Create Bell State Circuit** - Build quantum circuit with H and CNOT
3. **Visualise Circuit** - Display circuit diagram
4. **Run Single Simulation** - Execute circuit and observe measurement
5. **Analyse Single Result** - Interpret measurement outcome
6. **Multiple Circuit Executions** - Run circuit many times for statistics
7. **Statistical Analysis** - Calculate probabilities and deviations
8. **Visualise Distribution** - Create bar chart of measurement outcomes
9. **Error Analysis** - Quantify statistical fluctuations
10. **Compare Multiple Runs** - Observe consistency across executions

## Files in This Directory

- `task_01_starter.ipynb` - Student version with exercises to complete
- `task_01_solution.ipynb` - Complete reference solution with explanations
- `README.md` - This file

## Common Pitfalls

### API Confusion (Pre-1.0 vs 1.x)

**Problem:** Using deprecated `execute()` or `Aer.get_backend()`

**Solution:**
```python
# Correct (Qiskit 1.x)
from qiskit_aer import AerSimulator
simulator = AerSimulator()
transpiled = transpile(circuit, simulator)
job = simulator.run(transpiled, shots=1000)
```

### Forgetting to Measure

**Problem:** Circuit has no measurements, returns no results

**Solution:**
```python
qc.measure([0, 1], [0, 1])  # Measure qubits 0,1 to classical bits 0,1
```

### Misunderstanding Measurement Outcomes

**Problem:** Expecting exactly 500/500 split in 1000 shots

**Reality:** Statistical fluctuations are normal (e.g., 487/513)

**Explanation:** Quantum measurement is inherently probabilistic

### Gate Order Confusion

**Problem:** Applying CNOT before Hadamard doesn't create Bell state

**Solution:** Order matters! Hadamard first, then CNOT:
```python
qc.h(0)      # First: create superposition
qc.cx(0, 1)  # Second: create entanglement
```

### Qubit Indexing

**Problem:** Qiskit uses 0-based indexing

**Solution:**
- 2 qubits: indices 0 and 1 (not 1 and 2)
- `qc.cx(0, 1)`: qubit 0 is control, qubit 1 is target

## Testing Your Solution

Run tests for this task:

```bash
# From repository root
pytest tests/test_task_01.py -v
```

Tests verify:
- ✅ Correct circuit structure (H → CNOT → measurements)
- ✅ Bell state creation
- ✅ Measurement statistics match theoretical predictions
- ✅ Proper use of Qiskit 1.x API
- ✅ Visualisations generate correctly

## Visualisation Guide

The task produces several visualisations:

### Circuit Diagram

Shows the quantum circuit structure visually:
```
     ┌───┐     ┌─┐
q_0: ┤ H ├──■──┤M├───
     └───┘┌─┴─┐└╥┘┌─┐
q_1: ─────┤ X ├─╫─┤M├
          └───┘ ║ └╥┘
c: 2/═══════════╩══╩═
                0  1
```

### Measurement Histogram

Bar chart showing frequency of measurement outcomes:
- X-axis: Measurement results (|00⟩, |01⟩, |10⟩, |11⟩)
- Y-axis: Number of occurrences (counts)
- For Bell state: only |00⟩ and |11⟩ should have significant counts

### Statistical Analysis Plots

Multiple executions visualised to show:
- Consistency of probability distribution
- Statistical fluctuations across runs
- Error bars indicating uncertainty
- Deviation from theoretical 50-50 split

## Next Steps

After completing this task:

1. **Compare your solution** with `task_01_solution.ipynb`
2. **Experiment** - Try different gate sequences
3. **Proceed to Task 3** - Use entanglement for quantum teleportation
4. **Advanced exploration:**
   - Create other Bell states (|Φ⁻⟩, |Ψ±⟩)
   - Implement GHZ states (3-qubit entanglement)
   - Study Bell inequality violations

## Further Reading

- **[Qiskit Documentation](https://docs.quantum.ibm.com/)** - Official Qiskit 1.x documentation
- **[Qiskit Textbook: Entanglement](https://qiskit.org/textbook/ch-gates/entangled-states.html)** - Detailed explanation
- **[Bell States](https://en.wikipedia.org/wiki/Bell_state)** - Wikipedia article
- **[EPR Paradox](https://en.wikipedia.org/wiki/EPR_paradox)** - Historical context
- **[Bell's Theorem](https://en.wikipedia.org/wiki/Bell%27s_theorem)** - Non-locality and quantum mechanics

## Key Takeaways

After this task, you should understand:

✅ **Superposition** - Qubits can be in multiple states simultaneously

✅ **Entanglement** - Quantum correlations stronger than classical

✅ **Bell States** - Maximally entangled two-qubit states

✅ **Measurement** - Probabilistic collapse of superposition

✅ **Statistics** - Need multiple shots to estimate probabilities

✅ **Qiskit 1.x** - Modern API for quantum circuit creation and simulation

## Connection to Other Tasks

- **Task 2** provides the linear algebra foundation for understanding quantum states
- **Task 3** uses entanglement for quantum teleportation protocol
- **Task 5** uses multi-qubit entanglement for quantum error correction

Entanglement is the foundation of quantum advantage - it's what makes quantum computers potentially more powerful than classical ones for certain problems!

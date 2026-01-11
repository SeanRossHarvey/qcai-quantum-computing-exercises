# Task 2: Linear Algebra Foundations for Quantum Computing

**Quick Launch:**
[![Open Starter in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SeanRossHarvey/qcai-quantum-computing-exercises/blob/main/notebooks/task_02_linear_algebra/task_02_starter.ipynb)
[![Open Solution in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SeanRossHarvey/qcai-quantum-computing-exercises/blob/main/notebooks/task_02_linear_algebra/task_02_solution.ipynb)

## Overview

This task explores the mathematical foundations of quantum computing through linear algebra. You'll learn how quantum states are represented as vectors and how quantum gates operate as matrix transformations.

## Learning Objectives

By completing this task, you will:

- Represent quantum states as column vectors in Hilbert space
- Implement quantum gates as unitary matrices
- Apply gate operations using matrix multiplication
- Calculate inner products to determine state orthogonality
- Compute tensor products for multi-qubit systems
- Find eigenvalues and eigenvectors of quantum operators

## Prerequisites

**Required Knowledge:**
- Basic Python programming
- Fundamental linear algebra concepts (vectors, matrices, matrix multiplication)
- Complex numbers (basic understanding)

**Prior Tasks:**
- None - this task is independent and can be completed first

**Required Libraries:**
- NumPy (for numerical linear algebra operations)

## Estimated Time

- **Beginner**: 30-45 minutes
- **With prior linear algebra experience**: 20-30 minutes

## Key Concepts

### 1. Quantum States as Vectors

In quantum mechanics, a quantum state is represented as a column vector in a complex vector space (Hilbert space). For a single qubit:

$$
|\psi\rangle = \alpha|0\rangle + \beta|1\rangle = \begin{pmatrix} \alpha \\ \beta \end{pmatrix}
$$

where $|\alpha|^2 + |\beta|^2 = 1$ (normalisation condition).

**Example:**
- $|0\rangle = \begin{pmatrix} 1 \\ 0 \end{pmatrix}$ (computational basis state "zero")
- $|1\rangle = \begin{pmatrix} 0 \\ 1 \end{pmatrix}$ (computational basis state "one")

### 2. Quantum Gates as Matrices

Quantum gates are unitary transformations represented as matrices. They act on quantum states through matrix multiplication.

**Common Single-Qubit Gates:**

**Pauli-X (NOT gate):**
$$
X = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}
$$
Flips $|0\rangle \leftrightarrow |1\rangle$

**Hadamard Gate:**
$$
H = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}
$$
Creates superposition: $H|0\rangle = \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)$

### 3. Gate Application

To apply a gate $U$ to a state $|\psi\rangle$, compute the matrix-vector product:

$$
|\psi'\rangle = U|\psi\rangle
$$

**Example:**
$$
X|0\rangle = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix} \begin{pmatrix} 1 \\ 0 \end{pmatrix} = \begin{pmatrix} 0 \\ 1 \end{pmatrix} = |1\rangle
$$

### 4. Inner Products

The inner product (dot product) of two quantum states $|\psi\rangle$ and $|\phi\rangle$ is:

$$
\langle\psi|\phi\rangle = \sum_i \psi_i^* \phi_i
$$

where $\psi_i^*$ denotes complex conjugate.

**Properties:**
- $|\langle\psi|\phi\rangle|^2$ gives the probability of measuring $|\psi\rangle$ when the system is in state $|\phi\rangle$
- Orthogonal states have inner product zero: $\langle 0|1\rangle = 0$

### 5. Tensor Products

For multi-qubit systems, states are combined using the tensor product (Kronecker product):

$$
|0\rangle \otimes |1\rangle = \begin{pmatrix} 1 \\ 0 \end{pmatrix} \otimes \begin{pmatrix} 0 \\ 1 \end{pmatrix} = \begin{pmatrix} 0 \\ 1 \\ 0 \\ 0 \end{pmatrix} = |01\rangle
$$

In NumPy: `np.kron(state1, state2)`

### 6. Eigenvalues and Eigenvectors

Quantum measurements are described by eigenvalues and eigenvectors of observable operators:

$$
A|\lambda\rangle = \lambda|\lambda\rangle
$$

where $\lambda$ is an eigenvalue and $|\lambda\rangle$ is its corresponding eigenvector.

**Physical Meaning:**
- Eigenvalues represent possible measurement outcomes
- Eigenvectors represent the states that yield definite measurement results

## Exercise Structure

This task contains 10 exercises:

1. **Create quantum state vector** - Represent $|0\rangle$ as NumPy array
2. **Create Pauli-X gate matrix** - Define the NOT gate
3. **Apply Pauli-X gate** - Flip a quantum state
4. **Create Hadamard gate** - Define the superposition gate
5. **Apply Hadamard gate** - Create superposition
6. **Calculate inner product** - Test state orthogonality
7. **Create gate sequence** - Chain multiple gates (X-H-Y)
8. **Calculate tensor product** - Build two-qubit states
9. **Create identity matrix** - The "do nothing" gate
10. **Calculate eigenvalues/eigenvectors** - Analyse quantum operators

## Files in This Directory

- `task_02_starter.ipynb` - Student version with TODO sections to complete
- `task_02_solution.ipynb` - Complete reference solution with explanations
- `README.md` - This file

## Common Pitfalls

### Column vs Row Vectors

**Wrong:**
```python
state = np.array([1, 0])  # This is a row vector (shape: (2,))
```

**Correct:**
```python
state = np.array([[1], [0]])  # Column vector (shape: (2, 1))
```

### Matrix Multiplication Order

Matrix multiplication is not commutative: $AB \neq BA$

**Applying gates in sequence:**
```python
# Apply X then H: H(X|ψ⟩) = (HX)|ψ⟩
result = np.dot(H, np.dot(X, state))
# Or equivalently:
gate_sequence = np.dot(H, X)
result = np.dot(gate_sequence, state)
```

### Complex Conjugate in Inner Products

Use `np.vdot()` instead of `np.dot()` for inner products to ensure proper complex conjugation:

```python
# Correct for complex vectors
inner_product = np.vdot(state1, state2)

# Not: np.dot(state1.T, state2)  # Doesn't handle complex conjugation properly
```

### Normalisation

Quantum states must be normalised: $\langle\psi|\psi\rangle = 1$

```python
# Check normalisation
norm = np.linalg.norm(state)
assert np.isclose(norm, 1.0), "State must be normalised!"
```

## Testing Your Solution

Run tests for this task:

```bash
# From repository root
pytest tests/test_task_02.py -v
```

Tests verify:
- ✅ Correct gate matrix definitions
- ✅ Proper state vector shapes
- ✅ Accurate matrix-vector multiplications
- ✅ Correct inner product calculations
- ✅ Proper tensor product computations
- ✅ Eigenvalue calculation accuracy

## Next Steps

After completing this task:

1. **Review your solutions** - Compare with the solution notebook
2. **Experiment** - Try creating your own gates and states
3. **Proceed to Task 1** - Apply these concepts to actual quantum circuits with Qiskit
4. **Deepen understanding** - Read about unitary matrices and Hermitian operators

## Further Reading

- **[NumPy Linear Algebra Documentation](https://numpy.org/doc/stable/reference/routines.linalg.html)** - Reference for NumPy functions
- **[Qiskit Textbook: Linear Algebra](https://qiskit.org/textbook/ch-appendix/linear_algebra.html)** - Quantum computing perspective
- **[Quantum Computation and Quantum Information](http://mmrc.amss.cas.cn/tlb/201702/W020170224608149940643.pdf)** (Nielsen & Chuang) - Chapter 2: Introduction to quantum mechanics
- **[Mathematics for Quantum Computing](https://arxiv.org/abs/2010.08085)** - arXiv tutorial paper

## Key Takeaways

After this task, you should understand:

✅ Quantum states are vectors in complex Hilbert space

✅ Quantum gates are unitary matrices that transform states

✅ Matrix multiplication implements gate application

✅ Inner products measure state overlap and determine measurement probabilities

✅ Tensor products build multi-qubit systems

✅ Eigenvalues represent measurement outcomes

These mathematical tools are the foundation for all quantum computing operations. Once comfortable with these concepts, you'll find Qiskit circuits much easier to understand and design!

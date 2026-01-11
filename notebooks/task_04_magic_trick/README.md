# Task 4: Playing Card Magic Trick with Quantum States

**Quick Launch:**
[![Open Starter in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SeanRossHarvey/qcai-quantum-computing-exercises/blob/main/notebooks/task_04_magic_trick/task_04_starter.ipynb)
[![Open Solution in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SeanRossHarvey/qcai-quantum-computing-exercises/blob/main/notebooks/task_04_magic_trick/task_04_solution.ipynb)

**Difficulty**: Intermediate
**Prerequisites**: Task 2 (Linear Algebra), understanding of tensor products
**Estimated Time**: 45-60 minutes

## Learning Objectives

By completing this task, you will:

- ✅ Represent classical objects (playing cards) as quantum states
- ✅ Work with high-dimensional quantum systems (32D Hilbert space)
- ✅ Apply tensor (Kronecker) products to combine quantum states
- ✅ Calculate probability amplitudes and inner products
- ✅ Understand quantum measurement probabilities
- ✅ Explore quantum superposition in a classical context

## Overview

This task uses quantum mechanics to perform a "magic trick" with playing cards. We'll represent a deck of playing cards as quantum states and use quantum probability to predict card selections.

### The Magic Trick

**Setup**:
- A deck of 32 playing cards (8 ranks × 4 suits)
- Each card is represented as a quantum state in a 32-dimensional Hilbert space
- A "target" card is selected and encoded quantum mechanically

**Trick**:
- The "magician" prepares a quantum state
- Through quantum probability calculations, we can determine the likelihood of drawing specific cards
- The magic lies in how quantum superposition and inner products reveal information

### Classical vs Quantum

**Classical Approach**:
- Probability of drawing a specific card: 1/32
- No correlation between suits and ranks

**Quantum Approach**:
- Cards are quantum states with probability amplitudes
- Inner products reveal correlations
- Superposition allows multiple cards simultaneously

## Mathematical Background

### Representing Cards as Quantum States

A playing card has two properties:
1. **Rank**: 8 possibilities (e.g., 7, 8, 9, 10, Jack, Queen, King, Ace)
2. **Suit**: 4 possibilities (♠ Spades, ♥ Hearts, ♦ Diamonds, ♣ Clubs)

We encode each as a quantum state:

**Ranks** (8D basis):
$$|7\rangle = \begin{pmatrix} 1 \\ 0 \\ 0 \\ \vdots \\ 0 \end{pmatrix}, \quad |8\rangle = \begin{pmatrix} 0 \\ 1 \\ 0 \\ \vdots \\ 0 \end{pmatrix}, \quad \ldots$$

**Suits** (4D basis):
$$|♠\rangle = \begin{pmatrix} 1 \\ 0 \\ 0 \\ 0 \end{pmatrix}, \quad |♥\rangle = \begin{pmatrix} 0 \\ 1 \\ 0 \\ 0 \end{pmatrix}, \quad \ldots$$

**Complete Card State** (32D = 8 ⊗ 4):

$$|\text{card}\rangle = |\text{rank}\rangle \otimes |\text{suit}\rangle$$

For example, the **7 of Spades**:

$$|7♠\rangle = |7\rangle \otimes |♠\rangle$$

### Tensor (Kronecker) Product

The tensor product combines two quantum systems:

$$|a\rangle \otimes |b\rangle = |a\rangle|b\rangle$$

In NumPy:
```python
np.kron(state_a, state_b)
```

**Example**:
$$\begin{pmatrix} 1 \\ 0 \end{pmatrix} \otimes \begin{pmatrix} 0 \\ 1 \end{pmatrix} = \begin{pmatrix} 0 \\ 1 \\ 0 \\ 0 \end{pmatrix}$$

### Probability Calculations

The probability of measuring a state $|\psi\rangle$ when the system is in state $|\phi\rangle$ is:

$$P(\psi | \phi) = |\langle \psi | \phi \rangle|^2$$

Where $\langle \psi | \phi \rangle$ is the **inner product** (overlap between states).

**Properties**:
- $P \in [0, 1]$
- $P = 1$ when states are identical ($|\psi\rangle = |\phi\rangle$)
- $P = 0$ when states are orthogonal ($\langle \psi | \phi \rangle = 0$)

### Superposition States

A quantum state can be in a **superposition**:

$$|\psi\rangle = \alpha|7♠\rangle + \beta|K♥\rangle$$

where $|\alpha|^2 + |\beta|^2 = 1$ (normalization).

## Key Concepts

### 1. Basis States

Each card corresponds to exactly one basis state in the 32D Hilbert space:
- 32 orthogonal basis vectors
- Each representing one unique card

### 2. Quantum Card Encoding

**Rank Encoding** (8 ranks):
```python
rank_7 = np.array([[1], [0], [0], [0], [0], [0], [0], [0]])  # |7⟩
rank_8 = np.array([[0], [1], [0], [0], [0], [0], [0], [0]])  # |8⟩
# ... etc
```

**Suit Encoding** (4 suits):
```python
spades   = np.array([[1], [0], [0], [0]])  # |♠⟩
hearts   = np.array([[0], [1], [0], [0]])  # |♥⟩
diamonds = np.array([[0], [0], [1], [0]])  # |♦⟩
clubs    = np.array([[0], [0], [0], [1]])  # |♣⟩
```

**Card = Rank ⊗ Suit**:
```python
card_7_spades = np.kron(rank_7, spades)  # 32D vector
```

### 3. Inner Product and Overlap

The inner product measures similarity:

```python
overlap = np.dot(card1.T.conj(), card2)
probability = np.abs(overlap)**2
```

### 4. Superposition and Probability

Create superposition:
```python
superposition = (card1 + card2) / np.sqrt(2)
```

Measure probability:
```python
prob = np.abs(np.dot(card_target.T.conj(), superposition))**2
```

## Implementation Strategy

### Step 1: Define Basis States

Create 8 rank basis states and 4 suit basis states.

### Step 2: Construct Card States

Use Kronecker product to combine rank and suit:
```python
card = np.kron(rank, suit)
```

### Step 3: Calculate Probabilities

Use inner products to find measurement probabilities:
```python
inner_prod = np.dot(state1.T.conj(), state2)
prob = np.abs(inner_prod)**2
```

### Step 4: Explore Superposition

Create and analyse superposition states.

## Common Pitfalls

### 1. Dimension Mismatch
**Issue**: Incorrect vector dimensions in Kronecker product.

**Solution**:
- Ranks: 8×1 column vectors
- Suits: 4×1 column vectors
- Cards: 32×1 column vectors

### 2. Normalization
**Issue**: Superposition states must be normalized.

**Solution**:
```python
state_normalized = state / np.linalg.norm(state)
```

### 3. Complex Conjugate
**Issue**: Forgetting `.conj()` in inner product for complex states.

**Solution**:
```python
inner_product = np.dot(state1.T.conj(), state2)  # Correct
```

### 4. Orthogonality
**Issue**: Different cards should be orthogonal.

**Check**:
```python
overlap = np.dot(card1.T.conj(), card2)
assert np.abs(overlap) < 1e-10  # Should be ~0
```

## Visualisation Ideas

- **Card Probability Matrix**: Heatmap showing probability of each card
- **Inner Product Heatmap**: Overlap between all card pairs
- **Probability Distribution**: Bar chart of measurement probabilities
- **Superposition Amplitudes**: Visualise amplitude across all basis states

## Testing Your Implementation

Run the test suite:

```bash
# Test Task 4 specifically
pytest tests/test_task_04.py -v

# Run with detailed output
pytest tests/test_task_04.py -v -s
```

### Expected Test Results

- ✅ Basis states are orthonormal
- ✅ Card states are correctly constructed
- ✅ Probabilities sum to 1
- ✅ Inner products calculated correctly
- ✅ Superposition states are normalized

## Files

- `task_04_starter.ipynb` - Exercises with hints and guidance
- `task_04_solution.ipynb` - Complete implementation with explanations
- `../../tests/test_task_04.py` - Automated test suite

## Next Steps

1. Complete exercises in `task_04_starter.ipynb`
2. Compare with `task_04_solution.ipynb`
3. Run tests: `pytest tests/test_task_04.py`
4. Proceed to Task 5 (Quantum Error Correction)

## Extension Ideas

- Implement card selection strategies
- Explore correlations between rank and suit
- Calculate probabilities for multiple card draws
- Design your own quantum card game

## Mathematical Note

This task demonstrates that **classical objects can be represented in quantum Hilbert spaces**. While playing cards are classical, encoding them as quantum states allows us to:
- Use quantum probability theory
- Explore superposition and entanglement concepts
- Apply linear algebra to classical problems

The "magic" is purely mathematical - it's about understanding probability amplitudes and inner products in high-dimensional spaces.

## Help

If you encounter issues:
1. Check `docs/TROUBLESHOOTING.md`
2. Review linear algebra concepts in Task 2
3. Verify array shapes with `.shape` attribute

---

**Remember**: Quantum states are just vectors. Card states are 32D vectors. The magic is linear algebra!

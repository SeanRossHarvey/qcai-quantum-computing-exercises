# QCAI Quantum Computing - Learning Path

This document provides a structured learning path through the quantum computing exercises, explaining the pedagogical progression and how concepts build upon each other.

## Overview

The exercises are designed to build quantum computing knowledge progressively, starting with classical foundations and advancing to sophisticated quantum protocols.

**Total estimated time**: 5-8 hours
**Prerequisites**: Basic Python programming, linear algebra
**Tools**: Python 3.10+, Qiskit 1.x, Jupyter notebooks

## Recommended Learning Sequence

### Path 1: Complete Sequence (Recommended)

**For learners new to quantum computing:**

1. **Task 2: Linear Algebra Foundations** (45-60 min)
2. **Task 1: Quantum Entanglement** (45-60 min)
3. **Task 3: Quantum Teleportation** (60-75 min)
4. **Task 4: Playing Card Magic Trick** (45-60 min)
5. **Task 5: Quantum Error Correction** (75-90 min)

### Path 2: Qiskit-Focused (For experienced linear algebra practitioners)

**Skip Task 2 if you're comfortable with vectors and matrices:**

1. **Task 1: Quantum Entanglement** (45-60 min)
2. **Task 3: Quantum Teleportation** (60-75 min)
3. **Task 5: Quantum Error Correction** (75-90 min)
4. **Task 4: Playing Card Magic Trick** (optional, pure NumPy)
5. **Task 2: Linear Algebra Foundations** (review if needed)

### Path 3: Advanced (For quantum computing students)

**Focus on advanced protocols:**

1. **Task 3: Quantum Teleportation** (60-75 min)
2. **Task 5: Quantum Error Correction** (75-90 min)
3. **Task 1: Quantum Entanglement** (review fundamentals)
4. **Tasks 2 & 4** (skip or review if needed)

---

## Detailed Task Breakdown

### Task 2: Linear Algebra Foundations 🔢

**Difficulty**: Beginner
**Estimated Time**: 45-60 minutes
**Type**: Pure NumPy (no Qiskit)

**Why start here**:
- Establishes mathematical foundations for quantum mechanics
- No quantum computing knowledge required
- Builds confidence with computational tools

**Key Concepts**:
- Quantum states as column vectors
- Quantum gates as matrices
- Matrix multiplication (gate application)
- Inner products (measurement probabilities)
- Tensor products (multi-qubit systems)
- Eigenvalues and eigenvectors
- Unitary transformations

**Skills Developed**:
- ✓ Represent quantum states mathematically
- ✓ Apply gates using matrix multiplication
- ✓ Calculate measurement probabilities
- ✓ Combine quantum systems with tensor products

**Prerequisites**: Basic linear algebra (vectors, matrices)

**Builds Toward**: All subsequent tasks rely on these mathematical tools

---

### Task 1: Quantum Entanglement 🔗

**Difficulty**: Beginner-Intermediate
**Estimated Time**: 45-60 minutes
**Type**: Qiskit 1.x

**Why second**:
- First introduction to quantum circuits
- Introduces the Qiskit 1.x API
- Demonstrates quantum's most famous phenomenon
- Uses concepts from Task 2

**Key Concepts**:
- Bell states (maximally entangled states)
- Hadamard gate (creating superposition)
- CNOT gate (creating entanglement)
- Quantum measurement statistics
- No-cloning theorem
- Qiskit circuit construction
- AerSimulator workflow

**Skills Developed**:
- ✓ Build quantum circuits in Qiskit
- ✓ Create superposition and entanglement
- ✓ Simulate quantum circuits
- ✓ Analyse measurement statistics
- ✓ Visualise quantum circuits

**Prerequisites**: Task 2 (or equivalent linear algebra knowledge)

**Builds Toward**: Entanglement is used in Tasks 3 and 5

---

### Task 3: Quantum Teleportation 📡

**Difficulty**: Intermediate
**Estimated Time**: 60-75 minutes
**Type**: Qiskit 1.x

**Why third**:
- Combines entanglement with multi-qubit operations
- Introduces conditional operations
- Demonstrates quantum information transfer
- More complex circuit design

**Key Concepts**:
- Quantum teleportation protocol
- Bell measurements
- Classical communication in quantum protocols
- Conditional quantum operations (c_if)
- Statevector visualisation
- 3-qubit quantum systems
- Protocol verification

**Skills Developed**:
- ✓ Implement multi-step quantum protocols
- ✓ Use Bell measurements
- ✓ Apply conditional quantum gates
- ✓ Visualise quantum states (Bloch, Q-sphere)
- ✓ Verify protocol correctness

**Prerequisites**: Tasks 1-2

**Builds Toward**: Advanced quantum protocols and communication

---

### Task 4: Playing Card Magic Trick 🎴

**Difficulty**: Intermediate
**Estimated Time**: 45-60 minutes
**Type**: Pure NumPy (no Qiskit)

**Why fourth (or optional)**:
- Demonstrates quantum mechanics in a classical context
- Reinforces tensor products and probability
- Can be done independently of other tasks
- Fun, creative application

**Key Concepts**:
- High-dimensional Hilbert spaces (32D)
- Encoding classical information quantum mechanically
- Kronecker products for composite systems
- Probability amplitudes
- Superposition of classical states
- Inner products for correlations

**Skills Developed**:
- ✓ Work with high-dimensional quantum systems
- ✓ Apply tensor products systematically
- ✓ Calculate complex probability distributions
- ✓ Represent classical objects quantumly

**Prerequisites**: Task 2

**Builds Toward**: Understanding quantum state spaces

---

### Task 5: Quantum Error Correction 🛡️

**Difficulty**: Advanced
**Estimated Time**: 75-90 minutes
**Type**: Qiskit 1.x

**Why fifth (final)**:
- Synthesises all previous concepts
- Most complex quantum protocol
- Introduces error correction principles
- Uses advanced multi-qubit gates

**Key Concepts**:
- 3-qubit bit-flip code
- Quantum encoding with redundancy
- Syndrome measurement
- Error detection without state collapse
- Toffoli (CCX) gates
- Quantum error correction theory
- Fault tolerance concepts

**Skills Developed**:
- ✓ Implement quantum error correction codes
- ✓ Design syndrome measurement circuits
- ✓ Apply multi-qubit controlled operations
- ✓ Understand quantum fault tolerance
- ✓ Compare error-free vs error-prone scenarios

**Prerequisites**: Tasks 1, 2, 3 (Task 3 strongly recommended)

**Builds Toward**: Advanced quantum computing architectures

---

## Concept Dependency Map

```
Task 2 (Linear Algebra)
    ├─→ Task 1 (Entanglement)
    │       ├─→ Task 3 (Teleportation)
    │       │       └─→ Task 5 (Error Correction)
    │       │
    │       └─→ Task 5 (Error Correction)
    │
    └─→ Task 4 (Magic Trick) [independent]
```

**Key Dependencies**:
- Task 2 → All tasks (mathematical foundations)
- Task 1 → Task 3 (entanglement used in teleportation)
- Task 3 → Task 5 (multi-qubit operations)
- Task 4 is independent (can be done anytime after Task 2)

---

## Skill Progression

### Level 1: Foundations (Task 2)
- Quantum states as vectors
- Quantum gates as matrices
- Basic quantum operations

### Level 2: Single Protocol (Task 1)
- Circuit construction
- Simulation workflow
- Measurement analysis
- Entanglement creation

### Level 3: Complex Protocols (Tasks 3-4)
- Multi-step protocols
- Conditional operations
- High-dimensional systems
- State visualisation

### Level 4: Advanced Applications (Task 5)
- Error correction codes
- Syndrome measurement
- Multi-qubit controlled gates
- Fault tolerance

---

## Time Investment Guide

### Minimal Path (Core Quantum Concepts)
**Total**: ~3-4 hours
1. Task 1: Entanglement (60 min)
2. Task 3: Teleportation (75 min)
3. Task 5: Error Correction (90 min)

### Standard Path (Comprehensive)
**Total**: ~5-6 hours
1. Task 2: Linear Algebra (60 min)
2. Task 1: Entanglement (60 min)
3. Task 3: Teleportation (75 min)
4. Task 5: Error Correction (90 min)

### Complete Path (All Concepts)
**Total**: ~6-8 hours
- All 5 tasks in recommended order
- Review documentation
- Run all tests
- Experiment with variations

---

## Learning Strategies

### Strategy 1: Starter → Solution → Tests

1. **Work through starter notebook**
   - Try exercises independently
   - Use hints when stuck
   - Don't peek at solution

2. **Compare with solution**
   - Understand different approaches
   - Learn optimisations
   - Study code style

3. **Run tests**
   - `pytest tests/test_task_XX.py -v`
   - Understand what tests verify
   - Learn edge cases

### Strategy 2: Solution Study → Modification

1. **Read solution notebook thoroughly**
   - Understand each cell
   - Note key concepts
   - Run all visualisations

2. **Modify and experiment**
   - Change parameters
   - Test edge cases
   - Break things intentionally

3. **Rebuild from scratch**
   - Use starter notebook
   - Recall concepts from solution
   - Verify understanding

### Strategy 3: Test-Driven Learning

1. **Read tests first**
   - Understand requirements
   - See expected behaviour
   - Note edge cases

2. **Implement to pass tests**
   - Use starter notebook
   - Run tests frequently
   - Fix failing tests

3. **Study solution**
   - Compare approaches
   - Learn best practices
   - Understand optimisations

---

## Common Learning Paths by Background

### Physics Background
- Strong mathematical foundation
- **Start**: Task 1 (jump right into quantum concepts)
- **Focus**: Tasks 3, 5 (protocols and applications)
- **Review**: Task 2 if computational linear algebra is unfamiliar

### Computer Science Background
- Comfortable with programming
- **Start**: Task 2 (mathematical foundations)
- **Focus**: Tasks 1, 3, 5 (Qiskit and quantum computing)
- **Appreciate**: Task 4 (algorithmic thinking)

### Mathematics Background
- Excellent linear algebra
- **Start**: Task 2 (see quantum applications)
- **Focus**: All tasks (mathematical structures)
- **Enjoy**: Task 4 (abstract Hilbert spaces)

### Self-Taught / Hobbyist
- Variable mathematical background
- **Start**: Task 2 (build solid foundation)
- **Progress**: Sequentially through all tasks
- **Practice**: Repeat exercises for mastery

---

## Assessment Checkpoints

### After Task 2
**Can you**:
- ✓ Represent a qubit as a column vector?
- ✓ Apply a gate using matrix multiplication?
- ✓ Calculate measurement probability with inner products?
- ✓ Combine qubits with tensor products?

### After Task 1
**Can you**:
- ✓ Build a Bell state circuit in Qiskit?
- ✓ Explain what entanglement means?
- ✓ Simulate a circuit and interpret results?
- ✓ Predict measurement statistics?

### After Task 3
**Can you**:
- ✓ Explain the teleportation protocol step-by-step?
- ✓ Implement Bell measurements?
- ✓ Use conditional quantum operations?
- ✓ Verify protocol correctness?

### After Task 4
**Can you**:
- ✓ Encode classical information as quantum states?
- ✓ Work with 32-dimensional Hilbert spaces?
- ✓ Calculate probabilities in superposition?
- ✓ Use Kronecker products fluently?

### After Task 5
**Can you**:
- ✓ Explain quantum error correction principles?
- ✓ Implement the 3-qubit code?
- ✓ Design syndrome measurements?
- ✓ Apply Toffoli gates for correction?

---

## Next Steps After Completion

### Immediate Extensions
1. **Modify existing tasks**
   - Different initial states
   - More qubits
   - Different error types

2. **Run all tests**
   - `pytest`
   - Understand test structure
   - Write your own tests

3. **Explore Qiskit documentation**
   - [qiskit.org](https://qiskit.org/)
   - Advanced visualisations
   - Real quantum hardware

### Advanced Topics to Explore
- **Quantum Algorithms**: Deutsch-Jozsa, Grover, Shor
- **Error Correction**: Shor code, Steane code, Surface codes
- **Quantum Cryptography**: BB84, E91
- **Variational Algorithms**: VQE, QAOA
- **Quantum Machine Learning**: Quantum neural networks

### Real Hardware
- IBM Quantum Experience
- Submit jobs to real quantum computers
- Understand noise and decoherence
- Learn pulse-level control

---

## Resources

### Official Documentation
- **Qiskit**: [qiskit.org](https://qiskit.org/)
- **Qiskit Textbook**: [qiskit.org/textbook](https://qiskit.org/textbook)

### Books
- *Quantum Computation and Quantum Information* - Nielsen & Chuang
- *Programming Quantum Computers* - Johnston, Harrigan, Gimeno-Segovia
- *Quantum Computing: An Applied Approach* - Hidary

### Online Courses
- IBM Quantum Learning
- Brilliant.org Quantum Computing
- Coursera Quantum Computing courses

### Community
- Qiskit Slack
- Quantum Computing Stack Exchange
- GitHub Qiskit discussions

---

## Getting Help

1. **Documentation**
   - Task READMEs in each directory
   - `docs/TROUBLESHOOTING.md`
   - `docs/QISKIT_MIGRATION.md`

2. **Testing**
   - Run `pytest -v` to see what fails
   - Read test code for requirements
   - Use `pytest -s` for print output

3. **Verification Script**
   - `python scripts/verify_installation.py`
   - Checks environment setup
   - Tests basic Qiskit functionality

---

**Happy Learning!** Quantum computing is challenging but immensely rewarding. Take your time, experiment freely, and don't hesitate to revisit earlier concepts.

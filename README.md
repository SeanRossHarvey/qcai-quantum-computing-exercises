# Quantum Computing Exercises with Qiskit

A comprehensive, modern collection of Jupyter notebook exercises covering quantum computing fundamentals using Qiskit 1.x.

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Qiskit Version](https://img.shields.io/badge/qiskit-1.0%2B-blueviolet.svg)](https://qiskit.org/)
[![Licence](https://img.shields.io/badge/licence-MIT-green.svg)](LICENSE)

## Overview

This repository contains 5 progressive quantum computing exercises designed for students learning quantum computing and Qiskit. Each exercise includes:

- **Starter notebook**: Guided exercises with TODO sections for students
- **Solution notebook**: Complete reference implementations with detailed explanations
- **Automated tests**: Verify your solutions programmatically
- **Detailed documentation**: Learning objectives, prerequisites, and theoretical background

### Topics Covered

1. **Quantum Entanglement & Measurement Statistics**: Bell states, CNOT gates, measurement correlations
2. **Linear Algebra Foundations**: State vectors, quantum gates as matrices, tensor products, eigenvalues
3. **Quantum Teleportation Protocol**: Three-qubit teleportation, Bell measurements, statevector simulation
4. **Playing Card Magic Trick**: High-dimensional quantum spaces, Kronecker products, probability amplitudes
5. **Quantum Error Correction**: Three-qubit bit-flip code, encoding/decoding circuits, error detection and correction

## 🚀 Quick Launch (No Installation Required)

**Try the exercises instantly in your browser using Google Colab:**

| Task | Topic | Starter Notebook | Solution |
|:----:|:------|:----------------:|:--------:|
| **1** | Quantum Entanglement & Bell States | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SeanRossHarvey/qcai-quantum-computing-exercises/blob/main/notebooks/task_01_entanglement/task_01_starter.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SeanRossHarvey/qcai-quantum-computing-exercises/blob/main/notebooks/task_01_entanglement/task_01_solution.ipynb) |
| **2** | Linear Algebra Foundations | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SeanRossHarvey/qcai-quantum-computing-exercises/blob/main/notebooks/task_02_linear_algebra/task_02_starter.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SeanRossHarvey/qcai-quantum-computing-exercises/blob/main/notebooks/task_02_linear_algebra/task_02_solution.ipynb) |
| **3** | Quantum Teleportation Protocol | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SeanRossHarvey/qcai-quantum-computing-exercises/blob/main/notebooks/task_03_teleportation/task_03_starter.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SeanRossHarvey/qcai-quantum-computing-exercises/blob/main/notebooks/task_03_teleportation/task_03_solution.ipynb) |
| **4** | Playing Card Magic Trick | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SeanRossHarvey/qcai-quantum-computing-exercises/blob/main/notebooks/task_04_magic_trick/task_04_starter.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SeanRossHarvey/qcai-quantum-computing-exercises/blob/main/notebooks/task_04_magic_trick/task_04_solution.ipynb) |
| **5** | Quantum Error Correction | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SeanRossHarvey/qcai-quantum-computing-exercises/blob/main/notebooks/task_05_error_correction/task_05_starter.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SeanRossHarvey/qcai-quantum-computing-exercises/blob/main/notebooks/task_05_error_correction/task_05_solution.ipynb) |

**How it works:**
- Click any "Open in Colab" badge to launch the notebook in your browser
- Run the first cell to auto-install dependencies (takes ~30 seconds)
- Start learning immediately - no setup required!
- **Updates reflect instantly**: When notebooks are updated in GitHub, just refresh your Colab page to get the latest version

**Note**: Google account required. To save your work, go to **File → Save a copy in Drive**.

### Alternative: Binder (No Google Account Required)

If you don't have a Google account, you can use Binder instead:

[![Launch Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/SeanRossHarvey/qcai-quantum-computing-exercises/main)

**Note**: Binder takes 2-5 minutes to build the environment on first launch, and updates may take 30+ minutes to appear due to caching. For instant updates, use Google Colab.

## Quick Start (Local Installation)

```bash
# Clone the repository
git clone https://github.com/SeanRossHarvey/qcai-quantum-computing-exercises.git
cd qcai-quantum-computing-exercises

# Create virtual environment and install dependencies
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Verify installation
python scripts/verify_installation.py

# Start Jupyter Notebook
jupyter notebook
```

Navigate to `notebooks/task_01_entanglement/task_01_starter.ipynb` to begin!

## Repository Structure

```
qcai-quantum-computing-exercises/
├── notebooks/              # Jupyter notebooks for all tasks
│   ├── task_01_entanglement/
│   │   ├── task_01_starter.ipynb
│   │   ├── task_01_solution.ipynb
│   │   └── README.md
│   ├── task_02_linear_algebra/
│   ├── task_03_teleportation/
│   ├── task_04_magic_trick/
│   └── task_05_error_correction/
├── tests/                  # Automated test suite
├── scripts/                # Utility scripts
├── docs/                   # Comprehensive documentation
└── assets/                 # Images, styles, templates
```

## Learning Path

The exercises are designed to be completed in order, with each building on concepts from previous tasks:

**Prerequisites**: Basic Python programming, fundamental linear algebra knowledge

**Progression**:
1. **Task 1** (Beginner, ~45 min): Introduction to quantum circuits, superposition, and entanglement
2. **Task 2** (Beginner, ~30 min): Mathematical foundations with NumPy
3. **Task 3** (Intermediate, ~60 min): Quantum teleportation protocol implementation
4. **Task 4** (Intermediate, ~45 min): High-dimensional quantum systems and practical applications
5. **Task 5** (Advanced, ~60 min): Quantum error correction fundamentals

See [docs/LEARNING_PATH.md](docs/LEARNING_PATH.md) for a detailed progression guide and alternative learning paths.

## Requirements

- **Python**: 3.10 or higher (3.11 or 3.12 recommended)
- **Qiskit**: 1.0+ (automatically installed via requirements.txt)
- **Jupyter**: Notebook or JupyterLab
- **Operating System**: Windows, macOS, or Linux

For a complete list of dependencies, see [requirements.txt](requirements.txt).

## Installation Guide

### Method 1: Using venv (Recommended)

**Windows:**
```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python scripts/verify_installation.py
```

**macOS/Linux:**
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python scripts/verify_installation.py
```

### Method 2: Using Conda

```bash
# Create conda environment from file
conda env create -f environment.yml

# Activate environment
conda activate qcai

# Verify installation
python scripts/verify_installation.py
```

For detailed installation instructions, troubleshooting, and platform-specific guidance, see [docs/SETUP.md](docs/SETUP.md).

## Documentation

Comprehensive documentation is available in the `docs/` directory:

- **[SETUP.md](docs/SETUP.md)** - Detailed installation and setup instructions
- **[LEARNING_PATH.md](docs/LEARNING_PATH.md)** - Pedagogical progression guide and learning objectives
- **[TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** - Common issues and solutions
- **[QISKIT_MIGRATION.md](docs/QISKIT_MIGRATION.md)** - API changes from Qiskit pre-1.0 to 1.x

Each task directory also contains a README with task-specific learning objectives, prerequisites, and key concepts.

## Testing Your Solutions

The repository includes a comprehensive test suite to validate your implementations:

```bash
# Run all tests
pytest

# Test a specific task
pytest tests/test_task_01.py

# Test notebook execution
pytest --nbmake notebooks/**/task_*_solution.ipynb

# Run tests with coverage report
pytest --cov=notebooks --cov-report=html
```

Tests include:
- **Circuit structure validation**: Ensures quantum circuits are correctly constructed
- **Numerical correctness**: Validates mathematical operations and computations
- **Statistical validation**: Chi-squared tests for measurement probability distributions
- **Notebook execution**: Verifies that all notebooks run without errors

## Key Features

✅ **Modern Qiskit 1.x**: Updated to use the latest Qiskit APIs and best practices

✅ **Interactive Learning**: Progressive Jupyter notebooks with hands-on exercises

✅ **Automated Validation**: Test your solutions programmatically before moving forward

✅ **Enhanced Visualisations**: Modern matplotlib styling and advanced Qiskit visualisation tools

✅ **British English**: All documentation and comments use British English spelling conventions

✅ **Cross-platform**: Tested on Windows, macOS, and Linux

✅ **Well-Documented**: Comprehensive explanations of quantum computing concepts and implementations

## Pedagogical Approach

These exercises are designed with several educational principles in mind:

- **Progressive Complexity**: Each task builds on previous concepts
- **Hands-on Practice**: Learn by doing, not just reading
- **Immediate Feedback**: Automated tests provide quick validation
- **Multiple Perspectives**: Covers both mathematical foundations and practical implementations
- **Real-world Applications**: Examples like quantum teleportation and error correction demonstrate practical quantum computing

## Contributing

Contributions are welcome! Whether you've found a bug, have a suggestion, or want to add new exercises:

1. Open an issue to discuss your proposal
2. Fork the repository
3. Create a feature branch (`git checkout -b feature/amazing-addition`)
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-addition`)
6. Open a Pull Request

Please ensure all new code includes tests and documentation.

## Licence

This project is licensed under the MIT Licence - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

Based on original course materials developed for Quantum Computing and AI education. Modernised and expanded with:

- Updated Qiskit 1.x API integration
- Enhanced visualisations and interactive elements
- Comprehensive testing infrastructure
- Detailed pedagogical documentation

## Support and Contact

- **Issues**: Report bugs or request features via [GitHub Issues](https://github.com/SeanRossHarvey/qcai-quantum-computing-exercises/issues)
- **Discussions**: Join the conversation in [GitHub Discussions](https://github.com/SeanRossHarvey/qcai-quantum-computing-exercises/discussions)
- **Documentation**: Check [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for common issues

## Additional Resources

- **[Qiskit Documentation](https://docs.quantum.ibm.com/)** - Official Qiskit documentation
- **[Qiskit Textbook](https://qiskit.org/textbook/)** - Free online quantum computing textbook
- **[IBM Quantum Experience](https://quantum.ibm.com/)** - Access to real quantum hardware
- **[Quantum Country](https://quantum.country/)** - Interactive introduction to quantum computing

---

**Note**: These exercises use simulated quantum computers via Qiskit Aer. For access to real quantum hardware, create a free account at [IBM Quantum](https://quantum.ibm.com/).

**Getting Started**: New to quantum computing? Start with Task 1 and work through sequentially. Each task includes all necessary background information, but having a basic understanding of complex numbers and linear algebra will be helpful.

Happy learning! 🚀

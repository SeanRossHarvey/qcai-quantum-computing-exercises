# Installation and Setup Guide

This guide provides detailed instructions for setting up the QCAI Quantum Computing Exercises on your local machine.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation Methods](#installation-methods)
  - [Method 1: Using venv (Recommended)](#method-1-using-venv-recommended)
  - [Method 2: Using Conda](#method-2-using-conda)
- [Verifying Your Installation](#verifying-your-installation)
- [Running Jupyter Notebooks](#running-jupyter-notebooks)
- [Updating Dependencies](#updating-dependencies)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before you begin, ensure you have the following installed on your system:

### Required Software

- **Python**: Version 3.10 or higher (3.11 or 3.12 recommended)
  - Download from [python.org](https://www.python.org/downloads/)
  - Verify installation: `python --version` or `python3 --version`

- **pip**: Python package manager (usually included with Python)
  - Verify installation: `pip --version`
  - Upgrade if needed: `pip install --upgrade pip`

- **Git**: For cloning the repository
  - Download from [git-scm.com](https://git-scm.com/)
  - Verify installation: `git --version`

### System Requirements

- **Disk Space**: At least 2GB free space (for Python environment and dependencies)
- **Memory**: Minimum 4GB RAM (8GB recommended for larger quantum simulations)
- **Operating System**: Windows 10+, macOS 10.14+, or modern Linux distribution

### Recommended Background

- Basic Python programming knowledge
- Familiarity with command-line/terminal operations
- Understanding of complex numbers and linear algebra (helpful but not required)

## Installation Methods

### Method 1: Using venv (Recommended)

The Python virtual environment (venv) is the recommended method for most users. It creates an isolated Python environment, preventing conflicts with other projects.

#### Windows

1. **Open Command Prompt or PowerShell**

2. **Clone the repository**
   ```cmd
   git clone https://github.com/yourusername/qcai-quantum-computing-exercises.git
   cd qcai-quantum-computing-exercises
   ```

3. **Create a virtual environment**
   ```cmd
   python -m venv venv
   ```

4. **Activate the virtual environment**

   **Command Prompt:**
   ```cmd
   venv\Scripts\activate
   ```

   **PowerShell:** (If you encounter an error, see [PowerShell Execution Policy](#powershell-execution-policy))
   ```powershell
   venv\Scripts\Activate.ps1
   ```

5. **Install dependencies**
   ```cmd
   pip install -r requirements.txt
   ```

6. **Verify installation**
   ```cmd
   python scripts/verify_installation.py
   ```

#### macOS/Linux

1. **Open Terminal**

2. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/qcai-quantum-computing-exercises.git
   cd qcai-quantum-computing-exercises
   ```

3. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   ```

4. **Activate the virtual environment**
   ```bash
   source venv/bin/activate
   ```

5. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

6. **Verify installation**
   ```bash
   python scripts/verify_installation.py
   ```

### Method 2: Using Conda

Conda is an alternative package and environment manager, particularly popular in scientific computing.

#### Prerequisites

- Install [Anaconda](https://www.anaconda.com/products/distribution) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)

#### All Platforms

1. **Open Anaconda Prompt (Windows) or Terminal (macOS/Linux)**

2. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/qcai-quantum-computing-exercises.git
   cd qcai-quantum-computing-exercises
   ```

3. **Create conda environment**

   If an `environment.yml` file is provided:
   ```bash
   conda env create -f environment.yml
   ```

   Otherwise, create manually:
   ```bash
   conda create -n qcai python=3.11
   ```

4. **Activate the environment**
   ```bash
   conda activate qcai
   ```

5. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

6. **Verify installation**
   ```bash
   python scripts/verify_installation.py
   ```

## Verifying Your Installation

After installation, run the verification script to ensure everything is set up correctly:

```bash
python scripts/verify_installation.py
```

The script will check:
- ✅ Python version (3.10+)
- ✅ Qiskit installation and version (1.0+)
- ✅ Qiskit Aer installation (0.13+)
- ✅ NumPy, Matplotlib, and other dependencies
- ✅ Jupyter Notebook/Lab installation
- ✅ Basic quantum circuit execution

### Expected Output

If everything is installed correctly, you should see:

```
============================================================
QCAI Quantum Computing Exercises - Installation Verification
============================================================

Checking Python version...
  ✓ Python 3.11.5

Checking required packages...
  ✓ qiskit: 1.0.2
  ✓ qiskit_aer: 0.13.3
  ✓ numpy: 1.24.3
  ✓ matplotlib: 3.8.0
  ✓ jupyter: 1.0.0
  ✓ notebook: 7.0.6

Testing Qiskit functionality...
  ✓ Successfully created and simulated a quantum circuit
  ✓ Sample output: {'00': 52, '11': 48}

============================================================
✓ All checks passed! Your environment is ready.

To get started:
  1. Run: jupyter notebook
  2. Navigate to: notebooks/task_01_entanglement/
  3. Open: task_01_starter.ipynb
============================================================
```

## Running Jupyter Notebooks

### Starting Jupyter Notebook

1. **Activate your environment** (if not already active)

   **venv:**
   ```bash
   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

   **conda:**
   ```bash
   conda activate qcai
   ```

2. **Start Jupyter Notebook**
   ```bash
   jupyter notebook
   ```

   Your default web browser should open automatically to `http://localhost:8888`

3. **Navigate to a task**
   - In the Jupyter file browser, navigate to `notebooks/`
   - Choose a task directory (e.g., `task_01_entanglement/`)
   - Open the starter notebook (e.g., `task_01_starter.ipynb`)

### Starting JupyterLab (Alternative)

JupyterLab offers a more advanced interface with multiple panes:

```bash
jupyter lab
```

### Stopping Jupyter

To stop the Jupyter server:
1. Return to the terminal where Jupyter is running
2. Press `Ctrl+C` twice
3. Or close the terminal window

## Updating Dependencies

To update to the latest compatible versions of dependencies:

```bash
# Activate your environment first
pip install --upgrade -r requirements.txt
```

To update a specific package:

```bash
pip install --upgrade qiskit
pip install --upgrade qiskit-aer
```

After updating, verify the installation again:

```bash
python scripts/verify_installation.py
```

## Troubleshooting

### PowerShell Execution Policy

If you encounter an error when activating the virtual environment in PowerShell:

```
Error: running scripts is disabled on this system
```

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again:
```powershell
venv\Scripts\Activate.ps1
```

### pip Command Not Found

**Symptoms:** `'pip' is not recognized as an internal or external command`

**Solutions:**

1. **Use python -m pip instead:**
   ```bash
   python -m pip install -r requirements.txt
   ```

2. **Add Python to PATH** (Windows):
   - During Python installation, ensure "Add Python to PATH" is checked
   - Or manually add Python's Scripts directory to your PATH

### Virtual Environment Not Activating

**Symptoms:** Prompt doesn't change, `which python` shows system Python

**Solutions:**

1. **Ensure you're in the correct directory:**
   ```bash
   cd /path/to/qcai-quantum-computing-exercises
   ```

2. **Use the full path to activation script:**
   ```bash
   # Windows
   C:\path\to\project\venv\Scripts\activate

   # macOS/Linux
   /path/to/project/venv/bin/activate
   ```

### Jupyter Notebook Not Found

**Symptoms:** `'jupyter' is not recognized as an internal or external command`

**Solution:**

Ensure your virtual environment is activated, then:

```bash
pip install jupyter notebook
```

Or use:
```bash
python -m jupyter notebook
```

### ImportError: No module named 'qiskit_aer'

**Symptoms:** Import error when running notebooks or tests

**Solution:**

Qiskit Aer is a separate package in Qiskit 1.x:

```bash
pip install qiskit-aer
```

### SSL Certificate Error (macOS)

**Symptoms:**
```
ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED]
```

**Solution:**

Run Python's certificate installer:
```bash
/Applications/Python\ 3.x/Install\ Certificates.command
```

Replace `3.x` with your Python version (e.g., `3.11`).

### Permission Errors (Linux)

**Symptoms:** Permission denied when installing packages

**Solution:**

**Never use sudo with pip.** Instead:

1. **Use virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Install with --user flag:**
   ```bash
   pip install --user -r requirements.txt
   ```

### Slow Quantum Simulations

**Symptoms:** Notebooks take a very long time to execute

**Solutions:**

1. **Reduce the number of shots:** Edit notebook cells to use fewer shots (e.g., `shots=1000` instead of `shots=100000`)

2. **Limit circuit complexity:** Start with smaller numbers of qubits

3. **Close other applications:** Free up RAM for the simulation

4. **Use statevector simulator:** For circuits without measurements, use `StatevectorSimulator` which is often faster

### Module Import Errors in Notebooks

**Symptoms:** `ModuleNotFoundError` when running notebook cells

**Solution:**

Ensure your Jupyter kernel is using the correct Python environment:

1. **Install ipykernel in your environment:**
   ```bash
   pip install ipykernel
   ```

2. **Register the kernel:**
   ```bash
   python -m ipykernel install --user --name=qcai
   ```

3. **In Jupyter Notebook:**
   - Go to `Kernel` → `Change Kernel`
   - Select `qcai`

## Getting Further Help

If you continue to experience issues:

1. **Check the main troubleshooting guide:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

2. **Search existing issues:** [GitHub Issues](https://github.com/yourusername/qcai-quantum-computing-exercises/issues)

3. **Qiskit-specific problems:** [Qiskit Documentation](https://docs.quantum.ibm.com/)

4. **Open a new issue:** Provide the following information:
   - Operating system and version
   - Python version (`python --version`)
   - Output of `pip list | grep qiskit`
   - Full error message
   - Steps to reproduce the issue

## Next Steps

Once your installation is verified:

1. **Start with Task 1:** `notebooks/task_01_entanglement/task_01_starter.ipynb`
2. **Read the learning path:** [LEARNING_PATH.md](LEARNING_PATH.md)
3. **Explore the documentation:** Each task directory contains a README with specific guidance

Happy learning! 🚀

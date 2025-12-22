#!/usr/bin/env python3
"""
Verify that all dependencies are correctly installed for the QCAI exercises.

This script checks:
1. Python version (3.10+)
2. Required packages and their versions
3. Basic Qiskit functionality
4. Jupyter installation

Usage:
    python scripts/verify_installation.py
"""

import sys
import importlib
from typing import Tuple


def check_python_version() -> Tuple[bool, str]:
    """
    Check if Python version meets requirements (3.10+).

    Returns:
        Tuple of (success: bool, version_info: str)
    """
    version = sys.version_info
    if version >= (3, 10):
        return True, f"Python {version.major}.{version.minor}.{version.micro}"
    return False, f"Python {version.major}.{version.minor}.{version.micro} (requires 3.10+)"


def check_package(package_name: str, min_version: str = None) -> Tuple[bool, str]:
    """
    Check if a package is installed and optionally verify minimum version.

    Args:
        package_name: Name of the package to check
        min_version: Minimum required version (None to skip version check)

    Returns:
        Tuple of (success: bool, version_or_error: str)
    """
    try:
        module = importlib.import_module(package_name)
        version = getattr(module, '__version__', 'unknown')

        if min_version and version != 'unknown':
            try:
                from packaging import version as pkg_version
                if pkg_version.parse(version) < pkg_version.parse(min_version):
                    return False, f"{version} (requires {min_version}+)"
            except ImportError:
                # packaging not available, skip version check
                pass

        return True, version
    except ImportError:
        return False, "not installed"


def test_qiskit_functionality() -> Tuple[bool, str]:
    """
    Test basic Qiskit functionality by creating and simulating a simple circuit.

    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        from qiskit import QuantumCircuit, transpile
        from qiskit_aer import AerSimulator

        # Create a simple Bell state circuit
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure([0, 1], [0, 1])

        # Simulate the circuit
        simulator = AerSimulator()
        transpiled = transpile(qc, simulator)
        job = simulator.run(transpiled, shots=100)
        result = job.result()
        counts = result.get_counts()

        # Verify we got some results
        if len(counts) > 0:
            sample_output = dict(list(counts.items())[:2])
            return True, f"Successfully created and simulated a quantum circuit\n  Sample output: {sample_output}"
        else:
            return False, "Simulation produced no results"

    except Exception as e:
        return False, f"Error testing Qiskit: {str(e)}"


def main():
    """Run all verification checks and print results."""
    print("=" * 60)
    print("QCAI Quantum Computing Exercises - Installation Verification")
    print("=" * 60)
    print()

    # Define required packages with minimum versions
    packages = [
        ("qiskit", "1.0.0"),
        ("qiskit_aer", "0.13.0"),
        ("numpy", "1.24.0"),
        ("matplotlib", "3.7.0"),
        ("jupyter", None),
        ("notebook", None),
    ]

    all_passed = True

    # Check Python version
    print("Checking Python version...")
    passed, info = check_python_version()
    print(f"  {'[OK]' if passed else '[FAIL]'} {info}")
    all_passed = all_passed and passed
    print()

    # Check required packages
    print("Checking required packages...")
    for package_name, min_version in packages:
        passed, version = check_package(package_name, min_version)
        status = '[OK]' if passed else '[FAIL]'
        min_ver_str = f" (min {min_version})" if min_version else ""
        print(f"  {status} {package_name}: {version}{min_ver_str}")
        all_passed = all_passed and passed
    print()

    # Test Qiskit functionality
    print("Testing Qiskit functionality...")
    passed, message = test_qiskit_functionality()
    status = '[OK]' if passed else '[FAIL]'
    for line in message.split('\n'):
        print(f"  {status} {line}")
    all_passed = all_passed and passed
    print()

    # Final summary
    print("=" * 60)
    if all_passed:
        print("[SUCCESS] All checks passed! Your environment is ready.")
        print("\nTo get started:")
        print("  1. Run: jupyter notebook")
        print("  2. Navigate to: notebooks/task_01_entanglement/")
        print("  3. Open: task_01_starter.ipynb")
        print("\nFor guidance, see: docs/LEARNING_PATH.md")
    else:
        print("[ERROR] Some checks failed. Please review the output above.")
        print("\nFor troubleshooting:")
        print("  1. See: docs/SETUP.md")
        print("  2. See: docs/TROUBLESHOOTING.md")
        print("  3. Ensure you're in the correct virtual environment")
        print("  4. Try: pip install -r requirements.txt")
    print("=" * 60)

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

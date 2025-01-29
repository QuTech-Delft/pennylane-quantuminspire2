from typing import Any, Callable
from qiskit import QuantumCircuit
from qiskit_quantuminspire import cqasm

import pennylane as qml

def dumps(quantum_function: Callable, **options: Any) -> str:
    """Return the cQASM representation of the quantum function."""
    with qml.tape.QuantumTape() as tape:
        quantum_function(**options)

    print(tape.draw())
    openqasm_code = tape.to_openqasm()
    quantum_circuit =  QuantumCircuit.from_qasm_str(openqasm_code)
    return cqasm.dumps(quantum_circuit)



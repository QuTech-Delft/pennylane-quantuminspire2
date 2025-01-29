import pennylane as qml
from qiskit import QuantumCircuit
from qiskit_quantuminspire import cqasm


def dumps(q_node: qml.QNode) -> str:
    """Return the cQASM representation of the quantum function."""
    tape = qml.workflow.construct_tape(q_node)
    openqasm_code = tape().to_openqasm()

    quantum_circuit = QuantumCircuit.from_qasm_str(openqasm_code)

    return cqasm.dumps(quantum_circuit)

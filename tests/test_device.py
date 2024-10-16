import pennylane as qml
from pytest_mock import MockerFixture
from qiskit_quantuminspire.qi_backend import QIBackend

from pennylane_quantuminspire2.qi_device import QI2Device


def test_device_circuit(mocker: MockerFixture, QI2_backend: QIBackend) -> None:
    device = QI2Device(backend=QI2_backend)

    @qml.qnode(device=device)
    # untyped decorator in pennylane, so mypy will complain here
    def quantum_function():  # type: ignore
        qml.Hadamard(wires=[0])
        return qml.expval(qml.PauliX(wires=[0]))

    mocker.patch("qiskit_quantuminspire.qi_backend.QIJob")
    assert quantum_function() is not None

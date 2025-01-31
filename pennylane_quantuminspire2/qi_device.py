from typing import Any
from qiskit_quantuminspire.qi_backend import QIBackend


class QI2Device(RemoteDevice):  # type: ignore[misc]

    def __init__(self, backend: QIBackend, **kwargs: Any) -> None:
        super().__init__(wires=backend.num_qubits, backend=backend, **kwargs)

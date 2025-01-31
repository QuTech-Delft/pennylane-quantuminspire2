from typing import Any, Optional, Sequence

from pennylane_qiskit import RemoteDevice
from qiskit_quantuminspire.qi_backend import QIBackend


class QI2Device(RemoteDevice):  # type: ignore[misc]

    def __init__(self, backend: QIBackend, **kwargs: Any) -> None:
        super().__init__(wires=backend.num_qubits, backend=backend, **kwargs)

    @classmethod
    def backends(cls) -> Sequence[QIBackend]:
        return cls._qi_provider.backends()  # type: ignore[no-any-return]

    @classmethod
    def get_backend(cls, name: Optional[str] = None, id: Optional[int] = None) -> QIBackend:
        return cls._qi_provider.get_backend(name, id)

from typing import Any, Optional, Sequence

from pennylane import DeviceError
from pennylane.devices.execution_config import DefaultExecutionConfig, ExecutionConfig
from pennylane_qiskit import RemoteDevice
from pennylane_qiskit.qiskit_device import QuantumTape_or_Batch, Result_or_ResultBatch
from qiskit.exceptions import QiskitError
from qiskit_quantuminspire.qi_backend import QIBackend


class QI2Device(RemoteDevice):  # type: ignore[misc]

    def __init__(self, backend: QIBackend, **kwargs: Any) -> None:
        super().__init__(wires=backend.num_qubits, backend=backend, **kwargs)

    # pylint: disable=unused-argument, no-member
    def execute(
        self,
        circuits: QuantumTape_or_Batch,
        execution_config: ExecutionConfig = DefaultExecutionConfig,
    ) -> Result_or_ResultBatch:

        try:
            results = super().execute(circuits, execution_config)
            return results
        except QiskitError as e:
            raise DeviceError(str(e)) from e

    @classmethod
    def backends(cls) -> Sequence[QIBackend]:
        return cls._qi_provider.backends()  # type: ignore[no-any-return]

    @classmethod
    def get_backend(cls, name: Optional[str] = None, id: Optional[int] = None) -> QIBackend:
        return cls._qi_provider.get_backend(name, id)

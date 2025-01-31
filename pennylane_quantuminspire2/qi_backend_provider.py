from typing import Any, Optional, Sequence

from qiskit_quantuminspire.qi_backend import QIBackend
from qiskit_quantuminspire.qi_provider import QIProvider


class QI2BackendProvider():  # type: ignore[misc]
    _qi_provider: QIProvider

    def __init__(self, backend: QIBackend, **kwargs: Any) -> None:
        _qi_provider = QIProvider()

    @classmethod
    def backends(cls) -> Sequence[QIBackend]:
        return cls._qi_provider.backends()  # type: ignore[no-any-return]

    @classmethod
    def get_backend(cls, name: Optional[str] = None, id: Optional[int] = None) -> QIBackend:
        return cls._qi_provider.get_backend(name, id)


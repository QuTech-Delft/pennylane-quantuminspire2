import pennylane as qml

from .qi_device import QI2Device

qml.devices.register(
    "quantum_inspire.stubbed", lambda **kwargs: QI2Device(backend=QI2Device.get_backend(name="Stubbed"), **kwargs)
)

qml.devices.register(
    "quantum_inspire.qx_emulator",
    lambda **kwargs: QI2Device(backend=QI2Device.get_backend(name="QX emulator"), **kwargs),
)

"""Model for the deviceInfo endpoint."""

from dataclasses import dataclass
from typing import Annotated, Any, Self

from mashumaro import DataClassDictMixin
from mashumaro.types import Alias


@dataclass(slots=True, frozen=True, kw_only=True)
class DeviceInfo(DataClassDictMixin):
    """Response from the deviceInfo endpoint."""

    oem_code: Annotated[str, Alias("OEMCode")]
    boot_released_date: Annotated[str, Alias("bootReleasedDate")]
    boot_version: Annotated[str, Alias("bootVersion")]
    customized_info: Annotated[str, Alias("customizedInfo")]
    device_description: Annotated[str, Alias("deviceDescription")]
    device_id: Annotated[str, Alias("deviceID")]
    device_location: Annotated[str, Alias("deviceLocation")]
    device_name: Annotated[str, Alias("deviceName")]
    device_type: Annotated[str, Alias("deviceType")]
    encoder_released_date: Annotated[str, Alias("encoderReleasedDate")]
    encoder_version: Annotated[str, Alias("encoderVersion")]
    firmware_released_date: Annotated[str, Alias("firmwareReleasedDate")]
    firmware_version: Annotated[str, Alias("firmwareVersion")]
    firmware_version_info: Annotated[str, Alias("firmwareVersionInfo")]
    hardware_version: Annotated[str, Alias("hardwareVersion")]
    mac_address: Annotated[str, Alias("macAddress")]
    manufacturer: Annotated[str, Alias("manufacturer")]
    model: Annotated[str, Alias("model")]
    serial_number: Annotated[str, Alias("serialNumber")]
    sub_serial_number: Annotated[str, Alias("subSerialNumber")]
    support_beep: Annotated[str, Alias("supportBeep")]
    support_video_loss: Annotated[str, Alias("supportVideoLoss")]
    system_contact: Annotated[str, Alias("systemContact")]
    telecontrol_id: Annotated[str, Alias("telecontrolID")]

    @classmethod
    def __pre_deserialize__(
        cls: type[Self],
        d: dict[Any, Any],
    ) -> dict[Any, Any]:
        """Unwrap the dict before deserializing."""
        if info := d.get("DeviceInfo"):
            return info  # type: ignore[no-any-return]

        error = "Unknown response status occurred"
        raise ValueError(error)

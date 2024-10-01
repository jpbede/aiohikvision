"""Hikvision ISAPI client."""

from .hikvision import Hikvision
from .models.device_info import DeviceInfo

__all__ = ["Hikvision", "DeviceInfo"]

"""Hikvision API client."""

from dataclasses import dataclass
import logging
import socket
from typing import Any, Self

from aiohttp import BasicAuth, ClientError, ClientResponseError, ClientSession
import xmltodict

from aiohikvision.exceptions import (
    HikvisionConnectionError,
    HikvisionConnectionTimeoutError,
    HikvisionInvalidCredentialsError,
)
from aiohikvision.models.device_info import DeviceInfo

_LOGGER = logging.getLogger(__name__)


@dataclass(kw_only=True)
class Hikvision:
    """Hikvision API client."""

    host: str
    port: int = 80
    username: str
    password: str
    session: ClientSession | None = None

    _close_session: bool = False

    async def _get(self, url: str) -> Any:
        """Execute a GET request against the API."""
        if self.session is None:
            self.session = ClientSession()
            self._close_session = True

        try:
            async with self.session.get(
                f"http://{url}", auth=BasicAuth(self.username, self.password)
            ) as response:
                response.raise_for_status()
                response_text = await response.text()
        except TimeoutError as exception:
            msg = "Timeout occurred while connecting to the Electricity Maps API"
            raise HikvisionConnectionTimeoutError(msg) from exception
        except (
            ClientError,
            socket.gaierror,
        ) as exception:
            if isinstance(exception, ClientResponseError) and exception.status == 401:
                msg = "The given credentials are invalid"
                raise HikvisionInvalidCredentialsError(msg) from exception

            msg = "Error occurred while communicating to the Electricity Maps API"
            raise HikvisionConnectionError(msg) from exception

        _LOGGER.debug(
            "Got response with status %s and body: %s",
            response.status,
            response_text,
        )

        return xmltodict.parse(response_text)

    async def device_info(self) -> DeviceInfo:
        """Get device information."""
        data = await self._get(url=f"{self.host}/ISAPI/System/deviceInfo")
        return DeviceInfo.from_dict(data)

    async def system_capabilities(self) -> Any:
        """Get system capabilities."""
        return await self._get(url=f"{self.host}/ISAPI/System/capabilities")

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> Self:
        """Async enter."""
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        """Async exit."""
        await self.close()

"""The myindygo integration."""

from __future__ import annotations

import asyncio

from homeassistant.config_entries import ConfigFlow
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .client import myindygo_client
from .const import DOMAIN

# TODO List the platforms that you want to support.
# For your initial PR, limit it to 1 platform.
PLATFORMS: list[Platform] = [Platform.SENSOR]

# TODO Create ConfigEntry type alias with API object
# TODO Rename type alias and update all entry annotations
# type New_NameConfigEntry = ConfigEntry[MyApi]  # noqa: F821


# TODO Update entry annotation
async def async_setup_entry(hass: HomeAssistant, entry: ConfigFlow) -> bool:
    """Set up myindygo from a config entry."""

    # 1. Create API instance
    client = myindygo_client

    await asyncio.to_thread(
        lambda: client.authenticate(entry.data["username"], entry.data["password"])
    )
    # TODO 2. Validate the API connection (and authentication)
    # TODO 3. Store an API object for your platforms to access
    # entry.runtime_data = MyAPI(...)
    hass.data.setdefault(DOMAIN, {})
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


# TODO Update entry annotation
async def async_unload_entry(hass: HomeAssistant, entry: ConfigFlow) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

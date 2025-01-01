import asyncio

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfElectricPotential, UnitOfTemperature
from homeassistant.helpers.device_registry import DeviceInfo

from .client import myindygo_client


async def async_setup_entry(hass, entry, async_add_entities) -> None:
    """Set up the MyIndygo sensors."""
    new_devices = []
    sensors = await asyncio.to_thread(lambda: myindygo_client.updateSensors())
    if sensors:
        # 3 sensors values from pool sens device
        new_devices.append(PoolTemperatureSensor(entry, sensors[0]))
        new_devices.append(PoolPhSensor(entry, sensors[1]))
        new_devices.append(PoolRedoxSensor(entry, sensors[2]))
        new_devices.append(PoolHouseTemperatureSensor(entry, sensors[3]))
    # for sensor in sensors:
    #     new_devices.append(PoolTemperatureSensor(entry, sensor))

    # TODO: Remove existing devices?
    # TODO: Remove old existing devices?
    if new_devices:
        async_add_entities(new_devices)


class PoolTemperatureSensor(SensorEntity):
    _attr_has_entity_name = True
    _attr_temperature_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:thermometer"

    def __init__(self, entry, device):
        self._device = device
        self._attr_native_value = float(
            device["Sensor value"].replace("°C", "").strip()
        )
        self.name = device["Sensor type"]
        self._attr_name = device["Sensor type"]
        self._attr_unique_id = "unique_id_myindigy_pool_temperature"

    @property
    def update(self) -> None:
        result = self.client.updateSensors()
        self._attr_native_value = float(
            result[0].get("Sensor value").replace("°C", "").strip()
        )
        # self.value = result[0]

    @property
    def device_info(self) -> DeviceInfo:
        """Return te devce info."""
        return DeviceInfo(
            identifiers={("MyIndygo", self._device["Sensor type"])},
            manufacturer="MyIndygo",
            model="Temperature Sensor",
            name="Temperature sensor",
        )


class PoolHouseTemperatureSensor(SensorEntity):
    _attr_has_entity_name = True
    _attr_temperature_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:thermometer"

    def __init__(self, entry, device):
        self._device = device
        self._attr_native_value = float(
            device["Sensor value"].replace("°C", "").strip()
        )
        self.name = device["Sensor type"]
        self._attr_name = device["Sensor type"]
        self._attr_unique_id = "unique_id_myindigy_poolhouse_temperature"

    @property
    def update(self) -> None:
        result = self.client.updateSensors()
        self._attr_native_value = float(
            result[3].get("Sensor value").replace("°C", "").strip()
        )
        # self.value = result[0]

    @property
    def device_info(self) -> DeviceInfo:
        """Return te devce info."""
        return DeviceInfo(
            identifiers={("MyIndygo", self._device["Sensor type"])},
            manufacturer="MyIndygo",
            model="PoolHouse Temperature Sensor",
            name="PoolHouse Temperature sensor",
        )


class PoolPhSensor(SensorEntity):
    _attr_has_entity_name = True
    _attr_temperature_class = SensorDeviceClass.PH
    _attr_native_unit_of_measurement = None
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:ph"

    def __init__(self, entry, device):
        self._device = device
        self._attr_native_value = float(device["Sensor value"].strip())
        self.name = device["Sensor type"]
        self._attr_name = device["Sensor type"]
        self._attr_unique_id = "unique_id_myindigy_pool_PH"

    @property
    def update(self) -> None:
        result = self.client.updateSensors()
        self._attr_native_value = float(result[1].get("Sensor value").strip())
        # self.value = result[0]

    @property
    def device_info(self) -> DeviceInfo:
        """Return te devce info."""
        return DeviceInfo(
            identifiers={("MyIndygo", self._device["Sensor type"])},
            manufacturer="MyIndygo",
            model="PH Sensor",
            name="Ph sensor",
        )


class PoolRedoxSensor(SensorEntity):
    _attr_has_entity_name = True
    _attr_temperature_class = SensorDeviceClass.VOLTAGE
    _attr_native_unit_of_measurement = UnitOfElectricPotential.MILLIVOLT
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, entry, device):
        self._device = device
        self._attr_native_value = float(
            device["Sensor value"].replace("°C", "").strip()
        )
        self.name = device["Sensor type"]
        self._attr_name = device["Sensor type"]
        self._attr_unique_id = "unique_id_myindigy_pool_redox"

    @property
    def update(self) -> None:
        result = self.client.updateSensors()
        self._attr_native_value = float(result[2].get("Sensor value").strip())
        # self.value = result[0]

    @property
    def device_info(self) -> DeviceInfo:
        """Return te devce info."""
        return DeviceInfo(
            identifiers={("MyIndygo", self._device["Sensor type"])},
            manufacturer="MyIndygo",
            model="Redox Sensor",
            name="Redox sensor",
        )

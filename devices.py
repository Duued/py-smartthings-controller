import aiohttp
import os
from typing import Dict, Optional, Any
from dotenv import load_dotenv


# auto/manual - auto will discover devices from the SmartThings API, manual will use the devices in the devices dictionary
DISCOVERY_MODE = "auto"

# The end user is responsible for manual mode
# use this mode only if you know what you are doing and have the device IDs 
# otherwise auto does everything for you


load_dotenv(verbose=True)

SMARTTHINGS_API_KEY = os.getenv("SMARTTHINGS_API_KEY")

HEADERS = {"Authorization": f"Bearer {SMARTTHINGS_API_KEY}"}


class Device:
    def __init__(self, name: str, id: str, label: str):
        self.name = name
        self.id = id
        self.label = label

    async def toggle_power(self, state: str):
        url = f"https://api.smartthings.com/v1/devices/{self.id}/commands"
        payload: Dict[str, Any] = {
            "commands": [
                {
                    "component": "main",
                    "capability": "switch",
                    "command": state,
                    "arguments": [],
                }
            ]
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=HEADERS, json=payload) as response:
                if response.status == 200:
                    print(f"Device {self.label} turned {state}")
                else:
                    print(f"Failed to toggle power for {self.name}: {response.status}")

    async def turn_on(self):
        await self.toggle_power("on")

    async def turn_off(self):
        await self.toggle_power("off")

    async def set_level(self, level: int):
        url = f"https://api.smartthings.com/v1/devices/{self.id}/commands"
        payload: Dict[str, Any] = {
            "commands": [
                {
                    "component": "main",
                    "capability": "switchLevel",
                    "command": "setLevel",
                    "arguments": [level],
                }
            ]
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=HEADERS, json=payload) as response:
                if response.status == 200:
                    print(f"Device {self.label} set to {level}%")
                elif response.status == 422:
                    print(f"This action failed. {self.label} may not support dimming.")
                else:
                    print(f"Failed to set level for {self.name}: {response.status}")


async def fetch_devices():
    url = "https://api.smartthings.com/v1/devices/"
    headers = {"Authorization": f"Bearer {SMARTTHINGS_API_KEY}"}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                for device_data in data["items"]:
                    new_device = Device(
                        name=device_data["name"],
                        id=device_data["deviceId"],
                        label=device_data["label"],
                    )
                    device_list[new_device.id] = new_device
            else:
                print(f"Failed to fetch devices: {response.status}")


device_list: Dict[str, Device] = {}


def find_device(text):
    device = device_list.get(text)
    if device:
        return device
    return find_device_by_label(text)


def find_device_by_label(label: str) -> Optional[Device]:
    # Split the label into parts
    label_parts = label.lower().split()
    
    for key, device in device_list.items():
        device_label = device.label.lower()
        # Check if all parts of the label are in the device label
        if all(part in device_label for part in label_parts):
            return device
    return None


# this is a dictionary of devices that will be populated with the devices from the SmartThings API

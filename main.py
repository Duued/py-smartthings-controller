import asyncio
import os
from dotenv import load_dotenv
from devices import DISCOVERY_MODE, device_list
import devices

load_dotenv(verbose=True)

SMARTTHINGS_API_KEY = os.getenv("SMARTTHINGS_API_KEY")


async def main():
    if DISCOVERY_MODE == "auto":
        await devices.fetch_devices()
    elif DISCOVERY_MODE == "manual":
        # todo: implement manual device setup
        # or just hope that everyone uses auto and expect people to setup manual themselves
        pass
    else:
        print(
            "Invalid discovery mode.  ~ Please set DISCOVERY_MODE to 'auto' or 'manual' in devices.py."
        )
        return

    while True:
        command = (
            input(
                "Enter command (list, on <device_id/label>, off <device_id/label>, dim <device_id/label> <percent>, exit): "
            )
            .strip()
            .lower()
        )
        if command == "list":
            for device in device_list.values():
                print(f"{device.id}: {device.name} ({device.label})")
        elif command.startswith("on "):
            device_id = command.split(" ")[1]
            device = devices.find_device(device_id)
            if device:
                await device.turn_on()
            else:
                print(f"Device with ID/label {device_id} not found.")
        elif command.startswith("off "):
            device_id = command.split(" ")[1]
            device = devices.find_device(device_id)
            if device:
                await device.turn_off()
            else:
                print(f"Device with ID/label {device_id} not found.")
        elif command.startswith("dim "):
            device_id = command.split(" ")[1]
            level = int(command.split(" ")[2])
            device = devices.find_device(device_id)
            if device:
                await device.set_level(level)
            else:
                print(f"Device with ID/label {device_id} not found.")
        elif command == "exit":
            break
        else:
            print("Unknown command.")


if __name__ == "__main__":
    asyncio.run(main())

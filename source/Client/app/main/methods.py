import json
import os

from app import CONFIG_FILE, HOME_DIR


def load_from_device_config():
    with open(CONFIG_FILE) as json_data:
        data = json.load(json_data)
    return data


def device_metadata():
    config = load_from_device_config()
    return {
        "code": config["code"],
        "ip": config["ip"],
        "store_id": config["store_id"],
    }


def run_command(cmd):
    os.system(cmd + f" > {HOME_DIR}/temp.txt")
    with open(f"{HOME_DIR}/temp.txt", "r") as r:
        cmdOutput = r.read()

    os.system(f"rm {HOME_DIR}/temp.txt")

    return cmdOutput

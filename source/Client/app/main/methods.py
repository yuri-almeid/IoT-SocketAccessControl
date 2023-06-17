import json
import os
import time

import psutil
import speedtest
from app import (  # noqa
    CONFIG_FILE,
    HOME_DIR,
    IS_EMBEDDED,
    METADATA_WAIT_TIME,
    SOCKET_CLIENT,
)


def load_from_device_config():
    with open(CONFIG_FILE) as json_data:
        data = json.load(json_data)
    return data


def device_metadata():
    while True:
        config = load_from_device_config()

        st = speedtest.Speedtest()
        download_rate = round(st.download() / (1024**2), 5)
        upload_rate = round(st.upload() / (1024**2), 5)
        uptime = time.time() - psutil.boot_time()

        if IS_EMBEDDED:
            rasp_temperature_status = os.popen(
                "vcgencmd measure_temp"
            ).readline()  # noqa

            cpu_temperature = rasp_temperature_status.replace(
                "temp=", ""
            ).replace(  # noqa
                "'C\n", ""
            )

        else:
            cpu_temperature = 0

        metadata = {
            "code": config["code"],
            "store_id": config["store_id"],
            "download": download_rate,
            "upload": upload_rate,
            "cpu": psutil.cpu_percent(2),
            "ram": psutil.virtual_memory()[2],
            "ip": config["ip"],
            "disk": psutil.disk_usage("/").percent,
            "uptime": uptime,
            "temperature": cpu_temperature,
        }

        SOCKET_CLIENT.emit("rasp_metadata", metadata)

        time.sleep(METADATA_WAIT_TIME)


def run_command(cmd):
    os.system(cmd + f" > {HOME_DIR}/temp.txt")
    with open(f"{HOME_DIR}/temp.txt", "r") as r:
        cmdOutput = r.read()

    os.system(f"rm {HOME_DIR}/temp.txt")

    return cmdOutput

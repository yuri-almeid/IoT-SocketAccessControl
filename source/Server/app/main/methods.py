from app import DB as db
from app.models import Access, Device, Logs, Status, Store
from flask import session
from flask_socketio import close_room, emit

from .. import LIST_RPI, SOCKETIO  # noqa


def background_thread():
    count = 0
    while True:
        SOCKETIO.sleep(10)
        count += 1
        SOCKETIO.emit(
            "my_response",
            {
                "data": "Server generated event",
                "count": count,
            },
        )


def getList():
    global LIST_RPI
    return LIST_RPI


def list_update(type_, data):
    global LIST_RPI
    if type_ == "disconnect":
        try:
            current = next(filter(lambda x: x["sid"] == data, LIST_RPI))
            close_room(current["code"])
            LIST_RPI = list(filter(lambda i: i["sid"] != data, LIST_RPI))
            device_status = Status.query.filter_by(
                device_code=current["code"]
            ).first()  # noqa: E501
            device_status.status = "Offline"
            db.session.add(device_status)
            db.session.commit()

        except:  # noqa: E722
            print("Cliente web Desconectado.")

    elif type_ == "connect":
        LIST_RPI.append(data)
        device_status = Status.query.filter_by(
            device_code=data["code"]
        ).first()  # noqa: E501
        device_status.status = "Online"
        db.session.add(device_status)
        db.session.commit()
    return True


def create_device(data):
    device = Device.query.filter_by(code=data["code"]).first()
    if device is None:
        device = Device(
            code=data["code"],
            store_id=data["store_id"],
            ip=data["ip"],
        )
        db.session.add(device)
        db.session.commit()

    status = Status.query.filter_by(device_id=device.id).first()
    if status is None:
        status = Status(
            device_id=device.id,
            status="Online",
            device_code=device.code,
        )
        db.session.add(status)
        db.session.commit()


def update_dashboard():
    global LIST_RPI
    devices = Device.query.all()

    rpi_codes = set(rpi["code"] for rpi in LIST_RPI)

    list_status = []

    for device in devices:
        store = Store.query.filter_by(id=device.store_id).first()
        access = Access.query.filter_by(store_id=store.id).count()
        list_status.append(
            [
                ("Online" if device.code in rpi_codes else "Offline"),
                device.code,
                store.name,
                "--",
                access,
            ]
        )

    session["receive_count"] = session.get("receive_count", 0) + 1
    emit(
        "update_dashboard",
        {
            "data": list_status,
            "count": session["receive_count"],
        },
    )


def log_device_metadata(metadata):
    try:
        device = Device.query.filter_by(code=metadata["code"]).first()
        new_log = Logs(
            device_id=device.id,
            down_speed=metadata["download"],
            up_speed=metadata["upload"],
            cpu_usage=metadata["cpu"],
            ram_usage=metadata["ram"],
            disk_usage=metadata["disk"],
            uptime=metadata["uptime"],
            cpu_temperature=metadata["temperature"],
        )
        db.session.add(new_log)
        db.session.commit()
    except Exception as e:
        print("Erro ao salvar log de metadados: " + str(e))


def log_user_access(user_id, store_id, success):
    new_access = Access(
        user_id=user_id,
        store_id=store_id,
        success=success,
    )
    db.session.add(new_access)
    db.session.commit()

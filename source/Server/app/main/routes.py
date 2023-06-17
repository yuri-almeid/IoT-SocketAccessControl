from app import DB, SOCKETIO
from app.models import Device, Status, Store, User
from flask import Response, jsonify, render_template, request
from sqlalchemy.exc import IntegrityError

from ..main import main
from ..main.methods import log_user_access


@main.route("/")
def index():
    return render_template("dashboard.html", async_mode=SOCKETIO.async_mode)


@main.route("/test")
def test():
    return render_template("index.html", async_mode=SOCKETIO.async_mode)


@main.route("/register", methods=["POST"])
def create_user():
    data = request.json
    new_user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        phone_number=data["phone_number"],
        email=data["email"],
    )
    new_user.set_password(data["password"])
    try:
        DB.session.add(new_user)
        DB.session.commit()
    except IntegrityError:
        DB.session.rollback()
        return jsonify({"message": "User already exists"}), 409
    return jsonify(new_user.to_dict()), 201


@main.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()
    if not user or not user.check_password(data["password"]):
        return jsonify({"message": "Invalid email or password"}), 401
    return jsonify({"message": "success"}), 200


@main.route("/stores", methods=["GET"])
def get_stores():
    stores = Store.query.all()
    return jsonify([store.to_dict() for store in stores]), 200


@main.route("/stores/<name>", methods=["GET"])
def get_store(name):
    store = Store.query.filter_by(name=name).first()
    return jsonify(store.to_dict()), 200


@main.route("/stores/create", methods=["POST"])
def create_store():
    data = request.json
    new_store = Store(
        name=data["name"],
        address=data["address"],
        lat=data["lat"],
        lng=data["lng"],
    )
    try:
        DB.session.add(new_store)
        DB.session.commit()
        return jsonify(new_store.to_dict()), 201
    except IntegrityError:
        DB.session.rollback()
        return jsonify({"message": "Store already exists"}), 409


@main.route("/stores/delete/<int:id>", methods=["DELETE"])
def delete_store(id):
    store = Store.query.get(id)
    DB.session.delete(store)
    DB.session.commit()
    return jsonify({"message": "success"}), 200


@main.route("/devices", methods=["GET"])
def get_devices():
    devices = Device.query.all()
    return jsonify([device.to_dict() for device in devices]), 200


@main.route("/devices/<int:id>", methods=["GET"])
def get_device(id):
    device = Device.query.get(id)
    return jsonify(device.to_dict()), 200


@main.route("/devices/create", methods=["POST"])
def create_device():
    data = request.json
    new_device = Device(
        code=data["code"],
        store_id=data["store"],
        ip=data["ip"],
    )
    try:
        DB.session.add(new_device)
        DB.session.commit()
        return jsonify(new_device.to_dict()), 201
    except IntegrityError:
        DB.session.rollback()
        return jsonify({"message": "Device already exists"}), 409


@main.route("/devices/delete/<int:id>", methods=["DELETE"])
def delete_device(id):
    device = Device.query.get(id)
    status = Status.query.filter_by(device_code=device.code).first()
    try:
        DB.session.delete(status)
        DB.session.delete(device)
        DB.session.commit()
        return jsonify({"message": "success"}), 200
    except IntegrityError:
        DB.session.rollback()
        return jsonify({"message": "Fail to delete"}), 409


@main.route("/open", methods=["POST"])
def open():
    data = request.get_json()
    user = User.query.filter_by(email=data["user_email"]).first()
    store = Store.query.filter_by(id=data["store"]).first()
    device = Device.query.filter_by(store_id=store.id).first()
    if not user or not store or not device:
        return jsonify({"message": "Invalid data"}), 401

    if not device.is_online():
        log_user_access(user.id, store.id, False)
        return jsonify({"message": "Device is offline"}), 401

    try:
        SOCKETIO.emit("open_event", {"data": "open"}, room=device.code)
    except Exception:
        return jsonify({"message": "Device is offline"}), 401

    log_user_access(user.id, store.id, True)

    return Response(
        response="Comando enviado",
        status=200,
        mimetype="application/json",
    )

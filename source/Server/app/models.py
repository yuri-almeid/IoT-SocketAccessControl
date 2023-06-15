from datetime import datetime

import bcrypt
from app import DB as db


class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    address = db.Column(db.String(255), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    date_created = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now,
    )
    date_updated = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "lat": self.lat,
            "lng": self.lng,
            "date_created": self.date_created,
            "date_updated": self.date_updated,
        }


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(
        db.Integer,
        db.ForeignKey("device.id"),
        nullable=False,
    )
    device_code = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    date_updated = db.Column(db.DateTime, nullable=False, default=datetime.now)


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(
        db.Integer,
        db.ForeignKey("store.id"),
        nullable=True,
    )
    code = db.Column(db.String(255), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    ip = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "store_id": self.store_id,
            "code": self.code,
            "date_created": self.date_created,
            "ip": self.ip,
        }

    def is_online(self):
        status = Status.query.filter_by(device_id=self.id).first()
        return True if status.status == "Online" else False


class Logs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(
        db.Integer,
        db.ForeignKey("device.id"),
        nullable=False,
    )
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    cpu_temperature = db.Column(db.Float)
    cpu_usage = db.Column(db.Float)
    ram_usage = db.Column(db.Float)
    down_speed = db.Column(db.Float)
    up_speed = db.Column(db.Float)
    disk_usage = db.Column(db.Float)
    uptime = db.Column(db.Float)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    date_updated = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "email": self.email,
            "password": self.password,
        }

    def set_password(self, password):
        self.password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt(),
        ).decode("utf-8")

    def check_password(self, password):
        return bcrypt.checkpw(
            password.encode("utf-8"),
            self.password.encode("utf-8"),
        )


class Access(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False,
    )
    store_id = db.Column(
        db.Integer,
        db.ForeignKey("store.id"),
        nullable=False,
    )
    success = db.Column(db.Boolean, nullable=False)

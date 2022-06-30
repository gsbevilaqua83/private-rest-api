from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    uuid = db.Column(db.String(256), primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)

    def get_id(self):
        return self.uuid


class Patient(db.Model):
    __tablename__ = "patients"
    uuid = db.Column(db.String(256), primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    transactions = db.relationship("Transaction", backref="patient")


class Pharmacy(db.Model):
    __tablename__ = "pharmacies"
    uuid = db.Column(db.String(256), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    transactions = db.relationship("Transaction", backref="pharmacy")


class Transaction(db.Model):
    __tablename__ = "transactions"
    uuid = db.Column(db.String(256), primary_key=True)
    patient_uuid = db.Column(db.String(256),
                             db.ForeignKey("patients.uuid"),
                             nullable=False)
    pharmacy_uuid = db.Column(db.String(256),
                              db.ForeignKey("pharmacies.uuid"),
                              nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

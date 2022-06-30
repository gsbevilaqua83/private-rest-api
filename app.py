import bcrypt
from flask import Flask, jsonify, request
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

from models import (  # <-- this needs to be placed after app is created
    Patient, Pharmacy, Transaction, User, db)

db_name = 'backend_test.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)


def login(request):
    """
    Function used to handle login of users.

    Args:
        request: request data with username and password for authentication.

    Returns:
        (bool) True if user credentials are valid else False.
        (str) Descriptive message of login result.
    """

    if "username" not in request.json or "password" not in request.json:
        return False, "missing keys in POST request body"

    user = User.query.filter_by(username=request.json["username"]).first()
    if user:
        if bcrypt.check_password_hash(user.password, request.json["password"]):
            return True, "login successful."
        else:
            return False, "wrong password."
    return False, "username doesn't exist."


@app.route('/register', methods=['POST'])
def register():
    """
    View for registering new users.

    Args:
        None

    Returns:
        (dict) Key is either 'error' or 'success' and Value is a descriptive message of the registration result.
    """

    # First user created is admin
    if User.query.count() == 0:
        if "new_username" not in request.json or "new_password" not in request.json:
            return {"error": "missing keys in POST request body"}

        if len(request.json["new_username"]) < 4:
            return {"error": "username must have at least 4 characters"}

        if len(request.json["new_password"]) < 8:
            return {"error": "password must have at least 8 characters"}

        hashed_pass = bcrypt.generate_password_hash(
            request.json["new_password"])
        user_id = "USER" + str(User.query.count() + 1)
        user = User(uuid=user_id,
                    username=request.json["new_username"],
                    password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        return {"success": "registration successful."}

    logged_in, msg = login(request)
    if "new_username" not in request.json or "new_password" not in request.json:
        return {"error": "missing keys in POST request body"}

    if logged_in:
        if len(request.json["new_username"]) < 4:
            return {"error": "username must have at least 4 characters"}

        if len(request.json["new_password"]) < 8:
            return {"error": "password must have at least 8 characters"}

        req_user = User.query.filter_by(
            username=request.json["username"]).first()
        if req_user.uuid in ("TESTER", "USER1"):
            existing_username = User.query.filter_by(
                username=request.json["new_username"]).first()

            if existing_username:
                return {"error": "username already exists."}

            hashed_pass = bcrypt.generate_password_hash(
                request.json["new_password"])
            user_id = "USER" + str(User.query.count() + 1)
            user = User(uuid=user_id,
                        username=request.json["new_username"],
                        password=hashed_pass)
            db.session.add(user)
            db.session.commit()
            return {"success": "registration successful."}

        return {"error": "current user is not allowed to register new users"}

    return {"error": msg}


@app.route('/', methods=['POST'])
def index():
    """
    View for default api url.

    Args:
        None

    Returns:
        (dict) Key is either 'error' or 'endpoints'. If errored Value is a descriptive message of the request result
        else it's the list of endpoints of the api.
    """

    logged_in, msg = login(request)
    if logged_in:
        return {"endpoints": ["/patients", "/pharmacies", "/transactions"]}

    return {"error": msg}


@app.route('/patients', methods=['POST'])
def getPatients():
    """
    View for returning information about the patients.

    Args:
        None

    Returns:
        If failed returns the error message, otherwise returns a json with patients data.
    """

    logged_in, msg = login(request)
    if logged_in:
        filters = []
        if "first_name" in request.args:
            arg = request.args["first_name"]
            filters.append(Patient.first_name.like(f'%{arg}%'))
        if "last_name" in request.args:
            arg = request.args["last_name"]
            filters.append(Patient.last_name.like(f'%{arg}%'))
        if "date_of_birth" in request.args:
            arg = request.args["date_of_birth"]
            filters.append(Patient.date_of_birth.like(f'%{arg}%'))

        patients = Patient.query.filter(*filters).order_by(
            Patient.first_name).all()

        obj = []
        for patient in patients:
            obj.append({
                "id":
                patient.uuid,
                "first_name":
                patient.first_name,
                "last_name":
                patient.last_name,
                "date_of_birth":
                patient.date_of_birth.strftime('%m/%d/%Y')
            })

        return jsonify(obj)

    return {"error": msg}


@app.route('/pharmacies', methods=['POST'])
def getPharmacies():
    """
    View for returning information about the pharmacies.

    Args:
        None

    Returns:
        If failed returns the error message, otherwise returns a json with pharmacies data.
    """

    logged_in, msg = login(request)
    if logged_in:
        filters = []
        if "name" in request.args:
            arg = request.args["name"]
            filters.append(Pharmacy.name.like(f'%{arg}%'))
        if "city" in request.args:
            arg = request.args["city"]
            filters.append(Pharmacy.city.like(f'%{arg}%'))

        pharmacies = Pharmacy.query.filter(*filters).order_by(
            Pharmacy.name).all()

        obj = []
        for pharmacy in pharmacies:
            obj.append({
                "id": pharmacy.uuid,
                "name": pharmacy.name,
                "city": pharmacy.city,
            })

        return jsonify(obj)

    return {"error": msg}


@app.route('/transactions', methods=['POST'])
def getTransactions():
    """
    View for returning information about the transactions.

    Args:
        None

    Returns:
        If failed returns the error message, otherwise returns a json with transactions data.
    """

    logged_in, msg = login(request)
    if logged_in:
        filters = []
        if "patient_first_name" in request.args:
            arg = request.args["patient_first_name"]
            filters.append(Patient.first_name.like(f'%{arg}%'))
        if "patient_last_name" in request.args:
            arg = request.args["patient_last_name"]
            filters.append(Patient.last_name.like(f'%{arg}%'))
        if "patient_date_of_birth" in request.args:
            arg = request.args["patient_date_of_birth"]
            filters.append(Patient.date_of_birth.like(f'%{arg}%'))
        if "pharmacy_name" in request.args:
            arg = request.args["pharmacy_name"]
            filters.append(Pharmacy.name.like(f'%{arg}%'))
        if "pharmacy_city" in request.args:
            arg = request.args["pharmacy_city"]
            filters.append(Pharmacy.city.like(f'%{arg}%'))
        if "amount" in request.args:
            arg = request.args["amount"]
            filters.append(Transaction.amount == str(arg))
        if "timestamp" in request.args:
            arg = request.args["timestamp"]
            filters.append(Transaction.timestamp.like(f'%{arg}%'))

        transactions = Transaction.query.join(Patient).join(Pharmacy).filter(
            *filters).order_by(Patient.first_name).all()

        obj = []
        for transaction in transactions:
            obj.append({
                "patient": {
                    "id":
                    transaction.patient.uuid,
                    "first_name":
                    transaction.patient.first_name,
                    "last_name":
                    transaction.patient.last_name,
                    "date_of_birth":
                    transaction.patient.date_of_birth.strftime('%m/%d/%Y'),
                },
                "pharmacy": {
                    "id": transaction.pharmacy.uuid,
                    "name": transaction.pharmacy.name,
                    "city": transaction.pharmacy.city,
                },
                "id":
                transaction.uuid,
                "amount":
                transaction.amount,
                "timestamp":
                transaction.timestamp.strftime('%m/%d/%Y %H:%M:%S'),
            })

        return jsonify(obj)

    return {"error": msg}

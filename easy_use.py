import getpass
import json

import requests

url = "http://127.0.0.1:5000"
query_string_params = {
    "patients": ["first_name", "last_name", "date_of_birth"],
    "pharmacies": ["name", "city"],
    "transactions": [
        "patient_first_name", "patient_last_name", "patient_date_of_birth",
        "pharmacy_name", "pharmacy_city", "amount", "timestamp"
    ],
}


def register_admin():
    try:
        print("")
        print("Admin Registration")
        new_username = input("username: ")
        new_password = getpass.getpass("password: ")
        req_body = {"new_username": new_username, "new_password": new_password}
        res = requests.post(url + "/register", json=req_body)
        print(res.json())
        if "success" not in res.json():
            print("Are you sure an admin is not already registered?")
            return False, None, None
        return True, new_username, new_password
    except:
        print(
            "ERROR: Could not make request. Are you sure the api is running?")
        return False, None, None


def login(_username, _password):
    if _username is None and _password is None:
        while 1:
            username = input("Login: ")
            password = getpass.getpass("Password: ")
            req_body = {"username": username, "password": password}
            res = requests.post(url, json=req_body)
            if "endpoints" in res.json():
                return username, password
            else:
                print(res.json())
    else:
        return _username, _password


def main(_username=None, _password=None):
    username, password = login(_username, _password)

    while 1:
        print("")
        print("ENDPOINTS: ")
        print(" 0 - register")
        print(" 1 - patients")
        print(" 2 - pharmacies")
        print(" 3 - transactions")
        print(" 4 - logout")
        print(" 5 - quit")

        endpoint = input("Choose an endpoint: ")
        req_body = {"username": username, "password": password}

        if endpoint == "0" or endpoint == "register":
            try:
                print("")
                print("New User Registration")
                new_username = input("username to register: ")
                new_password = getpass.getpass("password to register: ")
                req_body["new_username"] = new_username
                req_body["new_password"] = new_password
                res = requests.post(url + "/register", json=req_body)
                print(res.json())
            except:
                print(
                    "ERROR: Could not make request. Are you sure the api is running?"
                )
        elif endpoint == "1" or endpoint == "patients":
            try:
                query_string = "?"
                for param in query_string_params["patients"]:
                    ans = input(param + ": ")
                    if ans != "":
                        query_string += param + "=" + ans + "&"
                res = requests.post(url + "/patients" + query_string,
                                    json=req_body)
                print("")
                print("RESPONSE:")
                print(json.dumps(res.json(), indent=4, sort_keys=True))
                print("")
            except:
                print(
                    "ERROR: Could not make request. Are you sure the api is running?"
                )
        elif endpoint == "2" or endpoint == "pharmacies":
            try:
                query_string = "?"
                for param in query_string_params["pharmacies"]:
                    ans = input(param + ": ")
                    if ans != "":
                        query_string += param + "=" + ans + "&"
                res = requests.post(url + "/pharmacies" + query_string,
                                    json=req_body)
                print("")
                print("RESPONSE:")
                print(json.dumps(res.json(), indent=4, sort_keys=True))
                print("")
            except:
                print(
                    "ERROR: Could not make request. Are you sure the api is running?"
                )
        elif endpoint == "3" or endpoint == "transactions":
            try:
                query_string = "?"
                for param in query_string_params["transactions"]:
                    ans = input(param + ": ")
                    if ans != "":
                        query_string += param + "=" + ans + "&"
                res = requests.post(url + "/transactions" + query_string,
                                    json=req_body)
                print("")
                print("RESPONSE:")
                print(json.dumps(res.json(), indent=4, sort_keys=True))
                print("")
            except:
                print(
                    "ERROR: Could not make request. Are you sure the api is running?"
                )
        elif endpoint == "4" or endpoint == "logout":
            return False
        elif endpoint == "5" or endpoint == "quit":
            return True
        else:
            print("")
            print("ERROR: No endpoint selected")
            print("")


while 1:
    quit = False
    has_admin = input("Does server already have an admin? y/n: ")
    if has_admin == "y":
        while 1:
            quit = main()
            if quit:
                break

    elif has_admin == "n":
        success, user, passw = register_admin()
        if success:
            quit = main(user, passw)
            if not quit:
                while 1:
                    quit = main()
                    if quit:
                        break

    if quit:
        break

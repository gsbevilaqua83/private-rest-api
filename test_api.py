import unittest
from http import client

from app import app, bcrypt
from models import (  # <-- this needs to be placed after app is created
    Patient, Pharmacy, Transaction, User, db)


class ApiTest(unittest.TestCase):
    app = app
    bcrypt = bcrypt
    tester_username = "tester"
    tester_password = "unittesting"
    api = "http://127.0.0.1:5000"
    index_endpoint = api + "/"
    register_endpoint = api + "/register"
    patients_endpoint = api + "/patients"
    pharmacies_endpoint = api + "/pharmacies"
    transactions_endpoint = api + "/transactions"

    def make_tester_user(self):
        hashed_pass = self.bcrypt.generate_password_hash(self.tester_password)
        user = User(uuid="TESTER",
                    username=self.tester_username,
                    password=hashed_pass)
        db.session.add(user)
        db.session.commit()

    def delete_tester_user(self):
        User.query.filter_by(uuid="TESTER").delete()
        db.session.commit()

    def make_notadmin_tester_user(self):
        hashed_pass = self.bcrypt.generate_password_hash(self.tester_password)
        user = User(uuid="NOTADMIN",
                    username=self.tester_username + "#",
                    password=hashed_pass)
        db.session.add(user)
        db.session.commit()

    def delete_notadmin_tester_user(self):
        User.query.filter_by(uuid="NOTADMIN").delete()
        db.session.commit()

    def test_1_patients_get_request(self):
        client = self.app.test_client()
        r = client.get(self.patients_endpoint)
        self.assertEqual(r.status_code, 405)

    def test_2_pharmacies_get_request(self):
        client = self.app.test_client()
        r = client.get(self.pharmacies_endpoint)
        self.assertEqual(r.status_code, 405)

    def test_3_transactions_get_request(self):
        client = self.app.test_client()
        r = client.get(self.transactions_endpoint)
        self.assertEqual(r.status_code, 405)

    def test_4_register_get_request(self):
        client = self.app.test_client()
        r = client.get(self.register_endpoint)
        self.assertEqual(r.status_code, 405)

    def test_5_patients_no_login(self):
        client = self.app.test_client()
        r = client.post(self.patients_endpoint, json={})
        self.assertEqual(r.status_code, 200)
        self.assertTrue("error" in r.json)
        self.assertTrue(r.json["error"] == "missing keys in POST request body")

    def test_6_patients_no_username(self):
        client = self.app.test_client()
        r = client.post(self.patients_endpoint, json={"password": ""})
        self.assertEqual(r.status_code, 200)
        self.assertTrue("error" in r.json)
        self.assertTrue(r.json["error"] == "missing keys in POST request body")

    def test_7_patients_no_username(self):
        client = self.app.test_client()
        r = client.post(self.patients_endpoint, json={"password": ""})
        self.assertEqual(r.status_code, 200)
        self.assertTrue("error" in r.json)
        self.assertTrue(r.json["error"] == "missing keys in POST request body")

    def test_8_patients_bad_username(self):
        client = self.app.test_client()
        r = client.post(self.patients_endpoint,
                        json={
                            "username": "",
                            "password": ""
                        })
        self.assertEqual(r.status_code, 200)
        self.assertTrue("error" in r.json)
        self.assertTrue(r.json["error"] == "username doesn't exist.")

    def test_9_patients_bad_password(self):
        client = self.app.test_client()
        with self.app.app_context():
            self.make_tester_user()
            r = client.post(self.patients_endpoint,
                            json={
                                "username": self.tester_username,
                                "password": self.tester_password + "#"
                            })
            self.delete_tester_user()
            self.assertEqual(r.status_code, 200)
            self.assertTrue("error" in r.json)
            self.assertTrue(r.json["error"] == "wrong password.")

    def test_10_patients_good_login(self):
        client = self.app.test_client()
        with self.app.app_context():
            self.make_tester_user()
            r = client.post(self.patients_endpoint,
                            json={
                                "username": self.tester_username,
                                "password": self.tester_password
                            })
            self.delete_tester_user()
            self.assertEqual(r.status_code, 200)
            self.assertFalse("error" in r.json)

    def test_11_pharmacies_no_login(self):
        client = self.app.test_client()
        r = client.post(self.pharmacies_endpoint, json={})
        self.assertEqual(r.status_code, 200)
        self.assertTrue("error" in r.json)
        self.assertTrue(r.json["error"] == "missing keys in POST request body")

    def test_12_pharmacies_no_username(self):
        client = self.app.test_client()
        r = client.post(self.pharmacies_endpoint, json={"password": ""})
        self.assertEqual(r.status_code, 200)
        self.assertTrue("error" in r.json)
        self.assertTrue(r.json["error"] == "missing keys in POST request body")

    def test_13_pharmacies_no_username(self):
        client = self.app.test_client()
        r = client.post(self.pharmacies_endpoint, json={"password": ""})
        self.assertEqual(r.status_code, 200)
        self.assertTrue("error" in r.json)
        self.assertTrue(r.json["error"] == "missing keys in POST request body")

    def test_14_pharmacies_bad_username(self):
        client = self.app.test_client()
        r = client.post(self.pharmacies_endpoint,
                        json={
                            "username": "",
                            "password": ""
                        })
        self.assertEqual(r.status_code, 200)
        self.assertTrue("error" in r.json)
        self.assertTrue(r.json["error"] == "username doesn't exist.")

    def test_15_pharmacies_bad_password(self):
        client = self.app.test_client()
        with self.app.app_context():
            self.make_tester_user()
            r = client.post(self.pharmacies_endpoint,
                            json={
                                "username": self.tester_username,
                                "password": self.tester_password + "#"
                            })
            self.delete_tester_user()
            self.assertEqual(r.status_code, 200)
            self.assertTrue("error" in r.json)
            self.assertTrue(r.json["error"] == "wrong password.")

    def test_16_pharmacies_good_login(self):
        client = self.app.test_client()
        with self.app.app_context():
            self.make_tester_user()
            r = client.post(self.pharmacies_endpoint,
                            json={
                                "username": self.tester_username,
                                "password": self.tester_password
                            })
            self.delete_tester_user()
            self.assertEqual(r.status_code, 200)
            self.assertFalse("error" in r.json)

    def test_17_transactions_no_login(self):
        client = self.app.test_client()
        r = client.post(self.transactions_endpoint, json={})
        self.assertEqual(r.status_code, 200)
        self.assertTrue("error" in r.json)
        self.assertTrue(r.json["error"] == "missing keys in POST request body")

    def test_18_transactions_no_username(self):
        client = self.app.test_client()
        r = client.post(self.transactions_endpoint, json={"password": ""})
        self.assertEqual(r.status_code, 200)
        self.assertTrue("error" in r.json)
        self.assertTrue(r.json["error"] == "missing keys in POST request body")

    def test_19_transactions_no_username(self):
        client = self.app.test_client()
        r = client.post(self.transactions_endpoint, json={"password": ""})
        self.assertEqual(r.status_code, 200)
        self.assertTrue("error" in r.json)
        self.assertTrue(r.json["error"] == "missing keys in POST request body")

    def test_20_transactions_bad_username(self):
        client = self.app.test_client()
        r = client.post(self.transactions_endpoint,
                        json={
                            "username": "",
                            "password": ""
                        })
        self.assertEqual(r.status_code, 200)
        self.assertTrue("error" in r.json)
        self.assertTrue(r.json["error"] == "username doesn't exist.")

    def test_21_transactions_bad_password(self):
        client = self.app.test_client()
        with self.app.app_context():
            self.make_tester_user()
            r = client.post(self.transactions_endpoint,
                            json={
                                "username": self.tester_username,
                                "password": self.tester_password + "#"
                            })
            self.delete_tester_user()
            self.assertEqual(r.status_code, 200)
            self.assertTrue("error" in r.json)
            self.assertTrue(r.json["error"] == "wrong password.")

    def test_22_transactions_good_login(self):
        client = self.app.test_client()
        with self.app.app_context():
            self.make_tester_user()
            r = client.post(self.transactions_endpoint,
                            json={
                                "username": self.tester_username,
                                "password": self.tester_password
                            })
            self.delete_tester_user()
            self.assertEqual(r.status_code, 200)
            self.assertFalse("error" in r.json)

    def test_23_register_no_login(self):
        client = self.app.test_client()
        r = client.post(self.register_endpoint, json={})
        self.assertEqual(r.status_code, 200)
        self.assertTrue("error" in r.json)
        self.assertTrue(r.json["error"] == "missing keys in POST request body")

    def test_24_register_no_username(self):
        client = self.app.test_client()
        r = client.post(self.register_endpoint, json={"password": ""})
        self.assertEqual(r.status_code, 200)
        self.assertTrue("error" in r.json)
        self.assertTrue(r.json["error"] == "missing keys in POST request body")

    def test_25_register_no_username(self):
        client = self.app.test_client()
        r = client.post(self.register_endpoint, json={"password": ""})
        self.assertEqual(r.status_code, 200)
        self.assertTrue("error" in r.json)
        self.assertTrue(r.json["error"] == "missing keys in POST request body")

    def test_26_register_no_new_username(self):
        client = self.app.test_client()
        with self.app.app_context():
            self.make_tester_user()
            r = client.post(self.register_endpoint,
                            json={
                                "username": self.tester_username,
                                "password": self.tester_password
                            })
            self.delete_tester_user()
            self.assertEqual(r.status_code, 200)
            self.assertTrue("error" in r.json)
            self.assertTrue(
                r.json["error"] == "missing keys in POST request body")

    def test_27_register_no_new_password(self):
        client = self.app.test_client()
        with self.app.app_context():
            self.make_tester_user()
            r = client.post(self.register_endpoint,
                            json={
                                "username": self.tester_username,
                                "password": self.tester_password,
                                "new_username": "newuser"
                            })
            self.delete_tester_user()
            self.assertEqual(r.status_code, 200)
            self.assertTrue("error" in r.json)
            self.assertTrue(
                r.json["error"] == "missing keys in POST request body")

    def test_28_register_bad_username(self):
        client = self.app.test_client()
        with self.app.app_context():
            self.make_tester_user()
            r = client.post(self.register_endpoint,
                            json={
                                "username": "",
                                "password": "",
                                "new_username": "newuser",
                                "new_password": "newpassword"
                            })
            self.delete_tester_user()
            self.assertEqual(r.status_code, 200)
            self.assertTrue("error" in r.json)
            self.assertTrue(r.json["error"] == "username doesn't exist.")

    def test_29_register_bad_password(self):
        client = self.app.test_client()
        with self.app.app_context():
            self.make_tester_user()
            r = client.post(self.register_endpoint,
                            json={
                                "username": self.tester_username,
                                "password": self.tester_password + "#",
                                "new_username": "newuser",
                                "new_password": "newpassword"
                            })
            self.delete_tester_user()
            self.assertEqual(r.status_code, 200)
            self.assertTrue("error" in r.json)
            self.assertTrue(r.json["error"] == "wrong password.")

    def test_30_register_existing_user(self):
        client = self.app.test_client()
        with self.app.app_context():
            self.make_tester_user()
            r = client.post(self.register_endpoint,
                            json={
                                "username": self.tester_username,
                                "password": self.tester_password,
                                "new_username": self.tester_username,
                                "new_password": self.tester_password
                            })
            self.delete_tester_user()
            self.assertEqual(r.status_code, 200)
            self.assertTrue("error" in r.json)
            self.assertTrue(r.json["error"] == "username already exists.")

    def test_31_register_not_allowed(self):
        client = self.app.test_client()
        with self.app.app_context():
            self.make_tester_user()
            self.make_notadmin_tester_user()
            r = client.post(self.register_endpoint,
                            json={
                                "username": self.tester_username + "#",
                                "password": self.tester_password,
                                "new_username": "newuser",
                                "new_password": "newpassword"
                            })
            self.delete_tester_user()
            self.delete_notadmin_tester_user()
            self.assertEqual(r.status_code, 200)
            self.assertTrue("error" in r.json)
            self.assertTrue(
                r.json["error"] ==
                "current user is not allowed to register new users")

    def test_32_register_username_bad_length(self):
        client = self.app.test_client()
        with self.app.app_context():
            self.make_tester_user()
            User.query.filter_by(username="new").delete()
            db.session.commit()
            r = client.post(self.register_endpoint,
                            json={
                                "username": self.tester_username,
                                "password": self.tester_password,
                                "new_username": "new",
                                "new_password": "newpassword"
                            })
            self.delete_tester_user()
            self.assertEqual(r.status_code, 200)
            self.assertTrue("error" in r.json)
            self.assertTrue(
                r.json["error"] == "username must have at least 4 characters")

    def test_33_register_password_bad_length(self):
        client = self.app.test_client()
        with self.app.app_context():
            self.make_tester_user()
            User.query.filter_by(username="new").delete()
            db.session.commit()
            r = client.post(self.register_endpoint,
                            json={
                                "username": self.tester_username,
                                "password": self.tester_password,
                                "new_username": "newusername",
                                "new_password": "newp"
                            })
            self.delete_tester_user()
            self.assertEqual(r.status_code, 200)
            self.assertTrue("error" in r.json)
            self.assertTrue(
                r.json["error"] == "password must have at least 8 characters")

    def test_34_register_good_request(self):
        client = self.app.test_client()
        with self.app.app_context():
            self.make_tester_user()
            r = client.post(self.register_endpoint,
                            json={
                                "username": self.tester_username,
                                "password": self.tester_password,
                                "new_username": "newusername",
                                "new_password": "newpassword"
                            })
            self.delete_tester_user()
            User.query.filter_by(username="newusername").delete()
            db.session.commit()
            self.assertEqual(r.status_code, 200)
            self.assertTrue("success" in r.json)
            self.assertTrue(r.json["success"] == "registration successful.")

    def test_35_index_no_login(self):
        client = self.app.test_client()
        r = client.post(self.index_endpoint, json={})
        self.assertEqual(r.status_code, 200)
        self.assertTrue("error" in r.json)
        self.assertTrue(r.json["error"] == "missing keys in POST request body")

    def test_36_index_no_username(self):
        client = self.app.test_client()
        r = client.post(self.index_endpoint, json={"password": ""})
        self.assertEqual(r.status_code, 200)
        self.assertTrue("error" in r.json)
        self.assertTrue(r.json["error"] == "missing keys in POST request body")

    def test_37_index_no_username(self):
        client = self.app.test_client()
        r = client.post(self.index_endpoint, json={"password": ""})
        self.assertEqual(r.status_code, 200)
        self.assertTrue("error" in r.json)
        self.assertTrue(r.json["error"] == "missing keys in POST request body")

    def test_38_index_bad_username(self):
        client = self.app.test_client()
        r = client.post(self.index_endpoint,
                        json={
                            "username": "",
                            "password": ""
                        })
        self.assertEqual(r.status_code, 200)
        self.assertTrue("error" in r.json)
        self.assertTrue(r.json["error"] == "username doesn't exist.")

    def test_39_index_bad_password(self):
        client = self.app.test_client()
        with self.app.app_context():
            self.make_tester_user()
            r = client.post(self.index_endpoint,
                            json={
                                "username": self.tester_username,
                                "password": self.tester_password + "#"
                            })
            self.delete_tester_user()
            self.assertEqual(r.status_code, 200)
            self.assertTrue("error" in r.json)
            self.assertTrue(r.json["error"] == "wrong password.")

    def test_40_index_good_login(self):
        client = self.app.test_client()
        with self.app.app_context():
            self.make_tester_user()
            r = client.post(self.index_endpoint,
                            json={
                                "username": self.tester_username,
                                "password": self.tester_password
                            })
            self.delete_tester_user()
            self.assertEqual(r.status_code, 200)
            self.assertFalse("error" in r.json)


if __name__ == "__main__":
    unittest.main()

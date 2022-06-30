# private-rest-api

## SETUP:

First clone the repository:
```
git clone https://github.com/gsbevilaqua83/private-rest-api.git
```

### Option 1: Docker

Change to the root folder
```
cd private-rest-api
```

Build docker container with the Makefile:
```
make build
```

Run container:
```
make run
```

Server will be running at port 5000


### Option 2: No Docker

Change to the root folder
```
cd private-rest-api
```

Create new virtual enviroment:
```
python3 -m venv env
```

Activate enviroment:
```
source env/bin/activate
```

Install project dependencies on the enviroment:
```
python3 -m pip install -r requirements.txt 
```

Run the application:
```
./gunicorn_starter.sh
```

Server will be running at port 5000



## USAGE:

### Option 1: CURL

Obs: I'm using curl on the following examples, however it should work with any tool that can make POST requests.

On the first initialization of the server the db has no users. Once the first user is registered that user will be the admin. Only the admin is allowed to register new users and all users registered are allowed to access the api endpoints with their respective credentials.

To register the admin make a POST request to the api url. If running locally it will be http://127.0.0.1:5000/register. The POST's body needs to have the following keys: "new_username", "new_password".
Here's an example making the POST request with a curl command:
```
curl -X POST -H "Content-Type: application/json" -d '{"new_username": "admin", "new_password": "bluestorm"}' "http://127.0.0.1:5000/register"
```

After that the admin can register new users the same way but also passing its credentials with the keys: "username", "password"
```
curl -X POST -H "Content-Type: application/json" -d '{"username": "admin", "password": "bluestorm", "new_username": "adam", "new_password": "adamspassword"}' "http://127.0.0.1:5000/register"
```

Any registered user can access the endpoints by passing their credentials in the POST's body:
```
curl -X POST -H "Content-Type: application/json" -d '{"username": "adam", "password": "adamspassword"}' "http://127.0.0.1:5000/patients"
```

### Filtros de Busca (Query Strings):

Users can filter the data received by including parameters at the end of the endpoint's url. Starting with a '?' and separating each parameter with a '&':
```
curl -X POST -H "Content-Type: application/json" -d '{"username": "adam", "password": "adamspassword"}' "http://127.0.0.1:5000/patients?first_name=abel&last_name=pereira"
```
This request will only return the patients named "Abel Pereira".

For date parameters they need to be queried in the format "year-month-day":
```
curl -X POST -H "Content-Type: application/json" -d '{"username": "adam", "password": "adamspassword"}' "http://127.0.0.1:5000/patients?date_of_birth=1974-12-03"
``` 

But can also querie by only using part of the date:
```
curl -X POST -H "Content-Type: application/json" -d '{"username": "adam", "password": "adamspassword"}' "http://127.0.0.1:5000/patients?date_of_birth=1974"
```
This will return any patient with a '1974' on it's date of birth.


Each endpoint's parameters are listed below:
```
/patients

parameters: {
  first_name
  last_name
  date_of_birth
}
```

```
/pharmacies

parameters: {
  name
  city
}
```

```
/transactions

parameters: {
  patient_first_name
  patient_last_name
  patient_date_of_birth
  pharmacy_name
  pharmacy_city
  amount
  timestamp
}
```


### Option 2: easy_use.py

I've made a simple script that helps interacting with the api.

If not created already create a new virtual enviroment:
```
python3 -m venv env
```

Activate enviroment:
```
source env/bin/activate
```

Install project dependencies on the enviroment:
```
python3 -m pip install -r requirements.txt 
```

To run the script just use:
```
python3 easy_use.py
```

The same way as option 1, if it's the first time initializing the server you should answer "yes" on the first prompt so that you can create an admin user. After that you'll be prompted with a choice for the endpoint to querie and will be followed with a prompt for each parameter of the filter. Can leave each parameter of the filter blank to not use it on the search.


## DEVELOPMENT:

Change to the root folder
```
cd private-rest-api
```

Create new virtual enviroment:
```
python3 -m venv env
```

Activate enviroment:
```
source env/bin/activate
```

Install project dependencies on the enviroment:
```
python3 -m pip install -r requirements.txt 
```

I'm using pre-commit with isort and yapf for automated code formatting when pushing to the repository. pre-commit's configuration is included in the file .pre-commit-config.yaml and yapf's configuration is included in the file .style.yapf. To enable pre-commit do:
```
pre-commit install
```

For Continuous Integration the repo is being watched by a CircleCI workflow. It runs the tests in test_api.py for every commit pushed to the repo.

# SMS Delivery System
This project implements the task requested by YektaNet in Python, using Django and Django REST Framework.

## Setup
To setup the project navigate to the root of the project and create a virtualenv.
```
cd sms_sender
python3 -m venv venv
```

Now install the dependencies via `pip`
```
pip install -r requirements.txt
```

Run the migrations
```
cd sms_sender
./manage.py migrate
```

The database is sqlite3 but it can be simply replaced by more sophisticated
database engines such as Postgres.

To run the server
```
./manage.py runserver
```

This however runs the project in the development mode. To run the project in the
production mode
```
cd sms_sender
DJANGO_SETTINGS_MODULE=sms_sender.settings.prod ./manage.py runserver
```

## Usage
The project defines several API endpoint to interact with. The list of the
endpoints as follows:

* `/register/` for registering a user
* `/login/` for login :)
* `/users/` for retrieving and editing the user but not creating
* `/contacts/` CRUD for contacts
* `/contact_groups/` CRUD for contact groups
* `/send_sms/` for sending SMS

All the endpoints are protected by token authentication except for `/register`
and `/login`. A user can only see his account and all of the operations are done
in the context of the authenticated user.

Example request for registration:
```
POST /register/

{
  "username": "foo",
  "password": "passw0rd",
  "password_repeat": "passw0rd" 
}
```
Returns an authentication token to be used for subsequent requests.
```
{
  "token": "0e07b32ee15a3e5d6c0a0c14df1a6cf0f2e255b6"
}
```

Example request for login:
```
POST /login/

{
  "username": "foo",
  "password": "passw0rd"
}
```
Returns the authentication token.
```
{
  "token": "0e07b32ee15a3e5d6c0a0c14df1a6cf0f2e255b6"
}
```

The token must be used as header with following form:
```
Authorization: Token 0e07b32ee15a3e5d6c0a0c14df1a6cf0f2e255b6
```

Example request for editing user data:
```
PATCH /users/foo/

{
  "name": "yektanet"
}
```
Changes the user (company) name.
```
{
  "name": "yektanet",
  "username": "foo",
  "address": "",
  "est_date": null,
  "email": ""
}
```

Example request for creating a contact:
```
POST /contacts/

{
  "name": "contact",
  "phone": "+989352140000"
}
```
Returns the created contact along with its contact id (`contact_id`).
```
{
  "name": "contact",
  "phone": "+989352140000",
  "contact_id": "c-2748232e522a4eba"
}
```

Example request to get all contacts:
```
GET /contacts/
```
Returns
```
[
  {
    "name": "contact",
    "phone": "+989352140000",
    "contact_id": "c-2748232e522a4eba"
  }
]
```

Example request for creating a contact group:
```
POST /contact_groups/

{
  "name": "contact-group",
  "contacts": [
    "c-2748232e522a4eba"
  ]
}
```
Returns the created contact group along with its group id (`group_id`).
```
{
  "name": "contact-group",
  "contacts": [
    "c-2748232e522a4eba"
  ],
  "group_id": "g-e832031180964cd2"
}
```

A user can send an SMS using the `/send_sms/` endpoint. This endpoint takes a
message and a list of contacts and contact groups.

Example request for sending SMS:
```
POST /send_sms/

{
  "contacts": [
    "c-2748232e522a4eba",
    "g-e832031180964cd2"
  ],
  "message": "Hello world!"
}
```
Sends the message to the provided contacts.

## Description of the SMS algorithm

To avoid sending a message to a contact multiple times, phone numbers are retrieved 
from the database based on the provided contacts and contact groups. At this point,
the list of the phone numbers is sorted in O(nlog(n)), then duplicate phone numbers
are removed in linear time.

Project Name: MediConnect
Project members: Giancarlos Cabrera(gjc357@nyu.edu), Nisha Khushboo(nlr10004@nyu.edu), Tan Kim(tk2496@nyu.edu)
Software Development Period: Jan 22, 2024 - Apr 30, 2024

Objective of the project:
Despite the emergence of efficient communication-technology including the Internet and phones, there still is a considerable amount of miscommunication in medical fields
MediConnect aims to reduce such the miscommunication between patients and medical professionals by constructing the database shared with each side
Therefore the product shall be easy-to-use and similarly accessible to everyone
Accessibility-wise and security-wise the product was decided to be Web-app and here we present codes for it

Extensional libraries(environments) used for software:
1. dotenv - load environment variables from .env file
2. flask - backend framework
3. flask_bcrypt - flaks module that is used to check hashing
4. flask_login - flask module that helps user authentication
5. flask_mail - flask module that sends emails from a Flask application using SMTP servers and integrating with email services
6. flask_socketio - flask module that enables real time chatting
7. flask_wtf - flask module that defines database framework on code
8. functools - help develop additional actions for routing
9. sqlalchemy - enable executing SQL queries
10. google - A library that interacts with Google Cloud Platform services, such as Google Cloud Storage, BigQuery, and Compute Engine
11. itsdangerous - A library for creating secure data serializers and managing URL-safe signing, often used for token-based mechanisms in Flask
12. pytest - unit-testing module
13. pytube - download video with url given
14. werkzeug -  A comprehensive WSGI library used by Flask for routing, request handling, HTTP utilities, and server management
15. wtforms - A library for creating and validating web forms with complex field types, validation rules, and integration with Flask applications

Additional requirements to run software:
1. .env - store databse information and various API keys
2. db_creds.json - store google API information for accessing database on GCP
These files are separately shared and managed on team group chat for security purpose
Please contact one of project members if the files needed

How to run software:
1. locate in the root directory(where .gitignore and app.py lcoate at)
2. type in "flask run" in terminal
3. "flask --debug run" is another option if monitoring changes based on code modification is needed

How to execute unit-test:
1. locate in the root directory(wehre .gitignore and app.py locate at)
2. type in "pytest" ion terminal

Files & folders descriptions:
/app.py - file to be run to initiate an app
/db_classes.py - file that describes structure of the database
/download_vid.py - file that stores functions to download a YouTube video
/extensions.py - file that initiates variables globally used
/__init__.py - file to be called when initializing an app
/routes.py - file that includes functions used to manage routings and API endpoints
/routing_protection.py - file that includes helper functions for secured routing
/db_creation - folder that stores sql files used to intiialize the database on GCP
/db_creation/create.sql - file that can be used to construct the database
/db_creation/insert.sql - file that includes ISNERT queries for example rows
/db_creation/test.sql - file that includes short queries temporarily used for testing
/static - folder that stores static files, which describe properties/structure of .html files
/static/css - folder that stores .css files for each .html file
/static/image - folder that stores images used in .html files
/static/script - folder that stores .js files adding more components or dynamic features to .html files
/templates - folder that stores .html files to be shown to end-users
/templates/users - folder that stores .html files specifically for end-users(patients, physicians, and pharamcies)
/tests - folder that stores test files
/tests/conftest.py - file that configures app for testing
/tests/__init__.py - file that helps pytest to distinguish between root and test directories
/tests/test_app.py - file that includes testing functions(starting with "test_")
/uploads - folder that stores files temporarily used for prototype

Container API
A REST API built with FastAPI that reads and manages container records stored in an
Oracle database. It uses a connection pool, bind variables, Pydantic input validation and
API-key security.
This is a personal learning project that connects my Oracle/PL/SQL background with
modern API development.
<img width="927" height="449" alt="image" src="https://github.com/user-attachments/assets/2283e8ae-6da2-411d-8c72-541bc7943ffc" />

API docs page
Tech stack
Python, FastAPI, Uvicorn, Pydantic, python-oracledb, Oracle Database (XE)
Endpoints
Method Path
What it does
GET
/health
Health check (no API key needed)
GET
/containers/{container_id}
Get one container
GET
/containers
List containers
POST
/containers
Create a container
PATCH
/containers/{container_id}/status
Update a container’s status
DELETE
/containers/{container_id}
Delete a container
POST
/predict/dwell-time
Predict dwell time (demo model)
All 
/containers and 
/predict endpoints require the header 
(Delete any rows for endpoints you did not build.)
How to run it
1. Create the table (in your Oracle user’s schema):
sql
X-API-Key .
CREATE TABLE containers (
container_id  VARCHAR2(11) PRIMARY KEY,
size_ft       
VARCHAR2(2)  NOT NULL,
weight_kg     
destination   
status
);
NUMBER(8,2)  NOT NULL,
VARCHAR2(50) NOT NULL,
VARCHAR2(20) DEFAULT 'IN_YARD' NOT NULL
2. Set up Python (Windows PowerShell):
powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
3. Set the environment variables (use your own values):
powershell
$env:DB_USER = "your_user"
$env:DB_PASSWORD = "your_password"
$env:DB_DSN = "127.0.0.1:1521/XEPDB1"
$env:API_KEY = "choose-a-key"
4. Train the demo model (needed only for the prediction endpoint):
powershell
mkdir models
python train_model.py
5. Start the server:
powershell
uvicorn app.main:app --reload
6. Try it:
Open 
http://127.0.0.1:8000/docs
Or from a second PowerShell window:
powershell
curl.exe -H "X-API-Key: choose-a-key" http://127.0.0.1:8000/containers/MSKU1234

Run the tests
powershell
python -m pytest -q

(Keep this section only if your tests pass.)
Notes
The prediction model is trained on synthetic (made-up) data for demonstration. It
shows how to serve a model through an API. It is not a real dwell-time model.
Passwords and API keys are read from environment variables and are never stored in
the code.
The data in the example is made up.
Author
Shaheeda Shaik [LinkedIn link] | [Email]

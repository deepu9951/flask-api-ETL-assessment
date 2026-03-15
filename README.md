# flask-api-ETL-assessment
Project to implement Flask APIs with Streamlit frontend and PostgreSQL database. Added an ETL Script to load the data from the database

## 1.Clone the repository
```
git clone https://github.com/deepu9951/flask-api-ETL-assessment.git
cd flask-api-ETL-assessment
```
## 2. Creating a Virtual Environment
```
python -m venv etl_uosh_tasks
```
## 3. Activate the Virtual Environment
```
etl_uosh_tasks\Scripts\activate
```
## 4 . Downloading and installing the appropriate packages
```
pip install -r requirements.txt
```
## 5 . Task 1: Set up Databases
```
psql -U username -d databasename -f datapreparation.sql
```
## 6 . Task 2: List the REST APIs
The project uses streamlit as a front-end that enables the users to render the API responses dynamically. An extra API is also developed to render the order details of active customers.


In a terminal run the following command
```
python app.py
```
The Flask application will be running on http://127.0.0.1:5000

Run the following command in the same virtual environment in a separate terminal to run the streamlit application
```
streamlit run streamlit_app.py
```

# flask-api-ETL-assessment
Project to implement Flask APIs with Streamlit frontend and PostgreSQL database. Added an ETL Script to load the data from the database

## Technology Stack

1. PostgreSQL
PostgreSQL is used to manage structured, relational data with enforced integrity constraints. It uses Multi-Version Concurrency Control that performs consistently well in high-concurrency systems and ensures data durability using a mechanism called Write-Ahead Logging (WAL).

2. Python Flask Framework
The Flask ecosystem provides numerous libraries and extensions for various functionalities like database integration, authentication (Flask-JWT) etc. It offers a powerful routing system that enables developers to define URL patterns and map them to specific functions or resources. 

3. Streamlit
In this assessment, streamlit is chosen as the frontend layer for prototyping applications making it suitable for rendering API responses interactively.

## Application Data Flow Achitecture
The architecture is organized into the following stages.

Stage 1 — Raw Data (Source)
The sample data originates from two CSV files, customer_dataset.csv and order_dataset.csv, stored in the data/ directory. These files contain the raw customer and order records that feed the entire pipeline.

Stage 2 — ETL Ingestion (data_preparation.py)
The ingestion script reads both CSVs using pandas, validates the expected columns. It then connects to PostgreSQL and first executes SQL file to execute the Data Defininition commands to create the relevant schema and the required tables. Data records are then loaded into the respective tables using batch upserts ensuring no duplicates are introduced on repeat runs. The database acts as the single source of truth for all downstream layers.

Stage 3 - REST API (app.py)
The Flask application connects to PostgreSQL and exposes the stored data as REST endpoints. The following endpoint queries the relevant table and returns the results as JSON. 

An additional endpoint is provided specifically to return order details for active customers only, joining across both tables.

Stage 5 — Frontend (streamlit_app.py)
The Streamlit app calls the Flask API endpoints over HTTP and renders the JSON responses as interactive tables.

Stage 6 — Export (etl_script.py)
The ETL export script queries the database directly, transforms or aggregates the data as needed, and writes the output to a CSV file.


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
python data_preparation.py
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
The Streamlit application will be running on http://localhost:8501/

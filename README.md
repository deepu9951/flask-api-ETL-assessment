# flask-api-ETL-assessment
Project to implement Flask APIs with Streamlit frontend and PostgreSQL database. Added an ETL Script to load the data from the database

## Technology Stack

1. PostgreSQL
- PostgreSQL is used to manage structured, relational data with enforced integrity constraints. It uses Multi-Version Concurrency Control that performs consistently well in high-concurrency systems and ensures data durability using a mechanism called Write-Ahead Logging (WAL).

2. Python Flask Framework
- The Flask ecosystem provides numerous libraries and extensions for various functionalities like database integration, authentication (Flask-JWT) etc. It offers a powerful routing system that enables developers to define URL patterns and map them to specific functions or resources. 

3. Streamlit
- In this assessment, streamlit is chosen as the frontend layer for prototyping the frontend layer to render API responses interactively.

## Application Data Flow Achitecture
The architecture is organized into the following stages.

- Stage 1 — Raw Data (Source)
The sample data originates from two CSV files, customer_dataset.csv and order_dataset.csv, stored in the data/ directory. These files contain the raw customer and order records that feed the entire pipeline.

- Stage 2 — ETL Ingestion (data_preparation.py)
The ingestion script reads both CSVs using pandas, validates the expected columns. It then connects to PostgreSQL and first executes SQL file to execute the Data Defininition commands to create the relevant schema and the required tables. Data records are then loaded into the respective tables using batch upserts ensuring no duplicates are introduced on repeat runs. The database acts as the single source of truth for all downstream layers.

- Stage 3 — REST API (app.py)
  The Flask application connects to PostgreSQL and exposes the stored data as REST endpoints. The following endpoint queries the relevant table and returns the   results as JSON. 

  An additional endpoint is provided specifically to return order details for active customers only, joining across both tables.

- Stage 5 — Frontend (streamlit_app.py)
  The Streamlit app calls the Flask API endpoints over HTTP and renders the JSON responses as interactive tables.

- Stage 6 — Export (etl_script.py)
  The ETL export script queries the database directly, transforms or aggregates the data as needed, and writes the output to a CSV file.


## Run Application Locally
Prerequisites: Before running the following steps, it is assumed that Python and PostgreSQL is installed. Execute the commands on the command prompt by following the steps sequentially

## 1. Clone the repository
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
## 5. Update the .env file

POSTGRES_HOST =  <host_name>     <br />
POSTGRES_PORT = 5432 (Typically) <br />
POSTGRES_DB =  <your_database_name>       <br />
POSTGRES_USER = <your_database_username>  <br />
POSTGRES_PASSWORD = <your_password> 

## 6 . Task 1: Set up Databases
```
python data_preparation.py
```
## 7 . Task 2: List the REST APIs
The project uses streamlit as a front-end that enables the users to render the API responses dynamically. An extra API is also developed to render the order details of active customers.


In a terminal run the following command
```
python app.py
```
The Flask application will be running on http://127.0.0.1:5000

# APIs Defined
- http://127.0.0.1:5000/ -- gives the unique customer IDs
- http://127.0.0.1:5000/orders/<customer_id> -- Gives the order details by the specified customer_id
- http://127.0.0.1:5000/customers/active -- Returns the order details of active customers

## 8 . Frontend
The project uses streamlit as a front-end that enables the users to render the API responses dynamically. An extra API is also developed to render the order details of active customers.

Run the following command in the same virtual environment in a separate terminal to run the streamlit application. (Execute the command on Step 3 by navigating to the appropriate directory before executing the command below)
```
streamlit run streamlit_app.py
```
- The Streamlit application will be running on http://localhost:8501/
- The application will be acting as a frontend layer to render the responses for the previously defined APIs.


## 9 . Task 3: ETL Script
Run the following command in the same virtual environment in a separate terminal to run the ETL script. (Execute the command on Step 3 by navigating to the appropriate directory before executing the command below)
```
python etl_script.py
```

## Improvements
1. Using UUID for storing unique customer and order details.
2. Implementing unit test cases in the code repository.
3. To schedule the ETL tasks using Task Scheduler (in Windows) or Cron Jobs (in Unix). Apache Airflow could also be utilized.  
4. Improving the efficiency of the source code.

import pandas as pd
import streamlit as st
import requests

st.set_page_config(page_title="Assessment Highlights", layout="wide")
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{
        width: 400px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child{
        width: 400px;
        margin-left: -400px;
    }

    """,
    unsafe_allow_html=True,
)

st.title('Assessment Tasks')

st.title('Task 1 - Database Setup implemented using scripts', width="stretch")

st.title('Task 2 - REST API returning records for a single customer', width="stretch")
# http://127.0.01:5000/ is from the flask api
response = requests.get("http://127.0.0.1:5000//")
print(response.json())
customer_ids = pd.DataFrame(response.json())
customer_id_options = st.selectbox('Unique Customers', customer_ids)
st.write('You selected:', customer_id_options)


# http://127.0.01:5000/ is from the flask api
response = requests.get(f"http://127.0.0.1:5000//orders//{customer_id_options}")
print(response.json())
order_details = pd.DataFrame(response.json())
st.data_editor(order_details, column_order=("customer_id", "first_name", "surname", "email_id", "order_id", "account_status", "product_name", "quantity","unit_price"))


st.title('Task 3 - REST API returning records of active customers with total values of orders', width="stretch")

st.markdown(
    """
Streamlit enables to download the records as CSV by default. However ETL Script based on the requirements for the assessment has also been implemented 
    """)

response = requests.get(f"http://127.0.0.1:5000//customers//active")
print(response.json())
active_customer_details = pd.DataFrame(response.json())
st.data_editor(active_customer_details, column_order=("customer_id", "customer_name", "email_id", "order_id", "product_name", "quantity","unit_price", "total_value"))








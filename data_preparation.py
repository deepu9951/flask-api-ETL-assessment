from app import get_db_connection
import  logging
import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch


logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

INSERT_QUERY_CUSTOMER = """
    INSERT INTO e_commerce.dim_customer
        (customer_id, first_name, surname, email_id, account_status)
    VALUES
        (%(customer_id)s, %(first_name)s, %(surname)s, %(email_id)s, %(account_status)s)
    ON CONFLICT (customer_id) DO UPDATE
    SET
        first_name     = EXCLUDED.first_name,
        surname        = EXCLUDED.surname,
        email_id       = EXCLUDED.email_id,
        account_status = EXCLUDED.account_status;
"""

INSERT_QUERY_ORDER = """
    INSERT INTO e_commerce.dim_orders
        (order_id, product_name, prod_qty, unit_price, cust_id)
    VALUES
        (%(order_id)s, %(product_name)s, %(prod_qty)s, %(unit_price)s, %(cust_id)s)
    ON CONFLICT (order_id) DO UPDATE
    SET
        product_name = EXCLUDED.product_name,
        prod_qty     = EXCLUDED.prod_qty,
        unit_price   = EXCLUDED.unit_price,
        cust_id      = EXCLUDED.cust_id;
"""


def load_csv(filepath: str, expected_cols: list[str]) -> list[dict]:
    """
    Reads a CSV and validates expected columns are present,
    and returns a list of dicts.
    """
    df = pd.read_csv(filepath, encoding="utf-8-sig")  # utf-8-sig strips BOM automatically
    missing = set(expected_cols) - set(df.columns)
    if missing:
        raise ValueError(f"[{filepath}] Missing expected columns: {missing}")
    # Retaining required columns
    df = df[expected_cols]

    # Strip whitespace from string columns
    df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

    logging.info(f"Loaded {len(df)} rows from '{filepath}'")
    return df.to_dict(orient="records")


def insert_values(cursor, sql: str, records: list[dict], label: str):
    """Executes a batch insert and logs a summary."""
    execute_batch(cursor, sql, records, page_size=100)
    logging.info(f"Inserted {len(records)} rows into {label}")


def data_definition():
    """
    Reads the SQL file and creates the required schema and tables.
    """
    with open('data_definition.sql', "r", encoding="utf-8-sig") as f:
        raw = f.read()
        # fetch individual queries from the SQL file
        sql_queries = [stmt.strip()
                      for stmt in raw.split(";")
                      if stmt.strip()
                    ]
        print(sql_queries)
        conn = get_db_connection()
        conn.autocommit = True
        cursor = conn.cursor()
        for query in sql_queries:
            cursor.execute(query)
        logging.info(f"Created Schema and Tables")


def data_manipulation():
    customer_dataset = load_csv(
        'data/customer_dataset.csv',
        expected_cols=["customer_id", "first_name", "surname", "email_id", "account_status"]
    )
    orders_dataset = load_csv(
        'data/order_dataset.csv',
        expected_cols=["order_id", "product_name", "prod_qty", "unit_price", "cust_id"]
    )
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        insert_values(cursor, INSERT_QUERY_CUSTOMER, customer_dataset, "e_commerce.dim_customer")
        insert_values(cursor, INSERT_QUERY_ORDER, orders_dataset, "e_commerce.dim_orders")
        conn.commit()
        logging.info("Data Loading Complete")
    except psycopg2.Error as e:
        logging.warning(f"Database error \n  Detail: {e}\n")
        raise


if __name__ == "__main__":
    data_definition()
    data_manipulation()
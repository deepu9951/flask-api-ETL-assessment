from app import get_db_connection
import psycopg2
import logging
import os
import csv


def data_loading():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Retrieve the order details of active customers from the database
        query = f"""
        SELECT 
            o.order_id,
			o.cust_id,
			CONCAT_WS(' ',c.first_name,  c.surname) AS customer_name,
			c.email_id,
			c.account_status,
            o.product_name,
            o.prod_qty,
            o.unit_price,
            (o.prod_qty * o.unit_price) AS total_value
        FROM e_commerce.dim_orders o
        JOIN e_commerce.dim_customer c
        ON o.cust_id = c.customer_id
        where c.account_status = 'active'
        """
        cursor.execute(query)
        with open("orders.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([desc[0] for desc in cursor.description])
            for row in cursor:
                writer.writerow(row)
    except Exception as e:
        return e

if __name__ == "__main__":
    data_loading()



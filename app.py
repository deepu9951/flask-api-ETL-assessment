from flask import Flask, jsonify, request
from dotenv import load_dotenv
import psycopg2
import os


load_dotenv()


app = Flask(__name__)

def get_db_connection():
    """
    Establishes a connection to the PostgreSQL database.
    """
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST","localhost"),
        port = int(os.getenv("POSTGRES_PORT", "5432")),
        database= os.getenv("POSTGRES_DB", "postgres"),
        user= os.getenv("POSTGRES_USER","postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "localhost")
    )
    return conn


@app.route('/', methods=['GET'])
def get_all_customers():
    """
    Retrieve all unique customer ids.
    ---
    responses:
      200:
        description: A list of customer ids.
    """

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT customer_id FROM e_commerce.dim_customer;")
        results = cursor.fetchall()
        print(results)
        formatted_results = []
        for row in results:
            order = {
                "customer_id": row[0]
            }
            formatted_results.append(order)
        return jsonify(formatted_results)
    except psycopg2.Error:
        return jsonify({'error': 'Failed to retrieve the list of customers'}), 500


@app.route('/orders/<customer_id>', methods=['GET'])
def get_order_by_number(customer_id):
    """
    Retrieve order details by customer_id
    ---
    responses:
      200:
        description: The customer and order details with the specified ID.
      404:
        description: Customer not found.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Retrieve the order from the database
        query = f"""
        SELECT 
            o.order_id,
            o.product_name,
            o.prod_qty,
            o.unit_price,
            o.cust_id,
            c.first_name,
            c.surname,
            c.email_id,
            c.account_status
        FROM e_commerce.dim_orders o
        JOIN e_commerce.dim_customer c
        ON o.cust_id = c.customer_id
        where o.cust_id = '{customer_id}'
        """
        cursor.execute(query)
        order = cursor.fetchall()
        orders_list =[]
        if order:
            for i in range(len(order)):
                # Format the order as a dictionary
                formatted_order = {
                    "order_id": [order[i][0]],
                    "product_name": order[i][1],
                    "quantity": order[i][2],
                    "unit_price": order[i][3],
                    "customer_id": order[i][4],
                    "first_name": order[i][5],
                    "surname": order[i][6],
                    "email_id": order[i][7],
                    "account_status": order[i][8]
                }
                orders_list.append(formatted_order)
            return jsonify(orders_list), 200
        else:
            return jsonify({'error': 'Order not found'}), 404
    except psycopg2.Error:
        return jsonify({'error': 'Failed to retrieve order'}), 500


@app.route('/customers/active/', methods=['GET'])
def get_order_details():
    """
    Retrieve order details of active customers
    ---
    responses:
      200:
        description: The customer and order details.
      404:
        description: Customer not found.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Retrieve the order from the database
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
        order = cursor.fetchall()
        print(order)
        orders_list =[]
        if order:
            for i in range(len(order)):
                # Format the order as a dictionary
                formatted_order = {
                    "order_id": [order[i][0]],
                    "customer_id": order[i][1],
                    "customer_name": order[i][2],
                    "email_id": order[i][3],
                    "product_name": order[i][5],
                    "prod_qty": order[i][6],
                    "unit_price": order[i][7],
                    "total_value": order[i][8]
                }
                orders_list.append(formatted_order)
            return jsonify(orders_list), 200
        else:
            return jsonify({'error': 'Order not found'}), 404
    except psycopg2.Error:
        return jsonify({'error': 'Failed to retrieve order'}), 500


if __name__ == "__main__":
    app.run(debug=True)
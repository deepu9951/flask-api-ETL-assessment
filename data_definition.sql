CREATE SCHEMA IF NOT EXISTS e_commerce AUTHORIZATION CURRENT_USER;

CREATE TABLE IF NOT EXISTS e_commerce.dim_customer(
customer_id TEXT PRIMARY KEY NOT NULL,
first_name TEXT NOT NULL,
surname TEXT NOT NULL,
email_id TEXT UNIQUE,
account_status TEXT CHECK (account_status IN ('archived','active','suspended'))
);

CREATE TABLE IF NOT EXISTS e_commerce.dim_orders(
order_id TEXT PRIMARY KEY NOT NULL,
product_name TEXT NOT NULL,
prod_qty INT NOT NULL CHECK (prod_qty >= 1),
unit_price NUMERIC(12,2) NOT NULL CHECK (unit_price >=0),
cust_id TEXT, CONSTRAINT fk_order_customer
	FOREIGN KEY (cust_id)
	REFERENCES e_commerce.dim_customer(customer_id)
	ON DELETE SET NULL
);

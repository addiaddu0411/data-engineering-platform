import psycopg2
import pandas as pd

# -------------------
# EXTRACT
# -------------------
def extract():
    return pd.read_csv("data/raw/customers.csv")


# -------------------
# LOAD
# -------------------
def load(df):
    conn = psycopg2.connect(
        host="localhost",
        database="warehouse",
        user="admin",
        password="admin",
        port=5432
    )

    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INT,
        name TEXT,
        amount INT
    );
    """)

    for _, row in df.iterrows():
        cur.execute(
            "INSERT INTO customers (id, name, amount) VALUES (%s, %s, %s)",
            (row["id"], row["name"], row["amount"])
        )

    conn.commit()
    cur.close()
    conn.close()


# -------------------
# TRANSFORM
# -------------------
def transform():
    conn = psycopg2.connect(
        host="localhost",
        database="warehouse",
        user="admin",
        password="admin",
        port=5432
    )

    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS customer_summary AS
    SELECT
        id,
        name,
        amount,
        amount * 1.1 AS adjusted_amount
    FROM customers;
    """)

    conn.commit()
    cur.close()
    conn.close()


# -------------------
# RUN PIPELINE
# -------------------
def run():
    df = extract()
    load(df)
    transform()
    print("ETL + Transformation completed successfully!")


if __name__ == "__main__":
    run()

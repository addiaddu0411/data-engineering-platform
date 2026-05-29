import psycopg2

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

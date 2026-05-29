import psycopg2

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

import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "database": "warehouse",
    "user": "admin",
    "password": "admin",
    "port": 5432
}

# -----------------------------
# RAW LOAD (INCREMENTAL)
# -----------------------------
def insert_data(df):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        print("Connected to PostgreSQL successfully!")

        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO customers (id, name, amount)
                VALUES (%s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (
                row["id"],
                row["name"],
                row["amount"]
            ))

        conn.commit()
        cursor.close()
        conn.close()

        print("Raw data load completed")

    except Exception as e:
        print("DB ERROR:", e)


# -----------------------------
# ANALYTICS LAYER
# -----------------------------
def build_analytics_layer(df):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        print("Building analytics layer...")

        for _, row in df.iterrows():

            amount = row["amount"]

            if amount >= 250:
                tier = "VIP"
            elif amount >= 150:
                tier = "Gold"
            else:
                tier = "Standard"

            cursor.execute("""
                INSERT INTO customer_summary (id, name, total_amount, tier)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (
                row["id"],
                row["name"],
                amount,
                tier
            ))

        conn.commit()
        cursor.close()
        conn.close()

        print("Analytics layer completed")

    except Exception as e:
        print("Analytics DB ERROR:", e)

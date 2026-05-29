import psycopg2
from config import DB_CONFIG


def insert_data(df):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        print("Connected to PostgreSQL successfully!")

        print("DF SHAPE:", df.shape)
        print("DF COLUMNS:", df.columns)
        print(df.head(2))

        inserted = 0

        for _, row in df.iterrows():
            try:
                print("Inserting row...")

                cursor.execute("""
                    INSERT INTO pollution_data (
                        state, county, city, date_local,
                        no2_mean, o3_mean, so2_mean, co_mean
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    row.get("State"),
                    row.get("County"),
                    row.get("City"),
                    row.get("Date Local"),
                    row.get("NO2 Mean"),
                    row.get("O3 Mean"),
                    row.get("SO2 Mean"),
                    row.get("CO Mean")
                ))

                inserted += 1

            except Exception as e:
                print("INSERT FAILED:", e)

        conn.commit()
        cursor.close()
        conn.close()

        print("TOTAL INSERTED:", inserted)

    except Exception as e:
        print("DB CONNECTION ERROR:", e)

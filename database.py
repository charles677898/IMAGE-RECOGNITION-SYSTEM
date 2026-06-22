import sqlite3


DATABASE_NAME = "image_predictions.db"


def create_database():

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            image_name TEXT,

            prediction TEXT,

            confidence REAL,

            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP

        )
    """)

    conn.commit()

    conn.close()


def save_prediction(
        image_name,
        prediction,
        confidence):

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions
        (
            image_name,
            prediction,
            confidence
        )
        VALUES (?, ?, ?)
    """,
    (
        image_name,
        prediction,
        confidence
    ))

    conn.commit()

    conn.close()


def get_history():

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM predictions
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data


def get_total_predictions():

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM predictions
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_average_confidence():

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT AVG(confidence)
        FROM predictions
    """)

    result = cursor.fetchone()[0]

    conn.close()

    if result:
        return round(result, 2)

    return 0


def get_most_common_prediction():

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT prediction,
               COUNT(*) as count
        FROM predictions
        GROUP BY prediction
        ORDER BY count DESC
        LIMIT 1
    """)

    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]

    return "No Data"
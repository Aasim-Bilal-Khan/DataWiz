import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def run_query(sql):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        cursor = conn.cursor()

        if sql.strip().lower().startswith("select"):
            cursor.execute(sql)
            cols = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            result = [dict(zip(cols, row)) for row in rows]
        else:
            cursor.execute(sql)
            conn.commit()
            result = {"status": "✅ Executed", "affected_rows": cursor.rowcount}

        cursor.close()
        conn.close()
        return result

    except Exception as e:
        return {"error": str(e)}

def get_schema():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        schema = ""

        for table in tables:
            cursor.execute(f"DESCRIBE {table}")
            columns = cursor.fetchall()
            col_names = [col[0] for col in columns]
            schema += f"{table}({', '.join(col_names)})\n"

        cursor.close()
        conn.close()
        return schema.strip()
    except Exception as e:
        return f"Error retrieving schema: {e}"

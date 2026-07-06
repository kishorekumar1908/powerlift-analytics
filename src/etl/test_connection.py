from sqlalchemy import text

from db_connection import get_engine

try:
    engine = get_engine()

    with engine.connect() as conn:
        version = conn.execute(text("SELECT VERSION();"))

        print("Connected Successfully!")
        print("MySQL Version:", version.scalar())

except Exception as e:
    print("Connection Failed")
    print(e)
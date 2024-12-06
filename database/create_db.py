from sqlalchemy import create_engine, text




def create_database_if_not_exists(user, password, host, dbname):
    """Checks if database exists and creates one if it does not"""
    engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}/postgres")

    with engine.connect() as conn:
        # Check if Database exists
        result = conn.execute(text(f"SELECT 1 from pg_database WHERE datname='{dbname}'"))

        if not result.scalar(): # No rows returned means the DB doesn't exist
            conn.execute(text("COMMIT")) # PostgreSQL requires a Commit before creating a db
            conn.execute(text(f"CREATE DATABASE {dbname}"))
            print(f"Database {dbname} created successfully")
        else:
            print(f"Database {dbname} already exists")
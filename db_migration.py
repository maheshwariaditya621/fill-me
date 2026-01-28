from sqlalchemy import text
from database import engine

def migrate():
    with engine.connect() as connection:
        try:
            # Check if column exists
            print("Checking if column 'other_platform_name' exists...")
            # This query works for MariaDB/MySQL information_schema
            result = connection.execute(text("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'survey_responses' AND COLUMN_NAME = 'other_platform_name'"))
            if result.rowcount == 0:
                print("Adding column 'other_platform_name'...")
                connection.execute(text("ALTER TABLE survey_responses ADD COLUMN other_platform_name VARCHAR(255) NULL"))
                print("Column added successfully.")
            else:
                print("Column 'other_platform_name' already exists.")
            
            # Since we only added new enum values for categories, and they are stored as JSON strings or raw strings in DB (which doesn't enforce standard SQL ENUM type constraints usually unless explicitly defined), we good.
            # But wait, schema validation handles Enums. DB just stores string.
            
            print("Migration check complete.")
        except Exception as e:
            print(f"Migration error: {e}")

if __name__ == "__main__":
    migrate()

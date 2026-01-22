import os
import re
import random

# --- Configuration ---
# Source tables location on Lenovo ThinkPad X390
SOURCE_TABLES_DIR = "/home/hunter/IdeaProjects/python/python->plsql_file_parser/examples/SOURCE_SCHEMA/TABLE"
OUTPUT_DIR = "/home/hunter/IdeaProjects/python/python->plsql_file_parser/examples/SOURCE_SCHEMA/DEPLOYMENT"
OUTPUT_FILE = "insert_test_data.sql"

def get_table_metadata(file_path):
    """
    Dynamically extracts table name and column metadata (name and data type) from DDL.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract table name (supports SCHEMA.TABLE or "TABLE")
    table_match = re.search(r'CREATE\s+TABLE\s+((?:"?\w+"?\.?)?"?\w+"?)', content, re.IGNORECASE)
    if not table_match:
        return None, []

    table_name = table_match.group(1)

    # Regex to find column names and their types (VARCHAR2, NUMBER, DATE, etc.)
    # It looks for "COL_NAME" TYPE_NAME
    col_pattern = re.compile(r'"(\w+)"\s+(\w+)')
    columns = []

    for match in col_pattern.finditer(content):
        name = match.group(1)
        data_type = match.group(2).upper()
        # Filter out SQL keywords that might be caught by regex
        if name not in ["CREATE", "TABLE"]:
            columns.append({"name": name, "type": data_type})

    return table_name, columns

def get_flexible_value(col_type):
    """
    Generates data based strictly on the Oracle data type.
    """
    if "DATE" in col_type or "TIMESTAMP" in col_type:
        return f"SYSDATE - {random.randint(0, 365)}"

    if "NUMBER" in col_type or "INTEGER" in col_type:
        # Generates a random numeric value
        return str(random.randint(1, 99999))

    if "VARCHAR2" in col_type or "CHAR" in col_type or "TEXT" in col_type:
        # Generates a generic test string
        return f"'TEST_DATA_{random.randint(100, 999)}'"

    # Fallback for unknown types
    return "'DUMMY_VALUE'"

def generate_test_data():
    """
    Main function to crawl DDLs and create a monolithic INSERT script.
    """
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    output_lines = [
        "-- DYNAMICALLY GENERATED TEST DATA",
        "SET DEFINE OFF;",
        "ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS';",
        ""
    ]

    # Process all SQL files in the source directory
    sql_files = sorted([f for f in os.listdir(SOURCE_TABLES_DIR) if f.endswith(".sql")])

    for sql_file in sql_files:
        table_name, columns = get_table_metadata(os.path.join(SOURCE_TABLES_DIR, sql_file))

        if not table_name or not columns:
            continue

        output_lines.append(f"-- Inserting 5 sample rows into {table_name}")
        col_names_formatted = ", ".join([f'"{c["name"]}"' for c in columns])

        for _ in range(5):
            values = [get_flexible_value(c["type"]) for c in columns]
            values_formatted = ", ".join(values)
            output_lines.append(f"INSERT INTO {table_name} ({col_names_formatted}) VALUES ({values_formatted});")

        output_lines.append("COMMIT;")
        output_lines.append("")

    # Save to the DEPLOYMENT folder
    final_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    with open(final_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(output_lines))

    print(f"Successfully generated flexible test data script at: {final_path}")

if __name__ == "__main__":
    generate_test_data()
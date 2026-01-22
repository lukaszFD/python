import re
import os

# --- Configuration variables ---
BASE_DIR = "/home/hunter/IdeaProjects/python/python->plsql_file_parser/examples"
INPUT_FILE = os.path.join(BASE_DIR, "tbl.sql")

SOURCE_SCHEMA_NAME = "SOURCE_SCHEMA"
TARGET_SCHEMA_NAME = "TARGET_SCHEMA"

TABLE_PREFIX = "TEST_"
VIEW_PREFIX = "V_"
ADD_AUDIT_COL = True

def prepare_directories():
    """Creates the folder structure: examples/SCHEMA_NAME/TABLE and examples/TARGET_SCHEMA/VIEW"""
    paths = {
        "source_table": os.path.join(BASE_DIR, SOURCE_SCHEMA_NAME, "TABLE"),
        "target_table": os.path.join(BASE_DIR, TARGET_SCHEMA_NAME, "TABLE"),
        "target_view": os.path.join(BASE_DIR, TARGET_SCHEMA_NAME, "VIEW")
    }
    for path in paths.values():
        os.makedirs(path, exist_ok=True)
    return paths

def finalize_sql(sql_block):
    """Ensures every SQL statement ends with a semicolon and removes trailing slashes"""
    sql_block = sql_block.strip().rstrip('/')
    if not sql_block.endswith(';'):
        return sql_block + ';'
    return sql_block

def split_and_generate_all():
    dirs = prepare_directories()

    if not os.path.exists(INPUT_FILE):
        print(f"Error: Input file not found at {INPUT_FILE}")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by the '/' separator
    blocks = re.split(r'\n\s*/\s*\n', content)

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        # Regex to find the table name
        table_pattern = r'CREATE\s+TABLE\s+("?\w+"?)'
        match = re.search(table_pattern, block, re.IGNORECASE)

        if match:
            original_table_name = match.group(1).replace('"', '')

            # 1. Generate SOURCE DDL
            source_ddl = re.sub(table_pattern, f'CREATE TABLE "{SOURCE_SCHEMA_NAME}"."{original_table_name}"', block, flags=re.IGNORECASE)
            source_ddl = finalize_sql(source_ddl)
            with open(os.path.join(dirs["source_table"], f"{original_table_name.upper()}.sql"), 'w') as f_src:
                f_src.write(source_ddl + "\n")

            # 2. Generate TARGET DDL (with guaranteed Audit Column)
            target_table_name = f"{TABLE_PREFIX}{original_table_name}"
            target_ddl = re.sub(table_pattern, f'CREATE TABLE "{TARGET_SCHEMA_NAME}"."{target_table_name}"', block, flags=re.IGNORECASE)

            if ADD_AUDIT_COL:
                # Robust injection before the last closing parenthesis
                target_ddl = target_ddl.strip().rstrip('/').rstrip(';').rstrip()
                target_ddl = re.sub(r'\)\s*$', ',\n    "INSERTED_ON" DATE DEFAULT SYSDATE\n)', target_ddl)

            target_ddl = finalize_sql(target_ddl)
            with open(os.path.join(dirs["target_table"], f"{target_table_name.upper()}.sql"), 'w') as f_tgt:
                f_tgt.write(target_ddl + "\n")

            # 3. Generate VIEW (filtering by today's date)
            view_name = f"{VIEW_PREFIX}{target_table_name}"
            view_ddl = f"""CREATE OR REPLACE VIEW "{TARGET_SCHEMA_NAME}"."{view_name}" AS
SELECT * FROM "{TARGET_SCHEMA_NAME}"."{target_table_name}"
WHERE TRUNC("INSERTED_ON") = TRUNC(SYSDATE);
/"""
            with open(os.path.join(dirs["target_view"], f"{view_name.upper()}.sql"), 'w') as f_vw:
                f_vw.write(view_ddl + "\n")

            print(f"Processed: {original_table_name} -> Source, Target, and View generated.")

if __name__ == "__main__":
    split_and_generate_all()
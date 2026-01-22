import re
import os

# Configuration variables
TARGET_SCHEMA = "TEST_SCHEMA"  # Change to "TEST" or "TEST2"
INPUT_FILE = "source_schema.sql"
OUTPUT_DIR = "generated_tables"

def split_and_fix_sql(input_filename, schema_name, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    with open(input_filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by the '/' separator
    blocks = re.split(r'\n\s*/\s*\n', content)

    for block in blocks:
        block = block.strip()
        if not block:
            continue
        
        # Regex to find the table name
        # It captures the table name and allows us to inject the schema
        table_pattern = r'CREATE\s+TABLE\s+("?\w+"?)'
        match = re.search(table_pattern, block, re.IGNORECASE)
        
        if match:
            original_table_name = match.group(1).replace('"', '')
            
            # Inject schema name: CREATE TABLE "SCHEMA"."TABLE"
            updated_block = re.sub(table_pattern, f'CREATE TABLE {schema_name}.{match.group(1)}', block, flags=re.IGNORECASE)
            
            # Ensure the statement ends with a semicolon after the last parenthesis
            # We look for the last ')' and ensure ';' follows it
            if not updated_block.strip().endswith(';'):
                updated_block = updated_block.rstrip()
                if updated_block.endswith(')'):
                    updated_block += ';'
                else:
                    # Fallback if there's text after the last parenthesis
                    updated_block += ';'

            output_path = os.path.join(output_dir, f"{original_table_name.upper()}.sql")
            
            with open(output_path, 'w', encoding='utf-8') as f_out:
                f_out.write(updated_block + "\n")
            
            print(f"Generated: {output_path} with schema {schema_name}")

if __name__ == "__main__":
    split_and_fix_sql(INPUT_FILE, TARGET_SCHEMA, OUTPUT_DIR)

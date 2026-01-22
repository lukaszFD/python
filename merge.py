import re
import os

# Configuration variables
SCHEMA_DEST = "TEST_SCHEMA"      # Target schema (where records are updated/inserted)
SCHEMA_SRC = "STAGING_SCHEMA"    # Source schema (where raw data comes from)
INPUT_DIR = "generated_tables"
OUTPUT_DIR = "generated_merges"

def generate_oracle_merges(input_dir, schema_tgt, schema_src, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".sql"):
            with open(os.path.join(input_dir, filename), 'r', encoding='utf-8') as f:
                content = f.read()

            # Find table name from the file content (already contains schema from Script 1)
            # We extract just the table name to build our logic
            table_match = re.search(r'CREATE\s+TABLE\s+(?:\w+\.)?"?(\w+)"?', content, re.IGNORECASE)
            if not table_match:
                continue
            
            table_name = table_match.group(1).upper()

            # Extract columns from the DDL
            columns = []
            for line in content.split('\n'):
                line = line.strip()
                # Basic column extraction: ignores CREATE, TABLE and constraints
                col_match = re.match(r'^"?(\w+)"?\s+\w+', line)
                if col_match:
                    name = col_match.group(1).upper()
                    if name not in ["CREATE", "TABLE"]:
                        columns.append(name)

            if columns:
                # First column as PK for the ON clause
                pk_col = columns[0]
                other_cols = columns[1:]

                # Update SET part
                update_set = ",\n        ".join([f"tgt.{c} = src.{c}" for c in other_cols])
                
                # Insert part
                cols_joined = ", ".join(columns)
                vals_joined = ", ".join([f"src.{c}" for c in columns])

                # Build MERGE script with Schema variables
                merge_sql = f"""MERGE INTO {schema_tgt}.{table_name} tgt
USING {schema_src}.{table_name} src
ON (tgt.{pk_col} = src.{pk_col})
WHEN MATCHED THEN
    UPDATE SET 
        {update_set}
WHEN NOT MATCHED THEN
    INSERT ({cols_joined})
    VALUES ({vals_joined});
/
"""
                output_path = os.path.join(output_dir, f"MERGE_{table_name}.sql")
                with open(output_path, 'w', encoding='utf-8') as f_out:
                    f_out.write(merge_sql)
                
                print(f"Created Merge script for {schema_tgt}.{table_name}")

if __name__ == "__main__":
    generate_oracle_merges(INPUT_DIR, SCHEMA_DEST, SCHEMA_SRC, OUTPUT_DIR)

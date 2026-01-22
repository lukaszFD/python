import os

# --- Configuration paths ---
BASE_DIR = "/home/hunter/IdeaProjects/python/python->plsql_file_parser/examples"
SCHEMAS = ["SOURCE_SCHEMA", "TARGET_SCHEMA"]
# Order of deployment to handle dependencies (Tables -> Views -> Packages -> Jobs)
DEPLOY_ORDER = ["TABLE", "VIEW", "PKG", "JOB"]

def generate_scripts_for_schema(schema_name):
    schema_path = os.path.join(BASE_DIR, schema_name)
    deploy_dir = os.path.join(schema_path, "DEPLOYMENT")

    # Create deployment directory if it does not exist
    if not os.path.exists(deploy_dir):
        os.makedirs(deploy_dir)

    # Initial headers for the monolithic installation script
    install_content = [
        f"-- DEPLOYMENT SCRIPT: {schema_name}",
        "SET DEFINE OFF;",
        "SET ECHO ON;",
        ""
    ]

    # Initial headers for the rollback script
    rollback_content = [
        f"-- ROLLBACK SCRIPT: {schema_name}",
        "SET ECHO ON;",
        ""
    ]

    # Iterate through folders in the predefined deployment order
    for folder in DEPLOY_ORDER:
        folder_path = os.path.join(schema_path, folder)
        if not os.path.exists(folder_path):
            continue

        # Sort files to maintain alphabetical order within the folder
        files = sorted([f for f in os.listdir(folder_path) if f.endswith(".sql")])

        for file in files:
            file_full_path = os.path.join(folder_path, file)
            object_name = file.replace(".sql", "").upper()

            # Read the original SQL file content
            with open(file_full_path, 'r', encoding='utf-8') as f_src:
                content = f_src.read().strip()

            # --- INSTALL LOGIC: Copy content to monolith ---
            install_content.append(f"PROMPT Deploying {object_name}...")
            install_content.append(content)

            # Logic for closing statements correctly in SQL*Plus
            if folder in ["PKG", "JOB"]:
                # Packages and Jobs always end with a slash in a new line
                if not content.endswith("/"):
                    install_content.append("\n/")
            else:
                # Tables and views end with a semicolon
                if not content.endswith(";"):
                    install_content.append(";")

            install_content.append("") # Blank line separator

            # --- ROLLBACK LOGIC: Generate DROP statements ---
            if folder == "TABLE":
                rollback_content.append(f"DROP TABLE \"{schema_name}\".\"{object_name}\" CASCADE CONSTRAINTS;")
            elif folder == "VIEW":
                rollback_content.append(f"DROP VIEW \"{schema_name}\".\"{object_name}\";")
            elif folder == "PKG":
                rollback_content.append(f"DROP PACKAGE \"{schema_name}\".\"{object_name}\";")
            elif folder == "JOB":
                # Check if job exists before dropping to make the rollback reusable
                rollback_content.append(f"BEGIN")
                rollback_content.append(f"    FOR r IN (SELECT job_name FROM all_scheduler_jobs WHERE owner = '{schema_name}' AND job_name = '{object_name}')")
                rollback_content.append(f"    LOOP DBMS_SCHEDULER.DROP_JOB(r.job_name); END LOOP;")
                rollback_content.append(f"END;")
                rollback_content.append("/")
                rollback_content.append("")

    # Save the monolithic installation script
    with open(os.path.join(deploy_dir, "install.sql"), 'w', encoding='utf-8') as f:
        f.write("\n".join(install_content) + "\nCOMMIT;\nEXIT;")

    # Save the monolithic rollback script
    with open(os.path.join(deploy_dir, "rollback.sql"), 'w', encoding='utf-8') as f:
        f.write("\n".join(rollback_content) + "\nCOMMIT;\nEXIT;")

    print(f"Scripts for {schema_name} generated successfully.")

if __name__ == "__main__":
    for schema in SCHEMAS:
        if os.path.exists(os.path.join(BASE_DIR, schema)):
            generate_scripts_for_schema(schema)
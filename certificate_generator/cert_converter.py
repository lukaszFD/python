import os

def generate_ansible_vault_yaml(certs_dir: str, output_file: str):
    """
    Reads .crt and .key files from a directory and formats them into an Ansible Vault-ready YAML file.
    """
    if not os.path.exists(certs_dir):
        print(f"Error: Directory {certs_dir} not found.")
        return

    # List all unique service names based on .crt files
    services = [f[:-4] for f in os.listdir(certs_dir) if f.endswith('.crt')]

    if not services:
        print("No certificates found in the directory.")
        return

    with open(output_file, "w") as yaml_out:
        yaml_out.write("---\n")
        yaml_out.write("# Ansible Vault variables for Cyber Sentinel certificates\n")
        yaml_out.write("# Generated automatically\n\n")

        for service in services:
            cert_path = os.path.join(certs_dir, f"{service}.crt")
            key_path = os.path.join(certs_dir, f"{service}.key")

            # Process Certificate
            if os.path.exists(cert_path):
                with open(cert_path, "r") as f:
                    cert_content = f.read().strip()

                # Indent content for YAML multiline block (2 spaces)
                indented_cert = cert_content.replace("\n", "\n  ")
                yaml_out.write(f"vault_{service}_cert: |\n  {indented_cert}\n\n")

            # Process Private Key
            if os.path.exists(key_path):
                with open(key_path, "r") as f:
                    key_content = f.read().strip()

                # Indent content for YAML multiline block (2 spaces)
                indented_key = key_content.replace("\n", "\n  ")
                yaml_out.write(f"vault_{service}_key: |\n  {indented_key}\n\n")

    print(f"Success: Created {output_file} with {len(services)} services.")

if __name__ == "__main__":
    # Settings for your project
    CERTS_FOLDER = "./certs"
    OUTPUT_YAML = "group_vars/all/vault_certs.yml"

    # Create directory if it's missing (e.g. group_vars/all/)
    os.makedirs(os.path.dirname(OUTPUT_YAML), exist_ok=True)

    generate_ansible_vault_yaml(CERTS_FOLDER, OUTPUT_YAML)
import os
import secrets

def generate_webui_secret_key(key_bytes: int, var_name: str, output_file: str):
    """
    Generates a cryptographically secure random secret and writes it as
    an Ansible Vault-ready YAML variable.

    Unlike cert_converter.py, this is not a cert/key pair for TLS —
    it's the WEBUI_SECRET_KEY consumed directly by the open-webui
    application to sign session cookies/tokens. A fixed value keeps
    sessions valid across container restarts.
    """
    secret_value = secrets.token_hex(key_bytes)

    with open(output_file, "w") as yaml_out:
        yaml_out.write("---\n")
        yaml_out.write("# Ansible Vault variable for open-webui session signing\n")
        yaml_out.write("# Generated automatically\n\n")
        yaml_out.write(f'{var_name}: "{secret_value}"\n')

    print(f"Success: Created {output_file}")
    print(f"  {var_name} ({key_bytes} bytes / {key_bytes * 2} hex chars)")

if __name__ == "__main__":
    # Settings for your project
    KEY_BYTES = 32                                    # 32 bytes = 64 hex chars, matches `openssl rand -hex 32`
    VAR_NAME = "vault_webui_secret_key"
    OUTPUT_YAML = "group_vars/all/vault_webui_secret.yml"

    # Create directory if it's missing (e.g. group_vars/all/)
    os.makedirs(os.path.dirname(OUTPUT_YAML), exist_ok=True)

    generate_webui_secret_key(KEY_BYTES, VAR_NAME, OUTPUT_YAML)

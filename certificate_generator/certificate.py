import datetime
import os
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_self_signed_cert(service_name: str, domain_suffix: str, output_path: str):
    """
    Generates a self-signed certificate for a specific service.
    """
    # Create directory if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # 1. Private Key Generation
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # 2. Subject/Issuer Details (CyberSentinel Branding)
    common_name = f"{service_name}.{domain_suffix}"
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "PL"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Masovia"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Warsaw"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "CyberSentinel"),
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
    ])

    # 3. Certificate Builder (365 days validity)
    now = datetime.datetime.now(datetime.UTC)
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        now
    ).not_valid_after(
        now + datetime.timedelta(days=365)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(common_name)]),
        critical=False,
    ).sign(private_key, hashes.SHA256())

    # 4. Save Private Key
    with open(f"{output_path}/{service_name}.key", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ))

    # 5. Save Certificate
    with open(f"{output_path}/{service_name}.crt", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

    print(f"[OK] Generated: {common_name}")

if __name__ == "__main__":
    # Your services list from Ansible vars
    services = [
        {"name": "open_webui", "port": 8080, "internal_host": "open-webui"}
    ]

    # Configuration for the run
    DOMAIN_SUFFIX = "local"
    OUTPUT_DIR = "./certs"

    print(f"Starting certificate generation for {len(services)} services...")

    # Iterate through services just like Ansible's loop
    for service in services:
        # We use service['name'] for filename and CN
        generate_self_signed_cert(
            service_name=service['name'],
            domain_suffix=DOMAIN_SUFFIX,
            output_path=OUTPUT_DIR
        )

    print("\nAll certificates are ready in the './certs' directory.")
import datetime
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_self_signed_cert(service_name: str, domain_suffix: str, output_path: str):
    """
    Generate self-signed certificates using Python 3.12+ timezone-aware datetimes.
    """
    # 1. Generate Private Key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # 2. Define Subject/Issuer
    common_name = f"{service_name}.{domain_suffix}"
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "PL"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Masovia"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Warsaw"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "CyberSentinel"),
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
    ])

    # 3. Create Certificate with modern UTC handling
    # We use datetime.now(datetime.UTC) to avoid DeprecationWarning
    now = datetime.datetime.now(datetime.UTC)
    expiry = now + datetime.timedelta(days=365)

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
        expiry
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(common_name)]),
        critical=False,
    ).sign(private_key, hashes.SHA256())

    # 4. Save files
    try:
        with open(f"{output_path}/{service_name}.key", "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            ))

        with open(f"{output_path}/{service_name}.crt", "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))

        print(f"Success: Certificate and Key generated for: {common_name}")
    except IOError as e:
        print(f"Error writing files: {e}")

if __name__ == "__main__":
    # Test for your n8n-server
    generate_self_signed_cert(
        service_name="n8n-server",
        domain_suffix="local",
        output_path="."
    )
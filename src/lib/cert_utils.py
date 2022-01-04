from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
import hashlib
import base64
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from typing import Optional

def generate_hpkp_from_pem_certificate(pem_cert: str) -> Optional[str]:
    # Take the certificate and convert it to a X.509 certificate
    cert = x509.load_pem_x509_certificate(pem_cert.encode("utf-8"), default_backend())

    # Get the pin type (e.g. SHA-1, SHA-256)
    encryption = cert.signature_hash_algorithm.name

    # Retrieve the SPKI Fingerprint i.e. get the DER-encoded ASN.1 representation of the Subject Public Key Info (SPKI)
    cert_subject_public_key_info = cert.public_key().public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo)

    # Hash the representation using a cryptographic hash (in this case SHA-1 or SHA-256)
    encryption_formatted = encryption.replace("-", "").lower()
    if encryption_formatted == "sha256":
        m = hashlib.sha256()
        prefix = "sha256/"
    elif encryption_formatted == "sha1":
        m = hashlib.sha1()
        prefix = "sha1/"
    else:
        raise Exception("Invalid path")

    # Base64-encode the SPKI Fingerprint
    if prefix and m:
        m.update(cert_subject_public_key_info)
        digest = m.digest()  # SPKI Fingerprint
        digest_base64 = base64.b64encode(digest)
        digest_str = digest_base64.decode("utf-8")

        return digest_str

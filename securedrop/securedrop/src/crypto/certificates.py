import os
from Crypto.PublicKey import RSA

# Pycryptodome sources
# https://www.pycryptodome.org/src/public_key/rsa
# https://www.pycryptodome.org/src/public_key/rsa#Crypto.PublicKey.RSA.RsaKey.export_key

class CertificateManager:
    def __init__(self, certs_dir="certs"):
        self.certs_dir = certs_dir
        os.makedirs(certs_dir, exist_ok=True)
    
    def generate_user_certificate(self, email, client_id):
        """Generate RSA Key Pair"""
        print(f"[CRYPTOGRAPHY] Generating 2048-bit RSA keys for {email}...")

        # Generate private key, basic following ref
        key = RSA.generate(2048)

        # Generate public key, easy :)
        public_key = key.publickey()
        
        # Cleans email file pem
        clean_email = email.replace('@', '_').replace('.', '_')
        
        # Save private key
        priv_path = os.path.join(self.certs_dir, f"{clean_email}_private.pem")
        with open(priv_path, "wb") as f:
            f.write(key.export_key(format='PEM'))

        # Save public key
        pub_path = os.path.join(self.certs_dir, f"{clean_email}_public.pem")
        with open(pub_path, "wb") as f:
            f.write(public_key.export_key(format='PEM'))
            
        return pub_path, priv_path

    def get_private_key_path(self, email):
        clean_email = email.replace('@', '_').replace('.', '_')
        return os.path.join(self.certs_dir, f"{clean_email}_private.pem")

    def get_public_key_path(self, email):
        clean_email = email.replace('@', '_').replace('.', '_')
        return os.path.join(self.certs_dir, f"{clean_email}_public.pem")
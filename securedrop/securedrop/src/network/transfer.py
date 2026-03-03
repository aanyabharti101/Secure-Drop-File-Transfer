import socket
import threading
import os
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from crypto.certificates import CertificateManager
# Sources:
# https://www.pycryptodome.org/src/cipher/aes
# https://www.pycryptodome.org/src/cipher/oaep
# https://www.pycryptodome.org/src/examples#encrypt-data-with-rsa

# Certs subfolder will be generated when running.
# File transfer class
class FileTransferManager:
    def __init__(self, client_id, user_email, listen_port):
        self.client_id = client_id
        self.user_email = user_email
        self.port = listen_port 
        self.cert_manager = CertificateManager()
        self.running = True
    # Private key loaded
    def _load_private_key(self):
        path = self.cert_manager.get_private_key_path(self.user_email)
        with open(path, "rb") as key_file:
            return RSA.import_key(key_file.read())
    # Checks for key
    def _load_recipient_public_key(self, recipient_email):
        path = self.cert_manager.get_public_key_path(recipient_email)
        if not os.path.exists(path):
            print(f"[ERROR] No public key found for {recipient_email}")
            return None
        with open(path, "rb") as key_file:
            return RSA.import_key(key_file.read())
        
    # Force exact bytes for sha256
    def _recv_all(self, sock, n):
        data = b''
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

    # Receiver starts here
    def start_receiver(self):
        def handle(conn):
            try:
                # Read starts
                mode = self._recv_all(conn, 9)
                if not mode or mode.decode().strip() != "SEND_FILE":
                    return

                # Reads header metadata
                header_data = self._recv_all(conn, 4096)
                if not header_data:
                    return

                metadata = json.loads(header_data.decode().strip())
                filename = metadata['filename']
                print(f"\n[RECEIVING] Incoming secure file from {metadata['sender']}...")
                
                # Decrypt session key rsa
                enc_session_key = bytes.fromhex(metadata['key'])
                private_key = self._load_private_key()
                cipher_rsa = PKCS1_OAEP.new(private_key)
                session_key = cipher_rsa.decrypt(enc_session_key)

                # Decrypt file aes
                iv = bytes.fromhex(metadata['iv'])
                cipher_aes = AES.new(session_key, AES.MODE_CFB, iv=iv)
                # makes download subfolder to save files
                os.makedirs("downloads", exist_ok=True)
                save_path = os.path.join("downloads", f"received_{filename}")

                with open(save_path, "wb") as f:
                    while True:
                        data = conn.recv(1024)
                        if not data: break 
                        decrypted_chunk = cipher_aes.decrypt(data)
                        f.write(decrypted_chunk)

                print(f"[DONE] File saved: {save_path}")
                print("secure_drop> ", end="", flush=True)

            except Exception as e:
                print(f"[ERROR] Transfer failed: {e}")
            finally:
                conn.close()
        # Server listening
        def server():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                try:
                    s.bind(('', self.port))
                    s.listen()
                    while self.running:
                        try:
                            conn, _ = s.accept()
                            threading.Thread(target=handle, args=(conn,), daemon=True).start()
                        except: break
                except Exception as e:
                    print(f"[SERVER ERROR] {e}")

        threading.Thread(target=server, daemon=True).start()

    # Sender starts
    def send_file(self, target_ip, target_port, target_email, filepath):
        if not os.path.exists(filepath):
            print("[ERROR] File not found.")
            return

        try:
            # Create session key aes
            session_key = get_random_bytes(32) # 256-bit AES key
            
            # Encrypt session key rsa
            recipient_key = self._load_recipient_public_key(target_email)
            if not recipient_key: return

            cipher_rsa = PKCS1_OAEP.new(recipient_key)
            enc_session_key = cipher_rsa.encrypt(session_key)

            print(f"[CONNECTING] Connecting to {target_ip}:{target_port}...")
            with socket.create_connection((target_ip, target_port), timeout=5) as s:
                # Send mode
                s.sendall(b"SEND_FILE")

                # Send metadata
                cipher_aes = AES.new(session_key, AES.MODE_CFB)
                iv = cipher_aes.iv
                
                metadata = {
                    'filename': os.path.basename(filepath),
                    'sender': self.user_email,
                    'iv': iv.hex(),
                    'key': enc_session_key.hex()
                }
                s.sendall(json.dumps(metadata).encode().ljust(4096))

                # Encrypt and send
                with open(filepath, "rb") as f:
                    while True:
                        chunk = f.read(1024)
                        if not chunk: break
                        encrypted_chunk = cipher_aes.encrypt(chunk)
                        s.sendall(encrypted_chunk)
                
            print(f"[SENT] File sent successfully.")

        except Exception as e:
            print(f"[FAILED] {e}")
import socket
import threading
import time
import json
import base64
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from crypto.certificates import CertificateManager
# Sourced from:
# https://www.pycryptodome.org/src/signature/pkcs1_15
# https://www.pycryptodome.org/src/hash/sha256
# https://docs.python.org/3/library/socket.html

# Network manager
class NetworkManager:
    def __init__(self, client_id, user_email, tcp_listening_port):
        self.client_id = client_id
        self.user_email = user_email
        self.tcp_listening_port = tcp_listening_port
        self.online_contacts = {}
        self.running = False
        self.broadcast_port = 5001
        self.cert_manager = CertificateManager()
    # Signs    
    def _sign_message(self, message_bytes):
        """Sign broadcast with Private Key"""
        path = self.cert_manager.get_private_key_path(self.user_email)
        with open(path, "rb") as f:
            private_key = RSA.import_key(f.read())
            
        h = SHA256.new(message_bytes)
        signature = pkcs1_15.new(private_key).sign(h)
        return base64.b64encode(signature).decode('utf-8')

    def start_discovery(self):
        self.running = True
        threading.Thread(target=self._listen, daemon=True).start()
        threading.Thread(target=self._broadcast, daemon=True).start()
    # Broadcasts for discovery by clients
    def _broadcast(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        while self.running:
            try:
                msg = {
                    'email': self.user_email,
                    'tcp_port': self.tcp_listening_port,
                    'type': 'DISCOVERY'
                }
                msg_bytes = json.dumps(msg).encode('utf-8')
                
                packet = {
                    'payload': msg,
                    'signature': self._sign_message(msg_bytes)
                }
                # Will broadcast every 5 seconds for discovery
                sock.sendto(json.dumps(packet).encode('utf-8'), ('<broadcast>', self.broadcast_port))
                time.sleep(5)
            except:
                time.sleep(5)
    # Socket fix for using multiple ports on same systems, diff terminals.
    def _listen(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        except AttributeError:
            pass 
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', self.broadcast_port))
        
        while self.running:
            try:
                data, addr = sock.recvfrom(4096)
                packet = json.loads(data.decode())
                payload = packet['payload']
                
                if payload['email'] != self.user_email:
                    self.online_contacts[payload['email']] = {
                        'ip': addr[0],
                        'port': payload['tcp_port']
                    }
            except:
                continue
    # Searches for contacts online            
    def get_online_contacts(self, my_contacts):
        found = []
        my_emails = [c['email'] for c in my_contacts]
        for email, info in self.online_contacts.items():
            if email in my_emails:
                found.append({'email': email, 'ip': info['ip'], 'port': info['port']})
        return found
        
    def stop_discovery(self):
        self.running = False
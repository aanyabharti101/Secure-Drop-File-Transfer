from storage.data_store import DataStore
from crypto.password_hasher import PasswordHasher

# Login class
class UserLogin:
    def __init__(self, client_id="CA"):
        self.client_id = client_id
        self.data_store = DataStore(client_id)
        self.password_hasher = PasswordHasher()
    
    def authenticate(self, email, password):
        """Verify user credentials"""
        users = self.data_store.load_all_users()
        
        # Check if user exists on this client
        if email not in users:
            return None
        
        user_data = users[email]
        
        # Get stored hash and salt
        stored_hash = bytes.fromhex(user_data['password_hash'])
        salt = bytes.fromhex(user_data['salt'])
        
        # Verify password
        if self.password_hasher.verify_password(password, stored_hash, salt):
            return user_data
        else:
            return None
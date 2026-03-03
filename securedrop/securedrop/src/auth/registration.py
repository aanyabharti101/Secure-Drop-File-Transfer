from storage.data_store import DataStore
from crypto.password_hasher import PasswordHasher
from crypto.certificates import CertificateManager
import getpass

# Registration class
class UserRegistration:
    def __init__(self, client_id="CA"):
        self.client_id = client_id
        self.data_store = DataStore(client_id)
        self.password_hasher = PasswordHasher()
        self.cert_manager = CertificateManager()
    
    # Check formatting
    def is_valid_email(self, email):
        """Check if email has proper format"""
        if '@' not in email:
            return False
        parts = email.split('@')
        if len(parts) != 2:
            return False
        if '.' not in parts[1]:
            return False
        return True
    
    def register_user(self):
        """Register a new user with secure password storage"""
        print("\n=== User Registration ===")
        
        # Get user information
        full_name = input("Enter Full Name: ").strip()
        email = input("Enter Email Address: ").strip()
        
        # Validate email format
        if not self.is_valid_email(email):
            print("Invalid email format.")
            return None
        
        # Check if user already exists
        existing_users = self.data_store.load_all_users()
        if email in existing_users:
            print("User already exists.")
            return None
        
        # Get password with asterisks
        password = getpass.getpass("Enter Password: ")
        confirm_password = getpass.getpass("Re-enter Password: ")
        
        # Validate passwords
        if password != confirm_password:
            print("Passwords do not match.")
            return None
            
        if len(password) < 8:
            print("Password must be at least 8 characters.")
            return None
        
        # Hash password securely
        password_hash, salt = self.password_hasher.hash_password(password)
        
        # Generate certificate for mutual authentication (for future milestones)
        cert_path = self.cert_manager.generate_user_certificate(email, self.client_id)
        
        # Create user data
        user_data = {
            'full_name': full_name,
            'email': email,
            'password_hash': password_hash.hex(),
            'salt': salt.hex(),
            'client_id': self.client_id,
            'certificate': cert_path,
            'contacts': [],  # Empty contacts list
        }
        
        # Save user
        if self.data_store.save_user(user_data):
            print("Passwords Match.")
            print("User Registered.")
            return user_data
        
        return None
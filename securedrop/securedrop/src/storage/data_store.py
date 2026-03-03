import json
import os
# Data storage
class DataStore:
    def __init__(self, client_id="CA"):
        self.client_id = client_id
        self.data_dir = f"data/{client_id}"
        self.users_file = f"{self.data_dir}/users.json"
        
        # Create data directory
        os.makedirs(self.data_dir, exist_ok=True)
    
    def save_user(self, user_data):
        """Save user data to JSON file"""
        all_users = self.load_all_users()
        
        # Add new user
        email = user_data['email']
        all_users[email] = user_data
        
        # Save to file
        with open(self.users_file, 'w') as f:
            json.dump(all_users, f, indent=2)
        
        print(f"\n✓ User data saved to: {self.users_file}")
        
        # Print contents as required in tests
        print("\n=== Contents of registration file ===")
        print(json.dumps(all_users, indent=2))
        
        # Print generated files
        self.print_generated_files()
        
        return True
    
    def print_generated_files(self):
        """Print list of files generated on this client"""
        print("\n=== Files generated on client ===")
        for root, dirs, files in os.walk(self.data_dir):
            for file in files:
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, ".")
                print(f"  - {rel_path}")
    
    def load_all_users(self):
        """Load all users from file"""
        if not os.path.exists(self.users_file):
            return {}
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def update_user(self, email, user_data):
        """Update user data"""
        all_users = self.load_all_users()
        if email in all_users:
            all_users[email] = user_data
            with open(self.users_file, 'w') as f:
                json.dump(all_users, f, indent=2)
            return True
        return False
    
    def get_user(self, email):
        """Get specific user data"""
        all_users = self.load_all_users()
        return all_users.get(email)
    
    def get_all_users(self):
        """Get all users"""
        return self.load_all_users()
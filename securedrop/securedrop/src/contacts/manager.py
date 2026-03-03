from storage.data_store import DataStore
import json

# Manager class
class ContactManager:
    def __init__(self, user_email, client_id):
        self.user_email = user_email
        self.client_id = client_id
        self.data_store = DataStore(client_id)
    
    # Contact add
    def add_contact_interactive(self):
        """Add a contact interactively"""
        print("\n=== Add Contact ===")
        full_name = input("Enter Full Name: ").strip()
        email = input("Enter Email Address: ").strip()
        
        if self.add_contact(full_name, email):
            print("Contact Added.")
        else:
            print("Failed to add contact.")
    
    def add_contact(self, full_name, email):
        """Add a contact to user's contact list"""
        # Get current user data
        user_data = self.data_store.get_user(self.user_email)
        if not user_data:
            return False
        
        # Create contact entry
        contact = {
            'full_name': full_name,
            'email': email
        }
        
        # Get current contacts
        contacts = user_data.get('contacts', [])
        
        # Check if contact already exists
        for i, existing_contact in enumerate(contacts):
            if existing_contact['email'] == email:
                # Update existing contact
                contacts[i] = contact
                user_data['contacts'] = contacts
                return self.data_store.update_user(self.user_email, user_data)
        
        # Add new contact
        contacts.append(contact)
        user_data['contacts'] = contacts
        
        # Save updated user data
        return self.data_store.update_user(self.user_email, user_data)
    
    def get_contacts(self):
        """Get user's contact list"""
        user_data = self.data_store.get_user(self.user_email)
        if user_data:
            return user_data.get('contacts', [])
        return []
    
    def print_contacts_list(self):
        """Print contacts list for testing"""
        contacts = self.get_contacts()
        print("\n=== Contacts List ===")
        print(json.dumps(contacts, indent=2))
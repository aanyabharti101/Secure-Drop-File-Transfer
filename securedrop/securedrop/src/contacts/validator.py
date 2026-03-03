# Validation class, checks for emails

class ContactValidator:
    @staticmethod
    def validate_contact_email(email):
        """Validate contact email format"""
        if '@' not in email:
            return False
        parts = email.split('@')
        if len(parts) != 2:
            return False
        if '.' not in parts[1]:
            return False
        return True
    
    @staticmethod
    def is_mutual_contact(user_contacts, contact_email, contact_contacts):
        """Check if contact relationship is mutual"""
        # Check if contact_email is in user's contacts
        user_has_contact = any(c['email'] == contact_email for c in user_contacts)
        
        # Check if user_email is in contact's contacts
        return user_has_contact
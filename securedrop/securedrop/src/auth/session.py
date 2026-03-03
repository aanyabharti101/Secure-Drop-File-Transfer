# Session class

class UserSession:
    def __init__(self, user_data):
        self.user_data = user_data
        self.logged_in = True
    
    def get_user_email(self):
        return self.user_data['email']
    
    def get_user_name(self):
        return self.user_data['full_name']
    
    def is_active(self):
        return self.logged_in
    
    def logout(self):
        self.logged_in = False
        # Clear sensitive data from memory
        self.user_data = {}
#!/usr/bin/env python3
import zlib
import sys
import os
import json
from getpass import getpass
from auth.registration import UserRegistration
from auth.login import UserLogin
from auth.session import UserSession
from storage.data_store import DataStore
from contacts.manager import ContactManager
from network.discovery import NetworkManager
from network.transfer import FileTransferManager

# Certs, data, downloads folders are generated when running through scenarios.

def get_client_id():
    if len(sys.argv) > 1: return sys.argv[1]
    return "CA"

def start_secure_shell(user_data, client_id):
    session = UserSession(user_data)
    contact_manager = ContactManager(user_data['email'], client_id)
    
    # Generates unique number from client_id string.
    # Safe range between 5000 and 7000.
    my_tcp_port = 5000 + (zlib.crc32(client_id.encode()) % 2000)
    
    # Init managers, manages network and file transfer. Passes tcp.
    net_manager = NetworkManager(client_id, user_data['email'], my_tcp_port)
    trans_manager = FileTransferManager(client_id, user_data['email'], my_tcp_port)
    
    # Background thread for discovery usage and sending. 
    net_manager.start_discovery()
    trans_manager.start_receiver()
    # Info for user
    print(f"\nWelcome to SecureDrop, {user_data['full_name']}!")
    print(f"Listening on Port {my_tcp_port}")
    print('Type "help" For Commands.')
    
    while session.is_active():
        try:
            cmd = input("secure_drop> ").strip().lower()
            
            if cmd == "help":
                print('"add"  -> Add a new contact')
                print('"list" -> List all online contacts')
                print('"contacts" -> Show all saved contacts (Milestone 3)') # Added for clarity in M3
                print('"send" -> Transfer file to contact')
                print('"exit" -> Exit SecureDrop')
            
            elif cmd == "add":
                contact_manager.add_contact_interactive()

            # Contact json dump for milestone 3, wanted clarity on scenarios.
            elif cmd == "contacts":
                print("\nSaved Contacts (Database Contents)")
                all_contacts = contact_manager.get_contacts()
                if all_contacts:
                    print(json.dumps(all_contacts, indent=4))
                else:
                    print("No contacts found.")
            # Lists ONLINE contacts
            elif cmd == "list":
                online = net_manager.get_online_contacts(contact_manager.get_contacts())
                if online:
                    print("\nThe following contacts are online:")
                    for c in online: 
                        print(f"* {c['email']}")
                else:
                    print("\nNo contacts are currently online.")
            # Starts sending process
            elif cmd == "send":
                target_email = input("Enter receiver email: ").strip()
                filename = input("Enter filename to send: ").strip()
                
                if not os.path.exists(filename):
                    print("[ERROR] File not found.")
                    continue
                
                # Look for the user's port or ip with discovery
                online = net_manager.get_online_contacts(contact_manager.get_contacts())
                target = next((c for c in online if c['email'] == target_email), None)
                
                if target:
                    trans_manager.send_file(target['ip'], target['port'], target_email, filename)
                else:
                    print(f"[ERROR] User {target_email} is not available or not in your contacts.")
            # exit threads to prevent port issues
            elif cmd == "exit":
                net_manager.stop_discovery()
                trans_manager.running = False
                session.logout()
                return
                
        except KeyboardInterrupt:
            print("\nExiting...")
            net_manager.stop_discovery()
            session.logout()
            return

def main():
    client_id = get_client_id()
    print(f"=== SecureDrop (Client {client_id}) ===")
    
    data_store = DataStore(client_id)
    users = data_store.load_all_users()
    # Start process
    if not users:
        print("\nNo users are registered with this client.")
        response = input("Do you want to register a new user (y/n)? ").lower()
        if response == 'y':
            registrar = UserRegistration(client_id)
            if registrar.register_user():
                print("\nUser Registered. Please restart to login.")
        else:
            print("\nExiting.")
    else:
        login = UserLogin(client_id)
        attempts = 0
        while attempts < 3:
            print()
            email = input("Enter Email Address: ").strip()
            password = getpass("Enter Password: ")
            user_data = login.authenticate(email, password)
            if user_data:
                start_secure_shell(user_data, client_id)
                return
            else:
                print("\nEmail and Password Combination Invalid.")
                attempts += 1
        print("\nToo many failed attempts.")

if __name__ == "__main__":
    main()
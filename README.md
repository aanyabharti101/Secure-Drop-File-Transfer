# SecureDrop - Secure File Transfer System

A Python-based secure file transfer application inspired by AirDrop, designed for encrypted peer-to-peer file sharing within a local network. The project includes user authentication, contact management, network discovery, and secure file transfer functionality.

---

## Features

- User registration and login authentication
- Password-protected accounts
- Secure local-network file transfer
- Contact management system
- Online user discovery
- Interactive command-line interface
- Background network discovery threads
- TCP-based file transfer system
- Local data storage and session handling

---

## Technologies Used

- Python
- Socket Programming
- TCP Networking
- JSON Data Storage
- Multithreading
- Cryptographic Authentication Concepts
- Command-Line Interface Development

---

## System Architecture

The application is organized into modular components for authentication, networking, storage, contacts, and secure file transfer.

```text
auth/           User registration and authentication
contacts/       Contact management system
network/        Discovery and file transfer logic
storage/        Local user data handling
main.py         Application entry point
```

---

## Commands

| Command | Description |
|---|---|
| `help` | Display available commands |
| `add` | Add a new contact |
| `contacts` | View saved contacts |
| `list` | Show online contacts |
| `send` | Transfer a file |
| `exit` | Exit the application |

---

## Example Workflow

1. Register a new user account
2. Log into SecureDrop
3. Add trusted contacts
4. Detect online users on the local network
5. Select a contact and securely transfer files

---

## Security Features

- Password-based authentication
- Session management
- Secure user handling
- Peer-to-peer local network communication
- Structured contact verification workflow

---

## Running the Project

### Requirements

- Python 3
- Local network access

## Getting Started

```bash
git clone https://github.com/aanyabharti101/Secure-Drop-File-Transfer.git
cd Secure-Drop-File-Transfer
```

### Run

```bash
python3 main.py
```

---

## Future Improvements

- End-to-end encryption
- GUI implementation
- Drag-and-drop file transfer
- Cross-platform discovery improvements
- File transfer progress indicators
- Enhanced authentication security

---

## Contributors

- Aanya Bharti
- Jacob Knowlton
- Arianna Quinlan

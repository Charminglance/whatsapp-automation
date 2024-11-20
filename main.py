import time
import json
from qrcode import QRCode
from whatsapp_web import WhatsApp

# Initialize the WhatsApp client instance
whatsapp = WhatsApp()

# Function to handle the QR code generation and display
def on_qr(qr_code):
    # Generate and print the QR code for scanning
    print("Scan the QR code below with WhatsApp Web:")
    qr = QRCode()
    qr.add_data(qr_code)
    qr.print_ascii()  # Print QR in ASCII format for terminal scanning

# Function to handle successful authentication
def on_authenticated():
    print("WhatsApp Web authenticated successfully!")

# Function to send a message once authenticated
def send_message(to_number, message):
    # Send message after successful authentication
    whatsapp.send_message(to_number, message)
    print(f"Message sent to {to_number}: {message}")

# Function to save session to file (for persistence)
def save_session(session_data):
    with open("session.json", "w") as session_file:
        json.dump(session_data, session_file)
    print("Session saved to session.json.")

# Function to load the session from file (if exists)
def load_session():
    try:
        with open("session.json", "r") as session_file:
            session_data = json.load(session_file)
            return session_data
    except FileNotFoundError:
        return None

# Set up the event listener for QR code generation
whatsapp.on('qr', on_qr)

# Set up the event listener for authentication
whatsapp.on('authenticated', on_authenticated)

# Load session if available
session_data = load_session()
if session_data:
    print("Loading saved session...")
    whatsapp.load_session(session_data)

# Start the WhatsApp client (this will either authenticate or use the saved session)
whatsapp.start()

# Wait for the user to scan the QR code and authenticate (if session is not loaded)
while not whatsapp.is_authenticated:
    print("Waiting for authentication...")
    time.sleep(5)

# If authenticated, send a test message
to_number = "whatsapp:+[Your Phone Number with Country Code]"  # Replace with your number
message = "Hello from the automated WhatsApp bot!"
send_message(to_number, message)

# Save the session data for future use
save_session(whatsapp.session)

import time
import json
import qrcode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Initialize WebDriver
def initialize_driver():
    # Setup for Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=./User_Data")  # Persist session
    options.add_argument("--profile-directory=Default")  # Use default profile

    # Launch browser with WebDriver Manager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://web.whatsapp.com/")
    return driver

# Function to handle QR code generation and display
def on_qr(driver):
    # Generate the QR code for scanning
    print("Scan the QR code below with WhatsApp Web:")
    time.sleep(2)  # Allow time for QR code to be displayed
    qr_code_image = driver.find_element(By.XPATH, '//div[@data-testid="qrcode"]')
    qr_code_url = qr_code_image.screenshot_as_base64

    # Generate QR code using the qrcode library and print to terminal
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_code_url)
    qr.make(fit=True)

    # Print QR code in terminal
    qr.print_ascii()

# Function to send a message
def send_message(driver, to_number, message):
    # Find the chat input and send the message
    search_box = driver.find_element(By.XPATH, "//div[@contenteditable='true']")
    search_box.click()
    search_box.send_keys(to_number + Keys.ENTER)
    
    time.sleep(2)  # Wait for chat to open

    message_box = driver.find_element(By.XPATH, "//div[@contenteditable='true']")
    message_box.send_keys(message)
    message_box.send_keys(Keys.RETURN)
    print(f"Message sent to {to_number}: {message}")

# Function to save session to file (for persistence)
def save_session(driver):
    session_data = driver.get_cookie("sid")
    with open("session.json", "w") as session_file:
        json.dump(session_data, session_file)
    print("Session saved to session.json.")

# Function to load session from file (if available)
def load_session():
    try:
        with open("session.json", "r") as session_file:
            session_data = json.load(session_file)
            return session_data
    except FileNotFoundError:
        return None

# Start the WebDriver and wait for QR scan
driver = initialize_driver()

# Load saved session if available
session_data = load_session()
if session_data:
    print("Loading saved session...")
    driver.add_cookie(session_data)

# Display QR code for scanning
on_qr(driver)

# Wait for user authentication (QR code scan)
while True:
    if driver.current_url == "https://web.whatsapp.com/":
        print("Waiting for authentication...")
        time.sleep(5)
    else:
        break

# Once authenticated, send the message
to_number = "[Your Phone Number with Country Code]"  # Example: +1234567890
message = "Hello from the automated WhatsApp bot!"
send_message(driver, to_number, message)

# Save session after authentication
save_session(driver)

# Close the browser after sending the message
driver.quit()

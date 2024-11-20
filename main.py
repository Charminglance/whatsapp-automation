from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import time
from webdriver_manager.firefox import GeckoDriverManager

# WhatsApp Web Automation
def send_message():
    try:
        # Countdown Logic
        trip_date = datetime(2025, 5, 1)  # Set your trip date
        today = datetime.today()
        remaining_days = (trip_date - today).days
        remaining_months = remaining_days // 30

        # Message Content
        message = f"""🗿 **ഡെയിലി REMAINDER ഇടും ഇനി** 🗿\n\n🌍 Ladakh Trip Countdown ⏳\nMonths Left: **{remaining_months}**\nDays Left: **{remaining_days}**\n\n**പൈസ റെഡി ആക്കി വെച്ചോ മൈരന്മാരെ** 💸."""

        # Setup Firefox options and path
        firefox_options = Options()
        firefox_options.add_argument("--headless")  # Run in headless mode (no GUI)

        # Using webdriver-manager to get the correct geckodriver
        firefox_service = GeckoDriverManager().install()

        # Initialize the WebDriver with the Firefox service
        driver = webdriver.Firefox(executable_path=firefox_service, options=firefox_options)

        # Open WhatsApp Web
        driver.get("https://web.whatsapp.com")
        print("Please scan the QR code to log in to WhatsApp Web.")
        time.sleep(15)  # Wait for the user to scan QR code

        # Search for the Group
        group_name = "LEH 🗿"  # Your WhatsApp group's name
        search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        search_box.click()
        search_box.send_keys(group_name + Keys.ENTER)

        # Send the Message
        time.sleep(5)  # Wait for the group chat to load
        message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
        message_box.send_keys(message + Keys.ENTER)

        print(f"Message sent successfully to {group_name}!")
        driver.quit()
    except Exception as e:
        print(f"An error occurred: {e}")

# Scheduler to Run Daily
scheduler = BlockingScheduler()
scheduler.add_job(send_message, 'cron', hour=9, minute=0)  # Schedule for 9:00 AM daily

if __name__ == "__main__":
    print("Starting WhatsApp message automation...")
    send_message()  # Run once immediately for testing
    scheduler.start()

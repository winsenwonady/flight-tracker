from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os  # For environment variables

# Configure Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run without opening a browser
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=chrome_options)

# Open Kayak Tracker
driver.get("https://www.kayak.co.id/tracker")

# Select Airport
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Airport')]"))).click()
driver.find_element(By.NAME, "airport").send_keys("Makassar, South Sulawesi, Indonesia (UPG)")
WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "ap-UPG/55821"))).click()

# Select Airline
airline_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Airline (optional)']")
airline_input.send_keys("Citilink (QG)")
WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "al-QG"))).click()

# Search Flight
driver.find_element(By.ID, "airportTrackForm-submit").click()

# Wait and select the flight
flight_xpath = "//div[@data-airlinecode='QG' and @data-flightnumber='353']"
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, flight_xpath))).click()

# Get Flight Information
actual_departure_time = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[text()='Actual departure']/following-sibling::div"))
).text

estimated_arrival_time = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[text()='Estimated arrival']/following-sibling::div"))
).text

driver.quit()  # Close the browser

# Email Configuration (Using Environment Variables for Security)
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# Compose Email
subject = "Daily Flight Update: QG-353"
body = f"""
Flight QG-353 Update:

- ✈ **Actual Departure:** {actual_departure_time}
- 🕓 **Estimated Arrival:** {estimated_arrival_time}
"""

msg = MIMEMultipart()
msg["From"] = EMAIL_SENDER
msg["To"] = EMAIL_RECEIVER
msg["Subject"] = subject
msg.attach(MIMEText(body, "plain"))

# Send Email
try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
    server.quit()
    print("✅ Email Sent!")
except Exception as e:
    print("❌ Email Failed:", e)

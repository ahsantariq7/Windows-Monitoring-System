import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import socket
from datetime import datetime
import platform
import psutil
import cv2
import os
from pathlib import Path
import time
import requests

# Function to check internet connectivity using requests library
def is_internet_connected():
    try:
        # Attempt to make a simple HTTP request to a known server (Google's public DNS)
        response = requests.get("http://www.google.com", timeout=5)
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False

# Function to send an email with laptop status
def send_status_email():
    # Your email configuration
    sender_email = ""
    sender_password = " "  # Use an "App Password" if you have two-factor authentication enabled
    recipient_email = ""

    # Get laptop status information
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)
    os_info = platform.platform()
    processor = platform.processor()
    cpu_usage = psutil.cpu_percent(interval=1)
    disk_usage = psutil.disk_usage("/")
    total_disk_space = disk_usage.total / (1024 ** 3)
    used_disk_space = disk_usage.used / (1024 ** 3)
    battery_info = "Battery status: Not available"
    battery = psutil.sensors_battery()
    if battery:
        percent = battery.percent
        power_plugged = "Plugged in" if battery.power_plugged else "Unplugged"
        battery_info = f"Battery status: {percent}% ({power_plugged})"

    # Create the email message
    subject = "Laptop Status Update Code By Engr.Ahsan Tariq"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = f"Hello,\n\nI wanted to inform you that your laptop is currently powered on. Here are the details:\n\n"
    message += f"- IP Address: {ip_address}\n"
    message += f"- Current Time: {current_time}\n"
    message += f"- Operating System: {os_info}\n"
    message += f"- Processor: {processor}\n"
    message += f"- CPU Usage: {cpu_usage}%\n"
    message += f"- Disk Space: Total {total_disk_space:.2f} GB, Used {used_disk_space:.2f} GB\n"
    message += f"- {battery_info}\n\n"
    message += "It appears that your laptop is actively in use. If you have any questions or need assistance, please don't hesitate to reach out.Enj>
    message += "Best regards,\nYour Laptop Monitoring System\nEngr.Ahsan Tariq"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    # Connect to the SMTP server (Gmail) and send the email
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Email sending failed: {str(e)}")

# Function to capture and save a photo using the laptop's camera
def capture_and_save_photo():
    # Open the camera (you may need to adjust the camera index)
    cap = cv2.VideoCapture(0)

    # Capture a photo
    ret, frame = cap.read()

    # Get the user's desktop folder
    desktop_folder = "C:/Users/YourUsername/Desktop"

    # Create a subfolder named "LaptopMonitoringPhotos" if it doesn't exist
    subfolder_name = "LaptopMonitoringPhotos"
    subfolder_path = os.path.join(desktop_folder, subfolder_name)
    os.makedirs(subfolder_path, exist_ok=True)

    # Save the photo in the subfolder with date and time
    if ret:
        current_time_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        photo_filename = f"person_photo_{current_time_str}.jpg"
        photo_path = os.path.join(subfolder_path, photo_filename)
        cv2.imwrite(photo_path, frame)
        print(f"Photo captured and saved: {photo_path}")

    # Release the camera
    cap.release()


if __name__ == "__main__":
        # Capture and save photo
    capture_and_save_photo()

    # Check if an internet connection is available
    while not is_internet_connected():
        print("Waiting for internet connection...")
        time.sleep(5)  # Wait for 5 seconds before checking again
       
    print("Internet connection established. Capturing photo and sending email...")

    # Send laptop status email
    send_status_email()

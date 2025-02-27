import os
import re
import string
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from faker import Faker
usernamefile = "email_usernames.txt"
import os
import subprocess

# Run git pull to update the script
def update_script():
    try:
        result = subprocess.run(["git", "pull"], check=True, capture_output=True, text=True)
        print(result.stdout)  # Show output of git pull
        print("Repository updated successfully.")
    except subprocess.CalledProcessError as e:
        print("Failed to update repository. Make sure Git is installed and configured.")
        print(e.stderr)

# Update the script before executing anything else
#update_script()

def get_username(email):
    """Searches for the username linked to the email."""
    if os.path.exists(usernamefile):
        with open(usernamefile, "r", encoding="utf-8") as file:
            for line in file:
                saved_email, saved_username = line.strip().split("|")
                if saved_email == email:
                    return saved_username  # Return username if found
    return "Unknown"  # Return default if not found


def random_english_firstname():
    european_locales = ['fr_FR', 'de_DE', 'it_IT', 'es_ES', 'nl_NL', 'ru_RU', 'pl_PL', 'sv_SE', 'da_DK']
    fake = Faker(european_locales)
    firstname = None
    lastname = None
    while firstname is None or lastname is None:
        random_fname = fake.first_name_female()
        random_lname = fake.last_name_female()
        if re.fullmatch(r'[A-Za-z]+', random_fname):
            firstname=random_fname
        if re.fullmatch(r'[A-Za-z]+', random_lname):
            lastname=random_lname
    return firstname, lastname

def generate_random_phone_number():
    random_number = str(random.randint(1000000, 9999999))
    third = random.randint(0, 4)
    forth = random.randint(1, 7)
    phone_formats = [
        f"03{third}{forth} {random_number}",
        f"03{third}{forth}{random_number}",
        f"+92 3{third}{forth} {random_number}",
        f"+923{third}{forth}{random_number}"
    ]
    return random.choice(phone_formats)
import random


def generate_user_details():
    fn,ln=random_english_firstname()
    year = random.randint(1960, 2006)
    date = random.randint(1, 28)
    month = random.randint(1, 12)
    formatted_date = f"{date:02d}-{month:02d}-{year:04d}"
    password = generate_random_password()
    phone_number = generate_random_phone_number()
    return fn, ln, date,year,month, phone_number, password

def generate_random_password():
    length = random.randint(10, 16)
    all_characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(all_characters) for _ in range(length))
    return password
import random
from datetime import datetime

def generate_old_android_ua():
    # Seed random with current time for variation
    random.seed(datetime.now().timestamp())
    
    # Components
    android_versions = [
        ("4.0.3", "2011"),
        ("4.0.4", "2012"),
        ("4.1.1", "JRO03"),
        ("4.1.2", "JZO54"),
        ("4.2.1", "JOP40"),
        ("4.2.2", "JDQ39"),
        ("4.3", "JSS15"),
        ("4.4.2", "KOT49"),
        ("4.4.3", "KTU84"),
        ("4.4.4", "KTU84Q")
    ]
    
    devices = [
        ("Galaxy Nexus", "Samsung"),
        ("Nexus S", "Samsung"),
        ("Xperia Z", "Sony"),
        ("Xperia SP", "Sony"),
        ("One M7", "HTC"),
        ("One M8", "HTC"),
        ("Optimus G", "LG"),
        ("G2", "LG"),
        ("Moto X", "Motorola"),
        ("DROID RAZR", "Motorola")
    ]

 
    android_ver, android_code = random.choice(android_versions)
    device, manufacturer = random.choice(devices)
    
    # Build number generation
    build_number = f"{android_code}"
    if android_ver.startswith("4.0"):
        build_number += f".{random.choice(['IMM76', 'GRK39', 'IMM76D'])}"
    else:
        build_number += random.choice(["D", "E", "F"]) + str(random.randint(10,99))
    
    # Chrome version correlation
    chrome_major = random.randint(
        18 if android_ver.startswith("4.0") else 25,
        35 if android_ver.startswith("4.4") else 32
    )
    chrome_build = random.randint(1000, 1999)
    chrome_patch = random.randint(50, 199)
    
    # WebKit version logic
    webkit_base = "534.30" if chrome_major < 25 else "537.36"
    webkit_ver = f"{webkit_base}.{random.randint(1, 99)}" if random.random() > 0.7 else webkit_base
    
    return (
        f"Mozilla/5.0 (Linux; Android {android_ver}; {device} Build/{build_number}) "
        f"AppleWebKit/{webkit_ver} (KHTML, like Gecko) "
        f"Chrome/{chrome_major}.0.{chrome_build}.{chrome_patch} Mobile Safari/{webkit_ver.split('.')[0]}.0"
    )

from selenium.common.exceptions import NoSuchElementException
def create_33mail(driver,usern):
    asdf = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    ua = generate_old_android_ua()
    fn, ln, date, year, month, phone_number, password = generate_user_details()
    username=fn+ln+asdf
    url = "https://m.facebook.com/reg/?is_two_steps_login=0&cid=103&refsrc=deprecated&soft=hjk"

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "dpr": "1",
        "priority": "u=0, i",
        "sec-ch-prefers-color-scheme": "dark",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": f"{ua}",
        "viewport-width": "720"
    }
    
    session = requests.Session()
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    form = soup.find("form")
    if form:
        action_url = requests.compat.urljoin(url, form["action"]) if form.has_attr("action") else url
        inputs = form.find_all("input")
        data = {
            "firstname": f"{fn}",
            "lastname": f"{ln}",
            "birthday_day": f"{date}",
            "birthday_month": f"{month}",
            "birthday_year": f"{year}",
            "reg_email__": f"{phone_number}",
            "sex": "2",
            "encpass": f"{password}",
            "submit": "Sign Up"
        }
        for inp in inputs:
            if inp.has_attr("name") and inp["name"] not in data:
                data[inp["name"]] = inp["value"] if inp.has_attr("value") else ""

        submit_response = session.post(action_url, headers=headers, data=data)
        if "c_user" in session.cookies:
            uid = session.cookies.get("c_user")
            
        else:
            pass
            return
    else:
        pass
    
    change_email_url = "https://m.facebook.com/changeemail/"
    email_response = session.get(change_email_url, headers=headers)
    
    soup = BeautifulSoup(email_response.text, "html.parser")
    form = soup.find("form")
    
    if form:

        action_url = requests.compat.urljoin(change_email_url, form["action"]) if form.has_attr("action") else change_email_url
        inputs = form.find_all("input")
        data = {}
        for inp in inputs:
            if inp.has_attr("name") and inp["name"] not in data:
                data[inp["name"]] = inp["value"] if inp.has_attr("value") else ""
        data["new"] = f"{username}@{usern}.protonsemail.com"
        data["submit"] = "Add"
        
        submit_response = session.post(action_url, headers=headers, data=data)
        print(usern)
        driver.implicitly_wait(10)
        for i in range(15):
            if i==12:
                return
            try:
                random_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + ".png"
                screenshot_path = f"/storage/emulated/0/{random_filename}"  # Save in SD card root
                driver.save_screenshot(screenshot_path)


                driver.find_element(By.XPATH, '//a[@title="Inbox"]').click()
                code_text = driver.find_element(By.XPATH, '//span[contains(text(),"code")]')
                code_string = code_text.text
                clean_code = re.search(r'\d+', code_string).group()
                break 
            except:
                continue
        otp =clean_code
        driver.find_element(By.XPATH,'//input[@id="idSelectAll"]')
        driver.implicitly_wait(3)
        try:
            # Check if the message container exists
            MESSAGES = driver.find_element(By.XPATH, '//div[@class="item-container-wrapper relative"]')
            if MESSAGES:
                try:
                    # Check if the "Select All" checkbox exists and click it
                    select_all_checkbox = driver.find_element(By.XPATH, '//input[@id="idSelectAll"]')
                    select_all_checkbox.click()
                except NoSuchElementException:
                    pass
                time.sleep(3)
                try:
                    # Check if the button exists and click it
                    button = driver.find_element(By.XPATH, '//button[@data-testid="toolbar:movetotrash"]')
                    button.click()
                except NoSuchElementException:
                    pass
        except NoSuchElementException:
            pass
        print(f"{uid}|{password}")
        email=f"{username}@{usern}.protonsemail.com"
        storage_dir = "/sdcard"  # Use "/data/data/com.termux/files/home/" for internal storage
        file_path = os.path.join(storage_dir, "unconfirmed_accounts.txt")

        if not os.path.exists(file_path):
            open(file_path, "w").close()

        
        credentials = f"{uid}|{password}|{otp}|{email}\n"

        # Append to the file
        with open(file_path, "a") as file:
            file.write(credentials)

    else:
        pass
    
    return
CREDENTIALS_FILE = os.path.expanduser("~/credentials.txt")  # Store in $HOME

def save_credentials(email, password):
    """Saves email and password to a file."""
    with open(CREDENTIALS_FILE, "w", encoding="utf-8") as file:
        file.write(f"{email}\n{password}")

def load_credentials():
    """Loads saved credentials if they exist."""
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r", encoding="utf-8") as file:
            lines = file.readlines()
            if len(lines) == 2:
                return lines[0].strip(), lines[1].strip()
    return None, None

def get_credentials():
    """Handle credential input or retrieval from file."""
    email_address, password_email = load_credentials()

    if email_address and password_email:
        print(f"Saved ProtonMail: {email_address}")
        choice = input("Do you want to use saved credentials? (yes/no): ").strip().lower()

        if choice == "no":
            print("Deleting old credentials...")
            os.remove(CREDENTIALS_FILE)  # Remove old credentials
            email_address = input("Enter your ProtonMail email: ")
            password_email = input("Enter your ProtonMail password: ")
            save_credentials(email_address, password_email)
            print("New credentials saved successfully!")
    else:
        email_address = input("Enter your ProtonMail email: ")
        password_email = input("Enter your ProtonMail password: ")
        save_credentials(email_address, password_email)
        print("Credentials saved successfully!")

    return email_address, password_email

def login_and_process(driver,email_address, password_email):
    """Login to ProtonMail and process emails."""

    driver.get("https://account.proton.me/login")
    driver.implicitly_wait(80)

    # Fill in login credentials
    username_field = driver.find_element(By.XPATH, '//input[@id="username"]')
    username_field.send_keys(email_address)
    
    password_field = driver.find_element(By.XPATH, '//input[@id="password"]')
    password_field.send_keys(password_email)
    
    time.sleep(1)
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(12)

    # Navigate to inbox
    driver.get("https://mail.proton.me/u/6/inbox")

    try:
        driver.find_element(By.XPATH, '//input[@id="idSelectAll"]')
        driver.implicitly_wait(7)

        # Check if the message container exists
        messages = driver.find_element(By.XPATH, '//div[@class="item-container-wrapper relative"]')
        if messages:
            try:
                # Click "Select All" checkbox
                select_all_checkbox = driver.find_element(By.XPATH, '//input[@id="idSelectAll"]')
                select_all_checkbox.click()
            except NoSuchElementException:
                pass
                time.sleep(3)

            try:
                # Click "Move to Trash" button
                button = driver.find_element(By.XPATH, '//button[@data-testid="toolbar:movetotrash"]')
                button.click()
            except NoSuchElementException:
                pass
    except NoSuchElementException:
        pass
if __name__ == "__main__":
    try:

        email_address, password_email = get_credentials()
        print(email_address)
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless=new")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-blink-features=AutomationControlled")

        driver = webdriver.Chrome(options=options)
        login_and_process(driver, email_address, password_email)

        while True:
            try:
                max_create = int(input("How many 33mail addresses do you want to create? (Max: 10, Enter 0 to exit): "))
                if max_create == 0:
                    print("Exiting...")
                    break
                elif 1 <= max_create <= 10:
                    for i in range(max_create):
                        usern = get_username(email_address)
                        print(usern)
                        create_33mail(driver, usern)
                else:
                    print("Invalid input. Please enter a number between 1 and 10.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
    except:
        if driver:
            driver.quit()
    finally:
        if driver:
            driver.quit()
        exit()

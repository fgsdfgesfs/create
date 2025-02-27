from datetime import datetime
import os
import random
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
        print("[*] Checking for updates...", end='\r')
        result = subprocess.run(["git", "pull"], check=True, capture_output=True, text=True)
        print("[+] Repository updated successfully: " + result.stdout.replace('\n', ' '))
    except subprocess.CalledProcessError as e:
        print("[-] Failed to update repository: " + e.stderr.replace('\n', ' '))

# Update the script before executing anything else
update_script()

def get_username(email):
    """Searches for the username linked to the email."""
    print(f"[*] Looking up username for {email}...", end='\r')
    if os.path.exists(usernamefile):
        with open(usernamefile, "r", encoding="utf-8") as file:
            for line in file:
                saved_email, saved_username = line.strip().split("|")
                if saved_email == email:
                    print(f"[+] Found username: {saved_username}          ")
                    return saved_username
    print("[-] Username not found, using default          ")
    return "Unknown"
CREDENTIALS_FILE = os.path.expanduser("~/credentials.txt")

def save_credentials(email, password):
    """Saves email and password to a file."""
    print("[*] Saving credentials...", end='\r')
    with open(CREDENTIALS_FILE, "w", encoding="utf-8") as file:
        file.write(f"{email}\n{password}")
    print("[+] Credentials saved successfully          ")

def load_credentials():
    """Loads saved credentials if they exist."""
    print("[*] Checking for saved credentials...", end='\r')
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r", encoding="utf-8") as file:
            lines = file.readlines()
            if len(lines) == 2:
                print("[+] Found saved credentials          ")
                return lines[0].strip(), lines[1].strip()
    print("[-] No saved credentials found          ")
    return None, None

def get_credentials():
    """Handle credential input or retrieval from file."""
    email_address, password_email = load_credentials()

    if email_address and password_email:
        print(f"[+] Loaded ProtonMail: {email_address}")
        choice = input("[?] Use saved credentials? (yes/no): ").strip().lower()

        if choice == "no":
            print("[*] Deleting old credentials...", end='\r')
            os.remove(CREDENTIALS_FILE)
            email_address = input("[?] Enter ProtonMail email: ")
            password_email = input("[?] Enter ProtonMail password: ")
            save_credentials(email_address, password_email)
    else:
        email_address = input("[?] Enter ProtonMail email: ")
        password_email = input("[?] Enter ProtonMail password: ")
        save_credentials(email_address, password_email)

    return email_address, password_email
import time
import re
import requests

EMAIL, PASSWORD = get_credentials()


BASE_URL = "https://api.mail.gw"
def get_token():
    print("[*] Authenticating with mail server...", end='\r')
    response = requests.post(f"{BASE_URL}/token", json={"address": EMAIL, "password": PASSWORD})
    if response.status_code == 200:
        print("[+] Authentication successful          ")
        return response.json().get("token")
    print("[-] Authentication failed          ")
    return None

def get_latest_email(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/messages", headers=headers)
    if response.status_code == 200:
        messages = response.json().get("hydra:member", [])
        return messages[0] if messages else None
    return None

def get_email_content(token, email_id):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/messages/{email_id}", headers=headers)
    if response.status_code == 200:
        return response.json().get("text")
    return None

def delete_email(token, email_id):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{BASE_URL}/messages/{email_id}", headers=headers)
    if response.status_code == 204:
        print(f"🗑️ Email {email_id} deleted successfully.")
        return True
    else:
        print(f"[-] Failed to delete email {email_id}: {response.text}")
        return False

def extract_code(text):
    pattern = r'\b(?:FB-)?(\d{4,6})\b'  # Match 4-6 digit codes with or without "FB-"
    matches = re.findall(pattern, text)
    return matches[-1] if matches else None  # Return the last valid match

def wait_for_email(timeout=120):
    token = get_token()
    if not token:
        return None

    deleted_emails = set()  # Track deleted emails
    start_time = time.time()
    check_count = 0

    while time.time() - start_time < timeout:
        check_count += 1
        print(f"[*] Checking for emails ({check_count})...", end='\r')
        email = get_latest_email(token)
        
        if email and email["id"] not in deleted_emails:
            print(f"[+] New email received (ID: {email['id']})          ")
            content = get_email_content(token, email["id"])
            print(content)
            code = extract_code(content) if content else None

            if delete_email(token, email["id"]):  # Ensure email deletion before proceeding
                deleted_emails.add(email["id"])

            if code:
                print(f"[+] Verification code found: {code}")
                return code
            else:
                print("[-] No code found in email, waiting for another...          ")

        time.sleep(10)  # Slightly longer delay to prevent API caching issues

    print("[-] Email timeout reached          ")
    return None


def random_english_firstname():
    print("[*] Generating random name...", end='\r')
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
    print(f"[+] Generated name: {firstname} {lastname}          ")
    return firstname, lastname

def generate_random_phone_number():
    print("[*] Generating phone number...", end='\r')
    random_number = str(random.randint(1000000, 9999999))
    third = random.randint(0, 4)
    forth = random.randint(1, 7)
    phone_formats = [
        f"03{third}{forth} {random_number}",
        f"03{third}{forth}{random_number}",
        f"+92 3{third}{forth} {random_number}",
        f"+923{third}{forth}{random_number}"
    ]
    number = random.choice(phone_formats)
    print(f"[+] Generated phone: {number}          ")
    return number

def generate_user_details():
    print("[*] Generating user details...")
    fn,ln=random_english_firstname()
    year = random.randint(1960, 2006)
    date = random.randint(1, 28)
    month = random.randint(1, 12)
    formatted_date = f"{date:02d}-{month:02d}-{year:04d}"
    password = generate_random_password()
    phone_number = generate_random_phone_number()
    print(f"[+] User details generated: {fn} {ln} | {formatted_date}          ")
    return fn, ln, date,year,month, phone_number, password

def generate_random_password():
    print("[*] Generating password...", end='\r')
    length = random.randint(10, 16)
    all_characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(all_characters) for _ in range(length))
    print(f"[+] Password generated: {password}          ")
    return password

def generate_old_android_ua():
    print("[*] Generating user agent...", end='\r')
    random.seed(datetime.now().timestamp())
    
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
    
    build_number = f"{android_code}"
    if android_ver.startswith("4.0"):
        build_number += f".{random.choice(['IMM76', 'GRK39', 'IMM76D'])}"
    else:
        build_number += random.choice(["D", "E", "F"]) + str(random.randint(10,99))
    
    chrome_major = random.randint(
        18 if android_ver.startswith("4.0") else 25,
        35 if android_ver.startswith("4.4") else 32
    )
    chrome_build = random.randint(1000, 1999)
    chrome_patch = random.randint(50, 199)
    
    webkit_base = "534.30" if chrome_major < 25 else "537.36"
    webkit_ver = f"{webkit_base}.{random.randint(1, 99)}" if random.random() > 0.7 else webkit_base
    
    ua = (
        f"Mozilla/5.0 (Linux; Android {android_ver}; {device} Build/{build_number}) "
        f"AppleWebKit/{webkit_ver} (KHTML, like Gecko) "
        f"Chrome/{chrome_major}.0.{chrome_build}.{chrome_patch} Mobile Safari/{webkit_ver.split('.')[0]}.0"
    )
    print(f"[+] User agent generated: {ua[:60]}...          ")
    return ua

from selenium.common.exceptions import NoSuchElementException
def create_fbunconfirmed(usern):
    print(f"\n[+] Starting fb creation process ")
    asdf = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    ua = generate_old_android_ua()
    fn, ln, date, year, month, phone_number, password = generate_user_details()
    username=fn+ln+asdf
    print(f"[*] Generated username: {username}")
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
    
    print("[*] Initializing session...")
    session = requests.Session()
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    form = soup.find("form")
    
    if form:
        print("[*] Found registration form")
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

        print("[*] Submitting registration form...")
        submit_response = session.post(action_url, headers=headers, data=data)
        
        if "c_user" in session.cookies:
            uid = session.cookies.get("c_user")
            print(f"[+] Registration successful! UID: {uid}")
        else:
            print("[-] Registration failed          ")
            return
    else:
        print("[-] No registration form found          ")
        return
    
    print("[*] Attempting email change...")
    change_email_url = "https://m.facebook.com/changeemail/"
    email_response = session.get(change_email_url, headers=headers)
    
    soup = BeautifulSoup(email_response.text, "html.parser")
    form = soup.find("form")
    
    if form:
        print("[*] Found email change form")
        action_url = requests.compat.urljoin(change_email_url, form["action"]) if form.has_attr("action") else change_email_url
        inputs = form.find_all("input")
        data = {}
        for inp in inputs:
            if inp.has_attr("name") and inp["name"] not in data:
                data[inp["name"]] = inp["value"] if inp.has_attr("value") else ""
        data["new"] = f"{username}@{usern}.protonsemail.com"
        data["submit"] = "Add"
        
        print("[*] Submitting email change request...")
        submit_response = session.post(action_url, headers=headers, data=data)
        print("[*] Waiting for confirmation email...")
        confirmation_code = wait_for_email()
        
        if not confirmation_code:
            print("[-] No confirmation code received          ")
            return
        
        print(f"[+] Account created: {uid}|{password}")
        email=f"{username}@{usern}.protonsemail.com"
        storage_dir = "/sdcard"
        file_path = os.path.join(storage_dir, "unconfirmed_accounts.txt")

        if not os.path.exists(file_path):
            open(file_path, "w").close()

        credentials = f"{uid}|{password}|{confirmation_code}|{email}\n"

        with open(file_path, "a") as file:
            file.write(credentials)
        print(f"[+] Saved credentials to {file_path}")
    else:
        print("[-] Email change form not found          ")
    
    return


if __name__ == "__main__":
    try:
        print("\n===== 33Mail Account Creator =====\n")
        
        while True:
            try:
                max_create = int(input("[?] How many addresses to create? (1-10, 0=exit): "))
                if max_create == 0:
                    print("[+] Exiting...")
                    break
                elif 1 <= max_create <= 10:
                    print(f"[*] Starting creation of {max_create} accounts")
                    for i in range(max_create):
                        print(f"\n=== Account {i+1}/{max_create} ===")
                        usern = get_username(EMAIL)
                        create_fbunconfirmed(usern)
                    print("\n[+] Batch creation completed")
                else:
                    print("[-] Invalid input (1-10 only)")
            except ValueError:
                print("[-] Please enter a valid number")
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")
    finally:
        print("[+] Clean exit")
        exit()

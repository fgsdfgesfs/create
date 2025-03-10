from datetime import datetime
import json
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

import os
import subprocess
import json
import re
import time
import requests
import random
import string
import bs4
# Run git pull to update the script

import time
import re
import requests


def extract_code(text):
    # Match "FB-" followed by 4-6 digits, capturing the digits
    pattern = r'FB-(\d{4,6})'
    matches = re.findall(pattern, text)
    # Return the first match (or None if no matches)
    return matches[0] if matches else None

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
    print(f"[+] User agent generated:...          ")
    return ua

def check_account(fb_id):
    url = f"https://www.facebook.com/p/{fb_id}"
    session = requests.Session()
    
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "accept-encoding": "gzip, deflate",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "sec-ch-ua": '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }

    response = session.get(url, headers=headers, allow_redirects=True)
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.find("title").text.strip()

    # Check for common checkpoint indicators
    if "content not available" in title.lower() or "facebook" == title.lower():
        return "CP"  # Account is in checkpoint or deactivated
    return "OK"  # Account is active

from selenium.common.exceptions import NoSuchElementException


def create_fbunconfirmed():
    email=input("enter email")
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
            "reg_email__": email,
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
    status=check_account(uid)
    print(status)
    if "CP" in status:
        print("account got to checkpoint")
        print("change ip address by turning on aeroplane mode")
        return
    print("[*] Attempting email change...")
    confirmation_code=input("enter otp: ")
    ccookies=json.dumps(session.cookies.get_dict())
    
    storage_dir = "/sdcard"
    file_path = os.path.join(storage_dir, "d_accounts.txt")

    if not os.path.exists( file_path):
        open(file_path, "w").close()
    
    credentials = f"{uid}|{password}|{confirmation_code}|{email}|{ccookies}\n"

    with open( file_path, "a") as file:
        file.write(credentials)
    print(f"[+] Saved credentials to  unconfirmed_accounts.txt")
    get_url = "https://m.facebook.com/confirmemail.php?next=https%3A%2F%2Fm.facebook.com%2F%3Fdeoia%3D1&soft=hjk"
    
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "dpr": "2",
        "Host": "m.facebook.com",
        "Referer": "https://m.facebook.com/login/save-device/",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/27.0 Chrome/125.0.0.0 Mobile Safari/537.36"
    }

    response = session.get(get_url, headers=headers)
    html_content = response.text


    # Parse HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract values using regex
    def extract_value(pattern, text):
        match = re.search(pattern, text)
        return match.group(1) if match else None

    # Extract fb_dtsg
    fb_dtsg = extract_value(r'"dtsg":\{"token":"(.*?)"', html_content)

    # Extract lsd
    lsd = extract_value(r'\["LSD", \[\], \{"token": "(.*?)"\]', html_content)

    # Extract jazoest
    jazoest = extract_value(r'jazoest", "(\d+)"', html_content)
    time.sleep(5)
    # Step 2: Perform the POST request
    post_url = f"https://m.facebook.com/confirmation_cliff/?contact={email}&type=submit&is_soft_cliff=false&medium=email&code={confirmation_code}"

    post_headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "m.facebook.com",
        "Origin": "https://m.facebook.com",
        "Referer": get_url,
        "User-Agent": headers["User-Agent"],
        "X-FB-LSD": lsd if lsd else ""
    }

    post_data = {
        "fb_dtsg": fb_dtsg if fb_dtsg else "",
        "jazoest": jazoest if jazoest else "",
        "lsd": lsd if lsd else "",
        "__user": uid
    }
    time.sleep(6)
    post_response = session.post(post_url, headers=post_headers, data=post_data)


    
    return


if __name__ == "__main__":
    try:
        print("\n===== 33Mail Account Creator =====\n")
        
        while True:
            try:
             #   max_create = int(input("[?] How many addresses to create? (1-10, 0=exit): "))
                max_create=10
                if max_create == 0:
                    print("[+] Exiting...")
                    break
                elif 1 <= max_create <= 40:
                    print(f"[*] Starting creation of {max_create} accounts")
                    for i in range(max_create):
                        print(f"\n=== Account {i+1}/{max_create} ===")
                      
                        create_fbunconfirmed()
                    print("\n[+] Batch creation completed")
                else:
                    print("[-] Invalid input (1-10 only)")
            except Exception as  e:
                print(e)
    except :
        print("\n[!] Interrupted by user")
    finally:
        print("[+] Clean exit")
        exit()

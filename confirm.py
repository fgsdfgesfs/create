
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

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
def create_chrome_instance():

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Headless mode for Termux
    options.add_argument("--no-sandbox")  
    options.add_argument("--disable-gpu")  
    options.add_argument("--disable-software-rasterizer")  
    options.add_argument("--disable-dev-shm-usage")  
    options.add_argument("--disable-infobars")  
    options.add_argument("--disable-blink-features=AutomationControlled")  
    options.add_argument("--window-size=400x640")  # Set window size

    user_agent = "Mozilla/5.0 (Linux; Android 11; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
    options.add_argument(f"user-agent={user_agent}")


    # Initialize Chrome WebDriver
    driver = webdriver.Chrome(options=options)
    return driver

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

def random_filename():
    return "response_" + "".join(random.choices(string.ascii_letters + string.digits, k=10)) + ".html"
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


class DeviceHeaderGenerator:
    def __init__(self):
        self.fake = Faker()
        self.device_profiles = []
        
    def generate_device_profile(self):
        """Create a random device profile with consistent attributes"""
        profile = {
            # Device Type (50% chance for mobile)
            'is_mobile': random.choice([True, False]),
            
            # Browser Components
            'chrome_version': f"{random.randint(120, 140)}.0.{random.randint(1000, 9999)}.{random.randint(100, 999)}",
            'chromium_version': f"{random.randint(120, 140)}.0.{random.randint(1000, 9999)}.{random.randint(100, 999)}",
            
            # Platform Details
            'os_type': random.choice(['Windows', 'Android', 'Linux', 'iOS']),
            'os_version': {
                'Windows': f"{random.randint(10, 11)}.0",
                'Android': f"{random.randint(10, 14)}.0.0",
                'Linux': "X11",
                'iOS': f"{random.randint(15, 17)}.{random.randint(0, 6)}"
            },
            
            # Device Characteristics
            'viewport_width': str(random.choice([360, 390, 412, 1440])),
            'dpr': str(round(random.uniform(1.0, 3.5), 1)),
            
            # Security Components
            'lsd_token': ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=24)),
            'asbd_id': str(random.randint(100000, 999999)),
        }
        
        # Set derived values
        profile['user_agent'] = self._generate_user_agent(profile)
        profile['sec_ch_ua'] = self._generate_sec_ch_ua(profile)
        profile['sec_ch_ua_full_version'] = self._generate_full_version(profile)
        
        return profile
    
    def _generate_user_agent(self, profile):
        """Generate consistent User-Agent string"""
        if profile['os_type'] == 'Windows':
            return f"Mozilla/5.0 (Windows NT {profile['os_version']['Windows']}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{profile['chrome_version']} Safari/537.36"
        elif profile['os_type'] == 'Android':
            return f"Mozilla/5.0 (Linux; Android {profile['os_version']['Android']}; {self.fake.word().capitalize()}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{profile['chrome_version']} Mobile Safari/537.36"
        else:
            return self.fake.user_agent()
    def _generate_sec_ch_ua(self, profile):
        """Generate sec-ch-ua header value with correct brand formatting"""
        base = [
            # Fixed brand string from "Not%A.Brand" to "Not(A:Brand"
            f'"Not(A:Brand";v="99"',
            f'"Chromium";v="{profile["chromium_version"].split(".")[0]}"',
            f'"Google Chrome";v="{profile["chrome_version"].split(".")[0]}"'
        ]
        if profile['os_type'] == 'Android':
            base.append('"Android WebView";v="132"')
        return ', '.join(base)

    def _generate_full_version(self, profile):
        """Generate full version list with consistent brand name"""
        return ', '.join([
            # Fixed brand string here too
            f'"Not(A:Brand";v="{profile["chromium_version"]}"',
            f'"Google Chrome";v="{profile["chrome_version"]}"',
            f'"Chromium";v="{profile["chromium_version"]}"'
        ])
    def generate_first_headers(self, profile):
        """Generate headers for initial request"""
        return {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "max-age=0",
            "dpr": profile['dpr'],
            "priority": "u=0, i",
            "referer": "https://www.facebook.com/?_rdc=2&_rdr",
            "sec-ch-prefers-color-scheme": random.choice(["light", "dark"]),
            "sec-ch-ua": profile['sec_ch_ua'],
            "sec-ch-ua-full-version-list": profile['sec_ch_ua_full_version'],
            "sec-ch-ua-mobile": "?1" if profile['is_mobile'] else "?0",
            "sec-ch-ua-platform": f'"{profile["os_type"]}"',
            "sec-ch-ua-platform-version": f'"{profile["os_version"][profile["os_type"]]}"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": profile['user_agent'],
            "viewport-width": profile['viewport_width']
        }
    
    def generate_second_headers(self, profile):
        """Generate headers for subsequent request"""
        return {
            "content-length": "551",
            "sec-ch-ua-full-version-list": "",
            "sec-ch-ua-platform": f'"{profile["os_type"]}"',
            "sec-ch-ua": profile['sec_ch_ua'],
            "sec-ch-ua-model": "",
            "sec-ch-ua-mobile": "?1" if profile['is_mobile'] else "?0",
            "x-asbd-id": profile['asbd_id'],
            "x-fb-lsd": profile['lsd_token'],
            "sec-ch-prefers-color-scheme": random.choice(["light", "dark"]),
            "user-agent": profile['user_agent'],
            "content-type": "application/x-www-form-urlencoded",
            "sec-ch-ua-platform-version": "",
            "accept": "/",
            "origin": "https://www.facebook.com",
            "x-requested-with": "mark.via.gp",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://www.facebook.com/confirmemail.php?next=https%3A%2F%2Fwww.facebook.com%2F%3Fsk%3Dwelcome%26lsrc%3Dlb",
            "accept-encoding": "gzip, deflate",
            "accept-language": "en-US,en;q=0.9",
            "priority": "u=1, i"
        }
def extract_code(text):
    # Match "FB-" followed by 4-6 digits, capturing the digits
    pattern = r'FB-(\d{4,6})'
    matches = re.findall(pattern, text)
    # Return the first match (or None if no matches)
    return matches[0] if matches else None

def create_fbunconfirmed(browser):

    email=browser.find_element(By.XPATH,'//input[@aria-label="Your temporary email address"]').text
    print(f"{email}||")
    print(f"\n[+] Starting fb creation process ")
    asdf = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    ua = generate_old_android_ua()
    fn, ln, date, year, month, phone_number, password = generate_user_details()

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
    browser.find_element(By.XPATH,'//button[@class="openMessage"]').click()
    code=browser.find_element(By.XPATH,'//h4[contains(text(),"confirmation ")]').text
    
    confirmation_code=extract_code(code)
    print(f"[+] Verification code found: {confirmation_code}")
    if confirmation_code:
        generator = DeviceHeaderGenerator()
        device_profile = generator.generate_device_profile()
        
        first_headers = generator.generate_first_headers(device_profile)
        second_headers = generator.generate_second_headers(device_profile)
        

        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "max-age=0",
            "dpr": "1",
            "priority": "u=0, i",
            "referer": "https://www.facebook.com/?_rdc=2&_rdr",
            "sec-ch-prefers-color-scheme": "dark",
            "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            "sec-ch-ua-full-version-list": '"Not(A:Brand";v="99.0.0.0", "Google Chrome";v="133.0.6943.141", "Chromium";v="133.0.6943.141"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "sec-ch-ua-platform-version": "10.0.0",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "viewport-width": "403"
        }

        # First request
        url_1 = "https://www.facebook.com/confirmemail.php?next=https%3A%2F%2Fwww.facebook.com%2F%3Fsk%3Dwelcome%26lsrc%3Dlb"
        response_1 = session.get(url_1, headers=first_headers)

        html_content = response_1.text  # Your HTML response
        soup = BeautifulSoup(html_content, "html.parser")
        def get_value(name):
            tag = soup.find("input", {"name": name})
            if tag and tag.has_attr("value"):
                return tag["value"]
            
            # Method 2: Search in script tags (JSON data)
            script_tags = soup.find_all("script")
            for script in script_tags:
                if name in script.text:
                    match = re.search(rf'"{name}":\s*"([^"]+)"', script.text)
                    if match:
                        return match.group(1)
                    try:
                        json_data = json.loads(script.text)
                        if name in json_data:
                            return json_data[name]
                    except json.JSONDecodeError:
                        continue
            
            # Method 3: Search in the entire HTML as a last resort
            match = re.search(rf'name="{name}"\s+value="([^"]+)"', html_content)
            return match.group(1) if match else None

        # Assigning values
        jazoest = get_value("jazoest")
        fb_dtsg = get_value("fb_dtsg")
        hs = get_value("hs")
        uid = get_value("uid")
        spin_r = get_value("spin_r")
        hsi = get_value("hsi")
        lsd = get_value("lsd")
        spin_b = get_value("spin_b")
        spin_t = get_value("spin_t")

        # Printing extracted values
        print(f"jazoest: {jazoest}")
        print(f"fb_dtsg: {fb_dtsg}")
        print(f"hs: {hs}")
        print(f"uid: {uid}")
        print(f"spin_r: {spin_r}")
        print(f"hsi: {hsi}")
        print(f"lsd: {lsd}")
        print(f"spin_b: {spin_b}")
        print(f"spin_t: {spin_t}")

        url = f"https://www.facebook.com/confirm_code/dialog/submit/?next=https%3A%2F%2Fwww.facebook.com%2F%3Fsk%3Dwelcome%26lsrc%3Dlb&cp={email}&from_cliff=1&conf_surface=hard_cliff&event_location=cliff"
        headers = {
            "content-length": "551",
            "sec-ch-ua-full-version-list": "",
            "sec-ch-ua-platform": "\"Android\"",
            "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Android WebView\";v=\"132\"",
            "sec-ch-ua-model": "",
            "sec-ch-ua-mobile": "?1",
            "x-asbd-id": "129477",
            "x-fb-lsd": lsd,
            "sec-ch-prefers-color-scheme": "dark",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "content-type": "application/x-www-form-urlencoded",
            "sec-ch-ua-platform-version": "",
            "accept": "/",
            "origin": "https://www.facebook.com",
            "x-requested-with": "mark.via.gp",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://www.facebook.com/confirmemail.php?next=https%3A%2F%2Fwww.facebook.com%2F%3Fsk%3Dwelcome%26lsrc%3Dlb",
            "accept-encoding": "gzip, deflate",
            "accept-language": "en-US,en;q=0.9",
            "priority": "u=1, i"
        }

        data = {
            "jazoest": jazoest,
            "fb_dtsg": fb_dtsg,
            "code": confirmation_code,
            "source_verified": "www_reg",
            "confirm": "1",
            "__user": uid,
            "__a": "1",
            "__req": "5",
            "__hs": hs,
            "dpr": "3",
            "__ccg": "EXCELLENT",
            "__rev": spin_r,
            "__s": "5qzil3:fcnekv:jdje7k",
            "__hsi": hsi,
            "__dyn": "7xeUmBwjbg7ebwKBAg5S3G2O5U4e1Fx-ewSwMxW0DUS2S0im4E9ohwem0nCq1ew8y11wdu0FE5-2G1Qw5Mx61vwnE2PwBgao6C0lW0H83bwdq1iwmE2ewnE2Lwg81soGdw46wbS1Lwqo1wU1UU7u1rwea",
            "__csr": "",
            "lsd": lsd,
            "__spin_r": spin_r,
            "__spin_b": spin_b,
            "__spin_t": spin_t
        }
        for attempt in range(10):
            try:
                response = session.post(url, headers=second_headers, data=data, timeout=20)
                # Save response to a randomly named HTML file
                filename = random_filename()
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(response.text)

                print(f"First response saved to {filename}")
                if response.status_code != 200:
                    print(f" OTP submission failed. Status code: {response.status_code}")
                    time.sleep(3)
                    continue
                if response.status_code == 200:
                    print("done")
                    break
            except requests.RequestException as e:
                time.sleep(3)
                continue

        time.sleep(5)
        statuss=check_account(uid)
        ccookies=json.dumps(session.cookies.get_dict())
        storage_dir = "/sdcard"
        file_path = os.path.join(storage_dir, "confirmed_accounts.txt")
        uid = session.cookies.get("c_user")
        if not os.path.exists( file_path):
            open(file_path, "w").close()
        if "CP" in statuss:
            credentials = f"CP|{uid}|{password}|{confirmation_code}|{email}|{ccookies}\n"

            with open( file_path, "a") as file:
                file.write(credentials)
            print(f"[+] Saved credentials to  unconfirmed_accounts.txt")
        else:
            credentials = f"OKay|{uid}|{password}|{confirmation_code}|{email}|{ccookies}\n"

            with open( file_path, "a") as file:
                file.write(credentials)
            print(f"[+] Saved credentials to  unconfirmed_accounts.txt")
    return


if __name__ == "__main__":
    try:
        print("\n===== 33Mail Account Creator =====\n")
        browser=create_chrome_instance()
        browser.implicitly_wait(60)
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
                        browser.get("https://temporarymail.com/en/")
                        create_fbunconfirmed(browser)
                        browser.delete_all_cookies()
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

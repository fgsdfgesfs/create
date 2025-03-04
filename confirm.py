import string
import time
from faker import Faker
import requests
import re
import json
from bs4 import BeautifulSoup
import random

# Define variables
# Generate a random filename for saving the HTML response
def random_filename():
    return "response_" + "".join(random.choices(string.ascii_letters + string.digits, k=10)) + ".html"
email ="kendyll.bizier@allfreemail.net"
otp = "99439"
uid ="61573919306724"
cookies ={"datr": "bSzHZ2vkDImLmKgZ59A-tESh", "fr": "0TWLGnLEQTwB6qCdH.AWWgaAtitl0gSDxM-9Hz_vT8kkRl4tkPRLN2_g.Bnxyxt..AAA.0.0.Bnxyxu.AWVuNHTF-Ts", "c_user": "61573919306724", "sb": "bizHZ04dj65Rhsjm9FqEaxNw", "xs": "24%3AYEQwwjlgmjv4Qw%3A2%3A1741106293%3A-1%3A-1"}
session = requests.Session()
import random
from faker import Faker

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

# Usage Example
if __name__ == "__main__":
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
    response_1 = session.get(url_1, headers=first_headers, cookies=cookies)

    filename = random_filename()
    with open(filename, "w", encoding="utf-8") as file:
        file.write(response_1.text)

    print(f"First response saved to {filename}")
    from bs4 import BeautifulSoup

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
        "code": otp,
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
            response = session.post(url, headers=second_headers, data=data,  cookies=cookies, timeout=20)
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

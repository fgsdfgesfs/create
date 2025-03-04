import time
import requests
import re
import json
from bs4 import BeautifulSoup
import random

# Define variables

email ="AstaValentinoqjwkc@xander.protonsemail.com"
otp = "14482"
uid ="61573870948550"
cookies = {"datr": "TcDGZ9c2IIYF3ccJCg3MWRAL", "fr": "07IBty6jhnXgZBxXW.AWVcgBz0mpB_9b8lETK1-NRB5mdvN4mEmlliLw.BnxsBN..AAA.0.0.BnxsBP.AWXtMQYFGuc", "c_user": "61573870948550", "sb": "T8DGZ5woyyxars4B91_tTKvC", "xs": "6%3ALzbOBgU0A4NWrg%3A2%3A1741078618%3A-1%3A-1"}

# Step 1: Perform the GET request
get_url = "https://m.facebook.com/confirmemail.php?next=https%3A%2F%2Fm.facebook.com%2F%3Fdeoia%3D1&soft=hjk"
session = requests.Session()
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

response = session.get(get_url, headers=headers, cookies=cookies)
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
post_url = f"https://m.facebook.com/confirmation_cliff/?contact={email}&type=submit&is_soft_cliff=false&medium=email&code={otp}"

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
post_response = session.post(post_url, headers=post_headers, data=post_data, cookies=cookies)


print(f"POST response   to {post_response.status_code}")

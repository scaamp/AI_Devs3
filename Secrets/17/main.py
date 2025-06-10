import requests
from dotenv import load_dotenv
import os

AIDEVS_API_KEY=os.getenv("AIDEVS_API_KEY")

# for user_id in range(0, 300):
response = requests.post("https://centrala.ag3nts.org/gps", json={
    "apikey": AIDEVS_API_KEY,
    "userID": 443
})

data = response.json()
if data.get("code") == 0:
    print(443, data["message"])
    
coords = [
    123.615125, 123.734855, 70.404575, 76.122349, 71.240630,
    58.283262, 87.243116, 72.173208, 69.391032, 82.301937,
    69.685946, 83.744884, 87.768239, 65.320696, 76.644297,
    76.120321, 89.612406, 125.615959, 125.455585
]

ascii_str = ''.join([chr(int(x)) for x in coords])
print(ascii_str)


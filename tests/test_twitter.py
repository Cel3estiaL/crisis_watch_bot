"""Test Twitter API"""

import os
from dotenv import load_dotenv
from requests_oauthlib import OAuth1
import requests

load_dotenv()

auth = OAuth1(
    os.getenv("TWITTER_API_KEY"),
    os.getenv("TWITTER_API_SECRET"),
    os.getenv("TWITTER_ACCESS_TOKEN"),
    os.getenv("TWITTER_ACCESS_SECRET")
)

print("\n🧪 Testing Twitter API...\n")

url = "https://api.twitter.com/2/users/me"
response = requests.get(url, auth=auth, timeout=10)

if response.status_code == 200:
    data = response.json()
    username = data.get("data", {}).get("username")
    print(f"✅ Authenticated as @{username}\n")
else:
    print(f"❌ Authentication failed: {response.status_code}\n")
    print(response.text)

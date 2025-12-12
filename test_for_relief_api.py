"""Quick ReliefWeb API test"""

import requests

APPNAME = "RakshitTwitterapiBot-1ZPbednY"

def test_api():
    print("\n🧪 Testing ReliefWeb API...")
    print(f"📝 Appname: {APPNAME}\n")
    
    url = "https://api.reliefweb.int/v2/reports"
    params = {
        "appname": APPNAME,
        "limit": 3,
        "preset": "latest",
        "filter[field]": "language.code",   # 👈 Filter by language
        "filter[value]": "en" 
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            reports = data.get("data", [])
            
            print(f"✅ SUCCESS! Found {len(reports)} reports:\n")
            
            for i, item in enumerate(reports, 1):
                title = item.get("fields", {}).get("title", "No title")
                print(f"{i}. {title}")
            
            print("\n✅ Your appname works!\n")
            return True
            
        elif response.status_code == 403:
            print("❌ NOT APPROVED YET")
            print("⏳ Wait for ReliefWeb email\n")
            return False
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Details: {response.text[:200]}\n")
            return False
            
    except Exception as e:
        print(f"❌ Failed: {e}\n")
        return False


if __name__ == "__main__":
    test_api()

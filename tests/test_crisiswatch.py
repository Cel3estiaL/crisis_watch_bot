"""Test ReliefWeb API"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from dotenv import load_dotenv
from src.crisiswatch import fetch_reports

load_dotenv()

print("\n🧪 Testing ReliefWeb API...\n")

reports = fetch_reports(
    appname=os.getenv("RELIEFWEB_APPNAME"),
    limit=3
)

if reports:
    print(f"✅ Found {len(reports)} reports:\n")
    for i, report in enumerate(reports, 1):
        print(f"{i}. {report['title'][:60]}...")
        if report.get("country"):
            print(f"   📍 {report['country']}")
        print(f"   🔗 {report['url']}\n")
else:
    print("❌ No reports returned")

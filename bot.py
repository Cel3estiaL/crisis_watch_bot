# #!/usr/bin/env python3
"""ReliefWeb Reports Bot - Main script"""

import sys
from dotenv import load_dotenv
from src.config import Config
from src.database import Database
from src.crisiswatch import fetch_reports
from src.twitterposter import TwitterPoster

load_dotenv()


def main():
    print("\n" + "=" * 70)
    print("🌍 ReliefWeb Reports Bot")
    print("=" * 70 + "\n")
    
    print("🔧 Validating configuration...")
    errors = Config.validate()
    
    if errors:
        print("\n❌ Configuration errors:")
        for error in errors:
            print(f"   • {error}")
        print("\n💡 Fix these in .env file")
        sys.exit(1)
    
    print("✅ Configuration valid\n")
    
    print("🔧 Initializing components...")
    try:
        db = Database()
        twitter = TwitterPoster()
        print()
    except Exception as e:
        print(f"\n❌ Initialization failed: {e}")
        sys.exit(1)
    
    print("📥 Fetching latest reports from ReliefWeb...")

    # Option 3: Get Situation Reports + Assessments + Appeals (uncomment to use)
    reports = fetch_reports(
        appname=Config.RELIEFWEB_APPNAME,
        limit=Config.FETCH_LIMIT,
        country=Config.FILTER_COUNTRY,
        report_formats=["News and Press Release", "Map", "Infographic", "UN Document"]
    )
    #reports = fetch_reports(
     #   appname=Config.RELIEFWEB_APPNAME,
      #  limit=Config.FETCH_LIMIT,
       # country=Config.FILTER_COUNTRY
    #)
    
    if not reports:
        print("⚠️  No reports found")
        return
    
    print(f"✅ Found {len(reports)} reports\n")
    
    print("📝 Processing reports...")
    print("-" * 70 + "\n")
    
    new_count = 0
    posted_count = 0
    
    for i, report in enumerate(reports, 1):
        report_id = report["id"]
        title = report["title"][:50]
        
        print(f"[{i}/{len(reports)}] {title}...")
        
        if report.get("format"):
            print(f"     📄 Type: {report['format']}")
        if report.get("country"):
            print(f"     📍 Location: {report['country']}")
        if report.get("source"):
            print(f"     📰 Source: {report['source']}")
        
        if not db.report_exists(report_id):
            if db.save_report(report):
                print(f"     💾 Saved to database")
                new_count += 1
            else:
                continue
        else:
            print(f"     ℹ️  Already in database")
        
        if not db.is_posted(report_id, "twitter"):
            if twitter.post(report):
                db.mark_posted(report_id, "twitter")
                posted_count += 1
        else:
            print(f"     ⏭️  Already posted to Twitter")
        
        print()
    
    db_stats = db.get_stats()
    
    print("=" * 70)
    print(f"✅ Done! New: {new_count} | Posted: {posted_count}")
    print(f"📊 Total in DB: {db_stats['total_reports']} reports, {db_stats['total_posts']} posts")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()

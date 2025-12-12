"""Supabase database operations"""

from supabase import create_client, Client
from src.config import Config


class Database:
    """Handle Supabase operations"""
    
    def __init__(self):
        if not Config.SUPABASE_URL or not Config.SUPABASE_KEY:
            raise ValueError("Missing Supabase credentials")
        
        self.client: Client = create_client(
            Config.SUPABASE_URL,
            Config.SUPABASE_KEY
        )
        print("✅ Database connected")
    
    def report_exists(self, report_id: int) -> bool:
        """Check if report exists"""
        try:
            result = self.client.table("reports")\
                .select("id")\
                .eq("id", report_id)\
                .execute()
            return len(result.data) > 0
        except Exception as e:
            print(f"❌ Error checking report: {e}")
            return False
    
    def save_report(self, report: dict) -> bool:
        """Save report to database"""
        try:
            self.client.table("reports").insert({
                "id": report["id"],
                "title": report["title"],
                "body": report.get("body"),
                "url": report["url"],
                "country": report.get("country"),
                "disaster_type": report.get("disaster_type"),
                "source": report.get("source"),
                "format": report.get("format"),
                "date_created": report.get("date_created")
            }).execute()
            return True
        except Exception as e:
            print(f"❌ Error saving: {e}")
            return False
    
    def is_posted(self, report_id: int, platform: str) -> bool:
        """Check if report was posted"""
        try:
            result = self.client.table("posts")\
                .select("id")\
                .eq("report_id", report_id)\
                .eq("platform", platform)\
                .execute()
            return len(result.data) > 0
        except Exception as e:
            print(f"❌ Error checking post: {e}")
            return False
    
    def mark_posted(self, report_id: int, platform: str) -> bool:
        """Mark report as posted"""
        try:
            self.client.table("posts").insert({
                "report_id": report_id,
                "platform": platform
            }).execute()
            return True
        except Exception as e:
            print(f"❌ Error marking posted: {e}")
            return False
    
    def get_stats(self) -> dict:
        """Get database statistics"""
        try:
            reports_result = self.client.table("reports")\
                .select("id", count="exact")\
                .execute()
            posts_result = self.client.table("posts")\
                .select("id", count="exact")\
                .execute()
            
            return {
                "total_reports": reports_result.count or 0,
                "total_posts": posts_result.count or 0,
            }
        except Exception:
            return {"total_reports": 0, "total_posts": 0}

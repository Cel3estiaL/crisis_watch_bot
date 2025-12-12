"""Twitter posting functionality"""

import requests
from requests_oauthlib import OAuth1
from src.config import Config


class TwitterPoster:
    """Handle Twitter posting"""
    
    def __init__(self):
        if not all([
            Config.TWITTER_API_KEY,
            Config.TWITTER_API_SECRET,
            Config.TWITTER_ACCESS_TOKEN,
            Config.TWITTER_ACCESS_SECRET
        ]):
            raise ValueError("Missing Twitter credentials")
        
        self.auth = OAuth1(
            Config.TWITTER_API_KEY,
            Config.TWITTER_API_SECRET,
            Config.TWITTER_ACCESS_TOKEN,
            Config.TWITTER_ACCESS_SECRET
        )
        
        if self.verify_credentials():
            user_info = self.get_user_info()
            print(f"✅ Twitter connected (@{user_info.get('username', 'unknown')})")
        else:
            raise ValueError("Twitter authentication failed")
    
    def verify_credentials(self) -> bool:
        """Verify Twitter credentials"""
        try:
            url = "https://api.twitter.com/2/users/me"
            response = requests.get(url, auth=self.auth, timeout=10)
            return response.status_code == 200
        except Exception:
            return False
    
    def get_user_info(self) -> dict:
        """Get user info"""
        try:
            url = "https://api.twitter.com/2/users/me"
            response = requests.get(url, auth=self.auth, timeout=10)
            if response.status_code == 200:
                return response.json().get("data", {})
            return {}
        except Exception:
            return {}
    def format_tweet(self, report: dict) -> str:
        """Use emojis for visual appeal"""

        tweet = f"🌍NEW {report['format']}!!!\n\n"
        tweet += f"{report['title']}\n\n"
    
        if report.get("country"):
            tweet += f"📍 {report['country']}\n"
        if report.get("source"):
            tweet += f"📢 {report['source']}\n"
        if report.get("disaster_type"):
            tweet += f"⚠️ {report['disaster_type']}\n"
    
        tweet += f"\n🔗 {report['url']}\n\n"
        tweet += "🌍"
    
        if len(tweet) > 280:
            tweet = f"🌍 {report['title'][:160]}...\n\n🔗 {report['url']}\n\n#ReliefWeb"
    
        return tweet

    
    def post(self, report: dict) -> bool:
        """Post tweet"""
        try:
            tweet_text = self.format_tweet(report)
            url = "https://api.twitter.com/2/tweets"
            payload = {"text": tweet_text}
            
            response = requests.post(
                url,
                json=payload,
                auth=self.auth,
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            
            if response.status_code == 201:
                tweet_data = response.json()
                tweet_id = tweet_data.get("data", {}).get("id", "unknown")
                preview = tweet_text.replace("\n", " | ")[:80]
                print(f"✅ Posted (ID: {tweet_id}): {preview}...")
                return True
            elif response.status_code == 403:
                error = response.json()
                print(f"⚠️  Blocked: {error.get('detail', 'Duplicate or rate limit')}")
                return False
            else:
                error = response.json()
                print(f"❌ Error ({response.status_code}): {error.get('detail', response.text[:100])}")
                return False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

"""Configuration management"""

import os
from typing import Optional


class Config:
    """Bot configuration from environment variables"""
    
    # ReliefWeb API
    RELIEFWEB_APPNAME: str = os.getenv("RELIEFWEB_APPNAME", "")
    RELIEFWEB_API_BASE: str = "https://api.reliefweb.int/v2"
    
    # Supabase
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    
    # Twitter
    TWITTER_API_KEY: str = os.getenv("TWITTER_API_KEY", "")
    TWITTER_API_SECRET: str = os.getenv("TWITTER_API_SECRET", "")
    TWITTER_ACCESS_TOKEN: str = os.getenv("TWITTER_ACCESS_TOKEN", "")
    TWITTER_ACCESS_SECRET: str = os.getenv("TWITTER_ACCESS_SECRET", "")
    
    # Bot Settings
    FETCH_LIMIT: int = int(os.getenv("FETCH_LIMIT", "5"))
    FILTER_COUNTRY: Optional[str] = os.getenv("FILTER_COUNTRY", None)

    # API Settings
    API_TIMEOUT: int = 20
    MAX_TWEET_LENGTH: int = 280
    
    @classmethod
    def validate(cls) -> list[str]:
        """Validate required configuration"""
        errors = []
        
        required = {
            "RELIEFWEB_APPNAME": cls.RELIEFWEB_APPNAME,
            "SUPABASE_URL": cls.SUPABASE_URL,
            "SUPABASE_KEY": cls.SUPABASE_KEY,
            "TWITTER_API_KEY": cls.TWITTER_API_KEY,
            "TWITTER_API_SECRET": cls.TWITTER_API_SECRET,
            "TWITTER_ACCESS_TOKEN": cls.TWITTER_ACCESS_TOKEN,
            "TWITTER_ACCESS_SECRET": cls.TWITTER_ACCESS_SECRET,
        }
        
        for var_name, var_value in required.items():
            if not var_value:
                errors.append(f"Missing: {var_name}")
        
        return errors

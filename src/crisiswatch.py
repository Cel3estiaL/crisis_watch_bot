"""ReliefWeb API client"""

import requests
from typing import Optional, List, Dict
from src.config import Config


def fetch_reports(
    appname: str,
    limit: int = 5,
    country: Optional[str] = None,
    report_formats: Optional[List[str]] = None
) -> List[Dict]:
    """
    Fetch latest reports from ReliefWeb API
    English only, all report types
    """
    
    url = f"{Config.RELIEFWEB_API_BASE}/reports"
    
    params = {
        "appname": appname,
        "limit": min(limit, 1000),
        "preset": "latest",
        "filter[field]": "language.code",
        "filter[value]": "en",
        "fields[include][]": [
            "title",
            "body",
            "url",
            "primary_country.name",
            "country.name",
            "disaster.name",
            "disaster_type.name",
            "source.name",
            "format.name",
            "date.created"
        ]
    }
    
    if country:
        params["filter[conditions][0][field]"] = "language.code"
        params["filter[conditions][0][value]"] = "en"
        params["filter[conditions][1][field]"] = "country"
        params["filter[conditions][1][value]"] = country
        params["filter[operator]"] = "AND"
        del params["filter[field]"]
        del params["filter[value]"]
    
    try:
        response = requests.get(url, params=params, timeout=Config.API_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        
        reports = []
        
        for item in data.get("data", []):
            fields = item.get("fields", {})
            
            # Extract country
            country_name = None
            if fields.get("primary_country"):
                country_name = fields["primary_country"].get("name")
            elif fields.get("country") and len(fields["country"]) > 0:
                country_name = fields["country"][0].get("name")
            
            # Extract source
            source_name = None
            if fields.get("source") and len(fields["source"]) > 0:
                source_name = fields["source"][0].get("name")
            
            # Extract disaster type
            disaster_type = None
            if fields.get("disaster_type") and len(fields["disaster_type"]) > 0:
                disaster_type = fields["disaster_type"][0].get("name")
            elif fields.get("disaster") and len(fields["disaster"]) > 0:
                disaster_type = fields["disaster"][0].get("name")
            
            # Extract format
            format_name = None
            if fields.get("format") and len(fields["format"]) > 0:
                format_name = fields["format"][0].get("name")
            
            # Clean body
            body = fields.get("body", "")
            if len(body) > 300:
                body = body[:300] + "..."
            
            reports.append({
                "id": item["id"],
                "title": fields.get("title", ""),
                "body": body,
                "url": fields.get("url", ""),
                "country": country_name,
                "disaster_type": disaster_type,
                "source": source_name,
                "format": format_name,
                "date_created": fields.get("date", {}).get("created")
            })
        
        return reports
    
    except Exception as e:
        print(f"❌ Error fetching reports: {e}")
        return []

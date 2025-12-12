"""Debug Supabase connection"""

from dotenv import load_dotenv
import os

load_dotenv()

print("\n🔍 Debugging Supabase Configuration\n")

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

print(f"✅ SUPABASE_URL loaded: {url}")
print(f"✅ SUPABASE_KEY loaded: {key[:30]}..." if key else "❌ SUPABASE_KEY missing")
print()

# Check URL format
if url:
    print("📋 URL Analysis:")
    print(f"   - Starts with https://: {url.startswith('https://')}")
    print(f"   - Contains .supabase.co: {'.supabase.co' in url}")
    print(f"   - Length: {len(url)} characters")
    print(f"   - Has whitespace: {' ' in url or '\\n' in url or '\\t' in url}")
    print()

# Try to connect
print("🔌 Attempting connection...")
try:
    from supabase import create_client, Client
    
    client: Client = create_client(url, key)
    print("✅ Supabase client created successfully!")
    
    # Test query
    print("\n🧪 Testing database query...")
    result = client.table("reports").select("id").limit(1).execute()
    print(f"✅ Database query successful! Found {len(result.data)} rows")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print(f"\n💡 Error type: {type(e).__name__}")

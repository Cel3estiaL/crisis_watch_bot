# 🌍 ReliefWeb Reports Bot

Automated bot that posts humanitarian reports from ReliefWeb to Twitter every 3 hours.

# 🚀 Features

-  Fetches latest English reports from ReliefWeb API
-  Stores in Supabase PostgreSQL database
-  Posts to Twitter automatically
-  Runs every 3 hours via GitHub Actions
-  Prevents duplicate posts
-  Tested with Postman before coding

# 🛠️ Tech Stack

- Python 3.11
- ReliefWeb API - UN humanitarian news
- Supabase - PostgreSQL database
- Twitter API v2 - OAuth 1.0a
- GitHub Actions - Automated scheduling

# 📦 Local Setup

Clone repo
git clone https://github.com/yourusername/reliefweb-bot.git
cd reliefweb-bot

Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1 # for windows

Install dependencies
pip install -r requirements.txt

Configure credentials
copy .env.example .env

Edit .env with your credentials
Test components
python tests\test_reliefweb.py
python tests\test_twitter.py

Run bot
python bot.py

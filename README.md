#### THIS BOT HAS BEEN DISABLED AFTER RUNNING 52 SUCCESSFUL WORKFLOW RUNS ON TWITTER/X.  (https://x.com/CrisisWatchBot)

# Crisis Watch Bot

Automated bot that posts humanitarian reports from ReliefWeb to Twitter every 3 hours.

## Features

-  Fetches latest English reports from ReliefWeb API
-  Stores in Supabase PostgreSQL database
-  Posts to Twitter automatically
-  Runs every 3 hours via GitHub Actions
-  Prevents duplicate posts
-  Tested with Postman before coding

## Tech Stack

- Python 3.11
- ReliefWeb API - UN humanitarian news
- Supabase - PostgreSQL database
- Twitter API v2 - OAuth 1.0a
- GitHub Actions - Automated scheduling

-- ReliefWeb Bot Database Schema
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS reports;

-- Reports table
CREATE TABLE reports (
    id BIGINT PRIMARY KEY,
    title TEXT NOT NULL,
    body TEXT,
    url TEXT NOT NULL,
    country TEXT,
    disaster_type TEXT,
    source TEXT,
    format TEXT,
    date_created TIMESTAMP,
    fetched_at TIMESTAMP DEFAULT NOW()
);

-- Posts tracking
CREATE TABLE posts (
    id BIGSERIAL PRIMARY KEY,
    report_id BIGINT REFERENCES reports(id) ON DELETE CASCADE,
    platform TEXT NOT NULL,
    posted_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(report_id, platform)
);

-- Indexes
CREATE INDEX idx_posts_report_platform ON posts(report_id, platform);
CREATE INDEX idx_reports_fetched_at ON reports(fetched_at DESC);
CREATE INDEX idx_reports_country ON reports(country);

-- Verify
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('reports', 'posts');

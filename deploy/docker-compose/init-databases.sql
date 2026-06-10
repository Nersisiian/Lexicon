CREATE DATABASE intake;
CREATE DATABASE audit;
CREATE DATABASE review;
\c intake
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY,
    regulator_id TEXT NOT NULL,
    filename TEXT NOT NULL,
    content_type TEXT NOT NULL,
    s3_key_raw TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

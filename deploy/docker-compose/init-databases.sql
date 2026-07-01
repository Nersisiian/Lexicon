CREATE DATABASE intake;
CREATE DATABASE audit;
CREATE DATABASE review;
\c test
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


-- ¬ключаем RLS дл€ таблицы documents
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
CREATE POLICY regulator_isolation ON documents
    USING (regulator_id = current_setting('app.current_regulator_id', true));
ALTER TABLE documents ADD COLUMN tenant_id TEXT NOT NULL DEFAULT 'default';
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON documents USING (tenant_id = current_setting('app.current_tenant')::TEXT);

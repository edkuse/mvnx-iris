CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    ms_id VARCHAR(255) UNIQUE,
    email VARCHAR(255) UNIQUE,
    display_name VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    job_title VARCHAR(255),
    department VARCHAR(255),
    profile_picture TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITHOUT TIME ZONE
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_users_ms_id ON users(ms_id);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

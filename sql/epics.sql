-- Create epics table
CREATE TABLE IF NOT EXISTS epics (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'draft' NOT NULL,
    priority VARCHAR(20) DEFAULT 'low' NOT NULL,
    created_by_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    assigned_to_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    start_date DATE,
    target_date DATE,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    business_value TEXT,
    acceptance_criteria TEXT,
    estimated_effort INTEGER,
    tags_json TEXT DEFAULT '[]'
);

-- Create indexes for faster lookups
CREATE INDEX IF NOT EXISTS idx_epics_status ON epics(status);
CREATE INDEX IF NOT EXISTS idx_epics_priority ON epics(priority);
CREATE INDEX IF NOT EXISTS idx_epics_created_by_id ON epics(created_by_id);
CREATE INDEX IF NOT EXISTS idx_epics_assigned_to_id ON epics(assigned_to_id);

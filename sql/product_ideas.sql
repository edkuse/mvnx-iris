-- Create product idea status enum type
CREATE TYPE product_idea_status_enum AS ENUM ('draft', 'submitted', 'under_review', 'approved', 'rejected', 'implemented');

-- Create priority level enum type
CREATE TYPE priority_level_enum AS ENUM ('low', 'medium', 'high', 'critical');

-- Create impact level enum type
CREATE TYPE impact_level_enum AS ENUM ('minimal', 'moderate', 'significant', 'transformative');

-- Create product_ideas table
CREATE TABLE IF NOT EXISTS product_ideas (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status product_idea_status_enum DEFAULT 'draft',
    priority priority_level_enum DEFAULT 'low',
    impact_level impact_level_enum DEFAULT 'moderate',
    created_by_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    assigned_to_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    target_date TIMESTAMP WITHOUT TIME ZONE,
    business_value TEXT,
    technical_feasibility TEXT,
    estimated_effort INTEGER, -- In hours or story points
    tags TEXT[] -- Array of tags
);

-- Create indexes for faster lookups
CREATE INDEX IF NOT EXISTS idx_product_ideas_status ON product_ideas(status);
CREATE INDEX IF NOT EXISTS idx_product_ideas_priority ON product_ideas(priority);
CREATE INDEX IF NOT EXISTS idx_product_ideas_impact_level ON product_ideas(impact_level);
CREATE INDEX IF NOT EXISTS idx_product_ideas_created_by_id ON product_ideas(created_by_id);
CREATE INDEX IF NOT EXISTS idx_product_ideas_assigned_to_id ON product_ideas(assigned_to_id);
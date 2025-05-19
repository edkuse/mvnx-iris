
-- Create product_ideas table
CREATE TABLE IF NOT EXISTS product_ideas (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'draft' NOT NULL,
    priority VARCHAR(20) DEFAULT 'low' NOT NULL,
    impact_level VARCHAR(20) DEFAULT 'moderate' NOT NULL,
    created_by_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    assigned_to_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    target_date TIMESTAMP WITHOUT TIME ZONE,
    business_value TEXT,
    technical_feasibility TEXT,
    estimated_effort INTEGER, -- In hours or story points
    tags TEXT[], -- Array of tags
    
    -- Add check constraints
    CONSTRAINT check_status_values CHECK (status IN ('draft', 'submitted', 'under_review', 'approved', 'rejected', 'implemented')),
    CONSTRAINT check_priority_values CHECK (priority IN ('low', 'medium', 'high', 'critical')),
    CONSTRAINT check_impact_values CHECK (impact_level IN ('minimal', 'moderate', 'significant', 'transformative'))
);

-- Create indexes for faster lookups
CREATE INDEX IF NOT EXISTS idx_product_ideas_status ON product_ideas(status);
CREATE INDEX IF NOT EXISTS idx_product_ideas_priority ON product_ideas(priority);
CREATE INDEX IF NOT EXISTS idx_product_ideas_impact_level ON product_ideas(impact_level);
CREATE INDEX IF NOT EXISTS idx_product_ideas_created_by_id ON product_ideas(created_by_id);
CREATE INDEX IF NOT EXISTS idx_product_ideas_assigned_to_id ON product_ideas(assigned_to_id);
-- Create permissions
INSERT INTO permissions (resource, action, description)
VALUES
    ('product_idea', 'create', 'Create new product ideas'),
    ('product_idea', 'read', 'View product ideas'),
    ('product_idea', 'update', 'Edit product ideas'),
    ('product_idea', 'delete', 'Delete product ideas');

-- Create roles
INSERT INTO roles (name, description)
VALUES
    ('admin', 'Administrator with full access'),
    ('manager', 'Manager with access to manage most resources'),
    ('developer', 'Developer with limited editing capabilities'),
    ('viewer', 'Viewer with read-only access');

-- Assign permissions to roles
-- Admin role (all permissions)
INSERT INTO role_permissions (role_id, permission_id)
SELECT 
    (SELECT id FROM roles WHERE name = 'admin'),
    id
FROM permissions;

-- Manager role
INSERT INTO role_permissions (role_id, permission_id)
SELECT 
    (SELECT id FROM roles WHERE name = 'manager'),
    id
FROM permissions
WHERE 
    (resource = 'product_idea' AND action IN ('create', 'read', 'update'));

-- Developer role
INSERT INTO role_permissions (role_id, permission_id)
SELECT 
    (SELECT id FROM roles WHERE name = 'developer'),
    id
FROM permissions
WHERE 
    (resource = 'product_idea' AND action IN ('read', 'update'));

-- Viewer role
INSERT INTO role_permissions (role_id, permission_id)
SELECT 
    (SELECT id FROM roles WHERE name = 'viewer'),
    id
FROM permissions
WHERE action = 'read';

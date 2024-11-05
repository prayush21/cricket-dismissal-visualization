INSERT INTO formats (name) VALUES 
    ('ODI'), 
    ('T20'), 
    ('IPL')
ON CONFLICT (name) DO NOTHING;  -- PostgreSQL syntax to avoid duplicates
-- Database Schema for Campus Deployment App
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'PENDING',
    priority VARCHAR(20) DEFAULT 'MEDIUM',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Seed Data
INSERT INTO tasks (title, status, priority) VALUES
('Setup Cloud Database', 'COMPLETED', 'HIGH'),
('Configure Environment Variables & CORS', 'IN_PROGRESS', 'HIGH'),
('Deploy Frontend & Connect API', 'PENDING', 'HIGH');

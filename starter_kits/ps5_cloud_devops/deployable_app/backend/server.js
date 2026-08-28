const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;
const CORS_ORIGIN = process.env.CORS_ORIGIN || '*';

// Middleware
app.use(cors({ origin: CORS_ORIGIN }));
app.use(express.json());

// In-memory / Mock DB data fallback for quick cloud deployment
let tasks = [
  { id: 1, title: 'Setup Cloud Database', status: 'COMPLETED', priority: 'HIGH' },
  { id: 2, title: 'Configure CORS & Environment Variables', status: 'IN_PROGRESS', priority: 'HIGH' },
  { id: 3, title: 'Deploy Frontend to Cloud Service', status: 'PENDING', priority: 'MEDIUM' }
];

// Health Check Endpoint (Crucial for Cloud Deployment Monitoring)
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'UP',
    timestamp: new Date().toISOString(),
    environment: process.env.NODE_ENV || 'development',
    uptime_seconds: process.uptime()
  });
});

// API Routes
app.get('/api/tasks', (req, res) => {
  res.json({ success: true, count: tasks.length, data: tasks });
});

app.post('/api/tasks', (req, res) => {
  const { title, priority } = req.body;
  if (!title) {
    return res.status(400).json({ success: false, error: 'Task title is required' });
  }
  const newTask = {
    id: tasks.length + 1,
    title: title,
    status: 'PENDING',
    priority: priority || 'MEDIUM'
  };
  tasks.push(newTask);
  res.status(201).json({ success: true, data: newTask });
});

app.listen(PORT, () => {
  console.log(`🚀 Backend Server running on port ${PORT}`);
  console.log(`Health Check available at http://localhost:${PORT}/health`);
});

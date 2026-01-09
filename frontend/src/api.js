import axios from 'axios';

// Create axios instance with base URL pointing to FastAPI backend
// In development, we'll use localhost:8000. In production, Nginx will handle proxy /api
const api = axios.create({
    baseURL: import.meta.env.PROD ? '/api/v1' : 'http://localhost:8000/api/v1',
    timeout: 5000,
});

export default api;

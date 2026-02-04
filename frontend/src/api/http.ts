/**
 * Axios HTTP client instance.
 * [Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-FE-T01]
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8005';

export const http = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Response interceptor for error handling
http.interceptors.response.use(
  (response) => response,
  (error) => {
    // Centralized error handling
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export default http;

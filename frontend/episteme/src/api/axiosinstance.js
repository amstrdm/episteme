// src/api/axiosInstance.js

import axios from 'axios';

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;

if (!apiBaseUrl && import.meta.env.PROD) {
  console.warn(
    "VITE_API_BASE_URL environment variable is not set for production build."
  );
}

const apiClient = axios.create({
  baseURL: apiBaseUrl || '',

  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});

export default apiClient;
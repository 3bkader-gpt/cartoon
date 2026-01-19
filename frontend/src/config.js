/**
 * Application Configuration
 * 
 * Centralizes all configuration values to avoid magic strings.
 * Environment variables can override defaults for deployment flexibility.
 */

// Backend API URL - can be overridden via VITE_API_URL environment variable
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

// API endpoints (convenience exports)
export const API_ENDPOINTS = {
    SEASON_STREAM: `${API_BASE_URL}/api/season/stream`,
    LIBRARY: `${API_BASE_URL}/api/library`,
    LIBRARY_TOGGLE: `${API_BASE_URL}/api/library/toggle`,
    LIBRARY_CHECK: `${API_BASE_URL}/api/library/check`,
    SEARCH: `${API_BASE_URL}/api/search`,
    OPEN_DOWNLOADS: `${API_BASE_URL}/api/open-downloads`,
    HEALTH: `${API_BASE_URL}/api/health`,
    PROXY: `${API_BASE_URL}/api/proxy`,
};

// App metadata
export const APP_VERSION = '4.2.0';

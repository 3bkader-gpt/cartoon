/**
 * Application Configuration
 *
 * Centralizes all configuration values to avoid magic strings.
 * Environment variables can override defaults for deployment flexibility.
 */

// Backend API URL
// - Dev default: http://127.0.0.1:8000
// - Prod default: same-origin (works with nginx proxying /api -> backend)
const DEFAULT_API_BASE = (typeof window !== 'undefined' && window.location)
  ? window.location.origin
  : 'http://127.0.0.1:8000';

export const API_BASE_URL = import.meta.env.VITE_API_URL || DEFAULT_API_BASE;

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

// API Configuration
export const API_CONFIG = {
  BASE_URL: process.env.REACT_APP_BACKEND_URL || '',
  ENDPOINTS: {
    LANGUAGES: '/api/languages',
    TEMPLATES: '/api/templates',
    PROJECTS: '/api/projects',
    GENERATE: '/api/generate'
  },
  TIMEOUT: 30000, // 30 seconds
  RETRY_ATTEMPTS: 3
};

// Theme Configuration
export const THEME_CONFIG = {
  STORAGE_KEY: 'theme',
  DEFAULT_THEME: 'light',
  SUPPORTED_THEMES: ['light', 'dark']
};

// UI Configuration
export const UI_CONFIG = {
  ANIMATION_DURATION: 300,
  TOAST_DURATION: 5000,
  LOADING_DELAY: 200,
  DEBOUNCE_DELAY: 300
};

// Project Configuration
export const PROJECT_CONFIG = {
  MAX_NAME_LENGTH: 50,
  MAX_DESCRIPTION_LENGTH: 200,
  MIN_NAME_LENGTH: 3,
  SUPPORTED_LANGUAGES: ['java', 'dotnet'],
  DEFAULT_TEMPLATE_TYPE: 'web'
};

// Validation Rules
export const VALIDATION_RULES = {
  PROJECT_NAME: {
    PATTERN: /^[a-zA-Z0-9-_]+$/,
    MESSAGE: 'Project name can only contain letters, numbers, hyphens, and underscores'
  },
  GITHUB_USERNAME: {
    PATTERN: /^[a-zA-Z0-9-_]+$/,
    MESSAGE: 'GitHub username can only contain letters, numbers, hyphens, and underscores'
  }
};

// Feature Flags
export const FEATURES = {
  DARK_MODE: true,
  ANIMATIONS: true,
  PROGRESS_BAR: true,
  COPY_TO_CLIPBOARD: true,
  STATS_DISPLAY: true,
  RECENT_PROJECTS: true
};

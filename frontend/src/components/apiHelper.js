import { API_BASE_URL } from './config';

const BASE_URL = API_BASE_URL;

let isRefreshing = false;
let refreshSubscribers = [];

function subscribeTokenRefresh(cb) {
  refreshSubscribers.push(cb);
}

function onRefreshed(token) {
  refreshSubscribers.forEach((cb) => cb(token));
  refreshSubscribers = [];
}

async function refreshAccessToken() {
  const refreshToken = localStorage.getItem('refresh_token');
  if (!refreshToken) return null;

  try {
    const response = await fetch(`${BASE_URL}/api/auth/token/refresh/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh: refreshToken }),
    });

    if (response.ok) {
      const data = await response.json();
      localStorage.setItem('access_token', data.access);
      return data.access;
    }
  } catch (error) {
    console.error('CRITICAL: Token refresh network error:', error);
  }

  logout();
  return null;
}

export async function apiFetch(url, options = {}) {
  let token = localStorage.getItem('access_token');

  if (!token) {
    window.location.href = '/login';
    return new Response(null, { status: 401 });
  }

  const headers = {
    ...options.headers,
    Authorization: `Bearer ${token}`,
  };

  if (!(options.body instanceof FormData) && !headers['Content-Type']) {
    headers['Content-Type'] = 'application/json';
  }

  let response = await fetch(url, { ...options, headers });

  if (response.status === 401) {
    if (!isRefreshing) {
      isRefreshing = true;

      const newToken = await refreshAccessToken();

      isRefreshing = false;

      if (newToken) {
        onRefreshed(newToken);
        
        headers.Authorization = `Bearer ${newToken}`;
        return fetch(url, { ...options, headers });
      }
    }

    return new Promise((resolve) => {
      subscribeTokenRefresh((newToken) => {
        headers.Authorization = `Bearer ${newToken}`;
        resolve(fetch(url, { ...options, headers }));
      });
    });
  }

  return response;
}

export function isAuthenticated() {
  const accessToken = localStorage.getItem('access_token');
  const refreshToken = localStorage.getItem('refresh_token');
  return !!(accessToken && refreshToken);
}

export function getCurrentUser() {
  const userStr = localStorage.getItem('user');
  try {
    return userStr ? JSON.parse(userStr) : null;
  } catch (e) {
    return null;
  }
}

export function logout() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('user');
  window.location.href = '/login';
}
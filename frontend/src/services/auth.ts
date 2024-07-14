import store from '../store';
import handleResponse from '../utils/api-utils';
import API_URLS from './apiUrls';

const getAuthToken = (): string | undefined  => {
  const state = store.getState() as { auth: { token: string } }; 
  return state.auth.token;
};

export const apiGet = async (endpoint: string) => {
  const token = getAuthToken() 
  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };


  const response = await fetch(`${API_URLS.AUTH.CREATE_USER}${endpoint}`, {
    method: 'GET',
    headers,
  });

  return handleResponse(response);
};

export const apiPost = async (body: any) => {
  const token = getAuthToken();
  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };

  const response = await fetch(`${API_URLS.AUTH.CREATE_USER}`, {
    method: 'POST',
    headers,
    body: JSON.stringify(body),
  });

  return handleResponse(response);
};

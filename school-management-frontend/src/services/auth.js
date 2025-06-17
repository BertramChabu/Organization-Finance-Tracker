import API from './api';

export const login = async (credentials) => {
  try {
    const response = await API.post('/auth/login/', credentials);
    localStorage.setItem('token', response.data.token);
    return response.data.user;
  } catch (error) {
    throw error.response?.data || error;
  }
};

export const register = async (userData) => {
  try {
    const response = await API.post('/auth/register/', userData);
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
};

export const logout = () => {
  localStorage.removeItem('token');
};

export const getCurrentUser = async () => {
  try {
    const response = await API.get('/auth/me/');
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
};
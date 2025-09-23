import { useState, useCallback } from 'react';
import axios from 'axios';
import { API_CONFIG } from '../config/constants';

const useApi = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const apiCall = useCallback(async (config) => {
    setLoading(true);
    setError(null);

    try {
      const response = await axios({
        ...config,
        baseURL: API_CONFIG.BASE_URL,
        timeout: API_CONFIG.TIMEOUT,
      });
      return response.data;
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'An error occurred';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  const get = useCallback((url, config = {}) => {
    return apiCall({
      method: 'GET',
      url,
      ...config
    });
  }, [apiCall]);

  const post = useCallback((url, data, config = {}) => {
    return apiCall({
      method: 'POST',
      url,
      data,
      ...config
    });
  }, [apiCall]);

  const put = useCallback((url, data, config = {}) => {
    return apiCall({
      method: 'PUT',
      url,
      data,
      ...config
    });
  }, [apiCall]);

  const del = useCallback((url, config = {}) => {
    return apiCall({
      method: 'DELETE',
      url,
      ...config
    });
  }, [apiCall]);

  return {
    loading,
    error,
    get,
    post,
    put,
    delete: del,
    clearError: () => setError(null)
  };
};

export default useApi;

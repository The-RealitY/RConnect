import axios from 'axios';
const TIMEOUT = 60 * 10000;
axios.defaults.timeout = TIMEOUT;

const setupAxiosInterceptors = () => {
  const onRequestSuccess = (config: any) => {
    const token =
      localStorage.getItem('token') || sessionStorage.getItem('token');

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  };

  const onResponseSuccess = (response: any) => response;
  axios.interceptors.request.use(onRequestSuccess);
  axios.interceptors.response.use(onResponseSuccess);
};

export default setupAxiosInterceptors;

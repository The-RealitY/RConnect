const backendUrl = 'http://localhost:5000';
const versionControl = '/api/v1/system';

const API_URLS = {
  AUTH: {
    SIGN_IN_USER: `${backendUrl}${versionControl}/sign-in`,
    CREATE_USER: `${backendUrl}${versionControl}/sign-up`,
    DELETE_USER: `${backendUrl}`,
    UPDATE_USER: `${backendUrl}`,
  },
};

export default API_URLS;

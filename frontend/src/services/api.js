import axios from 'axios';

const api = axios.create({
  baseURL: '/api', // Will be proxied to FastAPI
});

export default api;

// You can also export helpers
export async function generateVideo(prompt) {
  const response = await api.post('/generate', { prompt });
  return response.data;
}

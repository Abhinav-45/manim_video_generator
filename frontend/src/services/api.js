import axios from 'axios';

const api = axios.create({
  baseURL: '/api', 
});

export default api;


export async function generateVideo(prompt) {
  const response = await api.post('/generate', { prompt });
  return response.data;
}

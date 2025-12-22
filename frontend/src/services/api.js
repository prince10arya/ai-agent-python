import axios from 'axios';

const API_BASE_URL = 'http://localhost:8001/api';

export const emailService = {
  sendEmail: (data) => axios.post(`${API_BASE_URL}/emails/send`, data),
  sendDraft: (data) => axios.post(`${API_BASE_URL}/emails/send-draft`, data),
  createDraft: (data) => axios.post(`${API_BASE_URL}/emails/draft`, data),
  getHistory: () => axios.get(`${API_BASE_URL}/emails/history`),
};

export const templateService = {
  getAll: () => axios.get(`${API_BASE_URL}/templates/`),
};

export const ttsService = {
  speak: (data) => axios.post(`${API_BASE_URL}/tts/speak`, data, { responseType: 'blob' }),
};

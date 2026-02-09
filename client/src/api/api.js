import axios from "axios";
import { baseURL } from "../constants";

const api = axios.create({
  baseURL: baseURL,
  timeout: 30000, // 30 seconds timeout
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response;
      if (status === 500) {
        console.error("Server error:", data?.error || "Internal server error");
      } else if (status === 404) {
        console.error("Resource not found:", error.config?.url);
      } else if (status === 413) {
        console.error("File too large");
      }
    } else if (error.request) {
      // Request made but no response received
      console.error("Network error: No response from server");
      error.message = "שגיאת רשת. אנא בדוק את החיבור.";
    } else {
      // Something else happened
      console.error("Error:", error.message);
    }
    return Promise.reject(error);
  }
);

// === Thinker Endpoints ===
export const getThinkers = (lang) => api.get(`/thinkers/${lang}`);

// === Quote Endpoints ===
export const getQuotes = (lang, thinkerKey) =>
  api.get(`/quotes/${lang}/${thinkerKey}`);

export const uploadQuoteFile = (thinker, file) => {
  const formData = new FormData();
  formData.append("file", file);
  return api.post(`/upload/quote-file/${thinker}`, formData);
};

export const uploadSingleQuote = (thinker, quote) =>
  api.post(`/upload/quote/${thinker}`, { quote });

// === Image Endpoints ===
export const getImages = (thinker) => api.get(`/images/${thinker}`);

export const uploadImage = (thinker, imageFile) => {
  const formData = new FormData();
  formData.append("image", imageFile);
  return api.post(`/upload/image/${thinker}`, formData);
};

// === Generate & Download ===
export const generatePreview = (data) => api.post("/generate-preview", data);

export const downloadImage = (filename) =>
  api.get(`/download/${filename}`, { responseType: "blob" });

// === History Management ===
export const getHistory = () => api.get("/history");

export const deleteImage = (filename) => {
  if (filename) {
    return api.delete(`/history/${filename}`);
  }
  return api.delete(`/history`);
};

export default api;

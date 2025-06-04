import axios from "axios";

const api = axios.create({
  baseURL: "http://10.100.102.9:5000", // Adjust if needed
});

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

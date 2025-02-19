import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000"; // FastAPI backend

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await axios.post(`${API_BASE_URL}/upload/`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return response.data;
  } catch (error) {
    console.error("Upload error:", error);
    return { error: "Failed to upload file" };
  }
};

export const searchDocuments = async (query) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/search/`, {
      params: { query },
    });
    return response.data.results;
  } catch (error) {
    console.error("Search error:", error);
    return [];
  }
};

export const chatWithLLM = async (query) => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/chat/", { params: { query } });
    return response.data.response;
  } catch (error) {
    console.error("Chat error:", error);
    return "Error generating response.";
  }
};
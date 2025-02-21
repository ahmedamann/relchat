import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { "Content-Type": "application/json" },
});

/****************************************************************************************
 *                                    USERS                                             *
 * **************************************************************************************/

export const registerUser = async (username, password) => {
  return api.post("/auth/register/", { username, password });
};

export const loginUser = async (username, password) => {
  const response = await api.post("/auth/login/", { username, password });
  if (response.data.access_token) {
    localStorage.setItem("token", response.data.access_token);
  }
  return response.data;
};

export const logoutUser = () => {
  localStorage.removeItem("token");
};

export const isAuthenticated = () => {
  return !!localStorage.getItem("token");
};

/****************************************************************************************
 *                                    CHATS                                             *
 * **************************************************************************************/

export const getConversations = async () => {
  const token = localStorage.getItem("token");
  if (!token) throw new Error("Not authenticated");

  const response = await fetch("http://127.0.0.1:8000/conversations/", {
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  });

  return response.json();
};

export const addMessage = async (conversationId, query, response) => {
  const token = localStorage.getItem("token");
  if (!token) throw new Error("Not authenticated");

  await fetch(`http://127.0.0.1:8000/chat/`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ conversation_id: conversationId, query, response }),
  });
};

export const getChatHistory = async (conversationId) => {
  const token = localStorage.getItem("token");
  if (!token) throw new Error("Not authenticated");

  const response = await fetch(`http://127.0.0.1:8000/chat/history/?conversation_id=${conversationId}`, {
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  });

  return response.json();
};

export const chatWithLLM = async (query, onStreamUpdate, delay = 0) => {
  const token = localStorage.getItem("token");
  if (!token) throw new Error("Not authenticated");
  if (!query.trim()) throw new Error("Query cannot be empty");

  const response = await fetch(`${API_BASE_URL}/chat/?query=${encodeURIComponent(query)}`, {
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  });
  
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let result = "";
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    const chunk = decoder.decode(value, { stream: true });
    result += chunk;
    onStreamUpdate(result);
    if (delay > 0) {
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
  return result;
};

export const deleteConversation = async (conversationId) => {
  const token = localStorage.getItem("token");
  if (!token) throw new Error("Not authenticated");

  await fetch(`http://127.0.0.1:8000/conversations/delete/?conversation_id=${conversationId}`, {
    method: "DELETE",
    headers: {
      "Authorization": `Bearer ${token}`,
    },
  });
};

/****************************************************************************************
 *                                    FILES                                             *
 * **************************************************************************************/

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append("file", file);
  try {
    const response = await api.post("/upload/", formData, {
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
    const response = await api.get("/search/", {
      params: { query },
    });
    return response.data.results;
  } catch (error) {
    console.error("Search error:", error);
    return [];
  }
};

export const getUploadedFiles = async () => {
  const token = localStorage.getItem("token");
  if (!token) throw new Error("Not authenticated");

  const response = await fetch("http://127.0.0.1:8000/files/", {
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  });

  return response.json();
};

export const deleteFile = async (filename) => {
  const token = localStorage.getItem("token");
  if (!token) throw new Error("Not authenticated");

  await fetch(`http://127.0.0.1:8000/files/delete/?filename=${encodeURIComponent(filename)}`, {
    method: "DELETE",
    headers: {
      "Authorization": `Bearer ${token}`,
    },
  });
};


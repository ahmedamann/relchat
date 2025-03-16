import axios from "axios";
import { jwtDecode } from "jwt-decode";

const API_BASE_URL = "http://0.0.0.0:8000";

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
  const token = localStorage.getItem("token");
  if (!token){
    console.log('No token')
    return false;
  } 

  try {
    const decoded = jwtDecode(token);
    if (decoded.exp * 1000 < Date.now()) {
      console.log('Token expired')
      return false;
    }
    return true;
  } catch (error) {
    console.log(`another error: ${error}`)
    return false;
  }
};

/****************************************************************************************
 *                                    CHATS                                             *
 * **************************************************************************************/

export const getConversations = async () => {
  const token = localStorage.getItem("token");
  if (!token) throw new Error("Not authenticated");

  const response = await fetch(`${API_BASE_URL}/conversations/`, {
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch conversations: ${response.status}`);
  }

  return response.json();
};

export const getChatHistory = async (conversationId) => {
  const token = localStorage.getItem("token");
  if (!token) throw new Error("Not authenticated");

  const response = await fetch(`${API_BASE_URL}/chat/history/?conversation_id=${conversationId}`, {
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  });

  return response.json();
};


export const chatWithLLM = async (query, conversationId, onStreamUpdate, delay = 0) => {
  const token = localStorage.getItem("token");
  if (!token) throw new Error("Not authenticated");
  if (!query.trim()) throw new Error("Query cannot be empty");

  // Build query parameters based on whether a conversation exists.
  const conversationParam = conversationId ? `&conversation_id=${conversationId}` : "";
  const newConvoParam = conversationId ? "&new_conversation=false" : "&new_conversation=true";

  const response = await fetch(
    `${API_BASE_URL}/chat/?query=${encodeURIComponent(query)}${conversationParam}${newConvoParam}`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    }
  );
  
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
      await new Promise((resolve) => setTimeout(resolve, delay));
    }
  }
  return result;
};

export const deleteConversation = async (conversationId) => {
  const token = localStorage.getItem("token");
  if (!token) throw new Error("Not authenticated");

  await fetch(`${API_BASE_URL}/conversations/delete/?conversation_id=${conversationId}`, {
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
  const token = localStorage.getItem("token");
  if (!token) throw new Error("Not authenticated");

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await api.post(`${API_BASE_URL}/upload`, formData, {
      headers: { 
        "Authorization": `Bearer ${token}`,
        "Content-Type": "multipart/form-data" 
      },
    });

    return response.data;
  } catch (error) {
    console.error("Upload error:", error);
    return { error: "Failed to upload file" };
  }
};

export const getUploadedFiles = async () => {
  const token = localStorage.getItem("token");
  if (!token) throw new Error("Not authenticated");

  const response = await fetch(`${API_BASE_URL}/files/`, {
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  });

  return response.json();
};


export const deleteDocument = async (fileName) => {
  const token = localStorage.getItem("token");
  if (!token) throw new Error("Not authenticated");

  await fetch(`${API_BASE_URL}/documents/delete/?file_name=${encodeURIComponent(fileName)}`, {
    method: "DELETE",
    headers: {
      "Authorization": `Bearer ${token}`,
    },
  });
};
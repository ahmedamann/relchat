import React, { useState } from "react";
import { chatWithLLM } from "./api";

function App() {
  const [query, setQuery] = useState("");
  const [chatResponse, setChatResponse] = useState("");

  const handleChat = async () => {
    if (!query.trim()) return;
    const response = await chatWithLLM(query);
    setChatResponse(response);
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h2>RAG Chat App</h2>

      <input
        type="text"
        placeholder="Ask something..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button onClick={handleChat}>Chat</button>

      {chatResponse && (
        <div style={{ marginTop: "20px" }}>
          <h3>LLM Response:</h3>
          <p>{chatResponse}</p>
        </div>
      )}
    </div>
  );
}

export default App;
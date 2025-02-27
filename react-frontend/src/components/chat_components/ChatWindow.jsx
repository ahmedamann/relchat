import React, { useEffect, useRef } from "react";
import { Container } from "react-bootstrap";
import "../../styles/ChatWindow.css";
import ReactMarkdown from 'react-markdown';

const ChatWindow = ({ messages }) => {
  const chatRef = useRef(null);

  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <Container ref={chatRef} className="chat-window">
      {messages.length === 0 ? (
        <p className="text-muted text-center">No messages yet. Start chatting!</p>
      ) : (
        messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender === "user" ? "user-message" : "ai-message"}`}>
            <ReactMarkdown>{msg.text}</ReactMarkdown>
          </div>
        ))
      )}
    </Container>
  );
};

export default ChatWindow;
import React from "react";
import { ListGroup, Container } from "react-bootstrap";

const ChatWindow = ({ messages }) => {
  return (
    <Container className="chat-window border rounded p-3 mb-3" style={{ height: "400px", overflowY: "auto" }}>
      <ListGroup>
        {messages.length === 0 ? (
          <p className="text-muted text-center">No messages yet. Start chatting!</p>
        ) : (
          messages.map((msg, index) => (
            <ListGroup.Item key={index} className={msg.sender === "user" ? "text-end" : "text-start"}>
              <strong>{msg.sender === "user" ? "You" : "AI"}:</strong> {msg.text}
            </ListGroup.Item>
          ))
        )}
      </ListGroup>
    </Container>
  );
};

export default ChatWindow;
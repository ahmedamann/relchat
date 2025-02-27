import React, { useState, useEffect, useContext } from "react";
import { chatWithLLM, getChatHistory, getConversations, deleteConversation } from "../api";
import { AuthContext } from "../AuthContext";
import { useNavigate } from "react-router-dom";
import { Container, Row, Col, Card } from "react-bootstrap";
import ChatWindow from "../components/chat_components/ChatWindow";
import ChatInput from "../components/chat_components/ChatInput";
import ConversationList from "../components/chat_components/ConversationList";
import "../styles/Chat.css";

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [conversations, setConversations] = useState([]);
  const [activeConversation, setActiveConversation] = useState(null);
  const { isLoggedIn } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    if (!isLoggedIn) {
      navigate("/login");
    } else {
      fetchConversations();
    }
  }, [isLoggedIn, navigate]);

  const fetchConversations = async () => {
    try {
      const convos = await getConversations();
      setConversations(convos);
    } catch (error) {
      console.error("Failed to load conversations.");
    }
  };

  const fetchChatHistory = async (conversationId) => {
    try {
      const chatHistory = await getChatHistory(conversationId);

      console.log("Fetched chat history:", chatHistory);

      if (chatHistory.length === 0) {
        console.warn("No chat history found for conversation:", conversationId);
      }

      const formattedMessages = chatHistory.flatMap((chat) => [
        { sender: "user", text: chat.query },
        { sender: "ai", text: chat.response }
      ]);

      setMessages(formattedMessages);
      setActiveConversation(conversationId);
    } catch (error) {
      console.error("Failed to load chat history:", error);
    }
  };

  const handleSendMessage = async (message) => {
    if (!message.trim()) return;

    setMessages((prev) => [
      ...prev,
      { sender: "user", text: message },
      { sender: "ai", text: "" }
    ]);

    let conversationId = activeConversation;
    if (!conversationId) {
      conversationId = Date.now();
      setActiveConversation(conversationId);
    }

    await chatWithLLM(message, conversationId, (streamedText) => {
      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = { sender: "ai", text: streamedText };
        return updated;
      });
    });

    fetchConversations();
  };

  const handleDeleteConversation = async (conversationId) => {
    try {
      await deleteConversation(conversationId);
      setConversations((prev) => prev.filter((c) => c.id !== conversationId));

      if (activeConversation === conversationId) {
        setMessages([]);
        setActiveConversation(null);
      }
    } catch (error) {
      console.error("Failed to delete conversation.");
    }
  };

  const handleNewChat = () => {
    setMessages([]);
    setActiveConversation(null);
  };

  return (
    <Container fluid className="chat-container">
      <Row className="h-100">
        <Col xs={12} md={3} className="conversation-list">
          <ConversationList
            conversations={conversations}
            onSelectConversation={fetchChatHistory}
            onDeleteConversation={handleDeleteConversation}
            onNewChat={handleNewChat}
          />
        </Col>

        <Col xs={12} md={9} className="chat-area">
          <Card className="chat-card">
            <Card.Body className="chat-body">
              <ChatWindow messages={messages} />
            </Card.Body>
            <Card.Footer className="chat-input-container">
              <ChatInput onSendMessage={handleSendMessage} />
            </Card.Footer>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Chat;
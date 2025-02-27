import React, { useState, useEffect, useContext } from "react";
import { chatWithLLM, getChatHistory, getConversations, deleteConversation } from "../api";
import { AuthContext } from "../AuthContext";
import { useNavigate } from "react-router-dom";
import { Container, Row, Col, Card } from "react-bootstrap";
import ChatWindow from "../components/ChatWindow";
import ChatInput from "../components/ChatInput";
import ConversationList from "../components/ConversationList";

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
      
      console.log("Fetched chat history:", chatHistory); // Debugging log
  
      if (chatHistory.length === 0) {
        console.warn("No chat history found for conversation:", conversationId);
      }
  
      // Ensure proper message formatting
      const formattedMessages = chatHistory.reduce((acc, chat) => {
        acc.push({ sender: "user", text: chat.query });
        acc.push({ sender: "ai", text: chat.response });
        return acc;
      }, []);
  
      setMessages(formattedMessages);
      setActiveConversation(conversationId);
    } catch (error) {
      console.error("Failed to load chat history:", error);
    }
  };

  const handleSendMessage = async (message) => {
    // Append the user's message and a placeholder for the AI response
    setMessages((prev) => [
      ...prev,
      { sender: "user", text: message },
      { sender: "ai", text: "" }
    ]);
  
    // Ensure we have a conversation ID; if not, create one
    let conversationId = activeConversation;
    if (!conversationId) {
      conversationId = Date.now();
      setActiveConversation(conversationId);
    }
  
    // Stream the AI response token by token and update the placeholder message
    await chatWithLLM(message, conversationId, (streamedText) => {
      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = { sender: "ai", text: streamedText };
        return updated;
      });
    });
  
    // Refresh conversation list if needed
    fetchConversations();
  };



  const handleDeleteConversation = async (conversationId) => {
    try {
      await deleteConversation(conversationId);
      setConversations(conversations.filter((c) => c.id !== conversationId));

      // If the deleted conversation was active, clear the chat window
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
    setActiveConversation(Date.now());
  };

  return (
    <Container fluid className="d-flex" style={{ height: "90vh" }}>
      <ConversationList 
        conversations={conversations} 
        onSelectConversation={fetchChatHistory} 
        onDeleteConversation={handleDeleteConversation} 
        onNewChat={handleNewChat} 
      />
      <Row className="flex-grow-1">
        <Col>
          <Card style={{ height: "85vh" }}>
            <Card.Body>
              <ChatWindow messages={messages} />
              <ChatInput onSendMessage={handleSendMessage} />
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Chat;
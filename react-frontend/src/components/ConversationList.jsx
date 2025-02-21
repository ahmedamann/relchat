import React from "react";
import { ListGroup, Button, Card } from "react-bootstrap";
import { BsTrash } from "react-icons/bs";

const ConversationList = ({ conversations, onSelectConversation, onDeleteConversation, onNewChat }) => {
  return (
    <Card className="conversation-list border-end" style={{ height: "85vh", width: "250px", overflowY: "auto" }}>
      <Card.Body>
        <h5 className="text-center">Conversations</h5>
        <Button variant="primary" className="w-100 mb-3" onClick={onNewChat}>
          New Chat
        </Button>
        <ListGroup>
          {conversations.length === 0 ? (
            <p className="text-muted text-center">No conversations yet.</p>
          ) : (
            conversations.map((conv, index) => (
              <ListGroup.Item 
                key={index} 
                className="d-flex justify-content-between align-items-center"
                action 
                onClick={() => onSelectConversation(conv.id)}
              >
                {conv.title}
                <Button variant="link" className="text-danger p-0 ms-2" onClick={(e) => {
                  e.stopPropagation(); // Prevent selecting conversation
                  onDeleteConversation(conv.id);
                }}>
                  <BsTrash size={16} />  {/* ✅ Updated to use BsTrash */}
                </Button>
              </ListGroup.Item>
            ))
          )}
        </ListGroup>
      </Card.Body>
    </Card>
  );
};

export default ConversationList;
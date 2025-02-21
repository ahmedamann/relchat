import React from "react";
import { Button } from "react-bootstrap";

const ChatControls = ({ onNewChat }) => {
  return (
    <div className="d-flex justify-content-between mt-3">
      <Button variant="danger" onClick={onNewChat}>Start New Conversation</Button>
    </div>
  );
};

export default ChatControls;
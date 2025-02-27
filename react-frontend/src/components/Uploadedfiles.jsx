import React from "react";
import { ListGroup, Button, Card } from "react-bootstrap";
import { BsTrash } from "react-icons/bs";

const UploadedFiles = ({ files, onDelete }) => {
  return (
    <Card className="mt-4" style={{ width: "400px" }}>
      <Card.Body>
        <h3 className="text-center">Uploaded Files</h3>
        {files.length === 0 ? (
          <p className="text-muted text-center">No files uploaded yet.</p>
        ) : (
          <ListGroup>
            {files.map((filename, index) => (
              <ListGroup.Item 
                key={index} 
                className="d-flex justify-content-between align-items-center"
              >
                {filename}
                <Button 
                  variant="link" 
                  className="text-danger p-0" 
                  onClick={(e) => {
                    e.stopPropagation();
                    onDelete(filename);
                  }}
                >
                  <BsTrash size={16} />
                </Button>
              </ListGroup.Item>
            ))}
          </ListGroup>
        )}
      </Card.Body>
    </Card>
  );
};

export default UploadedFiles;
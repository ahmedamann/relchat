import React from "react";
import { ListGroup, Button, Card } from "react-bootstrap";

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
              <ListGroup.Item key={index} className="d-flex justify-content-between align-items-center">
                {filename}
                <Button variant="danger" size="sm" onClick={() => onDelete(filename)}>Delete</Button>
              </ListGroup.Item>
            ))}
          </ListGroup>
        )}
      </Card.Body>
    </Card>
  );
};

export default UploadedFiles;
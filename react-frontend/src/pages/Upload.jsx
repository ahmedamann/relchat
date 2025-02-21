import React, { useState } from "react";
import { Container, Card, Form, Button } from "react-bootstrap";
import UploadedFiles from "../components/Uploadedfiles"; // Import the new component

const Upload = () => {
  const [file, setFile] = useState(null);
  const [files, setFiles] = useState(["example1.pdf", "notes.txt"]); // Static files for now

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = () => {
    if (!file) return;
    // We'll handle actual file upload later
    setFiles([...files, file.name]);
    setFile(null);
  };

  const handleDelete = (filename) => {
    setFiles(files.filter(file => file !== filename)); // Remove file from state
  };

  return (
    <Container className="d-flex flex-column align-items-center" style={{ height: "80vh" }}>
      <Card style={{ width: "400px", padding: "20px" }}>
        <Card.Title className="text-center">Upload a File</Card.Title>
        <Form>
          <Form.Group className="mb-3">
            <Form.Control type="file" onChange={handleFileChange} accept=".pdf,.txt" />
          </Form.Group>
          <Button onClick={handleUpload} variant="primary" className="w-100">Upload</Button>
        </Form>
      </Card>

      {/* Display uploaded files */}
      <UploadedFiles files={files} onDelete={handleDelete} />
    </Container>
  );
};

export default Upload;
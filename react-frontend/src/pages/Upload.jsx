import React, { useState, useEffect } from "react";
import { Container, Card, Form, Button } from "react-bootstrap";
import UploadedFiles from "../components/Uploadedfiles"; 
import { uploadFile, getUploadedFiles, deleteDocument } from "../api"; // ✅ Import API functions

const Upload = () => {
  const [file, setFile] = useState(null);
  const [files, setFiles] = useState([]); // ✅ Empty list initially

  useEffect(() => {
    fetchUploadedFiles();
  }, []);

  const fetchUploadedFiles = async () => {
    try {
      const fetchedFiles = await getUploadedFiles();
      setFiles(fetchedFiles);
    } catch (error) {
      console.error("Failed to load uploaded files.");
    }
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;
    
    try {
      await uploadFile(file);
      fetchUploadedFiles();
      setFile(null);
    } catch (error) {
      console.error("Upload failed.");
    }
  };

  const handleDelete = async (filename) => {
    try {
      await deleteDocument(filename);
      setFiles(files.filter(file => file !== filename));
    } catch (error) {
      console.error("Failed to delete document.");
    }
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
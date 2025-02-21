import React, { useState } from "react";
import { registerUser } from "../api";
import { useNavigate } from "react-router-dom";
import { Form, Button, Card, Container, Alert } from "react-bootstrap";

const Register = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await registerUser(username, password);
      alert("Registered successfully!");
      navigate("/login");
    } catch (error) {
      setError("Registration failed. Username might be taken.");
    }
  };

  return (
    <Container className="d-flex justify-content-center align-items-center" style={{ height: "80vh" }}>
      <Card style={{ width: "400px", padding: "20px" }}>
        <Card.Title className="text-center">Register</Card.Title>
        {error && <Alert variant="danger">{error}</Alert>}
        <Form onSubmit={handleRegister}>
          <Form.Group>
            <Form.Label>Username</Form.Label>
            <Form.Control type="text" placeholder="Enter username" onChange={(e) => setUsername(e.target.value)} required />
          </Form.Group>
          <Form.Group>
            <Form.Label>Password</Form.Label>
            <Form.Control type="password" placeholder="Enter password" onChange={(e) => setPassword(e.target.value)} required />
          </Form.Group>
          <Button type="submit" variant="success" className="w-100 mt-3">Register</Button>
        </Form>
        <p className="mt-3 text-center">
          Already have an account? <a href="/login">Login</a>
        </p>
      </Card>
    </Container>
  );
};

export default Register;
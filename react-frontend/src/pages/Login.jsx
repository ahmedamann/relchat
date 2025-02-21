import React, { useState, useContext } from "react";
import { loginUser } from "../api";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../AuthContext";
import { Form, Button, Card, Container, Alert } from "react-bootstrap";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { setIsLoggedIn } = useContext(AuthContext);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await loginUser(username, password);
      setIsLoggedIn(true);
      navigate("/chat");
    } catch (error) {
      setError("Invalid username or password. Please try again.");
    }
  };

  return (
    <Container className="d-flex justify-content-center align-items-center" style={{ height: "80vh" }}>
      <Card style={{ width: "400px", padding: "20px" }}>
        <Card.Title className="text-center">Login</Card.Title>
        {error && <Alert variant="danger">{error}</Alert>}
        <Form onSubmit={handleLogin}>
          <Form.Group>
            <Form.Label>Username</Form.Label>
            <Form.Control type="text" placeholder="Enter username" onChange={(e) => setUsername(e.target.value)} required />
          </Form.Group>
          <Form.Group>
            <Form.Label>Password</Form.Label>
            <Form.Control type="password" placeholder="Enter password" onChange={(e) => setPassword(e.target.value)} required />
          </Form.Group>
          <Button type="submit" variant="primary" className="w-100 mt-3">Login</Button>
        </Form>
        <p className="mt-3 text-center">
          Don't have an account? <a href="/register">Register</a>
        </p>
      </Card>
    </Container>
  );
};

export default Login;
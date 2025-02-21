import React, { useContext } from "react";
import { Nav, Navbar, Container, Button } from "react-bootstrap";
import { AuthContext } from "../AuthContext";

const NavigationBar = () => {
  const { isLoggedIn, logout } = useContext(AuthContext);

  return (
    <Navbar bg="dark" variant="dark" expand="lg">
      <Container>
        <Navbar.Brand href="/">RelChat</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            {isLoggedIn ? (
              <>
                <Nav.Link href="/chat">Chat</Nav.Link>
                <Nav.Link href="/upload">Upload Files</Nav.Link>
                <Button variant="outline-light" onClick={logout} className="ms-2">
                  Logout
                </Button>
              </>
            ) : (
              <>
                <Nav.Link href="/login">Login</Nav.Link>
                <Nav.Link href="/register">Register</Nav.Link>
              </>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default NavigationBar;
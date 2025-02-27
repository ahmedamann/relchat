import React, { useContext } from "react";
import { Navbar, Nav, Container, Button } from "react-bootstrap";
import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from "../AuthContext";
import { BsChatDots, BsCloudUpload, BsPerson, BsBoxArrowRight, BsBoxArrowInRight } from "react-icons/bs";
import "../styles/Navbar.css";

const NavigationBar = () => {
  const { isLoggedIn, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <Navbar expand="lg" className="navbar-custom">
      <Container>
        <Navbar.Brand as={Link} to="/" className="fw-bold fs-4">
          <span className="brand-gradient">RelChat</span>
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="navbar-nav" />
        <Navbar.Collapse id="navbar-nav">
          <Nav className="ms-auto align-items-center">
            {isLoggedIn ? (
              <>
                <Nav.Link as={Link} to="/chat" className="nav-item">
                  <BsChatDots className="nav-icon" /> Chat
                </Nav.Link>
                <Nav.Link as={Link} to="/upload" className="nav-item">
                  <BsCloudUpload className="nav-icon" /> Upload Files
                </Nav.Link>
                <Button variant="outline-light" className="nav-btn" onClick={handleLogout}>
                  <BsBoxArrowRight className="nav-icon" /> Logout
                </Button>
              </>
            ) : (
              <>
                <Nav.Link as={Link} to="/login" className="nav-item">
                  <BsBoxArrowInRight className="nav-icon" /> Login
                </Nav.Link>
                <Nav.Link as={Link} to="/register" className="nav-item">
                  <BsPerson className="nav-icon" /> Register
                </Nav.Link>
              </>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default NavigationBar;
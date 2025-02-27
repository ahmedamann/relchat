import React from "react";
import { Outlet } from "react-router-dom";
import NavigationBar from "./components/Navbar";
import { Container } from "react-bootstrap";
import "./styles/Background.css";

const App = () => {
  return (
    <div className="app-background">
      <NavigationBar />
      <Container className="app-content">
        <Outlet />
      </Container>
    </div>
  );
};

export default App;
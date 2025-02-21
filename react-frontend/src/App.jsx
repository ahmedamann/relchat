import React from "react";
import { Outlet } from "react-router-dom";
import NavigationBar from "./components/Navbar";
import { Container } from "react-bootstrap";

const App = () => {
  return (
    <>
      <NavigationBar />
      <Container className="mt-4">
        <Outlet />
      </Container>
    </>
  );
};

export default App;
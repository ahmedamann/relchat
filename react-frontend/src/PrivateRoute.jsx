import React from "react";
import { Navigate, Outlet } from "react-router-dom";
import { isAuthenticated } from "./api";
import { AuthProvider, AuthContext } from "./AuthContext.jsx";

const PrivateRoute = () => {
  const { isLoggedIn } = React.useContext(AuthContext);
  if (!isAuthenticated() || !isLoggedIn) {
    return <Navigate to="/login" />;
  }
  return <Outlet />;
};

export default PrivateRoute;
import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import ReactDOM from "react-dom/client";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, AuthContext } from "./AuthContext.jsx";
import App from "./App";
import Chat from "./pages/Chat";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Upload from "./pages/Upload";

const ProtectedRoute = ({ children }) => {
  const { isLoggedIn } = React.useContext(AuthContext);
  return isLoggedIn ? children : <Navigate to="/login" />;
};

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<App />}>
            <Route path="login" element={<Login />} />
            <Route path="register" element={<Register />} />
            <Route path="chat" element={<ProtectedRoute><Chat /></ProtectedRoute>} />
            <Route path="upload" element={<ProtectedRoute><Upload /></ProtectedRoute>} />
            <Route path="*" element={<Navigate to="/" />} />
          </Route>
        </Routes>
      </Router>
    </AuthProvider>
  </React.StrictMode>
);
import React from "react";
import { Routes, Route, Navigate, Link, useNavigate } from "react-router-dom";
import LoginPage from "./LoginPage";
import IssueListPage from "./IssueListPage";
import IssueFormPage from "./IssueFormPage";
import DashboardPage from "./DashboardPage";

function getToken() {
  return localStorage.getItem("authToken");
}

function ProtectedRoute({ children }) {
  const token = getToken();
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  return children;
}

function Layout({ children }) {
  const navigate = useNavigate();
  const token = getToken();

  const logout = () => {
    localStorage.removeItem("authToken");
    navigate("/login");
  };

  return (
    <div className="app-shell">
      <header className="top-bar">
        <div className="logo">ZOLITS</div>
        {token && (
          <nav className="nav">
            <Link to="/dashboard">Dashboard</Link>
            <Link to="/issues">Issues</Link>
            <button onClick={logout} className="link-button">
              Logout
            </button>
          </nav>
        )}
      </header>
      <main className="content">{children}</main>
    </div>
  );
}

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <DashboardPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/issues"
          element={
            <ProtectedRoute>
              <IssueListPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/issues/new"
          element={
            <ProtectedRoute>
              <IssueFormPage />
            </ProtectedRoute>
          }
        />
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </Layout>
  );
}


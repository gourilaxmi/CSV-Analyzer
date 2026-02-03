import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Register from './components/Register';
import Login from './components/Login';
import ForgotPassword from './components/ForgotPassword';
import MainPage from './components/MainPage';
import Downloads from './components/Downloads';
import './App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    const userData = localStorage.getItem('user');
    
    if (token && userData) {
      setIsAuthenticated(true);
      setUser(JSON.parse(userData));
    }
  }, []);

  const handleLogin = (userData, tokens) => {
    localStorage.setItem('access_token', tokens.access);
    localStorage.setItem('refresh_token', tokens.refresh);
    localStorage.setItem('user', JSON.stringify(userData));
    setIsAuthenticated(true);
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    setIsAuthenticated(false);
    setUser(null);
  };

  return (
    <Router>
      <Routes>
        <Route 
          path="/register" 
          element={
            isAuthenticated ? 
            <Navigate to="/main" /> : 
            <Register onLogin={handleLogin} />
          } 
        />
        <Route 
          path="/login" 
          element={
            isAuthenticated ? 
            <Navigate to="/main" /> : 
            <Login onLogin={handleLogin} />
          } 
        />
        <Route 
          path="/forgot-password" 
          element={
            isAuthenticated ? 
            <Navigate to="/main" /> : 
            <ForgotPassword />
          } 
        />
        <Route 
          path="/main" 
          element={
            isAuthenticated ? 
            <MainPage user={user} onLogout={handleLogout} /> : 
            <Navigate to="/login" />
          } 
        />
        <Route 
          path="/downloads" 
          element={
            isAuthenticated ? 
            <Downloads user={user} onLogout={handleLogout} /> : 
            <Navigate to="/login" />
          } 
        />

        <Route path="/" element={<Navigate to={isAuthenticated ? "/main" : "/login"} />} />
      </Routes>
    </Router>
  );
}

export default App;
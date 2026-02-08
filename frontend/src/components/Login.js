import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Login.css';

const Login = ({ onLogin }) => {
  const navigate = useNavigate();

  const [credentials, setCredentials] = useState({
    login_id: '',
    password: '',
  });

  const [ui, setUi] = useState({
    isLoading: false,
    errors: {},
    serverError: ''
  });

  const onChange = (e) => {
    const { name, value } = e.target;
    setCredentials(prev => ({ ...prev, [name]: value }));
    
    if (ui.errors[name]) {
      setUi(prev => ({
        ...prev,
        errors: { ...prev.errors, [name]: '' }
      }));
    }
  };

  const validate = () => {
    const newErrors = {};
    if (!credentials.login_id.trim()) newErrors.login_id = 'Username or Email is required.';
    if (!credentials.password) newErrors.password = 'Password is required.';
    return newErrors;
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    
    const validationErrors = validate();
    if (Object.keys(validationErrors).length > 0) {
      setUi(prev => ({ ...prev, errors: validationErrors }));
      return;
    }

    setUi(prev => ({ ...prev, isLoading: true, serverError: '' }));

    try {
      const response = await fetch('http://localhost:8000/api/auth/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials),
      });

      const data = await response.json();

      if (response.ok) {
        onLogin(data.user, { 
          access: data.tokens.access, 
          refresh: data.tokens.refresh 
        });
        navigate('/main');
      } else {
        setUi(prev => ({
          ...prev,
          serverError: data.error || 'Check your credentials and try again.'
        }));
      }
    } catch (err) {
      console.error("Auth Exception:", err);
      setUi(prev => ({
        ...prev,
        serverError: 'Service unavailable. Please try again later.'
      }));
    } finally {
      setUi(prev => ({ ...prev, isLoading: false }));
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <header className="login-header">
          <h1>CSV Data Analysis System</h1>
        </header>

        <main className="login-content">
          <div className="login-card">
            <div className="card-header">
              <h2>Welcome Back</h2>
              <p>Sign in to your dashboard</p>
            </div>

            {ui.serverError && (
              <div className="error-banner" role="alert">
                {ui.serverError}
              </div>
            )}

            <form className="login-form" onSubmit={onSubmit} noValidate>
              <div className="form-group">
                <label htmlFor="login_id">Username or Email</label>
                <input
                  type="text"
                  id="login_id"
                  name="login_id"
                  placeholder="Enter username or email"
                  value={credentials.login_id}
                  onChange={onChange}
                  className={ui.errors.login_id ? 'input-error' : ''}
                  autoComplete="username"
                />
                {ui.errors.login_id && <span className="error-text">{ui.errors.login_id}</span>}
              </div>

              <div className="form-group">
                <label htmlFor="password">Password</label>
                <input
                  type="password"
                  id="password"
                  name="password"
                  placeholder="Enter your password"
                  value={credentials.password}
                  onChange={onChange}
                  className={ui.errors.password ? 'input-error' : ''}
                  autoComplete="current-password"
                />
                {ui.errors.password && <span className="error-text">{ui.errors.password}</span>}
              </div>

              <div className="forgot-password-link">
                <button 
                  type="button" 
                  className="link-style-btn"
                  onClick={() => navigate('/forgot-password')}
                >
                  Forgot password?
                </button>
              </div>

              <button 
                type="submit" 
                className="login-btn" 
                disabled={ui.isLoading}
              >
                {ui.isLoading ? 'Verifying...' : 'Sign In'}
              </button>
            </form>

            <footer className="register-sec">
              <p>Don't have an account? 
                <button className="link-style-btn" onClick={() => navigate('/register')}>
                  Register here
                </button>
              </p>
            </footer>
          </div>
        </main>
      </div>
    </div>
  );
};

export default Login;
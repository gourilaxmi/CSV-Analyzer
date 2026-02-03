import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Login.css';

function Login({ onLogin }) {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });

  const navigate = useNavigate();
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevState) => ({
      ...prevState,
      [name]: value,
    }));

    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.username.trim())
      newErrors.username = 'Username is required';
    if (!formData.password)
      newErrors.password = 'Password is required';

    return newErrors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const validationErrors = validateForm();
    
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/auth/token/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: formData.username,
          password: formData.password,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        // Fetch user profile
        const profileResponse = await fetch('http://localhost:8000/api/auth/profile/', {
          headers: {
            'Authorization': `Bearer ${data.access}`,
          },
        });

        const userData = await profileResponse.json();
        
        onLogin(userData, { access: data.access, refresh: data.refresh });
        navigate('/main');
      } else {
        setErrors({ general: 'Invalid username or password' });
      }
    } catch (error) {
      console.error('Login error:', error);
      setErrors({ general: 'Something went wrong. Please try again.' });
    } finally {
      setIsLoading(false);
    }
  };

  const handleGoToRegister = () => {
    navigate('/register');
  };

  const handleForgotPassword = () => {
    navigate('/forgot-password');
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-header">
          <div className="login-logo">
            <h1>CSV Data Analysis System</h1>
          </div>
        </div>

        <div className="login-content">
          <div className="login-card">
            <div className="card-header">
              <h2>Welcome Back</h2>
              <p>Sign in to access your data analysis dashboard</p>
            </div>

            {errors.general && (
              <div className="error-banner">
                {errors.general}
              </div>
            )}

            <form className="login-form" onSubmit={handleSubmit}>
              <div className="form-group">
                <label htmlFor="username">Username</label>
                <input
                  type="text"
                  id="username"
                  name="username"
                  value={formData.username}
                  onChange={handleChange}
                  className={errors.username ? 'error' : ''}
                  placeholder="Enter your username"
                />
                {errors.username && (
                  <span className="error-message">{errors.username}</span>
                )}
              </div>

              <div className="form-group">
                <label htmlFor="password">Password</label>
                <input
                  type="password"
                  id="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  className={errors.password ? 'error' : ''}
                  placeholder="Enter your password"
                />
                {errors.password && (
                  <span className="error-message">{errors.password}</span>
                )}
              </div>

              <div style={{ textAlign: 'right', marginTop: '-0.5rem' }}>
                <button 
                  type="button" 
                  onClick={handleForgotPassword} 
                  className="link-btn"
                  style={{ fontSize: '0.875rem' }}
                >
                  Forgot password?
                </button>
              </div>

              <div className="form-actions">
                <button
                  type="submit"
                  className="login-btn"
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <>
                      <span className="spinner"></span>
                      Signing In...
                    </>
                  ) : (
                    'Sign In'
                  )}
                </button>
              </div>
            </form>

            <div className="register-link">
              <p>
                Don't have an account?{' '}
                <button onClick={handleGoToRegister} className="link-btn">
                  Register here
                </button>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
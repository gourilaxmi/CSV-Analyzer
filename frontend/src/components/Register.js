import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Register.css';

const Register = ({ onLogin }) => {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    username: '',
    email: '',
    firstName: '',
    lastName: '',
    password: '',
    password2: '',
    agreeToTerms: false,
  });

  const [ui, setUi] = useState({
    isLoading: false,
    errors: {},
  });

  const onChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));

    if (ui.errors[name]) {
      setUi((prev) => ({
        ...prev,
        errors: { ...prev.errors, [name]: '' },
      }));
    }
  };

  const validate = () => {
    const newErrors = {};
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!formData.username.trim()) newErrors.username = 'Username is required';
    if (!formData.firstName.trim()) newErrors.firstName = 'First name is required';
    if (!formData.lastName.trim()) newErrors.lastName = 'Last name is required';
    
    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!emailRegex.test(formData.email)) {
      newErrors.email = 'Invalid email format';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    }

    if (formData.password !== formData.password2) {
      newErrors.password2 = 'Passwords do not match';
    }

    if (!formData.agreeToTerms) {
      newErrors.agreeToTerms = 'You must agree to the terms';
    }

    return newErrors;
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    const validationErrors = validate();
    
    if (Object.keys(validationErrors).length > 0) {
      setUi(prev => ({ ...prev, errors: validationErrors }));
      return;
    }

    setUi(prev => ({ ...prev, isLoading: true }));

    try {
      const response = await fetch('http://localhost:8000/api/auth/register/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: formData.username,
          email: formData.email,
          first_name: formData.firstName,
          last_name: formData.lastName,
          password: formData.password,
          password2: formData.password2,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        onLogin(data.user, data.tokens);
        navigate('/main');
      } else {
        const backendErrors = {};
        Object.keys(data).forEach(key => {
          backendErrors[key] = Array.isArray(data[key]) ? data[key][0] : data[key];
        });
        setUi(prev => ({ ...prev, errors: backendErrors }));
      }
    } catch (error) {
      console.error('Registration error:', error);
      alert('Network error. Please try again later.');
    } finally {
      setUi(prev => ({ ...prev, isLoading: false }));
    }
  };

  return (
    <div className="register-page">
      <div className="register-container">
        <header className="register-header">
          <h1>CSV Data Analysis System</h1>
        </header>

        <main className="register-content">
          <div className="register-card">
            <div className="card-header">
              <h2>Create Your Account</h2>
              <p>Join us to start analyzing your data</p>
            </div>

            <form className="register-form" onSubmit={onSubmit} noValidate>
              <section className="form-section">
                <h3>Personal Details</h3>
                
                <div className="form-group">
                  <label htmlFor="username">Username</label>
                  <input
                    type="text"
                    id="username"
                    name="username"
                    value={formData.username}
                    onChange={onChange}
                    className={ui.errors.username ? 'input-error' : ''}
                    placeholder="juser123"
                  />
                  {ui.errors.username && <span className="error-text">{ui.errors.username}</span>}
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="firstName">First Name</label>
                    <input
                      type="text"
                      id="firstName"
                      name="firstName"
                      value={formData.firstName}
                      onChange={onChange}
                      className={ui.errors.firstName ? 'input-error' : ''}
                    />
                    {ui.errors.firstName && <span className="error-text">{ui.errors.firstName}</span>}
                  </div>

                  <div className="form-group">
                    <label htmlFor="lastName">Last Name</label>
                    <input
                      type="text"
                      id="lastName"
                      name="lastName"
                      value={formData.lastName}
                      onChange={onChange}
                      className={ui.errors.lastName ? 'input-error' : ''}
                    />
                    {ui.errors.lastName && <span className="error-text">{ui.errors.lastName}</span>}
                  </div>
                </div>

                <div className="form-group">
                  <label htmlFor="email">Email Address</label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={onChange}
                    className={ui.errors.email ? 'input-error' : ''}
                    placeholder="user@example.com"
                  />
                  {ui.errors.email && <span className="error-text">{ui.errors.email}</span>}
                </div>
              </section>

              <section className="form-section">
                <h3>Security</h3>
                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="password">Password</label>
                    <input
                      type="password"
                      id="password"
                      name="password"
                      value={formData.password}
                      onChange={onChange}
                      className={ui.errors.password ? 'input-error' : ''}
                      autoComplete="new-password"
                    />
                    {ui.errors.password && <span className="error-text">{ui.errors.password}</span>}
                  </div>

                  <div className="form-group">
                    <label htmlFor="password2">Confirm</label>
                    <input
                      type="password"
                      id="password2"
                      name="password2"
                      value={formData.password2}
                      onChange={onChange}
                      className={ui.errors.password2 ? 'input-error' : ''}
                      autoComplete="new-password"
                    />
                    {ui.errors.password2 && <span className="error-text">{ui.errors.password2}</span>}
                  </div>
                </div>
              </section>

              <div className="checkbox-section">
                <label className="custom-checkbox">
                  <input
                    type="checkbox"
                    name="agreeToTerms"
                    checked={formData.agreeToTerms}
                    onChange={onChange}
                  />
                  <span>I agree to the Terms & Privacy Policy</span>
                </label>
                {ui.errors.agreeToTerms && <span className="error-text">{ui.errors.agreeToTerms}</span>}
              </div>

              <button type="submit" className="register-btn" disabled={ui.isLoading}>
                {ui.isLoading ? 'Creating Account...' : 'Register'}
              </button>
            </form>

            <footer className="login-sec">
              <p>Already have an account? 
                <button className="link-style-btn" onClick={() => navigate('/login')}>
                  Sign in
                </button>
              </p>
            </footer>
          </div>
        </main>
      </div>
    </div>
  );
};

export default Register;
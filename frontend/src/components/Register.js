import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Register.css';

function Register({ onLogin }) {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    firstName: '',
    lastName: '',
    password: '',
    password2: '',
    agreeToTerms: false,
  });

  const navigate = useNavigate();
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prevState) => ({
      ...prevState,
      [name]: type === 'checkbox' ? checked : value,
    }));

    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.username.trim())
      newErrors.username = 'Username is required';
    if (!formData.firstName.trim())
      newErrors.firstName = 'First name is required';
    if (!formData.lastName.trim())
      newErrors.lastName = 'Last name is required';
    if (!formData.email.trim())
      newErrors.email = 'Email is required';
    if (!formData.password)
      newErrors.password = 'Password is required';
    if (!formData.password2)
      newErrors.password2 = 'Please confirm password';

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (formData.email && !emailRegex.test(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }

    if (formData.password && formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters long';
    }

    if (formData.password !== formData.password2) {
      newErrors.password2 = 'Passwords do not match';
    }

    if (!formData.agreeToTerms) {
      newErrors.agreeToTerms = 'You must agree to the terms and conditions';
    }

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
        alert('Registration successful!');
        onLogin(data.user, data.tokens);
        navigate('/main');
      } else {
        const errorMessages = {};
        Object.keys(data).forEach(key => {
          if (Array.isArray(data[key])) {
            errorMessages[key] = data[key][0];
          } else {
            errorMessages[key] = data[key];
          }
        });
        setErrors(errorMessages);
      }
    } catch (error) {
      console.error('Registration error:', error);
      alert('Something went wrong. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleGoToLogin = () => {
    navigate('/login');
  };

  return (
    <div className="register-page">
      <div className="register-container">
        <div className="register-header">
          <div className="register-logo">
            <h1>Screening Task</h1>
          </div>
        </div>

        <div className="register-content">
          <div className="register-card">
            <div className="card-header">
              <h2>Create Your Account</h2>
            </div>

            <form className="register-form" onSubmit={handleSubmit}>
              <div className="form-section">
                <h3>Personal Information</h3>
                
                <div className="form-group">
                  <label htmlFor="username">Username *</label>
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

                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="firstName">First Name *</label>
                    <input
                      type="text"
                      id="firstName"
                      name="firstName"
                      value={formData.firstName}
                      onChange={handleChange}
                      className={errors.firstName ? 'error' : ''}
                      placeholder="Enter your first name"
                    />
                    {errors.firstName && (
                      <span className="error-message">{errors.firstName}</span>
                    )}
                  </div>

                  <div className="form-group">
                    <label htmlFor="lastName">Last Name *</label>
                    <input
                      type="text"
                      id="lastName"
                      name="lastName"
                      value={formData.lastName}
                      onChange={handleChange}
                      className={errors.lastName ? 'error' : ''}
                      placeholder="Enter your last name"
                    />
                    {errors.lastName && (
                      <span className="error-message">{errors.lastName}</span>
                    )}
                  </div>
                </div>

                <div className="form-group">
                  <label htmlFor="email">Email Address *</label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    className={errors.email ? 'error' : ''}
                    placeholder="Enter your email address"
                  />
                  {errors.email && (
                    <span className="error-message">{errors.email}</span>
                  )}
                </div>
              </div>

              <div className="form-section">
                <h3>Security</h3>
                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="password">Password *</label>
                    <input
                      type="password"
                      id="password"
                      name="password"
                      value={formData.password}
                      onChange={handleChange}
                      className={errors.password ? 'error' : ''}
                      placeholder="Create a strong password"
                    />
                    {errors.password && (
                      <span className="error-message">{errors.password}</span>
                    )}
                  </div>

                  <div className="form-group">
                    <label htmlFor="password2">Confirm Password *</label>
                    <input
                      type="password"
                      id="password2"
                      name="password2"
                      value={formData.password2}
                      onChange={handleChange}
                      className={errors.password2 ? 'error' : ''}
                      placeholder="Confirm your password"
                    />
                    {errors.password2 && (
                      <span className="error-message">{errors.password2}</span>
                    )}
                  </div>
                </div>
              </div>

              <div className="form-section">
                <div className="checkbox-group">
                  <label className="checkbox-label">
                    <input
                      type="checkbox"
                      name="agreeToTerms"
                      checked={formData.agreeToTerms}
                      onChange={handleChange}
                    />
                    <span className="checkmark"></span>
                    I agree to the{' '}
                    <a href="#" className="link">
                      Terms and Conditions
                    </a>{' '}
                    and{' '}
                    <a href="#" className="link">
                      Privacy Policy
                    </a>{' '}
                    *
                  </label>
                  {errors.agreeToTerms && (
                    <span className="error-message">{errors.agreeToTerms}</span>
                  )}
                </div>
              </div>

              <div className="form-actions">
                <button
                  type="submit"
                  className="register-btn"
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <>
                      <span className="spinner"></span>
                      Creating Account...
                    </>
                  ) : (
                    'Create Account'
                  )}
                </button>
              </div>
            </form>

            <div className="login-link">
              <p>
                Already have an account?{' '}
                <button onClick={handleGoToLogin} className="link-btn">
                  Sign in here
                </button>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Register;
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './ForgotPassword.css';

function ForgotPassword() {
  const [username, setUsername] = useState('');
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [showResetModal, setShowResetModal] = useState(false);
  const [resetData, setResetData] = useState({
    newPassword: '',
    confirmPassword: '',
  });
  const navigate = useNavigate();

  const handleUsernameSubmit = async (e) => {
    e.preventDefault();
    
    if (!username.trim()) {
      setErrors({ username: 'Username is required' });
      return;
    }

    setIsLoading(true);
    setErrors({});

    try {
      const response = await fetch('http://localhost:8000/api/auth/password-reset-request/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username }),
      });

      const data = await response.json();

      if (response.ok) {
        // Show the reset modal
        setShowResetModal(true);
      } else {
        setErrors({ general: data.error || 'Username not found' });
      }
    } catch (error) {
      console.error('Password reset request error:', error);
      setErrors({ general: 'Something went wrong. Please try again.' });
    } finally {
      setIsLoading(false);
    }
  };

  const handlePasswordReset = async (e) => {
    e.preventDefault();
    
    const newErrors = {};
    
    if (!resetData.newPassword) {
      newErrors.newPassword = 'Password is required';
    } else if (resetData.newPassword.length < 8) {
      newErrors.newPassword = 'Password must be at least 8 characters';
    }
    
    if (!resetData.confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your password';
    } else if (resetData.newPassword !== resetData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setIsLoading(true);
    setErrors({});

    try {
      const response = await fetch('http://localhost:8000/api/auth/password-reset-confirm/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username,
          new_password: resetData.newPassword,
          new_password2: resetData.confirmPassword,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        alert('Password reset successful! You can now login with your new password.');
        navigate('/login');
      } else {
        setErrors({ general: data.error || 'Failed to reset password' });
      }
    } catch (error) {
      console.error('Password reset error:', error);
      setErrors({ general: 'Something went wrong. Please try again.' });
    } finally {
      setIsLoading(false);
    }
  };

  const handleResetDataChange = (e) => {
    const { name, value } = e.target;
    setResetData((prev) => ({
      ...prev,
      [name]: value,
    }));
    
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  return (
    <div className="forgot-password-page">
      <div className="forgot-password-container">
        <div className="forgot-password-header">
          <div className="forgot-password-logo">
            <h1>CSV Data Analysis System</h1>
          </div>
        </div>

        <div className="forgot-password-card">
          <div className="card-header">
            <h2>Reset Password</h2>
            <p>Enter your username to reset your password</p>
          </div>

          {errors.general && (
            <div className="error-banner">
              {errors.general}
            </div>
          )}

          <form className="forgot-password-form" onSubmit={handleUsernameSubmit}>
            <div className="form-group">
              <label htmlFor="username">Username</label>
              <input
                type="text"
                id="username"
                name="username"
                value={username}
                onChange={(e) => {
                  setUsername(e.target.value);
                  if (errors.username) {
                    setErrors((prev) => ({ ...prev, username: '' }));
                  }
                }}
                className={errors.username ? 'error' : ''}
                placeholder="Enter your username"
              />
              {errors.username && (
                <span className="error-message">{errors.username}</span>
              )}
            </div>

            <div className="form-actions">
              <button
                type="submit"
                className="reset-btn"
                disabled={isLoading}
              >
                {isLoading ? (
                  <>
                    <span className="spinner"></span>
                    Processing...
                  </>
                ) : (
                  'Continue'
                )}
              </button>
            </div>
          </form>

          <div className="back-to-login">
            <p>
              Remember your password?{' '}
              <button onClick={() => navigate('/login')} className="link-btn">
                Back to Login
              </button>
            </p>
          </div>
        </div>
      </div>

      {/* Password Reset Modal */}
      {showResetModal && (
        <div className="modal-overlay" onClick={() => setShowResetModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Set New Password</h3>
              <button className="close-btn" onClick={() => setShowResetModal(false)}>
                ✕
              </button>
            </div>

            {errors.general && (
              <div className="error-banner">
                {errors.general}
              </div>
            )}

            <form className="modal-body" onSubmit={handlePasswordReset}>
              <div className="form-group">
                <label htmlFor="newPassword">New Password</label>
                <input
                  type="password"
                  id="newPassword"
                  name="newPassword"
                  value={resetData.newPassword}
                  onChange={handleResetDataChange}
                  className={errors.newPassword ? 'error' : ''}
                  placeholder="Enter new password"
                />
                {errors.newPassword && (
                  <span className="error-message">{errors.newPassword}</span>
                )}
              </div>

              <div className="form-group">
                <label htmlFor="confirmPassword">Confirm Password</label>
                <input
                  type="password"
                  id="confirmPassword"
                  name="confirmPassword"
                  value={resetData.confirmPassword}
                  onChange={handleResetDataChange}
                  className={errors.confirmPassword ? 'error' : ''}
                  placeholder="Confirm new password"
                />
                {errors.confirmPassword && (
                  <span className="error-message">{errors.confirmPassword}</span>
                )}
              </div>

              <button
                type="submit"
                className="reset-btn"
                disabled={isLoading}
              >
                {isLoading ? (
                  <>
                    <span className="spinner"></span>
                    Resetting...
                  </>
                ) : (
                  'Reset Password'
                )}
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default ForgotPassword;
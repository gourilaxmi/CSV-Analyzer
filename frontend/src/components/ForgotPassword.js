import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './ForgotPassword.css';

const ForgotPassword = () => {
  const navigate = useNavigate();

  const [ui, setUi] = useState({
    isLoading: false,
    errors: {},
    showResetModal: false
  });

  const [loginId, setLoginId] = useState('');
  
  const [resetData, setResetData] = useState({
    newPassword: '',
    confirmPassword: '',
  });

  const onChange = (e) => {
    setLoginId(e.target.value);
    if (ui.errors.loginId) {
      setUi(prev => ({ ...prev, errors: { ...prev.errors, loginId: '' } }));
    }
  };

  const onReset = (e) => {
    const { name, value } = e.target;
    setResetData(prev => ({ ...prev, [name]: value }));
    if (ui.errors[name]) {
      setUi(prev => ({ ...prev, errors: { ...prev.errors, [name]: '' } }));
    }
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    
    if (!loginId.trim()) {
      setUi(prev => ({ ...prev, errors: { loginId: 'Username or Email is required' } }));
      return;
    }

    setUi(prev => ({ ...prev, isLoading: true, errors: {} }));

    try {
      const response = await fetch('http://localhost:8000/api/auth/password-reset-request/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ login_id: loginId }),
      });

      const data = await response.json();

      if (response.ok) {
        setUi(prev => ({ ...prev, showResetModal: true }));
      } else {
        setUi(prev => ({ 
          ...prev, 
          errors: { general: data.login_id ? data.login_id[0] : 'Account not found' } 
        }));
      }
    } catch (error) {
      setUi(prev => ({ ...prev, errors: { general: 'Service unavailable. Please try again later.' } }));
    } finally {
      setUi(prev => ({ ...prev, isLoading: false }));
    }
  };

  const onPasswordReset = async (e) => {
    e.preventDefault();
    const newErrors = {};
    
    if (!resetData.newPassword) {
      newErrors.newPassword = 'Password is required';
    } else if (resetData.newPassword.length < 8) {
      newErrors.newPassword = 'Password must be at least 8 characters';
    }
    
    if (resetData.newPassword !== resetData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    if (Object.keys(newErrors).length > 0) {
      setUi(prev => ({ ...prev, errors: newErrors }));
      return;
    }

    setUi(prev => ({ ...prev, isLoading: true, errors: {} }));

    try {
      const response = await fetch('http://localhost:8000/api/auth/password-reset-confirm/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          login_id: loginId,
          new_password: resetData.newPassword,
          new_password2: resetData.confirmPassword,
        }),
      });

      if (response.ok) {
        navigate('/login');
      } else {
        const data = await response.json();
        setUi(prev => ({ ...prev, errors: { general: data.error || 'Reset failed' } }));
      }
    } catch (error) {
      setUi(prev => ({ ...prev, errors: { general: 'Network error occurred.' } }));
    } finally {
      setUi(prev => ({ ...prev, isLoading: false }));
    }
  };

  return (
    <div className="forgot-password-page">
      <div className="forgot-password-container">
        <header className="forgot-password-header">
          <h1>CSV Data Analysis System</h1>
        </header>

        <div className="forgot-password-card">
          <div className="card-header">
            <h2>Recover Account</h2>
            <p>Enter your username or email address to reset your password</p>
          </div>

          {ui.errors.general && <div className="error-banner">{ui.errors.general}</div>}

          <form className="forgot-password-form" onSubmit={onSubmit} noValidate>
            <div className="form-group">
              <label htmlFor="loginId">Username or Email</label>
              <input
                type="text"
                id="loginId"
                value={loginId}
                onChange={onChange}
                className={ui.errors.loginId ? 'input-error' : ''}
                placeholder="user123 or user@example.com"
              />
              {ui.errors.loginId && <span className="error-text">{ui.errors.loginId}</span>}
            </div>

            <div className="form-actions">
              <button type="submit" className="reset-btn" disabled={ui.isLoading}>
                {ui.isLoading ? 'Verifying...' : 'Continue'}
              </button>
            </div>
          </form>

          <footer className="back-to-login">
            <button onClick={() => navigate('/login')} className="link-style-btn">
              Back to Login
            </button>
          </footer>
        </div>
      </div>

      {ui.showResetModal && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3>Set New Password</h3>
              <button className="close-btn" onClick={() => setUi(prev => ({...prev, showResetModal: false}))}>✕</button>
            </div>

            {ui.errors.general && <div className="error-banner">{ui.errors.general}</div>}

            <form className="modal-body" onSubmit={onPasswordReset}>
              <div className="form-group">
                <label htmlFor="newPassword">New Password</label>
                <input
                  type="password"
                  id="newPassword"
                  name="newPassword"
                  value={resetData.newPassword}
                  onChange={onReset}
                  className={ui.errors.newPassword ? 'input-error' : ''}
                />
                {ui.errors.newPassword && <span className="error-text">{ui.errors.newPassword}</span>}
              </div>

              <div className="form-group">
                <label htmlFor="confirmPassword">Confirm Password</label>
                <input
                  type="password"
                  id="confirmPassword"
                  name="confirmPassword"
                  value={resetData.confirmPassword}
                  onChange={onReset}
                  className={ui.errors.confirmPassword ? 'input-error' : ''}
                />
                {ui.errors.confirmPassword && <span className="error-text">{ui.errors.confirmPassword}</span>}
              </div>

              <button type="submit" className="reset-btn" disabled={ui.isLoading}>
                {ui.isLoading ? 'Updating Password...' : 'Reset Password'}
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default ForgotPassword;
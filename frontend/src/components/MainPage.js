import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiFetch, isAuthenticated } from './apiHelper';
import './MainPage.css';

function MainPage({ user, onLogout }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadError, setUploadError] = useState('');
  const [showUserMenu, setShowUserMenu] = useState(false);
  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthenticated()) {
      navigate('/login');
    }
  }, [navigate]);

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (!file.name.endsWith('.csv')) {
        setUploadError('Please select a CSV file');
        setSelectedFile(null);
        return;
      }
      setSelectedFile(file);
      setUploadError('');
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file) {
      if (!file.name.endsWith('.csv')) {
        setUploadError('Please select a CSV file');
        return;
      }
      setSelectedFile(file);
      setUploadError('');
    }
  };



  const handleUpload = async () => {
    if (!selectedFile) {
      setUploadError('Please select a file first');
      return;
    }

    if (!isAuthenticated()) {
      setUploadError('You must be logged in to upload files');
      navigate('/login');
      return;
    }

    setIsUploading(true);
    setUploadError('');

    const formData = new FormData();
    formData.append('dataset_file', selectedFile);

    try {
      const response = await apiFetch('http://localhost:8000/api/upload-dataset/', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        alert('CSV uploaded successfully! Analysis is running in the background.');
        setSelectedFile(null);
        if (fileInputRef.current) {
          fileInputRef.current.value = '';
        }
        navigate('/downloads');
      } else {
        const data = await response.json();
        if (data.dataset_file) {
          setUploadError(data.dataset_file[0]);
        } else {
          setUploadError(data.error || 'Upload failed. Please try again.');
        }
      }
    } catch (error) {
      console.error('Upload error:', error);
      setUploadError('Something went wrong. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };

  const handleLogoutClick = async () => {
    try {
      const refreshToken = localStorage.getItem('refresh_token');
      await apiFetch('http://localhost:8000/api/auth/logout/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh: refreshToken }),
      });
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      onLogout();
      navigate('/login');
    }
  };

  const handleDownloadsClick = () => {
    navigate('/downloads');
  };

  return (
    <div className="main-page">
      <header className="main-header">
        <div className="header-content">
          <div className="logo-section">
            <h1>CSV Analyzer</h1>
          </div>
          
          <div className="user-section">
            <button 
              className="user-button"
              onClick={() => setShowUserMenu(!showUserMenu)}
            >
              <span className="user-name">{user?.username || 'User'}</span>
            </button>
            
            {showUserMenu && (
              <div className="user-menu">
                <button onClick={handleDownloadsClick} className="menu-item">
                  Downloads
                </button>
                <button onClick={handleLogoutClick} className="menu-item logout">
                  Logout
                </button>
              </div>
            )}
          </div>
        </div>
      </header>

      <main className="main-content">
        <div className="upload-section">
          <h2 className="section-title">CSV Analysis</h2>
          
          <div 
            className="upload-area"
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
          >
            <div className="upload-icon-container">
              <div className="upload-icon">
                <svg viewBox="0 0 100 100" width="120" height="120">
                  <rect x="10" y="30" width="35" height="45" fill="none" stroke="white" strokeWidth="2" rx="2"/>
                  <rect x="20" y="35" width="15" height="10" fill="white"/>
                  <rect x="20" y="50" width="15" height="3" fill="white"/>
                  <rect x="20" y="57" width="15" height="3" fill="white"/>
                  
                  <rect x="55" y="30" width="35" height="45" fill="none" stroke="white" strokeWidth="2" rx="2"/>
                  <text x="62" y="52" fill="white" fontSize="12" fontWeight="bold">PDF</text>
                  
                  <path d="M 45 52 L 55 52" stroke="white" strokeWidth="2"/>
                  <polygon points="53,50 58,52 53,54" fill="white"/>
                </svg>
              </div>
            </div>
            
            <button className="choose-files-btn">
              CHOOSE FILES
            </button>
            
            
            <input
              ref={fileInputRef}
              type="file"
              accept=".csv"
              onChange={handleFileSelect}
              style={{ display: 'none' }}
            />
          </div>

          {selectedFile && (
            <div className="selected-file">
              <span className="file-name">{selectedFile.name}</span>
              <button 
                className="remove-file"
                onClick={(e) => {
                  e.stopPropagation();
                  setSelectedFile(null);
                  if (fileInputRef.current) {
                    fileInputRef.current.value = '';
                  }
                }}
              >
                ✕
              </button>
            </div>
          )}

          {uploadError && (
            <div className="error-message">
              {uploadError}
            </div>
          )}

          {selectedFile && (
            <button 
              className="upload-btn"
              onClick={handleUpload}
              disabled={isUploading || !isAuthenticated()}
            >
              {isUploading ? (
                <>
                  <span className="spinner"></span>
                  Uploading...
                </>
              ) : (
                'Upload & Analyze'
              )}
            </button>
          )}
        </div>
      </main>
    </div>
  );
}

export default MainPage;
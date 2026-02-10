import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiFetch, isAuthenticated } from './apiHelper';
import { API_BASE_URL } from './config';
import './Downloads.css';

function Downloads({ user, onLogout }) {
  const [datasets, setDatasets] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [pollingInterval, setPollingInterval] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthenticated()) {
      navigate('/login');
    }
  }, [navigate]);

  const fetchDatasets = useCallback(async () => {
    try {
      const response = await apiFetch(`${API_BASE_URL}/api/datasets/`);

      if (response.ok) {
        const data = await response.json();
        setDatasets(data);
        
        const hasProcessing = data.some(
          dataset => dataset.status === 'processing' || dataset.status === 'pending'
        );
        
        if (hasProcessing && !pollingInterval) {
          const interval = setInterval(() => {
            fetchDatasets();
          }, 3000); 
          setPollingInterval(interval);
        } else if (!hasProcessing && pollingInterval) {
          clearInterval(pollingInterval);
          setPollingInterval(null);
        }
      } else {
        console.error('Failed to fetch datasets');
      }
    } catch (error) {
      console.error('Error fetching datasets:', error);
    } finally {
      setIsLoading(false);
    }
  }, [pollingInterval]);

  useEffect(() => {
    fetchDatasets();
    
    return () => {
      if (pollingInterval) {
        clearInterval(pollingInterval);
      }
    };
  }, []);

  const handleDownload = async (datasetId) => {
    try {
      const response = await apiFetch(`${API_BASE_URL}/api/download-pdf/${datasetId}/`);

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `analysis_report_${datasetId}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      } else {
        const data = await response.json();
        alert(data.error || 'Download failed');
      }
    } catch (error) {
      console.error('Download error:', error);
      alert('Failed to download PDF');
    }
  };

  const handleLogoutClick = async () => {
    try {
      const refreshToken = localStorage.getItem('refresh_token');
      await apiFetch(`${API_BASE_URL}/api/auth/logout/`, {
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

  const handleBackToMain = () => {
    navigate('/main');
  };

  const getStatusBadge = (status) => {
    const statusConfig = {
      pending: { color: '#fbbf24', text: 'Pending' },
      processing: { color: '#60a5fa', text: 'Processing' },
      completed: { color: '#34d399', text: 'Completed' },
      failed: { color: '#f87171', text: 'Failed' },
    };

    const config = statusConfig[status] || statusConfig.pending;

    return (
      <span 
        className="status-badge"
        style={{ backgroundColor: config.color }}
      >
        {config.text}
      </span>
    );
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="downloads-page">
      <header className="downloads-header">
        <div className="header-content">
          <div className="logo-section">
            <button className="back-btn" onClick={handleBackToMain}>
              ← Back
            </button>
            <h1>Downloads</h1>
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
                <button onClick={handleBackToMain} className="menu-item">
                  Main Page
                </button>
                <button onClick={handleLogoutClick} className="menu-item logout">
                  Logout
                </button>
              </div>
            )}
          </div>
        </div>
      </header>

      <main className="downloads-content">
        <div className="downloads-container">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h2>Recent Uploads</h2>
            {datasets.some(d => d.status === 'processing' || d.status === 'pending') && (
              <span style={{ color: '#60a5fa', fontSize: '14px' }}>
                Auto-refreshing...
              </span>
            )}
          </div>
          
          {isLoading ? (
            <div className="loading-state">
              <div className="spinner-large"></div>
              <p>Loading your uploads...</p>
            </div>
          ) : datasets.length === 0 ? (
            <div className="empty-state">
              <h3>No uploads yet</h3>
              <p>Upload your first CSV file to see it here</p>
              <button className="upload-now-btn" onClick={handleBackToMain}>
                Upload Now
              </button>
            </div>
          ) : (
            <div className="datasets-list">
              {datasets.map((dataset) => (
                <div key={dataset.id} className="dataset-card">
                  <div className="dataset-header">
                    <div className="dataset-info">
                      <h3 className="dataset-name">
                        Dataset #{dataset.id}
                      </h3>
                      <p className="dataset-date">
                        {formatDate(dataset.uploaded_at)}
                      </p>
                    </div>
                    {getStatusBadge(dataset.status)}
                  </div>
                  
                  <div className="dataset-details">
                    <div className="detail-item">
                      <span className="detail-label">CSV File:</span>
                      <span className="detail-value">
                        {dataset.dataset_file.split('/').pop()}
                      </span>
                    </div>
                    
                    {dataset.pdf_file && (
                      <div className="detail-item">
                        <span className="detail-label">Report:</span>
                        <span className="detail-value">
                          {dataset.pdf_file.split('/').pop()}
                        </span>
                      </div>
                    )}

                    {dataset.error_message && (
                      <div className="detail-item error">
                        <span className="detail-label">Error:</span>
                        <span className="detail-value">{dataset.error_message}</span>
                      </div>
                    )}
                  </div>

                  <div className="dataset-actions">
                    {dataset.status === 'completed' && dataset.pdf_file && (
                      <button 
                        className="download-btn"
                        onClick={() => handleDownload(dataset.id)}
                      >
                        Download PDF
                      </button>
                    )}
                    {(dataset.status === 'processing' || dataset.status === 'pending') && (
                      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                        <span className="spinner"></span>
                        <span style={{ color: '#60a5fa', fontSize: '14px' }}>
                          Processing...
                        </span>
                      </div>
                    )}
                    {dataset.status === 'failed' && (
                      <button className="refresh-btn" onClick={handleBackToMain}>
                        Upload New File
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default Downloads;
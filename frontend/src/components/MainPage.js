import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiFetch, isAuthenticated } from './apiHelper';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar, Pie, Line } from 'react-chartjs-2';
import './MainPage.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

function MainPage({ user, onLogout }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadError, setUploadError] = useState('');
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [currentDatasetId, setCurrentDatasetId] = useState(null);
  const [analysisData, setAnalysisData] = useState(null);
  const [processingStatus, setProcessingStatus] = useState(null);
  const fileInputRef = useRef(null);
  const navigate = useNavigate();
  const pollIntervalRef = useRef(null);

  useEffect(() => {
    if (!isAuthenticated()) {
      navigate('/login');
    }
  }, [navigate]);

  useEffect(() => {
    if (currentDatasetId && processingStatus !== 'completed' && processingStatus !== 'failed') {
      pollIntervalRef.current = setInterval(() => {
        checkDatasetStatus(currentDatasetId);
      }, 2000); 
      return () => {
        if (pollIntervalRef.current) {
          clearInterval(pollIntervalRef.current);
        }
      };
    }
  }, [currentDatasetId, processingStatus]);

  const checkDatasetStatus = async (datasetId) => {
    try {
      const response = await apiFetch(`http://localhost:8000/api/dataset-status/${datasetId}/`);
      if (response.ok) {
        const data = await response.json();
        setProcessingStatus(data.status);
        
        if (data.status === 'completed' && data.analysis) {
          setAnalysisData(data.analysis);
          if (pollIntervalRef.current) {
            clearInterval(pollIntervalRef.current);
          }
        } else if (data.status === 'failed') {
          setUploadError(data.error || 'Analysis failed. Please check your CSV file and try again.');
          if (pollIntervalRef.current) {
            clearInterval(pollIntervalRef.current);
          }
        }
      }
    } catch (error) {
      console.error('Error checking status:', error);
    }
  };

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
      setAnalysisData(null);
      setCurrentDatasetId(null);
      setProcessingStatus(null);
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
      setAnalysisData(null);
      setCurrentDatasetId(null);
      setProcessingStatus(null);
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
    setAnalysisData(null);

    const formData = new FormData();
    formData.append('dataset_file', selectedFile);

    try {
      const response = await apiFetch('http://localhost:8000/api/upload-dataset/', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setCurrentDatasetId(data.dataset_id);
        setProcessingStatus(data.status);
      } else {
        const data = await response.json();
        if (data.dataset_file) {
          setUploadError(data.dataset_file[0]);
        } else {
          setUploadError(data.error || 'Upload failed. Please try again.');
        }
        setProcessingStatus('failed');
      }
    } catch (error) {
      console.error('Upload error:', error);
      setUploadError('Something went wrong. Please try again.');
      setProcessingStatus('failed');
    } finally {
      setIsUploading(false);
    }
  };

  const handleTryAgain = () => {
    // Reset all states to allow retry
    setSelectedFile(null);
    setCurrentDatasetId(null);
    setProcessingStatus(null);
    setAnalysisData(null);
    setUploadError('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
    if (pollIntervalRef.current) {
      clearInterval(pollIntervalRef.current);
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

  const downloadPDF = async () => {
    if (!currentDatasetId) return;
    
    try {
      const response = await apiFetch(`http://localhost:8000/api/download-pdf/${currentDatasetId}/`);
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `analysis_report_${currentDatasetId}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      }
    } catch (error) {
      console.error('Download error:', error);
    }
  };

  // Prepare chart data
  const getEquipmentDistributionData = () => {
    if (!analysisData?.equipment_distribution) return null;
    
    const labels = Object.keys(analysisData.equipment_distribution);
    const data = Object.values(analysisData.equipment_distribution);
    
    return {
      labels,
      datasets: [{
        label: 'Equipment Count',
        data,
        backgroundColor: [
          'rgba(75, 192, 192, 0.6)',
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(153, 102, 255, 0.6)',
        ],
        borderColor: [
          'rgba(75, 192, 192, 1)',
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(153, 102, 255, 1)',
        ],
        borderWidth: 2,
      }],
    };
  };

  const getEquipmentAveragesData = (field) => {
    if (!analysisData?.equipment_averages) return null;
    
    const labels = Object.keys(analysisData.equipment_averages);
    const data = labels.map(equipment => 
      analysisData.equipment_averages[equipment][field] || 0
    );
    
    return {
      labels,
      datasets: [{
        label: `Average ${field}`,
        data,
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 2,
      }],
    };
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          color: 'white',
          font: { size: 12 }
        }
      },
      title: {
        display: true,
        color: 'white',
        font: { size: 14, weight: 'bold' }
      },
    },
    scales: {
      x: {
        ticks: { color: 'white' },
        grid: { color: 'rgba(255, 255, 255, 0.1)' }
      },
      y: {
        ticks: { color: 'white' },
        grid: { color: 'rgba(255, 255, 255, 0.1)' }
      }
    }
  };

  const pieOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'right',
        labels: {
          color: 'white',
          font: { size: 12 }
        }
      },
      title: {
        display: true,
        color: 'white',
        font: { size: 14, weight: 'bold' }
      },
    }
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
            onDragOver={(e) => e.preventDefault()}
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
              <p>{uploadError}</p>
              {processingStatus === 'failed' && (
                <button className="try-again-btn" onClick={handleTryAgain}>
                  Try Again
                </button>
              )}
            </div>
          )}

          {processingStatus && processingStatus !== 'completed' && processingStatus !== 'failed' && (
            <div className="processing-message">
              <div className="spinner"></div>
              <span>Processing your data... Status: {processingStatus}</span>
            </div>
          )}

          {selectedFile && !currentDatasetId && (
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

          {/* Analysis Results Section */}
          {analysisData && (
            <div className="analysis-results">
              <div className="results-header">
                <h3>Analysis Results</h3>
                <button className="download-pdf-btn" onClick={downloadPDF}>
                  Download PDF Report
                </button>
              </div>

              <div className="stats-summary">
                <div className="stat-card">
                  <h4>Total Records</h4>
                  <p>{analysisData.total_rows}</p>
                </div>
                <div className="stat-card">
                  <h4>Equipment Types</h4>
                  <p>{Object.keys(analysisData.equipment_distribution || {}).length}</p>
                </div>
              </div>

              {/* Equipment Distribution Pie Chart */}
              {analysisData.equipment_distribution && (
                <div className="chart-container">
                  <h4 className="chart-title">Equipment Type Distribution</h4>
                  <div className="chart-wrapper">
                    <Pie 
                      data={getEquipmentDistributionData()} 
                      options={{
                        ...pieOptions,
                        plugins: {
                          ...pieOptions.plugins,
                          title: { ...pieOptions.plugins.title, text: 'Equipment Distribution' }
                        }
                      }}
                    />
                  </div>
                </div>
              )}

              {/* Equipment Averages Bar Charts */}
              {analysisData.equipment_averages && Object.keys(analysisData.equipment_averages).length > 0 && (
                <div className="averages-section">
                  <h4 className="section-subtitle">Equipment Performance Metrics</h4>
                  {Object.keys(Object.values(analysisData.equipment_averages)[0] || {}).map(field => (
                    <div key={field} className="chart-container">
                      <h5 className="chart-title">Average {field} by Equipment</h5>
                      <div className="chart-wrapper">
                        <Bar 
                          data={getEquipmentAveragesData(field)} 
                          options={{
                            ...chartOptions,
                            plugins: {
                              ...chartOptions.plugins,
                              title: { ...chartOptions.plugins.title, text: `${field} Comparison` }
                            }
                          }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {/* Field Statistics Table */}
              {analysisData.field_statistics && (
                <div className="statistics-table">
                  <h4 className="section-subtitle">Field Statistics</h4>
                  {Object.entries(analysisData.field_statistics).map(([field, stats]) => (
                    <div key={field} className="stat-table-card">
                      <h5>{field}</h5>
                      <table>
                        <tbody>
                          {Object.entries(stats).map(([metric, value]) => (
                            <tr key={metric}>
                              <td>{metric}</td>
                              <td>{typeof value === 'number' ? value.toFixed(2) : value}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default MainPage;
import React, { useState, useEffect } from 'react';
import api from '../api/index.js';

const PortalIntegration = () => {
  const [userInfo, setUserInfo] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [showQuickLogin, setShowQuickLogin] = useState(false);

  useEffect(() => {
    checkUserSession();
  }, []);

  const checkUserSession = async () => {
    try {
      const user = await api.getUserInfo();
      setUserInfo(user);
    } catch (error) {
      console.log('No active session');
    }
  };

  const handleQuickLogin = async (email, password) => {
    setIsLoading(true);
    try {
      const response = await api.login(email, password);
      if (response.ok) {
        await checkUserSession();
        setShowQuickLogin(false);
        // Open the portal dashboard
        window.open('http://localhost:5001', '_blank');
      } else {
        alert('Login failed. Please check your credentials.');
      }
    } catch (error) {
      console.error('Login error:', error);
      alert('Login error. Please try again.');
    }
    setIsLoading(false);
  };

  const initializeDemoData = async () => {
    setIsLoading(true);
    try {
      await api.initializeDemoData();
      alert('Demo data initialized! You can now use the demo login credentials.');
    } catch (error) {
      console.error('Demo data initialization error:', error);
    }
    setIsLoading(false);
  };

  return (
    <div style={{ marginLeft: "-4rem", marginTop: "3rem", marginBottom: "2rem" }}>
      {/* Main Hospital Portal Button */}
      <button 
        onClick={() => window.open('http://localhost:5001', '_blank')}
        style={{
          background: "linear-gradient(45deg, #667eea 0%, #764ba2 100%)",
          border: "none",
          borderRadius: "50px",
          padding: "15px 40px",
          color: "white",
          fontSize: "18px",
          fontWeight: "600",
          fontFamily: 'Dmsans, Arial, sans-serif',
          cursor: "pointer",
          boxShadow: "0 8px 25px rgba(102, 126, 234, 0.3)",
          transition: "all 0.3s ease",
          textTransform: "uppercase",
          letterSpacing: "1px",
          position: "relative",
          overflow: "hidden"
        }}
        onMouseEnter={(e) => {
          e.target.style.transform = "translateY(-3px)";
          e.target.style.boxShadow = "0 12px 35px rgba(102, 126, 234, 0.4)";
        }}
        onMouseLeave={(e) => {
          e.target.style.transform = "translateY(0)";
          e.target.style.boxShadow = "0 8px 25px rgba(102, 126, 234, 0.3)";
        }}
      >
        <span style={{ marginRight: "10px" }}>🏥</span>
        Access Hospital Portal
      </button>

      {/* User Status Display */}
      {userInfo && (
        <div style={{ 
          marginTop: "1rem", 
          padding: "10px 15px", 
          background: "rgba(255,255,255,0.1)", 
          borderRadius: "25px",
          fontSize: "14px",
          color: "white"
        }}>
          Welcome back, {userInfo.name}! ({userInfo.role})
        </div>
      )}

      {/* Quick Actions */}
      <div style={{ marginTop: "1rem", display: "flex", gap: "10px", flexWrap: "wrap" }}>
        <button
          onClick={() => setShowQuickLogin(!showQuickLogin)}
          style={{
            background: "rgba(255,255,255,0.15)",
            border: "1px solid rgba(255,255,255,0.3)",
            borderRadius: "25px",
            padding: "8px 20px",
            color: "white",
            fontSize: "14px",
            fontFamily: 'Dmsans, Arial, sans-serif',
            cursor: "pointer",
            transition: "all 0.3s ease"
          }}
        >
          Quick Login
        </button>
        
        <button
          onClick={initializeDemoData}
          disabled={isLoading}
          style={{
            background: "rgba(255,255,255,0.15)",
            border: "1px solid rgba(255,255,255,0.3)",
            borderRadius: "25px",
            padding: "8px 20px",
            color: "white",
            fontSize: "14px",
            fontFamily: 'Dmsans, Arial, sans-serif',
            cursor: isLoading ? "not-allowed" : "pointer",
            transition: "all 0.3s ease",
            opacity: isLoading ? 0.7 : 1
          }}
        >
          {isLoading ? "Loading..." : "Setup Demo"}
        </button>
      </div>

      {/* Quick Login Form */}
      {showQuickLogin && (
        <div style={{
          marginTop: "1rem",
          padding: "20px",
          background: "rgba(255,255,255,0.1)",
          borderRadius: "15px",
          backdropFilter: "blur(10px)"
        }}>
          <h4 style={{ color: "white", marginBottom: "15px", fontSize: "16px" }}>Quick Login</h4>
          
          <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
            <button
              onClick={() => handleQuickLogin('alice@email.com', 'pat123')}
              disabled={isLoading}
              style={{
                background: "rgba(102, 126, 234, 0.8)",
                border: "none",
                borderRadius: "8px",
                padding: "10px 15px",
                color: "white",
                fontSize: "14px",
                cursor: isLoading ? "not-allowed" : "pointer"
              }}
            >
              Login as Patient (Alice)
            </button>
            
            <button
              onClick={() => handleQuickLogin('sarah@hospital.com', 'doc123')}
              disabled={isLoading}
              style={{
                background: "rgba(118, 75, 162, 0.8)",
                border: "none",
                borderRadius: "8px",
                padding: "10px 15px",
                color: "white",
                fontSize: "14px",
                cursor: isLoading ? "not-allowed" : "pointer"
              }}
            >
              Login as Doctor (Sarah)
            </button>
            
            <button
              onClick={() => handleQuickLogin('admin@hospital.com', 'admin123')}
              disabled={isLoading}
              style={{
                background: "rgba(255, 138, 1, 0.8)",
                border: "none",
                borderRadius: "8px",
                padding: "10px 15px",
                color: "white",
                fontSize: "14px",
                cursor: isLoading ? "not-allowed" : "pointer"
              }}
            >
              Login as Admin (John)
            </button>
          </div>
        </div>
      )}

      <div style={{ marginTop: "1rem", fontSize: "14px", color: "rgba(255,255,255,0.8)", fontFamily: 'Dmsans, Arial, sans-serif' }}>
        Manage appointments • View medical records • Connect with doctors
      </div>
    </div>
  );
};

export default PortalIntegration;

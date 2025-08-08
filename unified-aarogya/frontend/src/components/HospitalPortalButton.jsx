import React, { useState } from 'react';

const HospitalPortalButton = ({ 
  portalUrl = 'http://localhost:5000',
  buttonText = 'Access Hospital Portal',
  position = 'inline', // 'inline', 'floating', 'header'
  theme = 'gradient' // 'gradient', 'solid', 'outline'
}) => {
  const [isHovered, setIsHovered] = useState(false);

  const baseStyles = {
    border: 'none',
    borderRadius: '50px',
    padding: '15px 40px',
    fontSize: '18px',
    fontWeight: '600',
    fontFamily: 'Dmsans, Arial, sans-serif',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    textTransform: 'uppercase',
    letterSpacing: '1px',
    position: 'relative',
    overflow: 'hidden',
    display: 'inline-flex',
    alignItems: 'center',
    gap: '10px'
  };

  const themeStyles = {
    gradient: {
      background: 'linear-gradient(45deg, #667eea 0%, #764ba2 100%)',
      color: 'white',
      boxShadow: isHovered 
        ? '0 12px 35px rgba(102, 126, 234, 0.4)' 
        : '0 8px 25px rgba(102, 126, 234, 0.3)'
    },
    solid: {
      backgroundColor: '#667eea',
      color: 'white',
      boxShadow: isHovered 
        ? '0 8px 20px rgba(102, 126, 234, 0.4)' 
        : '0 4px 15px rgba(102, 126, 234, 0.2)'
    },
    outline: {
      backgroundColor: 'transparent',
      color: '#667eea',
      border: '2px solid #667eea',
      boxShadow: isHovered 
        ? '0 4px 15px rgba(102, 126, 234, 0.2)' 
        : 'none'
    }
  };

  const positionStyles = {
    inline: {},
    floating: {
      position: 'fixed',
      bottom: '30px',
      right: '30px',
      zIndex: 1000,
      borderRadius: '60px',
      padding: '12px 30px',
      fontSize: '16px'
    },
    header: {
      margin: '0 15px'
    }
  };

  const combinedStyles = {
    ...baseStyles,
    ...themeStyles[theme],
    ...positionStyles[position],
    transform: isHovered ? 'translateY(-3px)' : 'translateY(0)'
  };

  const handleClick = () => {
    window.open(portalUrl, '_blank');
  };

  return (
    <button
      style={combinedStyles}
      onClick={handleClick}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <span>🏥</span>
      {buttonText}
    </button>
  );
};

// Portal Integration Component with multiple options
const AarogyaPortalIntegration = ({ showQuickActions = true }) => {
  return (
    <div style={{ 
      marginTop: '3rem', 
      marginBottom: '2rem',
      marginLeft: '-4rem' // Matches your existing layout
    }}>
      {/* Main Portal Button */}
      <HospitalPortalButton 
        buttonText="Access Hospital Portal"
        theme="gradient"
        position="inline"
      />
      
      {/* Portal Description */}
      <div style={{ 
        marginTop: '1rem', 
        fontSize: '14px', 
        color: 'rgba(255,255,255,0.8)', 
        fontFamily: 'Dmsans, Arial, sans-serif' 
      }}>
        Manage appointments • View medical records • Connect with doctors
      </div>

      {/* Quick Actions (Optional) */}
      {showQuickActions && (
        <div style={{ 
          marginTop: '2rem',
          display: 'flex',
          gap: '15px',
          flexWrap: 'wrap'
        }}>
          <button
            style={{
              backgroundColor: 'rgba(255,255,255,0.1)',
              border: '1px solid rgba(255,255,255,0.3)',
              borderRadius: '25px',
              padding: '8px 20px',
              color: 'white',
              fontSize: '14px',
              cursor: 'pointer',
              transition: 'all 0.3s ease'
            }}
            onClick={() => window.open('http://localhost:5000/login', '_blank')}
            onMouseEnter={(e) => {
              e.target.style.backgroundColor = 'rgba(255,255,255,0.2)';
            }}
            onMouseLeave={(e) => {
              e.target.style.backgroundColor = 'rgba(255,255,255,0.1)';
            }}
          >
            👤 Patient Login
          </button>
          
          <button
            style={{
              backgroundColor: 'rgba(255,255,255,0.1)',
              border: '1px solid rgba(255,255,255,0.3)',
              borderRadius: '25px',
              padding: '8px 20px',
              color: 'white',
              fontSize: '14px',
              cursor: 'pointer',
              transition: 'all 0.3s ease'
            }}
            onClick={() => window.open('http://localhost:5000/login', '_blank')}
            onMouseEnter={(e) => {
              e.target.style.backgroundColor = 'rgba(255,255,255,0.2)';
            }}
            onMouseLeave={(e) => {
              e.target.style.backgroundColor = 'rgba(255,255,255,0.1)';
            }}
          >
            👩‍⚕️ Doctor Portal
          </button>
          
          <button
            style={{
              backgroundColor: 'rgba(255,255,255,0.1)',
              border: '1px solid rgba(255,255,255,0.3)',
              borderRadius: '25px',
              padding: '8px 20px',
              color: 'white',
              fontSize: '14px',
              cursor: 'pointer',
              transition: 'all 0.3s ease'
            }}
            onClick={() => window.open('http://localhost:5000/demo_data', '_blank')}
            onMouseEnter={(e) => {
              e.target.style.backgroundColor = 'rgba(255,255,255,0.2)';
            }}
            onMouseLeave={(e) => {
              e.target.style.backgroundColor = 'rgba(255,255,255,0.1)';
            }}
          >
            🎮 Try Demo
          </button>
        </div>
      )}
    </div>
  );
};

export { HospitalPortalButton, AarogyaPortalIntegration };
export default AarogyaPortalIntegration;

import React from 'react';
import ParallaxBackground from './parallaxBackground.jsx';
import { FlipWords } from './FlipWords.jsx';

const AarogyaContent = () => {
  return (
    <>
      <div className="hero_illustration_block" style={{ position: "relative", minHeight: "100vh", display: "flex", flexDirection: "column", alignItems: "top", justifyContent: "center", overflow: "hidden", paddingTop: 0 }}>
        <div style={{ width: '100%', background: 'transparent', color: 'white', textAlign: 'center', padding: '0rem 0', zIndex: 2100, position: 'absolute', top: 0, left: 0 }}>
          <nav className="navigation" style={{ width: "100%", position: "absolute", top: '2.5rem', left: 0, right: 0, zIndex: 2000, backgroundColor: "transparent", padding: "0.25rem 1rem 0.5rem 1rem", marginTop: 0 }}>
            <div className="navigation-items" style={{ display: "flex", justifyContent: "space-between", alignItems: "center", maxWidth: "1200px", margin: "0 auto" }}>
              <div className="nav-links" style={{ display: "flex", gap: "2rem", alignItems: "center" }}>
                <a href="/shop/products" className="navigation-item" style={{ color: "white", textDecoration: "none", fontWeight: "500" }}>Shop</a>
                <a href="/discoveries/discoveries" className="navigation-item" style={{ color: "white", textDecoration: "none", fontWeight: "500" }}>Discoveries</a>
                <a href="/blog/notebook" className="navigation-item" style={{ color: "white", textDecoration: "none", fontWeight: "500" }}>NOTEBOOK</a>
                <a href="/about" className="navigation-item" style={{ color: "white", textDecoration: "none", fontWeight: "500" }}>About</a>
                <a href="/contact" className="navigation-item" style={{ color: "white", textDecoration: "none", fontWeight: "500" }}>Contact</a>
                <div className="language-switcher" style={{ display: "flex", gap: "0.5rem" }}>
                  <a href="#Weglot-fr" className="navigation-item" style={{ color: "white", textDecoration: "none", fontWeight: "500" }}>FR</a>
                  <a href="#Weglot-en" className="navigation-item" style={{ color: "white", textDecoration: "none", fontWeight: "500" }}>EN</a>
                </div>
              </div>
            </div>
          </nav>
        </div>
        {/* Top side overlay */}
        <div style={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          height: "40%",
          background: "linear-gradient(180deg, rgba(0,0,0,0.4) 0%, rgba(0,0,0,0.2) 50%, transparent 100%)",
          zIndex: 5,
          pointerEvents: "none"
        }}></div>
        
        {/* Left side overlay */}
        <div style={{
          position: "absolute",
          top: 0,
          left: 0,
          bottom: 0,
          width: "30%",
          background: "linear-gradient(90deg, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.2) 50%, transparent 100%)",
          zIndex: 5,
          pointerEvents: "none"
        }}></div>
        
        <ParallaxBackground />
        <div className="w-layout-blockcontainer container w-container" style={{ position: "relative", zIndex: 10, display: 'flex', alignItems: 'flex-start', justifyContent: 'flex-start' }}>
          <div style={{ flex: 1 }}>
            <div className="h2" style={{ color: "white", textAlign: "left", textTransform: "uppercase", marginLeft: "-5rem", marginRight: "auto", fontFamily: 'Founders Grotesk Condensed, Impact, sans-serif', fontSize: "100px", fontWeight: 700, lineHeight: "70%", overflow: "visible" }}>
              WELCOME <br />TO PLANET
              <FlipWords 
                words={["AAROGYA", "HEALTH", "WELLNESS", "MEDICINE"]} 
                duration={1500}
                className="text-white font-bold text-[100px] leading-[70%] uppercase"
              />
            </div>
            <p className="paragraph-light discoveries" style={{ textAlign: "left", width: "55%", maxWidth: "650px", marginLeft: "-4rem", marginRight: "auto", fontFamily: 'Cardinalfruitweb, Times New Roman, sans-serif', fontSize: "32px", lineHeight: "110%" }}>
              Travel through the universe of Aarogya. <br />Unique pieces to adopt, limited editions, and scientific discoveries.
            </p>
            
            {/* Hospital Portal Button */}
            <div style={{ marginLeft: "-4rem", marginTop: "3rem", marginBottom: "2rem" }}>
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
              
              <div style={{ marginTop: "1rem", fontSize: "14px", color: "rgba(255,255,255,0.8)", fontFamily: 'Dmsans, Arial, sans-serif' }}>
                Manage appointments • View medical records • Connect with doctors
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default AarogyaContent;
import React from 'react';
import ParallaxBackground from './parallaxBackground.jsx';

const AarogyaContent = () => {
  return (
    <div>
      {/* Navigation */}
      <nav className="navigation" style={{ position: "fixed", top: 0, width: "100%", zIndex: 1000, backgroundColor: "transparent", padding: "1rem" }}>
        <div className="navigation-items" style={{ display: "flex", justifyContent: "space-between", alignItems: "center", maxWidth: "1200px", margin: "0 auto" }}>
          {/* <div className="logo-block">
            <img src="/assets/swan.png" alt="Logo" className="logo" style={{ height: "40px", width: "40px" }} />
          </div> */}
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

      {/* Hero Section with Parallax Effect */}
      <div className="hero_illustration_block" style={{ position: "relative", minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", overflow: "hidden" }}>
        <ParallaxBackground />
        <div className="w-layout-blockcontainer container w-container" style={{ position: "relative", zIndex: 10 }}>
          <h1 className="hero_episode" style={{ textAlign: "center", fontSize: "4rem", fontWeight: "bold", color: "white", marginBottom: "2rem" }}>
            WELCOME<br />TO PLANET AAROGYA
          </h1>
          <div className="hero-description" style={{ textAlign: "center", fontSize: "1.5rem", color: "white", maxWidth: "600px", margin: "0 auto" }}>
            <p>Travel through the universe of Aarogya. Unique pieces to adopt, limited editions, and scientific discoveries.</p>
          </div>
        </div>
      </div>

      {/* Regular Content Sections (No Parallax) */}
      <div className="w-layout-blockcontainer container w-container" style={{ backgroundColor: "rgba(255, 255, 255, 0.95)", padding: "4rem 2rem", minHeight: "100vh" }}>
        <div className="div-block-39" style={{ textAlign: "center", maxWidth: "800px", margin: "0 auto" }}>
          <h2 className="heading" style={{ fontSize: "3rem", fontWeight: "bold", marginBottom: "2rem", color: "#333" }}>Discover Our Universe</h2>
          <div className="text-block" style={{ fontSize: "1.2rem", lineHeight: "1.8", marginBottom: "2rem", color: "#666" }}>
            <p>Experience the artistry and innovation that defines Aarogya. Each piece tells a story of creativity, craftsmanship, and cosmic inspiration.</p>
          </div>
          <div className="text-block" style={{ fontSize: "1.2rem", lineHeight: "1.8", color: "#666" }}>
            <p>From contemporary ceramics to limited edition collections, explore a world where art meets science in perfect harmony.</p>
          </div>
        </div>
      </div>

      {/* Third Section */}
      <div className="w-layout-blockcontainer container w-container" style={{ backgroundColor: "rgba(0, 0, 0, 0.8)", padding: "4rem 2rem", minHeight: "100vh", color: "white" }}>
        <div className="div-block-40" style={{ textAlign: "center", maxWidth: "800px", margin: "0 auto" }}>
          <h2 className="heading" style={{ fontSize: "3rem", fontWeight: "bold", marginBottom: "2rem" }}>Healthcare Innovation</h2>
          <div className="text-block" style={{ fontSize: "1.2rem", lineHeight: "1.8", marginBottom: "2rem" }}>
            <p>Aarogya represents the future of healthcare technology, combining traditional wellness practices with cutting-edge medical innovations.</p>
          </div>
          <div className="text-block" style={{ fontSize: "1.2rem", lineHeight: "1.8" }}>
            <p>Our platform creates seamless connections between patients, healthcare providers, and innovative treatment solutions.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AarogyaContent;
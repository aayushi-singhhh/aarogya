import { Canvas, useFrame } from "@react-three/fiber";
import HeroText from "../components/HeroText";
import ParallaxBackground from "../components/parallaxBackground.jsx";
import { Float } from "@react-three/drei";
import { easing } from "maath";
import { Suspense } from "react";
import Loader from "../components/Loader";

const Hero = () => {
  const isMobile = useMediaQuery({ maxWidth: 853 });
  return (
    <section className="flex items-start justify-center min-h-screen overflow-hidden md:items-start md:justify-start c-space" style={{ position: 'relative' }}>
      {/* Navigation Bar on top of Hero Section */}
      <nav className="navigation" style={{ width: "100%", position: "absolute", top: 0, left: 0, right: 0, zIndex: 1000, backgroundColor: "transparent", padding: "0.25rem 1rem 0.5rem 1rem", marginTop: 0 }}>
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
      <HeroText />
      <ParallaxBackground />
      <figure
        className="absolute inset-0"
        style={{ width: "100vw", height: "100vh" }}
      >
        <Canvas camera={{ position: [0, 1, 3] }}>
          <Suspense fallback={<Loader />}>
            <Float>
              <Astronaut
                scale={isMobile && 0.23}
                position={isMobile && [0, -1.5, 0]}
              />
            </Float>
            <Rig />
          </Suspense>
        </Canvas>
      </figure>
    </section>
  );
};

function Rig() {
  return useFrame((state, delta) => {
    easing.damp3(
      state.camera.position,
      [state.mouse.x / 10, 1 + state.mouse.y / 10, 3],
      0.5,
      delta
    );
  });
}

export default Hero;
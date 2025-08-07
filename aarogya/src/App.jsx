import React from "react";
import Navbar from "./sections/navbar";
import Hero from "./sections/Hero";

const App = () => {
  return (
    <div className="container mx-auto max-w-7xl">
      <Navbar />
      <Hero />
    </div>
  );
};

export default App;
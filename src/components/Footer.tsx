"use client";
import React from 'react';

interface FooterProps {
  className?: string; // Allow optional className prop
}

const Footer: React.FC<FooterProps> = ({ className }) => {
  return (
    <footer className={`bg-foreground text-white py-4 ${className}`}>
      <div className="container mx-auto text-center">
        <p className="text-base">Developed by Team Debugging Dragons</p>
      </div>
    </footer>
  );
};

export default Footer;

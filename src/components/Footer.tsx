"use client";
import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-foreground text-white py-4">
      <div className="container mx-auto text-center">
        <p className="text-sm">&copy; {new Date().getFullYear()} Debugging Dragons. All rights reserved.</p>
        <div className="mt-2">
          <a
            href="https://github.com/Jway77-ai/uob-hackathon-dragons"
            target="_blank"
            rel="noopener noreferrer"
            className="text-gray-400 hover:text-white mx-2"
          >
            GitHub
          </a>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
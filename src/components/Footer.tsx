"use client";

import React from "react";
import Image from "next/image";
import Link from "next/link";
import UOBLogo from "@/images/uob-logo-white.png";
import { FaGithub, FaBitbucket, FaArrowUp } from "react-icons/fa";

const Footer = () => {
  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <footer className="bg-foreground text-white py-8 w-full relative">
      <div className="container mx-auto px-4">
        <div className="flex flex-col items-center mb-8">
          <div className="text-lg font-bold flex items-center mb-4">
            <Link href="/" aria-label="Go to homepage">
              <Image src={UOBLogo} alt="UOB" width={100} height={100} />
            </Link>
          </div>
          <p className="text-sm text-center">
            Code Reviewer - Hackathon Project 2024
          </p>
          <p className="text-sm text-center mt-2 font-semibold">
            Developed by UOB GBT Debugging Dragons
          </p>
        </div>

        <div className="w-full h-px bg-white mb-6"></div>

        <div className="flex flex-col md:flex-row justify-between items-center">
          <p className="text-sm text-center md:text-left mb-4 md:mb-0">
            &copy; 2024 UOB Code Reviewer Hackathon Project. All rights
            reserved.
          </p>
          <div className="flex items-center space-x-4">
            <div className="flex space-x-4">
              <a
                href="https://github.com/"
                target="_blank"
                rel="noopener noreferrer"
                className="hover:text-blue-300 transition-colors duration-200"
              >
                <FaGithub size={24} />
              </a>
              <a
                href="https://bitbucket.org/"
                target="_blank"
                rel="noopener noreferrer"
                className="hover:text-blue-300 transition-colors duration-200"
              >
                <FaBitbucket size={24} />
              </a>
            </div>
            <button
              onClick={scrollToTop}
              className="flex items-center text-white hover:text-blue-300 transition-colors duration-200 ml-4"
              aria-label="Back to top"
            >
              <span className="mr-2">Back to Top</span>
              <FaArrowUp size={16} />
            </button>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;

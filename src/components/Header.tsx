"use client";
import React from "react";
import Link from "next/link";
import Image from "next/image";
import UOBLogo from "@/images/uob-logo-white.png";

const Header: React.FC = () => {
  return (
    <header className="bg-foreground text-white py-4 shadow-2xl">
      <div className="container mx-auto flex justify-between items-center px-4">
        <div className="text-lg font-bold flex flex-row items-center">
          <Link href="/" aria-label="Go to homepage">
            <Image src={UOBLogo} alt="UOB Logo" width={100} height={100} />
          </Link>
        </div>
        <nav className="space-x-4 flex flex-row">
          <Link href="/">
            <p className="text-gray-300 hover:text-white">Dashboard</p>
          </Link>
          <Link
            href="https://github.com/Jway77-ai/uob-hackathon-dragons"
            target="_blank"
            rel="noopener noreferrer"
          >
            <p className="text-gray-300 hover:text-white">GitHub</p>
          </Link>
        </nav>
      </div>
    </header>
  );
};

export default Header;

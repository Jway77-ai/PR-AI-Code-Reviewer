"use client";
import React from "react";
import Link from "next/link";
import Image from "next/image";
import UOBLogo from "@/images/uob-logo.png";

const Header: React.FC = () => {
  return (
    <header className="bg-foreground text-white py-4 shadow-2xl">
      <div className="container mx-auto flex justify-between items-center px-4">
        <div className="text-lg font-bold flex flex-row items-center">
          <Image src={UOBLogo} alt="UOB" width={40} />
          <div className="text-3xl cursor-default">
            <Link href="/">
              <p>UOB</p>
            </Link>
          </div>
        </div>
        <nav className="space-x-4 flex flex-row">
          <Link href="/">
            <p className="text-white-300 hover:text-white transition-transform duration-300 transform hover:scale-105">
              Dashboard
            </p>
          </Link>
          <Link
            href="https://github.com/Jway77-ai/uob-hackathon-dragons"
            target="_blank"
            rel="noopener noreferrer"
          >
            <p className="text-white-300 hover:text-white transition-transform duration-300 transform hover:scale-105">
              GitHub
            </p>
          </Link>
        </nav>
      </div>
    </header>
  );
};

export default Header;

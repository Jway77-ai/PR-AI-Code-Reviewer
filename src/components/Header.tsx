"use client";
import React from 'react';
import Link from 'next/link';
import Image from 'next/image';
import teamLogo from '@/images/team_logo.png';

const Header: React.FC = () => {
  return (
    <header className="bg-foreground text-white py-4 shadow-md">
      <div className="container mx-auto flex justify-between items-center px-4">
        <div className="text-lg font-bold">
            <Image
                src={teamLogo}
                alt="Team Logo"
                className="rounded-full"
                width={200}
            />
        </div>

        <nav className="space-x-4 flex flex-row">
          <Link href="/">
            <p className="text-gray-300 hover:text-white">Dashboard</p>
          </Link>
          <Link href="/feedback">
            <p className="text-gray-300 hover:text-white">Feedback</p>
          </Link>
        </nav>
      </div>
    </header>
  );
};

export default Header;
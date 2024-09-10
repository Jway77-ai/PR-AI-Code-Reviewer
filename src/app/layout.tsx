import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Debugging Dragons Hackathon Project",
  description: "Automated Pull Request Reviewer",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

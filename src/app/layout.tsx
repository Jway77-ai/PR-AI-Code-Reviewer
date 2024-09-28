import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "UOB Code Reviewer",
  description:
    " This code reviewer tool was developed as part of a hackathon to streamline the code review process and improve collaboration among UOB developers.",
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

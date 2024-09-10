/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        // Proxy API requests to the Flask backend in development
        source: "/api/:path*",
        destination:
          process.env.NODE_ENV === "development"
            ? "http://127.0.0.1:8000/api/:path*" // Ensure this matches your Flask port
            : "/api/:path*", // In production, route internally
      },
    ];
  },
};

export default nextConfig;

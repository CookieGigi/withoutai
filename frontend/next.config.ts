import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      { source: "/models", destination: "http://localhost:8000/models" },
      {
        source: "/models/current",
        destination: "http://localhost:8000/models/current",
      },
    ];
  },
  /* config options here */
};

export default nextConfig;

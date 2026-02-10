import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactCompiler: true,
  allowedDevOrigins: ['cleverhire.saisrinu.online'],
  experimental: {
    turbo: {
      resolveAlias: {
        // Add any aliases if needed
      },
    },
  },
};

export default nextConfig;

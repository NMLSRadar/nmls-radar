import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        primary: "#09090B",
        secondary: "#1E1B4B",
        tertiary: "#1D4ED8",
        accent: "#A78BFA",
        neutral: "#FFFFFF",
        "neutral-muted": "#94A3B8",
        "background-card": "#0F172A",
        "border-subtle": "#1F2937",
      },
      fontFamily: {
        sans: ["Inter", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
    },
  },
  plugins: [],
};
export default config;
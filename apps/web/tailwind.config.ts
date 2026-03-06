import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        surface: "var(--color-surface)",
        text: "var(--color-text)",
        primary: "var(--color-primary)"
      }
    }
  },
  plugins: []
};

export default config;

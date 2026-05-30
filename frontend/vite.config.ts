import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    proxy: {
      // /auth/* へのリクエストを FastAPI バックエンドへ転送 (CORS を回避)
      "/auth": "http://localhost:8000",
    },
  },
});

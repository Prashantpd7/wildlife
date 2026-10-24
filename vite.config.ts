import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: [
      {
        find: /^@designcodeio\/threeui\/style\.css$/,
        replacement: path.resolve(__dirname, "src/shaders/threeui.css"),
      },
      {
        find: /^@designcodeio\/threeui$/,
        replacement: path.resolve(
          __dirname,
          "src/shaders/sylva-living-world/SylvaLivingWorldScene.tsx"
        ),
      },
    ],
  },
});

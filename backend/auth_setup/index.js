// index.js
import dotenv from "dotenv";
import http from "http";
import { app } from "./app.js";
import connectDB from "./src/db/connection.js"; // ✅ corrected path

dotenv.config({ path: "./.env" });

const PORT = process.env.PORT || 8000;

// Immediately invoked async function for clean async handling
(async () => {
  try {
    // Connect to MongoDB
    await connectDB();
    console.log("✅ MongoDB connected successfully");

    // Create HTTP server
    const server = http.createServer(app);

    // Start server
    server.listen(PORT, () => {
      console.log(`🚀 Server is running at: http://localhost:${PORT}`);
    });
  } catch (err) {
    console.error("❌ Server startup failed:", err.message);
    process.exit(1); // Exit the process with failure
  }
})();

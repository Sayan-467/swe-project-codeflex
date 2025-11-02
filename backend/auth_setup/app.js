import express from "express";
import cors from "cors";
import userRoutes from "./src/routes/user.route.js";
import noteRoutes from "./src/routes/note.route.js";

const app = express();

// ✅ Middleware setup
app.use(
  cors({
    origin: process.env.CORS_ORIGIN || "*", // Allow all origins in development, restrict in production
    credentials: true,
  })
);

app.use(express.json({ limit: "16kb" }));
app.use(express.urlencoded({ extended: true, limit: "16kb" }));
app.use(express.static("public"));

// ✅ API Routes
app.use("/api/users", userRoutes);
app.use("/api/notes", noteRoutes);

// ✅ Health check route
app.get("/", (req, res) => {
  res.send("🚀 Server is running... Backend connected successfully!");
});

export { app };

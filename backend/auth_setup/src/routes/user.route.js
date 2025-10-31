import express from "express";
import { registerUser, loginUser, logoutUser } from "../controller/user.controller.js";

const router = express.Router();

// Register new user
router.post("/register", registerUser);

// Login
router.post("/login", loginUser);

// Logout
router.post("/logout", logoutUser);

export default router;

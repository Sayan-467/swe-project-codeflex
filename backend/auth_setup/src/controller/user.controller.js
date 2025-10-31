import User from "../models/user.model.js";
import {asynchandler} from "../utils/asynchandler.js";
import {ApiError} from "../utils/ApiError.js";
import {ApiResponse} from "../utils/ApiResponse.js";

// REGISTER user
export const registerUser = asynchandler(async (req, res) => {
  const { username, email, password } = req.body;

  if (!username || !email || !password) {
    throw new ApiError(400, "All fields are required");
  }

  const existingUser = await User.findOne({ email });
  if (existingUser) {
    throw new ApiError(400, "User already exists with this email");
  }

  const user = await User.create({ username, email, password });

  return res
    .status(201)
    .json(new ApiResponse(201, user, "User registered successfully"));
});

// LOGIN user (simple - no JWT, just check and return user info)
export const loginUser = asynchandler(async (req, res) => {
  const { email, password } = req.body;

  if (!email || !password) {
    throw new ApiError(400, "Email and password required");
  }

  const user = await User.findOne({ email });
  if (!user || user.password !== password) {
    throw new ApiError(401, "Invalid email or password");
  }

  return res
    .status(200)
    .json(new ApiResponse(200, user, "Login successful"));
});

// LOGOUT user (simple response since no tokens/session here)
export const logoutUser = asynchandler(async (req, res) => {
  return res
    .status(200)
    .json(new ApiResponse(200, null, "User logged out successfully"));
});

// GET all users
export const getAllUsers = asynchandler(async (req, res) => {
  const users = await User.find();
  return res
    .status(200)
    .json(new ApiResponse(200, users, "Fetched all users"));
});

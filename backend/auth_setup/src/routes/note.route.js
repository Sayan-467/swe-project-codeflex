import express from "express";
import {
  createNote,
  getAllNotes,
  getNotesByUser,
  updateNote,
  deleteNote
} from "../controller/note.controller.js";

const router = express.Router();

// Create a new note
router.post("/create", createNote);

// Get all notes
router.get("/all", getAllNotes);

// Get all notes by a specific user
router.get("/user/:userId", getNotesByUser);

// Update a note
router.put("/update/:id", updateNote);

// Delete a note
router.delete("/delete/:id", deleteNote);

export default router;

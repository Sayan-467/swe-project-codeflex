import Note from "../models/note.model.js";
import { asynchandler } from "../utils/asynchandler.js";
import { ApiError } from "../utils/ApiError.js";
import { ApiResponse } from "../utils/ApiResponse.js";

// CREATE Note
export const createNote = asynchandler(async (req, res) => {
  const { title, content, userId } = req.body;

  if (!title || !content || !userId) {
    throw new ApiError(400, "Title, content, and userId are required");
  }

  const note = await Note.create({ title, content, userId });

  return res
    .status(201)
    .json(new ApiResponse(201, note, "Note created successfully"));
});

// GET all Notes
export const getAllNotes = asynchandler(async (req, res) => {
  const notes = await Note.find();
  return res
    .status(200)
    .json(new ApiResponse(200, notes, "Fetched all notes"));
});

// GET Notes by user
export const getNotesByUser = asynchandler(async (req, res) => {
  const { userId } = req.params;

  const notes = await Note.find({ userId });
  if (!notes.length) {
    throw new ApiError(404, "No notes found for this user");
  }

  return res
    .status(200)
    .json(new ApiResponse(200, notes, "Fetched user notes"));
});

// UPDATE Note
export const updateNote = asynchandler(async (req, res) => {
  const { id } = req.params;
  const { title, content } = req.body;

  const note = await Note.findByIdAndUpdate(
    id,
    { title, content },
    { new: true }
  );

  if (!note) {
    throw new ApiError(404, "Note not found");
  }

  return res
    .status(200)
    .json(new ApiResponse(200, note, "Note updated successfully"));
});

// DELETE Note
export const deleteNote = asynchandler(async (req, res) => {
  const { id } = req.params;

  const note = await Note.findByIdAndDelete(id);

  if (!note) {
    throw new ApiError(404, "Note not found");
  }

  return res
    .status(200)
    .json(new ApiResponse(200, null, "Note deleted successfully"));
});

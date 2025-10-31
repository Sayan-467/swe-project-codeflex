// db/index.js
import mongoose from "mongoose";

const DB_NAME = "codeclue"; // name of your database

const connectDB = async () => {
  try {
    const connectionInstance = await mongoose.connect(`mongodb://127.0.0.1:27017/${DB_NAME}`, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });

    console.log(`✅ MongoDB connected successfully: ${connectionInstance.connection.host}`);
  } catch (error) {
    console.error("❌ Failed to connect to MongoDB:", error.message);
    process.exit(1);
  }
};

export default connectDB;

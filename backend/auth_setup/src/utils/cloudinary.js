// src/utils/cloudinary.js
import { v2 as cloudinary } from "cloudinary";
import fs from "fs";

const getCloudinary = () => {
  cloudinary.config({
    cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
    api_key: process.env.CLOUDINARY_API_KEY,
    api_secret: process.env.CLOUDINARY_API_SECRET,
  });
  return cloudinary;
};

export const uploadonCloudinary = async (localFilePath) => {
  try {
    if (!localFilePath) return null;

    const cloudinary = getCloudinary(); // credentials loaded here
    const response = await cloudinary.uploader.upload(localFilePath, { resource_type: "auto" });

    fs.unlinkSync(localFilePath); // delete temp file
    console.log("✅ Cloudinary uploaded:", response.secure_url);
    return response;
  } catch (error) {
    fs.unlinkSync(localFilePath);
    console.error("❌ Cloudinary upload error:", error);
    return null;
  }
};

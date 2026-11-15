import axios from 'axios';

// Base URL pointing to your FastAPI backend
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
/**
 * Sends a plant leaf image file to the FastAPI backend for disease classification.
 * @param {File} file - The image file selected from the upload component.
 * @returns {Promise<Object>} - The JSON response containing { class, confidence }.
 */
export const predictPlantDisease = async (file) => {
  try {
    // 1. Create a FormData object to hold the file stream
    const formData = new FormData();
    formData.append('file', file);

    // 2. Post the form data to the /predict endpoint using Axios
    const response = await axios.post(`${API_BASE_URL}/predict`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    // 3. Return the data payload from the backend
    return response.data;
  } catch (error) {
    // Extract a clean error message if FastAPI sent back an HTTPException detail
    const errorMessage =
      error.response?.data?.detail || error.message || 'Failed to connect to the prediction server.';
    throw new Error(errorMessage);
  }
};
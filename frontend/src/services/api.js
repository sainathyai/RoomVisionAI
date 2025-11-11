/**
 * API service for room detection.
 */

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:3001';
const API_KEY = import.meta.env.VITE_API_KEY || '';

class RoomDetectionAPI {
  constructor(baseURL = API_BASE_URL, apiKey = API_KEY) {
    this.client = axios.create({
      baseURL,
      headers: {
        'Content-Type': 'application/json',
        ...(apiKey && { 'x-api-key': apiKey })
      },
      timeout: 60000 // 60 seconds
    });

    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => {
        return response;
      },
      (error) => {
        console.error('API Error:', error.response?.data || error.message);
        return Promise.reject(this.handleError(error));
      }
    );
  }

  /**
   * Detect rooms from blueprint image.
   * @param {File} imageFile - Blueprint image file
   * @returns {Promise<Object>} Detection results
   */
  async detectRooms(imageFile) {
    try {
      // Convert file to base64
      const base64Image = await this.fileToBase64(imageFile);

      const response = await this.client.post('/detect-rooms', {
        image: base64Image,
        filename: imageFile.name
      });

      return {
        success: true,
        data: response.data,
        error: null
      };
    } catch (error) {
      return {
        success: false,
        data: null,
        error: error.message || 'Failed to detect rooms'
      };
    }
  }

  /**
   * Convert file to base64 string.
   * @param {File} file - File to convert
   * @returns {Promise<string>} Base64 string
   */
  fileToBase64(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        const base64 = reader.result.split(',')[1]; // Remove data:image/...;base64, prefix
        resolve(base64);
      };
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  }

  /**
   * Handle API errors.
   * @param {Error} error - Error object
   * @returns {Error} Formatted error
   */
  handleError(error) {
    if (error.response) {
      // Server responded with error
      const message = error.response.data?.error || error.response.data?.message || 'Server error';
      return new Error(message);
    } else if (error.request) {
      // Request made but no response
      return new Error('No response from server. Please check your connection.');
    } else {
      // Error in request setup
      return new Error(error.message || 'An unexpected error occurred');
    }
  }
}

// Export singleton instance
export const api = new RoomDetectionAPI();

// Export class for testing
export default RoomDetectionAPI;


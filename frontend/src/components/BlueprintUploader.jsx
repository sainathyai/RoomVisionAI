import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

/**
 * BlueprintUploader - Component for uploading blueprint images.
 */
export default function BlueprintUploader({ onFileSelect, isProcessing = false }) {
  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      
      // Validate file type
      const validTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif'];
      if (!validTypes.includes(file.type)) {
        alert('Please upload a valid image file (PNG, JPG, or GIF)');
        return;
      }
      
      // Validate file size (max 10MB)
      const maxSize = 10 * 1024 * 1024; // 10MB
      if (file.size > maxSize) {
        alert('File size must be less than 10MB');
        return;
      }
      
      onFileSelect(file);
    }
  }, [onFileSelect]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.gif']
    },
    maxFiles: 1,
    disabled: isProcessing
  });

  return (
    <div className="w-full">
      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-lg p-8 text-center cursor-pointer
          transition-colors duration-200
          ${isDragActive 
            ? 'border-primary-500 bg-primary-50' 
            : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
          }
          ${isProcessing ? 'opacity-50 cursor-not-allowed' : ''}
        `}
      >
        <input {...getInputProps()} />
        
        <div className="flex flex-col items-center space-y-4">
          <svg
            className="w-12 h-12 text-gray-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
            />
          </svg>
          
          {isDragActive ? (
            <p className="text-primary-600 font-medium">Drop the blueprint here...</p>
          ) : (
            <>
              <div>
                <p className="text-gray-700 font-medium">
                  Drag and drop a blueprint image here
                </p>
                <p className="text-gray-500 text-sm mt-1">or click to browse</p>
              </div>
              <p className="text-gray-400 text-xs">
                Supports PNG, JPG, GIF (max 10MB)
              </p>
            </>
          )}
        </div>
      </div>
    </div>
  );
}


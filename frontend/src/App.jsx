import React, { useState } from 'react';
import BlueprintUploader from './components/BlueprintUploader';
import BlueprintCanvas from './components/BlueprintCanvas';
import RoomList from './components/RoomList';
import { api } from './services/api';

function App() {
  const [blueprintFile, setBlueprintFile] = useState(null);
  const [blueprintPreview, setBlueprintPreview] = useState(null);
  const [detectedRooms, setDetectedRooms] = useState([]);
  const [selectedRoomId, setSelectedRoomId] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [processingTime, setProcessingTime] = useState(null);
  const [error, setError] = useState(null);

  const handleFileSelect = (file) => {
    setBlueprintFile(file);
    setError(null);
    setDetectedRooms([]);
    setSelectedRoomId(null);
    
    // Create preview URL
    const previewUrl = URL.createObjectURL(file);
    setBlueprintPreview(previewUrl);
  };

  const handleDetectRooms = async () => {
    if (!blueprintFile) {
      setError('Please select a blueprint image first');
      return;
    }

    setIsProcessing(true);
    setError(null);
    setDetectedRooms([]);
    setSelectedRoomId(null);

    try {
      const startTime = Date.now();
      const result = await api.detectRooms(blueprintFile);
      const endTime = Date.now();

      if (result.success && result.data.success) {
        setDetectedRooms(result.data.rooms || []);
        setProcessingTime(result.data.processing_time || (endTime - startTime) / 1000);
      } else {
        setError(result.error || result.data?.error || 'Failed to detect rooms');
      }
    } catch (err) {
      setError(err.message || 'An unexpected error occurred');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleRoomSelect = (roomId) => {
    setSelectedRoomId(roomId === selectedRoomId ? null : roomId);
  };

  const handleRoomEdit = (roomId) => {
    const room = detectedRooms.find(r => r.id === roomId);
    if (room) {
      const newName = prompt('Enter new room name:', room.name_hint || '');
      if (newName !== null) {
        setDetectedRooms(rooms =>
          rooms.map(r =>
            r.id === roomId ? { ...r, name_hint: newName } : r
          )
        );
      }
    }
  };

  const handleRoomDelete = (roomId) => {
    if (confirm('Are you sure you want to delete this room?')) {
      setDetectedRooms(rooms => rooms.filter(r => r.id !== roomId));
      if (selectedRoomId === roomId) {
        setSelectedRoomId(null);
      }
    }
  };

  const handleExport = () => {
    console.log('Rooms exported');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">RoomVisionAI</h1>
              <p className="text-sm text-gray-500">Automatic Room Detection from Blueprints</p>
            </div>
            {processingTime && (
              <div className="text-right">
                <div className="text-sm text-gray-500">Processing Time</div>
                <div className="text-lg font-semibold text-primary-600">
                  {processingTime.toFixed(2)}s
                </div>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-6">
          {/* Upload Section */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">Upload Blueprint</h2>
            <BlueprintUploader 
              onFileSelect={handleFileSelect}
              isProcessing={isProcessing}
            />
            
            {blueprintFile && (
              <div className="mt-4 flex items-center justify-between">
                <div className="text-sm text-gray-600">
                  Selected: <span className="font-medium">{blueprintFile.name}</span>
                  {' '}({(blueprintFile.size / 1024 / 1024).toFixed(2)} MB)
                </div>
                <button
                  onClick={handleDetectRooms}
                  disabled={isProcessing}
                  className={`
                    px-6 py-2 rounded-lg font-medium transition-colors
                    ${isProcessing
                      ? 'bg-gray-400 cursor-not-allowed text-white'
                      : 'bg-primary-600 hover:bg-primary-700 text-white'
                    }
                  `}
                >
                  {isProcessing ? 'Processing...' : 'Detect Rooms'}
                </button>
              </div>
            )}

            {error && (
              <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-sm text-red-800">{error}</p>
              </div>
            )}
          </div>

          {/* Results Section */}
          {blueprintPreview && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Canvas */}
              <div className="lg:col-span-2">
                <div className="bg-white rounded-lg shadow-md p-4">
                  <h2 className="text-lg font-semibold text-gray-800 mb-4">Blueprint Visualization</h2>
                  <div className="h-[600px]">
                    <BlueprintCanvas
                      blueprintImage={blueprintPreview}
                      detectedRooms={detectedRooms}
                      selectedRoomId={selectedRoomId}
                      onRoomSelect={handleRoomSelect}
                    />
                  </div>
                </div>
              </div>

              {/* Room List */}
              <div className="lg:col-span-1">
                <div className="h-[600px]">
                  <RoomList
                    rooms={detectedRooms}
                    selectedRoomId={selectedRoomId}
                    onRoomSelect={handleRoomSelect}
                    onRoomEdit={handleRoomEdit}
                    onRoomDelete={handleRoomDelete}
                    onExport={handleExport}
                  />
                </div>
              </div>
            </div>
          )}

          {/* Empty State */}
          {!blueprintPreview && (
            <div className="bg-white rounded-lg shadow-md p-12 text-center">
              <svg
                className="mx-auto h-12 w-12 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
              <h3 className="mt-4 text-lg font-medium text-gray-900">No Blueprint Loaded</h3>
              <p className="mt-2 text-sm text-gray-500">
                Upload a blueprint image to get started with room detection
              </p>
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-12 border-t border-gray-200 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-sm text-gray-500">
            RoomVisionAI - Powered by AWS Bedrock & Claude Vision
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;


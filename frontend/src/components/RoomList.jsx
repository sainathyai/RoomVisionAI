import React from 'react';

/**
 * RoomList - Component for displaying list of detected rooms.
 */
export default function RoomList({ 
  rooms = [], 
  selectedRoomId = null,
  onRoomSelect = () => {},
  onRoomEdit = () => {},
  onRoomDelete = () => {},
  onExport = () => {}
}) {
  const selectedRoom = rooms.find(r => r.id === selectedRoomId);

  const handleExport = () => {
    const dataStr = JSON.stringify(rooms, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'detected_rooms.json';
    link.click();
    URL.revokeObjectURL(url);
    
    if (onExport) onExport();
  };

  const calculateArea = (bbox) => {
    const width = bbox[2] - bbox[0];
    const height = bbox[3] - bbox[1];
    return (width * height / 1000000).toFixed(2); // Normalized area
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-4 h-full flex flex-col">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold text-gray-800">Detected Rooms</h2>
        <span className="text-sm text-gray-500">{rooms.length} rooms</span>
      </div>

      {rooms.length === 0 ? (
        <div className="flex-1 flex items-center justify-center text-gray-400">
          <p>No rooms detected yet</p>
        </div>
      ) : (
        <>
          <div className="flex-1 overflow-y-auto space-y-2 mb-4">
            {rooms.map((room, index) => {
              const isSelected = selectedRoomId === room.id;
              const bbox = room.bounding_box;

              return (
                <div
                  key={room.id}
                  className={`
                    p-3 rounded-lg border-2 cursor-pointer transition-all
                    ${isSelected 
                      ? 'border-primary-500 bg-primary-50' 
                      : 'border-gray-200 hover:border-primary-300 hover:bg-gray-50'
                    }
                  `}
                  onClick={() => onRoomSelect(room.id)}
                >
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center space-x-2">
                        <span className="font-semibold text-gray-800">
                          {room.name_hint || `Room ${index + 1}`}
                        </span>
                        <span className="text-xs text-gray-400">#{room.id}</span>
                      </div>
                      <div className="mt-1 text-xs text-gray-600">
                        <div>Coordinates: [{bbox[0]}, {bbox[1]}, {bbox[2]}, {bbox[3]}]</div>
                        <div>Area: {calculateArea(bbox)} units²</div>
                      </div>
                    </div>
                    <div className="flex space-x-1">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          onRoomEdit(room.id);
                        }}
                        className="p-1 text-gray-400 hover:text-primary-600"
                        title="Edit room"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                        </svg>
                      </button>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          onRoomDelete(room.id);
                        }}
                        className="p-1 text-gray-400 hover:text-red-600"
                        title="Delete room"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {selectedRoom && (
            <div className="mb-4 p-3 bg-gray-50 rounded-lg">
              <h3 className="font-semibold text-sm text-gray-700 mb-2">Selected Room</h3>
              <div className="text-xs text-gray-600 space-y-1">
                <div><strong>ID:</strong> {selectedRoom.id}</div>
                <div><strong>Name:</strong> {selectedRoom.name_hint || 'Unnamed'}</div>
                <div><strong>Bounding Box:</strong> [{selectedRoom.bounding_box.join(', ')}]</div>
              </div>
            </div>
          )}

          <button
            onClick={handleExport}
            className="w-full bg-primary-600 text-white py-2 px-4 rounded-lg hover:bg-primary-700 transition-colors font-medium"
          >
            Export JSON
          </button>
        </>
      )}
    </div>
  );
}


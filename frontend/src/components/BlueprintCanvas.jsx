import React, { useRef, useEffect, useState } from 'react';
import { Stage, Layer, Image as KonvaImage, Rect, Text } from 'react-konva';

/**
 * BlueprintCanvas - Component for displaying blueprint with detected rooms.
 */
export default function BlueprintCanvas({ 
  blueprintImage, 
  detectedRooms = [], 
  selectedRoomId = null,
  onRoomSelect = () => {}
}) {
  const [image, setImage] = useState(null);
  const [scale, setScale] = useState(1);
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const stageRef = useRef(null);

  // Load blueprint image
  useEffect(() => {
    if (!blueprintImage) {
      setImage(null);
      return;
    }

    const img = new window.Image();
    img.crossOrigin = 'anonymous';
    img.onload = () => {
      setImage(img);
      
      // Auto-fit to canvas
      if (stageRef.current) {
        const stage = stageRef.current;
        const stageWidth = stage.width();
        const stageHeight = stage.height();
        
        const scaleX = stageWidth / img.width;
        const scaleY = stageHeight / img.height;
        const newScale = Math.min(scaleX, scaleY, 1); // Don't scale up
        
        setScale(newScale);
        setPosition({
          x: (stageWidth - img.width * newScale) / 2,
          y: (stageHeight - img.height * newScale) / 2
        });
      }
    };
    
    if (typeof blueprintImage === 'string') {
      img.src = blueprintImage;
    } else if (blueprintImage instanceof File) {
      img.src = URL.createObjectURL(blueprintImage);
    }
  }, [blueprintImage]);

  // Convert normalized coordinates (0-1000) to canvas coordinates
  const normalizeToCanvas = (coord, dimension) => {
    if (!image) return coord;
    return (coord / 1000) * dimension * scale;
  };

  // Handle room click
  const handleRoomClick = (roomId) => {
    onRoomSelect(roomId);
  };

  // Colors for rooms
  const roomColors = [
    '#3b82f6', '#ef4444', '#10b981', '#f59e0b',
    '#8b5cf6', '#ec4899', '#06b6d4', '#84cc16'
  ];

  const getRoomColor = (index) => {
    return roomColors[index % roomColors.length];
  };

  if (!image) {
    return (
      <div className="w-full h-full flex items-center justify-center bg-gray-100 rounded-lg">
        <p className="text-gray-400">No blueprint loaded</p>
      </div>
    );
  }

  return (
    <div className="w-full h-full border border-gray-300 rounded-lg overflow-hidden bg-white">
      <Stage
        ref={stageRef}
        width={800}
        height={600}
        onWheel={(e) => {
          e.evt.preventDefault();
          const scaleBy = 1.1;
          const stage = e.target.getStage();
          const oldScale = scale;
          const mousePointTo = {
            x: stage.getPointerPosition().x / oldScale - position.x / oldScale,
            y: stage.getPointerPosition().y / oldScale - position.y / oldScale,
          };

          const newScale = e.evt.deltaY > 0 ? oldScale / scaleBy : oldScale * scaleBy;
          const clampedScale = Math.max(0.5, Math.min(2, newScale));

          setScale(clampedScale);
          setPosition({
            x: (stage.getPointerPosition().x / clampedScale - mousePointTo.x) * clampedScale,
            y: (stage.getPointerPosition().y / clampedScale - mousePointTo.y) * clampedScale,
          });
        }}
        draggable
        onDragEnd={(e) => {
          setPosition({
            x: e.target.x(),
            y: e.target.y(),
          });
        }}
      >
        <Layer>
          {/* Blueprint image */}
          <KonvaImage
            image={image}
            x={position.x}
            y={position.y}
            scaleX={scale}
            scaleY={scale}
          />

          {/* Detected rooms */}
          {detectedRooms.map((room, index) => {
            const bbox = room.bounding_box;
            const x = normalizeToCanvas(bbox[0], image.width) + position.x;
            const y = normalizeToCanvas(bbox[1], image.height) + position.y;
            const width = normalizeToCanvas(bbox[2] - bbox[0], image.width);
            const height = normalizeToCanvas(bbox[3] - bbox[1], image.height);
            
            const isSelected = selectedRoomId === room.id;
            const color = getRoomColor(index);

            return (
              <React.Fragment key={room.id}>
                {/* Room bounding box */}
                <Rect
                  x={x}
                  y={y}
                  width={width}
                  height={height}
                  stroke={color}
                  strokeWidth={isSelected ? 3 : 2}
                  fill={`${color}20`} // 20% opacity
                  opacity={0.7}
                  onClick={() => handleRoomClick(room.id)}
                  onTap={() => handleRoomClick(room.id)}
                  draggable={false}
                />
                
                {/* Room label */}
                {room.name_hint && (
                  <Text
                    x={x + width / 2}
                    y={y + height / 2}
                    text={room.name_hint}
                    fontSize={14}
                    fill={color}
                    fontStyle="bold"
                    align="center"
                    verticalAlign="middle"
                    offsetX={50}
                    offsetY={7}
                    onClick={() => handleRoomClick(room.id)}
                    onTap={() => handleRoomClick(room.id)}
                  />
                )}
              </React.Fragment>
            );
          })}
        </Layer>
      </Stage>
    </div>
  );
}


import React, { useState, useCallback } from 'react';

const ShearStrainDemo = () => {
  const [shearAmount, setShearAmount] = useState(0.3);
  const [selectedMaterial, setSelectedMaterial] = useState('rubber');
  
  // Material properties with different rigidity/stiffness values
  // Higher values = more resistance to shear (lower deformation at same stress)
  const materials = {
    rubber: { name: "Rubber", stiffness: 0.5, color: "#4169E1" },
    wood: { name: "Wood (parallel to grain)", stiffness: 2.0, color: "#4169E1" },
    aluminum: { name: "Aluminum", stiffness: 3.5, color: "#4169E1" },
    steel: { name: "Steel", stiffness: 4.0, color: "#4169E1" },
    concrete: { name: "Concrete", stiffness: 3.0, color: "#4169E1" },
    glass: { name: "Glass", stiffness: 2.5, color: "#4169E1" },
    diamond: { name: "Diamond", stiffness: 5.0, color: "#4169E1" }
  };
  
  // Handle material selection
  const handleMaterialChange = (e) => {
    setSelectedMaterial(e.target.value);
  };
  
  // Calculate actual deformation based on material stiffness
  // Stiffer materials deform less under the same shear stress
  const getActualShearAmount = useCallback(() => {
    const normalizedStiffness = materials[selectedMaterial].stiffness / 5.0; // Normalize to 0-1 scale
    return shearAmount * (1 - 0.7 * normalizedStiffness); // Adjust deformation by stiffness
  }, [shearAmount, selectedMaterial, materials]);
  
  const actualShear = getActualShearAmount();
  
  // Base dimensions for the rectangular block
  const baseWidth = 200;
  const baseHeight = 200;
  
  // Calculate the sheared position
  const shearMatrix = (x, y) => {
    // Shear transformation matrix
    return {
      x: x + y * actualShear,
      y: y
    };
  };
  
  // Generate grid points
  const generateGrid = useCallback((width, height, cols, rows) => {
    const points = [];
    
    for (let i = 0; i <= rows; i++) {
      for (let j = 0; j <= cols; j++) {
        const normalX = j * (width / cols);
        const normalY = i * (height / rows);
        
        // Apply shear transformation
        const { x, y } = shearMatrix(normalX, normalY);
        
        points.push({ x, y, row: i, col: j });
      }
    }
    
    return points;
  }, [actualShear]);
  
  const gridPoints = generateGrid(baseWidth, baseHeight, 4, 4);
  
  // Draw grid lines
  const renderGrid = () => {
    const lines = [];
    const cols = 5; // Number of points in a row (4 cells + 1)
    
    // Horizontal lines
    for (let i = 0; i <= 4; i++) {
      const rowStartIdx = i * 5;
      for (let j = 0; j < 4; j++) {
        const idx = rowStartIdx + j;
        lines.push(
          <line 
            key={`h${idx}`}
            x1={gridPoints[idx].x} 
            y1={gridPoints[idx].y} 
            x2={gridPoints[idx + 1].x} 
            y2={gridPoints[idx + 1].y} 
            stroke="#4169E1" 
            strokeWidth="1.5"
          />
        );
      }
    }
    
    // Vertical lines
    for (let j = 0; j <= 4; j++) {
      for (let i = 0; i < 4; i++) {
        const idx = i * 5 + j;
        lines.push(
          <line 
            key={`v${idx}`}
            x1={gridPoints[idx].x} 
            y1={gridPoints[idx].y} 
            x2={gridPoints[idx + 5].x} 
            y2={gridPoints[idx + 5].y} 
            stroke="#4169E1" 
            strokeWidth="1.5"
          />
        );
      }
    }
    
    return lines;
  };
  
  // Calculate the angle between two initially perpendicular lines
  const calculateShearAngle = useCallback(() => {
    // Tan-1(shear) gives the angle in radians
    const angleInRadians = Math.atan(actualShear);
    // Convert to degrees
    return (angleInRadians * 180 / Math.PI).toFixed(1);
  }, [actualShear]);
  
  // Calculate the deformed angle (90° - shear angle)
  const calculateDeformedAngle = useCallback(() => {
    return (90 - parseFloat(calculateShearAngle())).toFixed(1);
  }, [calculateShearAngle]);

  // Max dimensions to prevent layout shift
  const maxSvgWidth = baseWidth * 1.5 + 80;
  const maxSvgHeight = baseHeight + 80;

  const shearAngle = calculateShearAngle();
  const deformedAngle = calculateDeformedAngle();

  return (
    <div className="tw-flex tw-justify-center tw-w-full">
      <div className="tw-w-full tw-max-w-2xl tw-my-10 tw-px-4">
        <div className="tw-flex tw-flex-col tw-items-center tw-p-6 tw-bg-gray-50 tw-rounded-lg tw-shadow-md">
          
          {/* Simple metrics display */}
          <div className="tw-flex tw-justify-between tw-w-full tw-mb-4">
            <div className="tw-p-2 tw-rounded-md tw-w-full tw-flex tw-justify-between">
              <span className="tw-font-medium">Material: {materials[selectedMaterial].name}</span>
              <span className="tw-font-medium">Shear Angle (γ): {shearAngle}°</span>
            </div>
          </div>
          
          {/* Fixed size visualization container */}
          <div className="tw-relative tw-mb-6 tw-overflow-hidden tw-bg-white tw-p-6 tw-rounded tw-border tw-border-gray-200 tw-shadow-sm" 
               style={{ width: '100%', height: 'auto', minHeight: '300px' }}>
            <div className="tw-flex tw-justify-center tw-items-center">
              <svg 
                style={{ maxWidth: '100%', height: 'auto' }}
                width={maxSvgWidth}
                height={maxSvgHeight}
                viewBox={`-40 -40 ${baseWidth * 1.5 + 80} ${baseHeight + 80}`}
                preserveAspectRatio="xMidYMid meet"
              >
                {/* Original 90-degree angle marker - top left */}
                <g>
                  <path 
                    d="M0,30 L0,0 L30,0" 
                    stroke="#FF0000" 
                    strokeWidth="2"
                    fill="none"
                  />
                  <text 
                    x="20" 
                    y="-5" 
                    textAnchor="middle" 
                    fill="#000000" 
                    fontSize="12"
                  >
                    90°
                  </text>
                  
                  {/* Deformed angle value */}
                  <text 
                    x="40" 
                    y="20" 
                    textAnchor="start" 
                    fill="#FF0000" 
                    fontSize="14"
                    fontWeight="bold"
                  >
                    {deformedAngle}°
                  </text>
                </g>
                
                {/* Material block with shear deformation */}
                <g transform={`translate(30, 30)`}>
                  {/* Outline of the deformed shape */}
                  <path 
                    d={`M0,0 L${baseWidth},0 L${baseWidth + baseHeight * actualShear},${baseHeight} L${baseHeight * actualShear},${baseHeight} Z`} 
                    fill="#CCCCCC" 
                    stroke="#4169E1" 
                    strokeWidth="2"
                  />
                  
                  {/* Grid lines */}
                  {renderGrid()}
                  
                  {/* Angle change indicator - top right corner */}
                  <g transform={`translate(${baseWidth + 10}, 10)`}>
                    <text 
                      x="0" 
                      y="0" 
                      textAnchor="start" 
                      fill="#4169E1" 
                      fontSize="14"
                      fontWeight="bold"
                    >
                      Angle Change
                    </text>
                    
                    {/* Angle marker */}
                    <path 
                      d={`M-20,20 L0,0 L20,0`} 
                      stroke="#FF0000"
                      strokeWidth="2"
                      fill="none"
                    />
                    
                    {/* Gamma value */}
                    <text 
                      x="15" 
                      y="25" 
                      textAnchor="middle" 
                      fill="#FF0000" 
                      fontSize="14"
                      fontWeight="bold"
                    >
                      γ = {shearAngle}°
                    </text>
                  </g>
                </g>
                
                {/* Top and bottom force arrows */}
                <g>
                  {/* Top arrow (pointing right) */}
                  <g transform="translate(120, 10)">
                    <line 
                      x1="-40" 
                      y1="0" 
                      x2="40" 
                      y2="0" 
                      stroke="#FF0000" 
                      strokeWidth="2"
                    />
                    <polygon 
                      points="40,0 30,-5 30,5" 
                      fill="#FF0000" 
                    />
                    <text 
                      x="0" 
                      y="-10" 
                      textAnchor="middle" 
                      fill="#4169E1" 
                      fontSize="16"
                      fontWeight="bold"
                    >
                      Shear Force
                    </text>
                  </g>
                  
                  {/* Bottom arrow (pointing left) */}
                  <g transform={`translate(${120 + baseHeight * actualShear}, ${baseHeight + 50})`}>
                    <line 
                      x1="40" 
                      y1="0" 
                      x2="-40" 
                      y2="0" 
                      stroke="#FF0000" 
                      strokeWidth="2"
                    />
                    <polygon 
                      points="-40,0 -30,-5 -30,5" 
                      fill="#FF0000" 
                    />
                  </g>
                </g>
              </svg>
            </div>
          </div>
          
          <div className="tw-w-full tw-max-w-md tw-space-y-4">
            <div>
              <label className="tw-flex tw-justify-between tw-text-sm tw-font-medium tw-mb-1">
                <span>Material Selection</span>
                <span>Deformed Angle: {deformedAngle}°</span>
              </label>
              <select 
                value={selectedMaterial} 
                onChange={handleMaterialChange}
                className="tw-w-full tw-p-2 tw-border tw-border-gray-300 tw-rounded-md tw-shadow-sm"
              >
                {Object.keys(materials).map(key => (
                  <option key={key} value={key}>
                    {materials[key].name}
                  </option>
                ))}
              </select>
            </div>
          
            <div>
              <label className="tw-block tw-text-sm tw-font-medium tw-mb-1">
                Applied Shear Stress: {(shearAmount * 100).toFixed(0)}%
              </label>
              <input 
                type="range" 
                min="0" 
                max="1" 
                step="0.01" 
                value={shearAmount} 
                onChange={(e) => setShearAmount(parseFloat(e.target.value))}
                className="tw-w-full tw-h-2 tw-bg-blue-200 tw-rounded-lg tw-appearance-none tw-cursor-pointer"
              />
              <div className="tw-flex tw-justify-between tw-text-xs tw-mt-1">
                <span>No Stress</span>
                <span>Maximum Stress</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ShearStrainDemo;

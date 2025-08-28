import React, { useState, useEffect } from 'react';

const PoissonsRatioDemo = () => {
  const [stretchAmount, setStretchAmount] = useState(0.5);
  const [poissonsRatio, setPoissonsRatio] = useState(0.3);
  const [selectedMaterial, setSelectedMaterial] = useState('custom');
  const [animateDemo, setAnimateDemo] = useState(false);
  
  // Material presets with their Poisson's ratios
  const materials = {
    custom: { name: "Custom Value", ratio: poissonsRatio, color: "#3b82f6" },
    rubber: { name: "Rubber", ratio: 0.5, color: "#000000" },
    steel: { name: "Steel", ratio: 0.3, color: "#6b7280" },
    aluminum: { name: "Aluminum", ratio: 0.33, color: "#9ca3af" },
    brass: { name: "Brass", ratio: 0.34, color: "#fbbf24" },
    glass: { name: "Glass", ratio: 0.22, color: "#a5f3fc" },
    concrete: { name: "Concrete", ratio: 0.2, color: "#9ca3af" },
    cork: { name: "Cork", ratio: 0.0, color: "#d97706" },
    foam: { name: "Typical Foam", ratio: 0.1, color: "#fef3c7" },
    bone: { name: "Bone", ratio: 0.3, color: "#f3f4f6" },
    auxetic: { name: "Auxetic Material", ratio: -0.3, color: "#ec4899" }
  };
  
  // Handle material selection
  const handleMaterialChange = (e) => {
    const material = e.target.value;
    setSelectedMaterial(material);
    
    if (material !== 'custom') {
      setPoissonsRatio(materials[material].ratio);
    }
  };
  
  // Calculate dimensions based on stretchAmount and Poisson's ratio
  const lengthScale = 1 + stretchAmount;
  const widthScale = poissonsRatio === 0 ? 1 : 1 - (poissonsRatio * stretchAmount);
  
  // Generate coordinate grid
  const generateGrid = (baseWidth, baseHeight, cols, rows) => {
    const points = [];
    
    for (let i = 0; i <= rows; i++) {
      for (let j = 0; j <= cols; j++) {
        const normalizedX = j / cols;
        const normalizedY = i / rows;
        
        const x = normalizedX * baseWidth * lengthScale;
        const y = normalizedY * baseHeight * widthScale;
        
        points.push({ x, y, row: i, col: j });
      }
    }
    
    return points;
  };
  
  const baseWidth = 300;
  const baseHeight = 120;
  const gridPoints = generateGrid(baseWidth, baseHeight, 10, 4);
  
  // Draw connections between adjacent points
  const renderGrid = () => {
    const lines = [];
    const cols = 11; // Number of points in a row (10 cells + 1)
    
    // Horizontal lines
    for (let i = 0; i < gridPoints.length - 1; i++) {
      if (gridPoints[i].col < 10) { // Not the last in row
        lines.push(
          <line 
            key={`h${i}`}
            x1={gridPoints[i].x} 
            y1={gridPoints[i].y} 
            x2={gridPoints[i+1].x} 
            y2={gridPoints[i+1].y} 
            stroke="#3b82f6" 
            strokeWidth="2"
          />
        );
      }
    }
    
    // Vertical lines
    for (let i = 0; i < gridPoints.length - cols; i++) {
      lines.push(
        <line 
          key={`v${i}`}
          x1={gridPoints[i].x} 
          y1={gridPoints[i].y} 
          x2={gridPoints[i+cols].x} 
          y2={gridPoints[i+cols].y} 
          stroke="#3b82f6" 
          strokeWidth="2"
        />
      );
    }
    
    return lines;
  };

  // Animation toggle effect
  useEffect(() => {
    if (animateDemo) {
      const interval = setInterval(() => {
        setStretchAmount(prev => {
          // Oscillate between 0.1 and 0.8
          if (prev >= 0.8) return 0.1;
          return prev + 0.1;
        });
      }, 800);
      
      return () => clearInterval(interval);
    }
  }, [animateDemo]);


  
  // Calculate the maximum possible SVG dimensions to create a stable container
  const maxSvgWidth = baseWidth * 2 + 80; // Maximum width with max stretch
  const maxSvgHeight = baseHeight * 2 + 80; // Maximum height with max contraction

  return (
    // Main container with fixed width to prevent layout shifts
    <div className="tw-flex tw-justify-center tw-w-full">
      <div className="tw-w-full tw-max-w-2xl tw-my-10 tw-px-4">
        <div className="tw-flex tw-flex-col tw-items-center tw-p-6 tw-bg-gray-50 tw-rounded-lg tw-shadow-md">
          
          {/* Simple metrics display */}
          <div className="tw-flex tw-justify-between tw-w-full tw-mb-4">
            <div className="tw-p-3 tw-rounded-md tw-w-full tw-flex tw-justify-between">
              <span className="tw-font-medium">ν = {poissonsRatio.toFixed(2)}</span>
              <span className="tw-font-medium">Stretch: {(stretchAmount * 100).toFixed(0)}%</span>
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
                viewBox={`-40 -40 ${baseWidth * Math.max(lengthScale, 1) + 80} ${baseHeight * Math.max(1, 1/Math.abs(widthScale)) + 80}`}
                preserveAspectRatio="xMidYMid meet"
              >
                {/* Material block */}
                <rect 
                  x="0" 
                  y="0" 
                  width={baseWidth * lengthScale} 
                  height={baseHeight * widthScale} 
                  fill={`rgba(${parseInt(materials[selectedMaterial].color.slice(1, 3), 16)}, 
                         ${parseInt(materials[selectedMaterial].color.slice(3, 5), 16)}, 
                         ${parseInt(materials[selectedMaterial].color.slice(5, 7), 16)}, 0.3)`} 
                  stroke={materials[selectedMaterial].color} 
                  strokeWidth="3"
                />
                
                {/* Grid */}
                {renderGrid()}
                
                {/* Original dimensions overlay (dotted line) */}
                <rect
                  x="0"
                  y="0"
                  width={baseWidth}
                  height={baseHeight}
                  fill="none"
                  stroke="#6b7280"
                  strokeWidth="1.5"
                  strokeDasharray="5,5"
                  opacity="0.7"
                />
                
                {/* Labels */}
                <text x={baseWidth * lengthScale / 2} y={-25} textAnchor="middle" fill="#1e40af" fontWeight="bold">
                  Stretching
                </text>
                
                {/* Vertical effect label */}
                {poissonsRatio !== 0 && (
                  <text x={-35} y={baseHeight * widthScale / 2} textAnchor="middle" fill="#1e40af" fontWeight="bold" transform={`rotate(-90 -35 ${baseHeight * widthScale / 2})`}>
                    {poissonsRatio > 0 ? "Contracting" : "Expanding"}
                  </text>
                )}
                
                {/* Visual indicators moved closer to edges */}
                <g opacity={stretchAmount > 0.05 ? 1 : 0}>
                  {/* Horizontal stretch arrows */}
                  <g>
                    {/* Left arrow */}
                    <path d="M-20,0 L-5,0" stroke="#dc2626" strokeWidth="1.5"/>
                    <path d="M-10,-4 L-5,0 L-10,4" stroke="#dc2626" strokeWidth="1.5" fill="none"/>
                    
                    {/* Right arrow */}
                    <path d={`M${baseWidth * lengthScale + 5},0 L${baseWidth * lengthScale + 20},0`} stroke="#dc2626" strokeWidth="1.5"/>
                    <path d={`M${baseWidth * lengthScale + 15},-4 L${baseWidth * lengthScale + 20},0 L${baseWidth * lengthScale + 15},4`} stroke="#dc2626" strokeWidth="1.5" fill="none"/>
                  </g>
                  
                  {/* Vertical contraction/expansion indicators */}
                  {poissonsRatio !== 0 && (
                    <g>
                      {poissonsRatio > 0 ? (
                        <>
                          {/* Top arrow pointing inward for contraction */}
                          <path d="M0,-20 L0,-5" stroke="#dc2626" strokeWidth="1.5"/>
                          <path d="M-4,-10 L0,-5 L4,-10" stroke="#dc2626" strokeWidth="1.5" fill="none"/>
                          
                          {/* Bottom arrow pointing inward for contraction */}
                          <path d={`M0,${baseHeight * widthScale + 5} L0,${baseHeight * widthScale + 20}`} stroke="#dc2626" strokeWidth="1.5"/>
                          <path d={`M-4,${baseHeight * widthScale + 15} L0,${baseHeight * widthScale + 20} L4,${baseHeight * widthScale + 15}`} stroke="#dc2626" strokeWidth="1.5" fill="none"/>
                        </>
                      ) : (
                        <>
                          {/* Top arrow pointing outward for expansion */}
                          <path d="M0,-20 L0,-5" stroke="#dc2626" strokeWidth="1.5"/>
                          <path d="M-4,-15 L0,-20 L4,-15" stroke="#dc2626" strokeWidth="1.5" fill="none"/>
                          
                          {/* Bottom arrow pointing outward for expansion */}
                          <path d={`M0,${baseHeight * widthScale + 5} L0,${baseHeight * widthScale + 20}`} stroke="#dc2626" strokeWidth="1.5"/>
                          <path d={`M-4,${baseHeight * widthScale + 10} L0,${baseHeight * widthScale + 5} L4,${baseHeight * widthScale + 10}`} stroke="#dc2626" strokeWidth="1.5" fill="none"/>
                        </>
                      )}
                    </g>
                  )}
                </g>
                

              </svg>
            </div>
          </div>
          
          {/* Controls with fixed width to prevent layout shifts */}
          <div className="tw-w-full tw-max-w-md tw-space-y-4">
            <div className="tw-flex tw-justify-end tw-mb-2">
              <button 
                onClick={() => setAnimateDemo(!animateDemo)} 
                className={`tw-px-3 tw-py-2 tw-text-sm tw-rounded-md tw-shadow-sm ${animateDemo 
                  ? 'tw-bg-red-100 tw-text-red-700 tw-border tw-border-red-300' 
                  : 'tw-bg-blue-100 tw-text-blue-700 tw-border tw-border-blue-300'}`}
              >
                {animateDemo ? 'Stop Animation' : 'Animate Demo'}
              </button>
            </div>
            
            <div>
              <label className="tw-block tw-text-sm tw-font-medium tw-mb-1">
                Material Selection
              </label>
              <select 
                value={selectedMaterial} 
                onChange={handleMaterialChange}
                className="tw-w-full tw-p-2 tw-border tw-border-gray-300 tw-rounded-md tw-shadow-sm"
                disabled={animateDemo}
              >
                {Object.keys(materials).map(key => (
                  <option key={key} value={key}>
                    {materials[key].name} {key !== 'custom' ? `(ν = ${materials[key].ratio.toFixed(2)})` : ''}
                  </option>
                ))}
              </select>
            </div>
          
            <div>
              <label className="tw-block tw-text-sm tw-font-medium tw-mb-1">
                Poisson's Ratio
              </label>
              <input 
                type="range" 
                min="-0.5" 
                max="0.5" 
                step="0.01" 
                value={poissonsRatio} 
                onChange={(e) => {
                  setPoissonsRatio(parseFloat(e.target.value));
                  setSelectedMaterial('custom');
                }}
                className="tw-w-full tw-h-2 tw-bg-gray-200 tw-rounded-lg tw-appearance-none tw-cursor-pointer"
                disabled={animateDemo || selectedMaterial !== 'custom'}
              />
              <div className="tw-flex tw-justify-between tw-text-xs tw-text-gray-500 tw-mt-1">
                <span>-0.5</span>
                <span>0</span>
                <span>0.5</span>
              </div>
            </div>
            
            <div>
              <label className="tw-block tw-text-sm tw-font-medium tw-mb-1">
                Stretch Amount
              </label>
              <input 
                type="range" 
                min="0" 
                max="1" 
                step="0.01" 
                value={stretchAmount} 
                onChange={(e) => setStretchAmount(parseFloat(e.target.value))}
                className="tw-w-full tw-h-2 tw-bg-gray-200 tw-rounded-lg tw-appearance-none tw-cursor-pointer"
                disabled={animateDemo}
              />
            </div>
            

          </div>
        </div>
      </div>
    </div>
  );
};

export default PoissonsRatioDemo;

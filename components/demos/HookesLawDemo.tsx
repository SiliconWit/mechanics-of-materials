import React, { useState, useEffect, useRef } from 'react';

const HookesLawDemo = () => {
  const [force, setForce] = useState(0.3);
  const [selectedMaterial, setSelectedMaterial] = useState('steel');
  const [animate, setAnimate] = useState(false);
  const [showElasticLine, setShowElasticLine] = useState(true);
  const animationRef = useRef(null);
  
  // Material properties with Young's Modulus values (in GPa)
  const materials = {
    steel: { name: "Steel", E: 200, color: "#6b7280", maxStrain: 0.005 },
    aluminum: { name: "Aluminum", E: 69, color: "#9ca3af", maxStrain: 0.01 },
    titanium: { name: "Titanium", E: 110, color: "#d1d5db", maxStrain: 0.008 },
    abs: { name: "ABS Plastic", E: 2.3, color: "#fbbf24", maxStrain: 0.03 },
    rubber: { name: "Rubber", E: 0.05, color: "#1f2937", maxStrain: 0.3 },
  };
  
  // Handle material selection
  const handleMaterialChange = (e) => {
    setSelectedMaterial(e.target.value);
  };
  
  // Calculate strain based on force and material's Young's Modulus
  const calculateStrain = () => {
    // Normalize force to be between 0 and 1 for slider
    const normalizedForce = force; 
    
    // Scale force proportionally to material's maximum strain
    const materialStrain = normalizedForce * materials[selectedMaterial].maxStrain;
    
    return materialStrain;
  };
  
  const startAnimation = () => {
    setAnimate(true);
    let startTime = Date.now();
    let duration = 3000; // 3 seconds

    const animateForce = () => {
      const elapsedTime = Date.now() - startTime;
      const progress = elapsedTime / duration;

      if (progress < 1) {
        // Sinusoidal animation for smooth back and forth
        setForce(0.5 + 0.49 * Math.sin(progress * Math.PI * 2));
        animationRef.current = requestAnimationFrame(animateForce);
      } else {
        setAnimate(false);
      }
    };

    animationRef.current = requestAnimationFrame(animateForce);
  };

  useEffect(() => {
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, []);
  
  const strain = calculateStrain();
  const stressValue = strain * materials[selectedMaterial].E;

  // Dimensions for material block
  const baseWidth = 200;
  const baseHeight = 60;
  const blockInitialWidth = baseWidth;
  const blockDeformedWidth = blockInitialWidth * (1 + strain * 10); // Amplify deformation for visibility
  const deltaLength = blockDeformedWidth - blockInitialWidth;
  
  // Generate data points for the graph
  const generateGraphPoints = () => {
    const points = [];
    const numPoints = 20;
    const material = materials[selectedMaterial];
    const maxStrainPlot = material.maxStrain;
    
    for (let i = 0; i <= numPoints; i++) {
      const x = (i / numPoints) * maxStrainPlot;
      const y = x * material.E;
      points.push({ x, y });
    }
    
    return points;
  };
  
  const graphPoints = generateGraphPoints();
  
  // Calculate graph scaling
  const graphWidth = 300;
  const graphHeight = 200;
  const maxStrainOnGraph = materials[selectedMaterial].maxStrain;
  const maxStressOnGraph = maxStrainOnGraph * materials[selectedMaterial].E;
  
  // Scale coordinates to fit the graph
  const scaleX = (x) => (x / maxStrainOnGraph) * graphWidth;
  const scaleY = (y) => graphHeight - (y / maxStressOnGraph) * graphHeight;

  // Current point on graph
  const currentX = scaleX(strain);
  const currentY = scaleY(stressValue);
  
  // Calculate grid spacing
  const gridXCount = 10;
  const gridYCount = 10;
  const gridXStep = graphWidth / gridXCount;
  const gridYStep = graphHeight / gridYCount;

  // Generate material grid points for visualization
  const generateGridPoints = () => {
    const gridPoints = [];
    const columns = 10;
    const rows = 4;
    
    for (let i = 0; i <= rows; i++) {
      for (let j = 0; j <= columns; j++) {
        // Calculate the position with scaling
        // Here we stretch the x positions based on the current strain
        const x = j * (blockInitialWidth / columns);
        const stretchedX = j * (blockDeformedWidth / columns);
        const y = i * (baseHeight / rows);
        
        gridPoints.push({
          originalX: x,
          x: stretchedX,
          y: y
        });
      }
    }
    
    return gridPoints;
  };
  
  const gridPoints = generateGridPoints();

  return (
    <div className="tw-flex tw-flex-col tw-items-center tw-w-full tw-bg-white tw-rounded-lg tw-shadow-lg tw-overflow-hidden">
      <div className="tw-w-full tw-px-4 tw-py-2 tw-bg-gray-100 tw-border-b tw-flex tw-justify-between tw-items-center">
        <h3 className="tw-text-lg tw-font-semibold tw-text-gray-800">Hooke's Law: σ = E × ε</h3>
        <div className="tw-text-sm tw-text-gray-600">Young's Modulus: E = {materials[selectedMaterial].E} GPa</div>
      </div>
      
      <div className="tw-grid tw-grid-cols-1 md:tw-grid-cols-2 tw-gap-2 tw-p-4 tw-w-full">
        {/* Material visualization side */}
        <div className="tw-bg-gray-50 tw-rounded-lg tw-p-4 tw-flex tw-flex-col tw-items-center">
          <svg 
            width="100%" 
            height="280"
            viewBox="-50 -50 400 200"
            preserveAspectRatio="xMidYMid meet"
          >
            {/* Background grid */}
            <g opacity="0.1">
              {Array.from({ length: 11 }).map((_, i) => (
                <line 
                  key={`grid-h-${i}`}
                  x1="-30" 
                  y1={i * 10} 
                  x2="350" 
                  y2={i * 10} 
                  stroke="#000" 
                  strokeWidth="0.5" 
                />
              ))}
              {Array.from({ length: 20 }).map((_, i) => (
                <line 
                  key={`grid-v-${i}`}
                  x1={i * 20 - 30} 
                  y1="-10" 
                  x2={i * 20 - 30} 
                  y2="100" 
                  stroke="#000" 
                  strokeWidth="0.5" 
                />
              ))}
            </g>
            
            {/* Original position outline */}
            <rect 
              x="0" 
              y="0" 
              width={blockInitialWidth} 
              height={baseHeight} 
              stroke="#9ca3af" 
              strokeWidth="1" 
              strokeDasharray="5,5" 
              fill="none" 
            />
            
            {/* Left fixed support */}
            <g>
              <rect 
                x="-15" 
                y="-15" 
                width="15" 
                height={baseHeight + 30} 
                fill="#374151" 
              />
              <path 
                d="M-15,0 L-10,10 L-5,0 L0,10 L5,0 L10,10 L15,0" 
                stroke="#9ca3af" 
                strokeWidth="2" 
                fill="none"
                transform="translate(-15, -15)"
              />
              <path 
                d="M-15,0 L-10,10 L-5,0 L0,10 L5,0 L10,10 L15,0" 
                stroke="#9ca3af" 
                strokeWidth="2" 
                fill="none"
                transform={`translate(-15, ${baseHeight + 5})`}
              />
            </g>
            
            {/* Deformed material block */}
            <g>
              {/* Material fill */}
              <rect 
                x="0" 
                y="0" 
                width={blockDeformedWidth} 
                height={baseHeight} 
                fill={materials[selectedMaterial].color} 
                fillOpacity="0.7"
                stroke={materials[selectedMaterial].color} 
                strokeWidth="2" 
              />
              
              {/* Grid visualization */}
              {/* Horizontal grid lines */}
              {Array.from({ length: 5 }).map((_, i) => (
                <line 
                  key={`h-line-${i}`}
                  x1={0} 
                  y1={i * (baseHeight / 4)} 
                  x2={blockDeformedWidth} 
                  y2={i * (baseHeight / 4)} 
                  stroke="white" 
                  strokeWidth="1.5"
                  opacity="0.7"
                />
              ))}
              
              {/* Vertical grid lines - spacing changes based on strain */}
              {Array.from({ length: 11 }).map((_, i) => {
                // Calculate stretched position
                const originalX = i * (blockInitialWidth / 10);
                const stretchedX = i * (blockDeformedWidth / 10);
                
                return (
                  <line 
                    key={`v-line-${i}`}
                    x1={stretchedX} 
                    y1={0} 
                    x2={stretchedX} 
                    y2={baseHeight} 
                    stroke="white" 
                    strokeWidth="1.5"
                    opacity="0.7"
                  />
                );
              })}
            </g>
            
            {/* Force arrow */}
            <g transform={`translate(${blockDeformedWidth + 10}, ${baseHeight/2})`} opacity={force > 0.05 ? 1 : 0.3}>
              <line 
                x1="0" 
                y1="0" 
                x2="25" 
                y2="0" 
                stroke="#ef4444" 
                strokeWidth={4 + force * 4} 
              />
              <polygon 
                points="0,0 -10,-8 -10,8" 
                fill="#ef4444"
              />
              <text 
                x="15" 
                y="-15" 
                textAnchor="middle" 
                fill="#ef4444" 
                fontSize="24"
                fontWeight="bold"
              >
                F
              </text>
            </g>
            
            {/* Measurements and labels */}
            <text 
              x={blockDeformedWidth / 2} 
              y={-20} 
              textAnchor="middle" 
              fill="#1f2937" 
              fontSize="16"
              fontWeight="bold"
            >
              Strain (ε) = {strain.toFixed(4)}
            </text>
            
            <text 
              x={blockDeformedWidth / 2} 
              y={-40} 
              textAnchor="middle" 
              fill="#1f2937" 
              fontSize="16"
              fontWeight="bold"
            >
              Stress (σ) = {stressValue.toFixed(2)} GPa
            </text>
            
            {/* Delta L measurement */}
            <g>
              <line 
                x1={blockInitialWidth} 
                y1={baseHeight + 10} 
                x2={blockDeformedWidth} 
                y2={baseHeight + 10} 
                stroke="#3b82f6" 
                strokeWidth="2" 
              />
              <polygon 
                points="0,0 -5,-5 -5,5" 
                fill="#3b82f6" 
                transform={`translate(${blockInitialWidth}, ${baseHeight + 10})`}
              />
              <polygon 
                points="0,0 5,-5 5,5" 
                fill="#3b82f6" 
                transform={`translate(${blockDeformedWidth}, ${baseHeight + 10})`}
              />
              <text 
                x={(blockInitialWidth + blockDeformedWidth) / 2} 
                y={baseHeight + 25} 
                textAnchor="middle" 
                fill="#3b82f6" 
                fontSize="14"
                fontWeight="bold"
              >
                ΔL = {deltaLength.toFixed(2)} mm
              </text>
            </g>
            
            {/* Original length label */}
            <g>
              <line 
                x1="0" 
                y1={baseHeight + 40} 
                x2={blockInitialWidth} 
                y2={baseHeight + 40} 
                stroke="#6b7280" 
                strokeWidth="1.5" 
              />
              <polygon 
                points="0,0 -5,-5 -5,5" 
                fill="#6b7280" 
                transform={`translate(0, ${baseHeight + 40})`}
              />
              <polygon 
                points="0,0 5,-5 5,5" 
                fill="#6b7280" 
                transform={`translate(${blockInitialWidth}, ${baseHeight + 40})`}
              />
              <text 
                x={blockInitialWidth / 2} 
                y={baseHeight + 55} 
                textAnchor="middle" 
                fill="#6b7280" 
                fontSize="12"
              >
                L₀ = {blockInitialWidth.toFixed(0)} mm
              </text>
            </g>
          </svg>
        </div>
        
        {/* Stress-strain graph side */}
        <div className="tw-bg-gray-50 tw-rounded-lg tw-p-4 tw-flex tw-flex-col tw-items-center">
          <svg 
            width="100%" 
            height="280"
            viewBox="-50 -50 400 300"
            preserveAspectRatio="xMidYMid meet"
          >
            {/* Background grid */}
            <g opacity="0.1">
              {Array.from({ length: gridYCount + 1 }).map((_, i) => (
                <line 
                  key={`grid-h-${i}`}
                  x1="0" 
                  y1={i * gridYStep} 
                  x2={graphWidth} 
                  y2={i * gridYStep} 
                  stroke="#000" 
                  strokeWidth="0.5" 
                />
              ))}
              {Array.from({ length: gridXCount + 1 }).map((_, i) => (
                <line 
                  key={`grid-v-${i}`}
                  x1={i * gridXStep} 
                  y1="0" 
                  x2={i * gridXStep} 
                  y2={graphHeight} 
                  stroke="#000" 
                  strokeWidth="0.5" 
                />
              ))}
            </g>
            
            {/* Axes */}
            <line 
              x1="0" 
              y1={graphHeight} 
              x2={graphWidth + 20} 
              y2={graphHeight} 
              stroke="#000000" 
              strokeWidth="2" 
            />
            
            <line 
              x1="0" 
              y1={graphHeight} 
              x2="0" 
              y2="-20" 
              stroke="#000000" 
              strokeWidth="2" 
            />
            
            {/* Grid labels */}
            {[0, 0.25, 0.5, 0.75, 1.0].map((fraction, i) => (
              <text 
                key={`x-label-${i}`}
                x={graphWidth * fraction} 
                y={graphHeight + 20} 
                textAnchor="middle" 
                fill="#000000" 
                fontSize="12"
              >
                {(maxStrainOnGraph * fraction).toFixed(3)}
              </text>
            ))}
            
            {[0, 0.25, 0.5, 0.75, 1.0].map((fraction, i) => (
              <text 
                key={`y-label-${i}`}
                x="-10" 
                y={graphHeight - (graphHeight * fraction)} 
                textAnchor="end" 
                dominantBaseline="middle"
                fill="#000000" 
                fontSize="12"
              >
                {(maxStressOnGraph * fraction).toFixed(1)}
              </text>
            ))}
            
            {/* Axis labels */}
            <text 
              x={graphWidth / 2} 
              y={graphHeight + 40} 
              textAnchor="middle" 
              fill="#000000" 
              fontSize="16"
            >
              Strain (ε)
            </text>
            
            <text 
              x="-40" 
              y={graphHeight / 2} 
              textAnchor="middle" 
              fill="#000000" 
              fontSize="16"
              transform={`rotate(-90 -40 ${graphHeight / 2})`}
            >
              Stress (σ) in GPa
            </text>
            
            {/* Graph line */}
            <path 
              d={`M 0 ${graphHeight} ${graphPoints.map(p => `L ${scaleX(p.x)} ${scaleY(p.y)}`).join(' ')}`} 
              stroke={materials[selectedMaterial].color} 
              strokeWidth="3" 
              fill="none" 
            />
            
            {/* Elastic limit line */}
            {showElasticLine && (
              <line 
                x1="0" 
                y1={graphHeight} 
                x2={currentX} 
                y2={currentY} 
                stroke="#3b82f6" 
                strokeWidth="2" 
                strokeDasharray="5,5" 
              />
            )}
            
            {/* Current point */}
            <circle 
              cx={currentX} 
              cy={currentY} 
              r="8" 
              fill="#ef4444"
              stroke="#ffffff"
              strokeWidth="2"
            />
            
            {/* Formula box */}
            <rect 
              x={graphWidth - 110} 
              y="10" 
              width="100" 
              height="90" 
              fill="rgba(255, 255, 255, 0.8)" 
              stroke="#d1d5db" 
              strokeWidth="1" 
              rx="4" 
            />
            
            <text 
              x={graphWidth - 60} 
              y="30" 
              textAnchor="middle" 
              fill="#000000" 
              fontSize="16"
              fontWeight="bold"
            >
              σ = E × ε
            </text>
            
            <text 
              x={graphWidth - 100} 
              y="55" 
              textAnchor="start" 
              fill="#000000" 
              fontSize="14"
            >
              E = {materials[selectedMaterial].E} GPa
            </text>
            
            <text 
              x={graphWidth - 100} 
              y="75" 
              textAnchor="start" 
              fill="#000000" 
              fontSize="14"
            >
              ε = {strain.toFixed(4)}
            </text>
            
            <text 
              x={graphWidth - 100} 
              y="95" 
              textAnchor="start" 
              fill="#000000" 
              fontSize="14"
            >
              σ = {stressValue.toFixed(2)} GPa
            </text>
          </svg>
        </div>
      </div>
      
      {/* Controls */}
      <div className="tw-w-full tw-p-4 tw-border-t tw-border-gray-200 tw-bg-gray-50">
        <div className="tw-grid tw-grid-cols-1 md:tw-grid-cols-2 tw-gap-4">
          <div>
            <label className="tw-block tw-text-sm tw-font-medium tw-text-gray-700 tw-mb-1">
              Material Selection
            </label>
            <select 
              value={selectedMaterial} 
              onChange={handleMaterialChange}
              className="tw-w-full tw-p-2 tw-border tw-border-gray-300 tw-rounded-md"
            >
              {Object.keys(materials).map(key => (
                <option key={key} value={key}>
                  {materials[key].name} (E = {materials[key].E} GPa)
                </option>
              ))}
            </select>
          </div>
        
          <div>
            <label className="tw-block tw-text-sm tw-font-medium tw-text-gray-700 tw-mb-1">
              Applied Force: {(force * 100).toFixed(0)}%
            </label>
            <input 
              type="range" 
              min="0" 
              max="1" 
              step="0.01" 
              value={force} 
              onChange={(e) => setForce(parseFloat(e.target.value))}
              className="tw-w-full tw-h-2 tw-bg-gray-200 tw-rounded-lg tw-appearance-none tw-cursor-pointer"
            />
          </div>
        </div>

        <div className="tw-flex tw-justify-center tw-gap-4 tw-mt-4">
          <button 
            onClick={startAnimation}
            disabled={animate}
            className={`tw-px-4 tw-py-2 tw-rounded-md ${animate ? 'tw-bg-gray-400 tw-text-white' : 'tw-bg-blue-500 tw-text-white hover:tw-bg-blue-600'}`}
          >
            {animate ? 'Animating...' : 'Animate Force'}
          </button>
          
          <button 
            onClick={() => setShowElasticLine(!showElasticLine)}
            className="tw-px-4 tw-py-2 tw-bg-gray-100 tw-text-gray-800 tw-rounded-md hover:tw-bg-gray-200"
          >
            {showElasticLine ? 'Hide Elastic Line' : 'Show Elastic Line'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default HookesLawDemo;

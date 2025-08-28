import React, { useState, useMemo } from 'react';

const ThermalExpansionDemo = () => {
  const [temperature, setTemperature] = useState(20);
  const [selectedMaterial, setSelectedMaterial] = useState('aluminum');
  const [constraintType, setConstraintType] = useState('free');
  
  // Material properties
  const materials = {
    steel: { name: "Steel", alpha: 12e-6, color: "#6b7280", E: 200e9 },
    aluminum: { name: "Aluminum", alpha: 23e-6, color: "#9ca3af", E: 70e9 },
    copper: { name: "Copper", alpha: 17e-6, color: "#d97706", E: 110e9 },
    brass: { name: "Brass", alpha: 19e-6, color: "#fbbf24", E: 100e9 },
    invar: { name: "Invar", alpha: 1.2e-6, color: "#4b5563", E: 140e9 }
  };
  
  // Base dimensions
  const baseLength = 300;
  const baseHeight = 50;
  const initialTemp = 20;
  
  // Magnification factor to make expansion more visible
  const magnificationFactor = 50;
  
  // Calculate thermal expansion - memoized for better performance
  const expansion = useMemo(() => {
    const deltaT = temperature - initialTemp;
    const alpha = materials[selectedMaterial].alpha;
    
    // Actual expansion (in mm)
    const actualExpansion = baseLength * alpha * deltaT;
    
    // Magnified expansion for visualization
    const visualExpansion = actualExpansion * magnificationFactor;
    
    if (constraintType === 'free') {
      return {
        actualLength: baseLength + actualExpansion,
        visualLength: baseLength + visualExpansion,
        stress: 0,
        actualExpansion,
        visualExpansion
      };
    } else {
      // Constrained - no length change but stress develops
      return {
        actualLength: baseLength,
        visualLength: baseLength,
        stress: alpha * deltaT * materials[selectedMaterial].E,
        actualExpansion,
        visualExpansion: 0
      };
    }
  }, [temperature, selectedMaterial, constraintType]);
  
  const { actualLength, visualLength, stress, actualExpansion, visualExpansion } = expansion;
  
  // Calculate color intensity based on stress or temperature
  const barColor = useMemo(() => {
    if (constraintType === 'free') {
      return materials[selectedMaterial].color;
    } else {
      // For constrained bars, show stress color intensity
      const maxStress = 200e6; // 200 MPa as max for color scaling
      const normalizedStress = Math.min(Math.abs(stress) / maxStress, 1);
      
      if (temperature > initialTemp) {
        // Compressive stress - blue
        return `rgba(59, 130, 246, ${0.3 + 0.7 * normalizedStress})`;
      } else {
        // Tensile stress - red
        return `rgba(239, 68, 68, ${0.3 + 0.7 * normalizedStress})`;
      }
    }
  }, [constraintType, stress, temperature, selectedMaterial]);

  // Calculate marker positions to show the expansion effect
  const markerPositions = useMemo(() => {
    const spacing = baseLength / 5;
    const positions = [];
    
    for (let i = 0; i <= 5; i++) {
      if (constraintType === 'free') {
        // In free expansion, markers move with the material
        if (temperature > initialTemp) {
          // Expanding right
          positions.push(i * spacing + (visualExpansion * i / 5));
        } else {
          // Contracting from right side
          positions.push(i * spacing + (visualExpansion * i / 5));
        }
      } else {
        // In constrained mode, markers are fixed
        positions.push(i * spacing);
      }
    }
    
    return positions;
  }, [constraintType, temperature, visualExpansion]);

  return (
    <div className="tw-flex tw-flex-col tw-items-center tw-w-full tw-max-w-2xl tw-mx-auto tw-my-4 tw-p-4 tw-bg-gray-50 tw-rounded-lg tw-shadow-md">
      <div className="tw-flex tw-justify-between tw-w-full tw-mb-2">
        <span className="tw-font-medium">Material: {materials[selectedMaterial].name}</span>
        <span className="tw-font-medium">
          {constraintType === 'free' 
            ? `ΔL: ${Math.abs(actualExpansion).toFixed(2)} mm` 
            : `Stress: ${(stress / 1e6).toFixed(1)} MPa`}
        </span>
      </div>
      
      <div className="tw-w-full tw-mb-4 tw-bg-white tw-p-4 tw-rounded tw-border tw-border-gray-200 tw-shadow-sm">
        <svg 
          width="100%" 
          height="180" 
          viewBox={`-40 -30 ${baseLength + Math.max(Math.abs(visualExpansion), 150) + 80} 140`} 
          className="tw-bg-white"
          preserveAspectRatio="xMidYMid meet"
        >
          {/* Reference position (outline) */}
          <rect 
            x="0" 
            y="0" 
            width={baseLength} 
            height={baseHeight} 
            stroke="#9ca3af" 
            strokeWidth="1" 
            strokeDasharray="5,5"
            fill="none"
          />
          
          {/* Current position with expansion */}
          <rect 
            x={constraintType === 'constrained' ? 0 : (temperature < initialTemp ? (baseLength - visualLength < 0 ? 0 : baseLength - visualLength) : 0)} 
            y="0" 
            width={Math.max(visualLength, 10)} 
            height={baseHeight} 
            fill={barColor} 
            stroke="#374151" 
            strokeWidth="2"
          />
          
          {/* Internal strain markers */}
          {markerPositions.map((pos, idx) => (
            <line 
              key={idx}
              x1={pos} 
              y1="0" 
              x2={pos} 
              y2={baseHeight} 
              stroke="#374151" 
              strokeWidth="1"
              strokeDasharray={idx === 0 || idx === 5 ? "none" : "3,2"}
            />
          ))}
          
          {/* Ruler markings - simplified to avoid clutter */}
          <line x1="0" y1={baseHeight + 15} x2={baseLength} y2={baseHeight + 15} stroke="#4b5563" strokeWidth="1" />
          {[0, baseLength/2, baseLength].map((pos, i) => (
            <g key={i}>
              <line 
                x1={pos} 
                y1={baseHeight + 10} 
                x2={pos} 
                y2={baseHeight + 20} 
                stroke="#4b5563" 
                strokeWidth="1" 
              />
              <text 
                x={pos} 
                y={baseHeight + 30} 
                textAnchor="middle" 
                fill="#4b5563" 
                fontSize="10"
              >
                {pos.toFixed(0)}
              </text>
            </g>
          ))}
          
          {/* Constraint visualization */}
          {constraintType === 'constrained' && (
            <>
              {/* Left wall */}
              <rect x="-20" y="-20" width="20" height={baseHeight + 40} fill="#6b7280" />
              
              {/* Right wall */}
              <rect x={baseLength} y="-20" width="20" height={baseHeight + 40} fill="#6b7280" />
              
              {/* Arrows showing internal forces when constrained */}
              {temperature !== initialTemp && (
                <>
                  {temperature > initialTemp ? (
                    // Compression arrows (pointing inward)
                    <>
                      <g transform="translate(75, 25)">
                        <line x1="-30" y1="0" x2="30" y2="0" stroke="#ef4444" strokeWidth="2" />
                        <polygon points="-20,0 -30,5 -30,-5" fill="#ef4444" />
                      </g>
                      <g transform="translate(225, 25)">
                        <line x1="-30" y1="0" x2="30" y2="0" stroke="#ef4444" strokeWidth="2" />
                        <polygon points="20,0 30,5 30,-5" fill="#ef4444" />
                      </g>
                    </>
                  ) : (
                    // Tension arrows (pointing outward)
                    <>
                      <g transform="translate(75, 25)">
                        <line x1="-30" y1="0" x2="30" y2="0" stroke="#3b82f6" strokeWidth="2" />
                        <polygon points="20,0 30,5 30,-5" fill="#3b82f6" />
                      </g>
                      <g transform="translate(225, 25)">
                        <line x1="-30" y1="0" x2="30" y2="0" stroke="#3b82f6" strokeWidth="2" />
                        <polygon points="-20,0 -30,5 -30,-5" fill="#3b82f6" />
                      </g>
                    </>
                  )}
                </>
              )}
            </>
          )}
          
          {/* Temperature indicator */}
          <g transform="translate(baseLength + 40, 25)">
            <circle 
              r="15" 
              fill={temperature > initialTemp ? "#ef4444" : "#3b82f6"} 
              stroke="#374151" 
              strokeWidth="1"
            />
            <text 
              x="0"
              y="0"
              textAnchor="middle" 
              dominantBaseline="middle" 
              fill="white" 
              fontSize="14"
              fontWeight="bold"
            >
              {temperature > initialTemp ? "+" : "−"}
            </text>
          </g>
          
          {/* Length change indicator */}
          {constraintType === 'free' && temperature !== initialTemp && Math.abs(visualExpansion) > 1 && (
            <g>
              <line 
                x1={temperature > initialTemp ? baseLength : Math.max(0, baseLength + visualExpansion)} 
                y1={baseHeight + 5} 
                x2={temperature > initialTemp ? Math.max(0, baseLength + visualExpansion) : baseLength} 
                y2={baseHeight + 5} 
                stroke="#ef4444" 
                strokeWidth="2" 
                strokeDasharray="4,2"
              />
              
              {/* Only show arrows if expansion/contraction is significant */}
              {Math.abs(visualExpansion) > 10 && (
                <>
                  <polygon 
                    points={temperature > initialTemp ? 
                      `${baseLength},${baseHeight+5} ${baseLength-5},${baseHeight} ${baseLength-5},${baseHeight+10}` : 
                      `${baseLength},${baseHeight+5} ${baseLength+5},${baseHeight} ${baseLength+5},${baseHeight+10}`
                    }
                    fill="#ef4444"
                  />
                  <polygon 
                    points={temperature > initialTemp ? 
                      `${baseLength+visualExpansion},${baseHeight+5} ${baseLength+visualExpansion+5},${baseHeight} ${baseLength+visualExpansion+5},${baseHeight+10}` : 
                      `${baseLength+visualExpansion},${baseHeight+5} ${baseLength+visualExpansion-5},${baseHeight} ${baseLength+visualExpansion-5},${baseHeight+10}`
                    }
                    fill="#ef4444"
                  />
                </>
              )}
              
              {/* Only show measurement text if expansion is significant */}
              {Math.abs(visualExpansion) > 5 && (
                <text 
                  x={temperature > initialTemp ? 
                    (baseLength + (visualExpansion / 2)) : 
                    (baseLength + (visualExpansion / 2))
                  } 
                  y={baseHeight + 18} 
                  textAnchor="middle" 
                  fill="#ef4444" 
                  fontSize="10"
                  fontWeight="bold"
                >
                  ΔL = {Math.abs(actualExpansion).toFixed(2)} mm (×{magnificationFactor})
                </text>
              )}
            </g>
          )}
        </svg>
      </div>
      
      <div className="tw-w-full tw-max-w-md tw-space-y-3">
        <div>
          <label className="tw-block tw-text-sm tw-font-medium tw-mb-1">
            Material Selection
          </label>
          <select 
            value={selectedMaterial} 
            onChange={(e) => setSelectedMaterial(e.target.value)}
            className="tw-w-full tw-p-2 tw-border tw-border-gray-300 tw-rounded-md tw-shadow-sm"
          >
            {Object.keys(materials).map(key => (
              <option key={key} value={key}>
                {materials[key].name} (α = {(materials[key].alpha * 1e6).toFixed(1)} × 10⁻⁶/°C)
              </option>
            ))}
          </select>
        </div>
        
        <div>
          <label className="tw-block tw-text-sm tw-font-medium tw-mb-1">
            Constraint Type
          </label>
          <div className="tw-flex tw-space-x-4">
            <label className="tw-inline-flex tw-items-center">
              <input
                type="radio"
                value="free"
                checked={constraintType === 'free'}
                onChange={() => setConstraintType('free')}
                className="tw-h-4 tw-w-4 tw-text-blue-600 tw-border-gray-300"
              />
              <span className="tw-ml-2 tw-text-gray-700">Free to Expand</span>
            </label>
            <label className="tw-inline-flex tw-items-center">
              <input
                type="radio"
                value="constrained"
                checked={constraintType === 'constrained'}
                onChange={() => setConstraintType('constrained')}
                className="tw-h-4 tw-w-4 tw-text-blue-600 tw-border-gray-300"
              />
              <span className="tw-ml-2 tw-text-gray-700">Fully Constrained</span>
            </label>
          </div>
        </div>
        
        <div>
          <label className="tw-block tw-text-sm tw-font-medium tw-mb-1">
            Temperature: {temperature}°C
          </label>
          <input 
            type="range" 
            min="-20" 
            max="100" 
            value={temperature} 
            onChange={(e) => setTemperature(parseInt(e.target.value))}
            className="tw-w-full tw-h-2 tw-bg-gray-200 tw-rounded-lg tw-appearance-none tw-cursor-pointer"
          />
          <div className="tw-flex tw-justify-between tw-text-xs tw-text-gray-500 tw-mt-1">
            <span>-20°C</span>
            <span>{initialTemp}°C</span>
            <span>100°C</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ThermalExpansionDemo;

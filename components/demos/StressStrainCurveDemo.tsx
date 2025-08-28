import React, { useState, useEffect, useRef, useMemo } from 'react';

const StressStrainCurveDemo = () => {
  const [testProgress, setTestProgress] = useState(0);
  const [selectedMaterial, setSelectedMaterial] = useState('steel');
  const [isRunning, setIsRunning] = useState(false);
  const [pointLabels, setPointLabels] = useState(true);
  const animationRef = useRef(null);
  
  // Material properties to simulate different stress-strain behaviors
  const materials = {
    steel: { 
      name: "Mild Steel", 
      color: "#6b7280",
      elasticLimit: 0.12, // proportion of curve
      yieldPoint: 0.15,
      ultimateStrength: 0.7,
      failurePoint: 0.95,
      elasticSlope: 200, // simulated modulus
      maxStress: 400, // MPa
      neckingFactor: 0.85 // how much necking occurs (width reduction)
    },
    aluminum: { 
      name: "Aluminum Alloy", 
      color: "#9ca3af",
      elasticLimit: 0.1,
      yieldPoint: 0.12,
      ultimateStrength: 0.6,
      failurePoint: 0.9,
      elasticSlope: 70,
      maxStress: 300,
      neckingFactor: 0.8
    },
    titanium: { 
      name: "Titanium Alloy", 
      color: "#d1d5db",
      elasticLimit: 0.15,
      yieldPoint: 0.18,
      ultimateStrength: 0.75,
      failurePoint: 0.92,
      elasticSlope: 110,
      maxStress: 900,
      neckingFactor: 0.7
    },
    brass: { 
      name: "Brass", 
      color: "#fbbf24",
      elasticLimit: 0.08,
      yieldPoint: 0.1,
      ultimateStrength: 0.65,
      failurePoint: 0.88,
      elasticSlope: 100,
      maxStress: 350,
      neckingFactor: 0.75
    },
    copper: { 
      name: "Copper", 
      color: "#b45309",
      elasticLimit: 0.05,
      yieldPoint: 0.08,
      ultimateStrength: 0.55,
      failurePoint: 0.85,
      elasticSlope: 120,
      maxStress: 250,
      neckingFactor: 0.7
    }
  };
  
  const handleMaterialChange = (e) => {
    if (isRunning) return; // Prevent changing material during test
    setSelectedMaterial(e.target.value);
    setTestProgress(0);
  };
  
  const startTest = () => {
    setIsRunning(true);
    setTestProgress(0);
    
    let startTime = Date.now();
    let duration = 8000; // 8 seconds for full test
    
    const animateTest = () => {
      const elapsedTime = Date.now() - startTime;
      const progress = Math.min(elapsedTime / duration, 1);
      
      setTestProgress(progress);
      
      if (progress < 1) {
        animationRef.current = requestAnimationFrame(animateTest);
      } else {
        setIsRunning(false);
      }
    };
    
    animationRef.current = requestAnimationFrame(animateTest);
  };
  
  useEffect(() => {
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, []);
  
  const resetTest = () => {
    if (isRunning) {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
      setIsRunning(false);
    }
    setTestProgress(0);
  };
  
  const material = materials[selectedMaterial];
  
  // Calculate stress and strain based on test progress
  const calculateStressStrain = (progress) => {
    const elasticEnd = material.elasticLimit;
    const yieldEnd = material.yieldPoint;
    const ultimateStrengthPoint = material.ultimateStrength;
    const failurePoint = material.failurePoint;
    
    let strain = 0;
    let stress = 0;
    let phase = '';
    
    if (progress <= elasticEnd) {
      // Elastic phase - linear relationship
      phase = 'elastic';
      strain = progress * 0.05; // Max strain in elastic region
      stress = strain * material.elasticSlope;
    } else if (progress <= yieldEnd) {
      // Yield point - slight plateau
      phase = 'yield';
      const yieldProgress = (progress - elasticEnd) / (yieldEnd - elasticEnd);
      strain = 0.05 + yieldProgress * 0.02;
      stress = material.elasticSlope * 0.05 * (1 + yieldProgress * 0.05);
    } else if (progress <= ultimateStrengthPoint) {
      // Strain hardening phase
      phase = 'hardening';
      const hardeningProgress = (progress - yieldEnd) / (ultimateStrengthPoint - yieldEnd);
      strain = 0.07 + hardeningProgress * 0.18;
      stress = material.elasticSlope * 0.05 * 1.05 + hardeningProgress * (material.maxStress - material.elasticSlope * 0.05 * 1.05);
    } else if (progress <= failurePoint) {
      // Necking phase
      phase = 'necking';
      const neckingProgress = (progress - ultimateStrengthPoint) / (failurePoint - ultimateStrengthPoint);
      strain = 0.25 + neckingProgress * 0.25;
      stress = material.maxStress - neckingProgress * (material.maxStress * 0.3);
    } else {
      // Failure
      phase = 'failure';
      strain = 0.5;
      stress = material.maxStress * 0.7;
    }
    
    return { strain, stress, phase };
  };
  
  const { strain, stress, phase } = calculateStressStrain(testProgress);
  
  // Generate data points for the curve using useMemo to prevent infinite re-renders
  const curvePoints = useMemo(() => {
    const points = [];
    const numPoints = 100;
    
    for (let i = 0; i <= numPoints; i++) {
      const progress = i / numPoints;
      const { strain, stress } = calculateStressStrain(progress);
      points.push({ x: strain, y: stress, progress });
    }
    
    return points;
  }, [selectedMaterial]); // Only recalculate when material changes
  
  // Find key points on the curve
  const elasticLimitPoint = curvePoints.find(p => p.progress >= material.elasticLimit);
  const yieldPoint = curvePoints.find(p => p.progress >= material.yieldPoint);
  const ultimateStrengthPoint = curvePoints.find(p => p.progress >= material.ultimateStrength);
  const failurePoint = curvePoints.find(p => p.progress >= material.failurePoint);
  
  // Calculate graph scaling
  const graphWidth = 220;
  const graphHeight = 220;
  const maxX = 0.5; // max strain
  const maxY = material.maxStress;
  
  // Scale coordinates to fit the graph
  const scaleX = (x) => (x / maxX) * graphWidth;
  const scaleY = (y) => graphHeight - (y / maxY) * graphHeight;
  
  // Current point on graph
  const currentX = scaleX(strain);
  const currentY = scaleY(stress);
  
  // Visible portion of the curve based on test progress
  const visibleCurvePoints = curvePoints.filter(p => p.progress <= testProgress);
  
  // Dimensions for test specimen
  const specimenLength = 220;
  const specimenWidth = 25;
  const clampWidth = 40;
  const clampHeight = 30;
  
  // Calculate deformation based on current phase
  const calculateDeformation = () => {
    let currentLength = specimenLength * (1 + strain * 0.8); // Scale the elongation to fit
    let currentWidth = specimenWidth;
    let neckingWidth = specimenWidth;
    let neckingPosition = currentLength / 2; // Middle
    let broken = false;
    let breakOffset = 0;
    
    if (phase === 'elastic' || phase === 'yield') {
      // Uniform elongation in early phases
      currentWidth = specimenWidth * (1 - strain * 0.1); // Slight reduction due to Poisson effect
    } else if (phase === 'hardening') {
      // Begin to show slight necking
      const neckingStart = (testProgress - material.yieldPoint) / (material.ultimateStrength - material.yieldPoint);
      neckingWidth = specimenWidth * (1 - strain * 0.15 - neckingStart * 0.05);
    } else if (phase === 'necking') {
      // Significant necking
      const neckingProgress = (testProgress - material.ultimateStrength) / (material.failurePoint - material.ultimateStrength);
      currentWidth = specimenWidth * (1 - strain * 0.2);
      neckingWidth = currentWidth * (1 - neckingProgress * (1 - material.neckingFactor));
    } else if (phase === 'failure') {
      // Fracture
      currentWidth = specimenWidth * (1 - strain * 0.2);
      neckingWidth = currentWidth * material.neckingFactor;
      broken = true;
      breakOffset = 4; // Small gap to show fracture
    }
    
    return { 
      currentLength, 
      currentWidth, 
      neckingWidth, 
      neckingPosition, 
      broken, 
      breakOffset 
    };
  };
  
  const { 
    currentLength, 
    currentWidth, 
    neckingWidth, 
    neckingPosition, 
    broken, 
    breakOffset
  } = calculateDeformation();

  return (
    <div className="tw-flex tw-justify-center tw-w-full">
      <div className="tw-w-full tw-bg-white tw-shadow-md tw-rounded-lg tw-overflow-hidden">
        <div className="tw-grid tw-grid-cols-1 md:tw-grid-cols-2 tw-gap-2 tw-p-4">
          
          {/* Left side: Test specimen visualization */}
          <div className="tw-flex tw-flex-col tw-items-center">
            <div className="tw-bg-gray-50 tw-rounded-lg tw-p-2 tw-w-full">
              <svg 
                width="100%" 
                height="280"
                viewBox={`-50 -40 ${specimenLength + 100} ${specimenWidth * 6}`}
                preserveAspectRatio="xMidYMid meet"
              >
                {/* Grid lines */}
                <g opacity="0.1">
                  {Array.from({ length: 10 }).map((_, i) => (
                    <line 
                      key={`grid-h-${i}`}
                      x1="-40" 
                      y1={i * 10} 
                      x2={specimenLength + 40} 
                      y2={i * 10} 
                      stroke="#000" 
                      strokeWidth="0.5" 
                      strokeDasharray="2,2"
                    />
                  ))}
                  {Array.from({ length: 20 }).map((_, i) => (
                    <line 
                      key={`grid-v-${i}`}
                      x1={i * 20 - 40} 
                      y1="-20" 
                      x2={i * 20 - 40} 
                      y2="80" 
                      stroke="#000" 
                      strokeWidth="0.5" 
                      strokeDasharray="2,2"
                    />
                  ))}
                </g>
                
                {/* Original specimen outline (dashed) */}
                <rect 
                  x="0" 
                  y={(specimenWidth * 6 - specimenWidth) / 2} 
                  width={specimenLength} 
                  height={specimenWidth} 
                  stroke="#9ca3af" 
                  strokeWidth="1" 
                  strokeDasharray="5,5" 
                  fill="none" 
                />
                
                {/* Left clamp - fixed */}
                <g>
                  <rect 
                    x={-clampWidth} 
                    y={(specimenWidth * 6 - specimenWidth - 5) / 2} 
                    width={clampWidth} 
                    height={specimenWidth + 10} 
                    fill="#374151" 
                  />
                  <rect 
                    x={-clampWidth + 5} 
                    y={(specimenWidth * 6 - specimenWidth + 5) / 2} 
                    width={clampWidth - 5} 
                    height={specimenWidth - 10} 
                    fill="#4b5563" 
                  />
                  <line 
                    x1={-clampWidth + 12} 
                    y1={(specimenWidth * 6 - specimenWidth - 15) / 2} 
                    x2={-clampWidth + 12} 
                    y2={(specimenWidth * 6 + specimenWidth + 15) / 2} 
                    stroke="#9ca3af" 
                    strokeWidth="3" 
                  />
                  <line 
                    x1={-clampWidth + 22} 
                    y1={(specimenWidth * 6 - specimenWidth - 15) / 2} 
                    x2={-clampWidth + 22} 
                    y2={(specimenWidth * 6 + specimenWidth + 15) / 2} 
                    stroke="#9ca3af" 
                    strokeWidth="3" 
                  />
                </g>
                
                {/* Right clamp - moves with deformation */}
                <g transform={`translate(${currentLength}, 0)`}>
                  <rect 
                    x={0} 
                    y={(specimenWidth * 6 - specimenWidth - 5) / 2} 
                    width={clampWidth} 
                    height={specimenWidth + 10} 
                    fill="#374151" 
                  />
                  <rect 
                    x={0} 
                    y={(specimenWidth * 6 - specimenWidth + 5) / 2} 
                    width={clampWidth - 5} 
                    height={specimenWidth - 10} 
                    fill="#4b5563" 
                  />
                  <line 
                    x1={8} 
                    y1={(specimenWidth * 6 - specimenWidth - 15) / 2} 
                    x2={8} 
                    y2={(specimenWidth * 6 + specimenWidth + 15) / 2} 
                    stroke="#9ca3af" 
                    strokeWidth="3" 
                  />
                  <line 
                    x1={18} 
                    y1={(specimenWidth * 6 - specimenWidth - 15) / 2} 
                    x2={18} 
                    y2={(specimenWidth * 6 + specimenWidth + 15) / 2} 
                    stroke="#9ca3af" 
                    strokeWidth="3" 
                  />
                </g>
                
                {/* Material specimen with deformation */}
                {!broken ? (
                  // Intact specimen with possible necking
                  <path 
                    d={`
                      M 0,${(specimenWidth * 6 - currentWidth) / 2}
                      L ${neckingPosition - 20},${(specimenWidth * 6 - currentWidth) / 2}
                      C ${neckingPosition - 10},${(specimenWidth * 6 - currentWidth) / 2} ${neckingPosition - 5},${(specimenWidth * 6 - neckingWidth) / 2} ${neckingPosition},${(specimenWidth * 6 - neckingWidth) / 2}
                      L ${neckingPosition + 5},${(specimenWidth * 6 - neckingWidth) / 2}
                      C ${neckingPosition + 10},${(specimenWidth * 6 - neckingWidth) / 2} ${neckingPosition + 15},${(specimenWidth * 6 - currentWidth) / 2} ${neckingPosition + 20},${(specimenWidth * 6 - currentWidth) / 2}
                      L ${currentLength},${(specimenWidth * 6 - currentWidth) / 2}
                      L ${currentLength},${(specimenWidth * 6 + currentWidth) / 2}
                      L ${neckingPosition + 20},${(specimenWidth * 6 + currentWidth) / 2}
                      C ${neckingPosition + 15},${(specimenWidth * 6 + currentWidth) / 2} ${neckingPosition + 10},${(specimenWidth * 6 + neckingWidth) / 2} ${neckingPosition + 5},${(specimenWidth * 6 + neckingWidth) / 2}
                      L ${neckingPosition},${(specimenWidth * 6 + neckingWidth) / 2}
                      C ${neckingPosition - 5},${(specimenWidth * 6 + neckingWidth) / 2} ${neckingPosition - 10},${(specimenWidth * 6 + currentWidth) / 2} ${neckingPosition - 20},${(specimenWidth * 6 + currentWidth) / 2}
                      L 0,${(specimenWidth * 6 + currentWidth) / 2}
                      Z
                    `}
                    fill={material.color}
                    stroke="#1f2937"
                    strokeWidth="0.5"
                  />
                ) : (
                  // Broken specimen - two separate parts
                  <>
                    {/* Left part */}
                    <path 
                      d={`
                        M 0,${(specimenWidth * 6 - currentWidth) / 2}
                        L ${neckingPosition - 20},${(specimenWidth * 6 - currentWidth) / 2}
                        C ${neckingPosition - 10},${(specimenWidth * 6 - currentWidth) / 2} ${neckingPosition - 5},${(specimenWidth * 6 - neckingWidth) / 2} ${neckingPosition - breakOffset},${(specimenWidth * 6 - neckingWidth) / 2}
                        L ${neckingPosition - breakOffset},${(specimenWidth * 6 - neckingWidth) / 2}
                        
                        C ${neckingPosition - breakOffset - 2},${(specimenWidth * 6 - neckingWidth) / 2 + 2} 
                          ${neckingPosition - breakOffset - 1},${(specimenWidth * 6) / 2} 
                          ${neckingPosition - breakOffset - 3},${(specimenWidth * 6 + neckingWidth) / 2 - 2}
                        
                        L ${neckingPosition - breakOffset},${(specimenWidth * 6 + neckingWidth) / 2}
                        C ${neckingPosition - 5},${(specimenWidth * 6 + neckingWidth) / 2} ${neckingPosition - 10},${(specimenWidth * 6 + currentWidth) / 2} ${neckingPosition - 20},${(specimenWidth * 6 + currentWidth) / 2}
                        L 0,${(specimenWidth * 6 + currentWidth) / 2}
                        Z
                      `}
                      fill={material.color}
                      stroke="#1f2937"
                      strokeWidth="0.5"
                    />
                    
                    {/* Right part */}
                    <path 
                      d={`
                        M ${neckingPosition + breakOffset},${(specimenWidth * 6 - neckingWidth) / 2}
                        C ${neckingPosition + 5},${(specimenWidth * 6 - neckingWidth) / 2} ${neckingPosition + 10},${(specimenWidth * 6 - currentWidth) / 2} ${neckingPosition + 20},${(specimenWidth * 6 - currentWidth) / 2}
                        L ${currentLength},${(specimenWidth * 6 - currentWidth) / 2}
                        L ${currentLength},${(specimenWidth * 6 + currentWidth) / 2}
                        L ${neckingPosition + 20},${(specimenWidth * 6 + currentWidth) / 2}
                        C ${neckingPosition + 10},${(specimenWidth * 6 + currentWidth) / 2} ${neckingPosition + 5},${(specimenWidth * 6 + neckingWidth) / 2} ${neckingPosition + breakOffset},${(specimenWidth * 6 + neckingWidth) / 2}
                        
                        C ${neckingPosition + breakOffset + 2},${(specimenWidth * 6 + neckingWidth) / 2 - 2} 
                          ${neckingPosition + breakOffset + 1},${(specimenWidth * 6) / 2} 
                          ${neckingPosition + breakOffset + 3},${(specimenWidth * 6 - neckingWidth) / 2 + 2}
                        Z
                      `}
                      fill={material.color}
                      stroke="#1f2937"
                      strokeWidth="0.5"
                    />
                  </>
                )}
                
                {/* Gauge length indicators */}
                <line 
                  x1="10" 
                  y1={(specimenWidth * 6 - specimenWidth) / 2 - 10} 
                  x2="10" 
                  y2={(specimenWidth * 6 + specimenWidth) / 2 + 10} 
                  stroke="#ef4444" 
                  strokeWidth="1" 
                  strokeDasharray="4,4" 
                />
                
                <line 
                  x1={specimenLength - 10} 
                  y1={(specimenWidth * 6 - specimenWidth) / 2 - 10} 
                  x2={specimenLength - 10} 
                  y2={(specimenWidth * 6 + specimenWidth) / 2 + 10} 
                  stroke="#ef4444" 
                  strokeWidth="1" 
                  strokeDasharray="4,4" 
                />
                
                {/* Force arrows */}
                <g opacity={isRunning || testProgress > 0 ? 1 : 0.3}>
                  {/* Left arrow */}
                  <path 
                    d="M -32 30 L -20 30" 
                    stroke="#ef4444" 
                    strokeWidth="3" 
                  />
                  <path 
                    d="M -20 30 L -25 26 L -25 34 Z" 
                    fill="#ef4444" 
                  />
                  
                  {/* Right arrow */}
                  <path 
                    d={`M ${currentLength + 22} 30 L ${currentLength + 34} 30`} 
                    stroke="#ef4444" 
                    strokeWidth="3" 
                  />
                  <path 
                    d={`M ${currentLength + 34} 30 L ${currentLength + 29} 26 L ${currentLength + 29} 34 Z`} 
                    fill="#ef4444" 
                  />
                </g>
                
                {/* Status measurements */}
                <text 
                  x={currentLength / 2} 
                  y="80" 
                  textAnchor="middle" 
                  fill="#1f2937" 
                  fontSize="14"
                  fontWeight="bold"
                >
                  {phase === 'failure' ? 'FRACTURED' : 
                    phase === 'necking' ? 'NECKING' : 
                    phase === 'hardening' ? 'STRAIN HARDENING' : 
                    phase === 'yield' ? 'YIELDING' :
                    'ELASTIC DEFORMATION'}
                </text>
                
                <text 
                  x={currentLength / 2} 
                  y="95" 
                  textAnchor="middle" 
                  fill="#1f2937" 
                  fontSize="12"
                >
                  ε = {strain.toFixed(3)} | σ = {stress.toFixed(0)} MPa
                </text>
              </svg>
            </div>
          </div>
          
          {/* Right side: Stress-strain curve */}
          <div className="tw-flex tw-flex-col tw-items-center tw-bg-gray-50 tw-rounded-lg tw-p-2 tw-h-full">
            <svg 
              width="100%" 
              height="280"
              viewBox="-30 -30 300 300"
              preserveAspectRatio="xMidYMid meet"
            >
              {/* Background grid */}
              <g opacity="0.1">
                {Array.from({ length: 11 }).map((_, i) => (
                  <line 
                    key={`grid-h-${i}`}
                    x1="0" 
                    y1={i * (graphHeight/10)} 
                    x2={graphWidth} 
                    y2={i * (graphHeight/10)} 
                    stroke="#000" 
                    strokeWidth="0.5" 
                  />
                ))}
                {Array.from({ length: 11 }).map((_, i) => (
                  <line 
                    key={`grid-v-${i}`}
                    x1={i * (graphWidth/10)} 
                    y1="0" 
                    x2={i * (graphWidth/10)} 
                    y2={graphHeight} 
                    stroke="#000" 
                    strokeWidth="0.5" 
                  />
                ))}
              </g>
              
              {/* Graph Box */}
              <rect 
                x="0" 
                y="0" 
                width={graphWidth} 
                height={graphHeight} 
                fill="none" 
                stroke="#000000" 
                strokeWidth="1" 
              />
              
              {/* Axes labels */}
              <text 
                x={graphWidth / 2} 
                y={graphHeight + 25} 
                textAnchor="middle" 
                fill="#000000" 
                fontSize="14"
              >
                Strain (ε)
              </text>
              
              <text 
                x="-20" 
                y={graphHeight / 2} 
                textAnchor="middle" 
                fill="#000000" 
                fontSize="14"
                transform={`rotate(-90 -20 ${graphHeight / 2})`}
              >
                Stress (σ) MPa
              </text>
              
              {/* X-axis numbers */}
              {[0, 0.1, 0.2, 0.3, 0.4, 0.5].map((val, i) => (
                <text 
                  key={`x-label-${i}`}
                  x={scaleX(val)} 
                  y={graphHeight + 15} 
                  textAnchor="middle" 
                  fill="#000000" 
                  fontSize="10"
                >
                  {val.toFixed(1)}
                </text>
              ))}
              
              {/* Y-axis numbers */}
              {[0, maxY*0.25, maxY*0.5, maxY*0.75, maxY].map((val, i) => (
                <text 
                  key={`y-label-${i}`}
                  x="-5" 
                  y={scaleY(val)} 
                  textAnchor="end" 
                  dominantBaseline="middle"
                  fill="#000000" 
                  fontSize="10"
                >
                  {val.toFixed(0)}
                </text>
              ))}
              
              {/* Reference curve (faint) */}
              <path 
                d={`M 0 ${graphHeight} ${curvePoints.map(p => `L ${scaleX(p.x)} ${scaleY(p.y)}`).join(' ')}`} 
                stroke={material.color} 
                strokeWidth="1" 
                strokeDasharray="3,3"
                strokeOpacity="0.3"
                fill="none" 
              />
              
              {/* Current curve */}
              <path 
                d={`M 0 ${graphHeight} ${visibleCurvePoints.map(p => `L ${scaleX(p.x)} ${scaleY(p.y)}`).join(' ')}`} 
                stroke={material.color} 
                strokeWidth="3" 
                fill="none" 
              />
              
              {/* Key points */}
              {pointLabels && elasticLimitPoint && testProgress >= material.elasticLimit && (
                <g>
                  <circle 
                    cx={scaleX(elasticLimitPoint.x)} 
                    cy={scaleY(elasticLimitPoint.y)} 
                    r="4" 
                    fill="#3b82f6" 
                  />
                  <text 
                    x={scaleX(elasticLimitPoint.x) + 8} 
                    y={scaleY(elasticLimitPoint.y) - 8} 
                    fontSize="10" 
                    fill="#3b82f6"
                  >
                    A: Elastic Limit
                  </text>
                </g>
              )}
              
              {pointLabels && yieldPoint && testProgress >= material.yieldPoint && (
                <g>
                  <circle 
                    cx={scaleX(yieldPoint.x)} 
                    cy={scaleY(yieldPoint.y)} 
                    r="4" 
                    fill="#8b5cf6" 
                  />
                  <text 
                    x={scaleX(yieldPoint.x) + 8} 
                    y={scaleY(yieldPoint.y) - 8} 
                    fontSize="10" 
                    fill="#8b5cf6"
                  >
                    B: Yield Point
                  </text>
                </g>
              )}
              
              {pointLabels && ultimateStrengthPoint && testProgress >= material.ultimateStrength && (
                <g>
                  <circle 
                    cx={scaleX(ultimateStrengthPoint.x)} 
                    cy={scaleY(ultimateStrengthPoint.y)} 
                    r="4" 
                    fill="#ec4899" 
                  />
                  <text 
                    x={scaleX(ultimateStrengthPoint.x) - 8} 
                    y={scaleY(ultimateStrengthPoint.y) - 8} 
                    fontSize="10" 
                    fill="#ec4899"
                    textAnchor="end"
                  >
                    C: Ultimate Strength
                  </text>
                </g>
              )}
              
              {pointLabels && failurePoint && testProgress >= material.failurePoint && (
                <g>
                  <circle 
                    cx={scaleX(failurePoint.x)} 
                    cy={scaleY(failurePoint.y)} 
                    r="4" 
                    fill="#ef4444" 
                  />
                  <text 
                    x={scaleX(failurePoint.x) - 8} 
                    y={scaleY(failurePoint.y) + 15} 
                    fontSize="10" 
                    fill="#ef4444"
                    textAnchor="end"
                  >
                    D: Fracture
                  </text>
                </g>
              )}
              
              {/* Current point */}
              <circle 
                cx={currentX} 
                cy={currentY} 
                r="6" 
                fill="#ef4444" 
                stroke="#fff"
                strokeWidth="1.5"
              />
              
              {/* Material info label */}
              <rect 
                x={graphWidth - 100} 
                y="5" 
                width="95" 
                height="70"
                fill="rgba(255, 255, 255, 0.8)"
                stroke="#ddd"
                strokeWidth="1"
                rx="3"
              />
              
              <text 
                x={graphWidth - 95} 
                y="20" 
                fill="#000000" 
                fontSize="12"
                fontWeight="bold"
              >
                {material.name}
              </text>
              
              <text 
                x={graphWidth - 95} 
                y="35" 
                fill="#000000" 
                fontSize="10"
              >
                Strain: {strain.toFixed(3)}
              </text>
              
              <text 
                x={graphWidth - 95} 
                y="50" 
                fill="#000000" 
                fontSize="10"
              >
                Stress: {stress.toFixed(0)} MPa
              </text>
              
              <text 
                x={graphWidth - 95} 
                y="65" 
                fill="#000000" 
                fontSize="10"
              >
                E: {material.elasticSlope} GPa
              </text>
            </svg>
          </div>
        </div>
        
        {/* Controls section */}
        <div className="tw-p-4 tw-border-t tw-border-gray-200 tw-bg-gray-50">
          <div className="tw-grid tw-grid-cols-1 md:tw-grid-cols-2 tw-gap-4">
            <div>
              <label className="tw-block tw-text-sm tw-font-medium tw-text-gray-700 tw-mb-1">
                Material Selection
              </label>
              <select 
                value={selectedMaterial} 
                onChange={handleMaterialChange}
                disabled={isRunning}
                className="tw-w-full tw-p-2 tw-border tw-border-gray-300 tw-rounded-md"
              >
                {Object.keys(materials).map(key => (
                  <option key={key} value={key}>
                    {materials[key].name} (E = {materials[key].elasticSlope} GPa)
                  </option>
                ))}
              </select>
            </div>
          
            <div>
              <label className="tw-block tw-text-sm tw-font-medium tw-text-gray-700 tw-mb-1">
                Test Progress: {(testProgress * 100).toFixed(0)}%
              </label>
              <input 
                type="range" 
                min="0" 
                max="1" 
                step="0.01" 
                value={testProgress} 
                onChange={(e) => !isRunning && setTestProgress(parseFloat(e.target.value))}
                disabled={isRunning}
                className="tw-w-full tw-h-2 tw-bg-gray-200 tw-rounded-lg tw-appearance-none tw-cursor-pointer"
              />
            </div>
          </div>

          <div className="tw-flex tw-gap-4 tw-justify-center tw-mt-4">
            <button 
              onClick={startTest}
              disabled={isRunning}
              className={`tw-px-4 tw-py-2 tw-rounded-md ${isRunning ? 'tw-bg-gray-400 tw-text-white' : 'tw-bg-blue-500 tw-text-white hover:tw-bg-blue-600'}`}
            >
              {isRunning ? 'Testing...' : 'Run Test'}
            </button>
            
            <button 
              onClick={resetTest}
              className="tw-px-4 tw-py-2 tw-bg-gray-500 tw-text-white tw-rounded-md hover:tw-bg-gray-600"
            >
              Reset
            </button>
            
            <button 
              onClick={() => setPointLabels(!pointLabels)}
              className="tw-px-4 tw-py-2 tw-bg-gray-100 tw-text-gray-800 tw-rounded-md hover:tw-bg-gray-200"
            >
              {pointLabels ? 'Hide Labels' : 'Show Labels'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StressStrainCurveDemo;

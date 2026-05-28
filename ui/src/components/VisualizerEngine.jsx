import React, { useState, useEffect, useRef } from 'react';
import { Play, Pause, SkipForward, SkipBack, FastForward } from 'lucide-react';
import ArrayVisualizer from './renderers/ArrayVisualizer';
import VariablesGrid from './renderers/VariableVisualizer';
import HashMapVisualizer from './renderers/HashMapVisualizer';
import MatrixVisualizer from './renderers/MatrixVisualizer';
import TreeVisualizer from './renderers/TreeVisualizer';

const VisualizerEngine = ({ steps }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [speed, setSpeed] = useState(1000);
  const timerRef = useRef(null);

  useEffect(() => {
    setCurrentStep(0);
    setIsPlaying(false);
  }, [steps]);

  useEffect(() => {
    if (isPlaying) {
      timerRef.current = setInterval(() => {
        setCurrentStep((prev) => {
          if (prev >= steps.length - 1) {
            setIsPlaying(false);
            return prev;
          }
          return prev + 1;
        });
      }, speed);
    } else {
      if (timerRef.current) clearInterval(timerRef.current);
    }
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [isPlaying, speed, steps.length]);

  if (!steps || steps.length === 0) {
    return <div className="visualizer-container glass"><div className="visualizer-canvas">Select a problem to visualize.</div></div>;
  }

  const stepData = steps[currentStep];
  const { description, structures } = stepData;

  // Group variables together
  const variables = Object.entries(structures).filter(([_, data]) => data.type === 'variable');
  const otherStructures = Object.entries(structures).filter(([_, data]) => data.type !== 'variable');

  const renderStructure = (name, data) => {
    switch (data.type) {
      case 'array':
        return <ArrayVisualizer data={data} />;
      case 'hashmap':
        return <HashMapVisualizer data={data} />;
      case 'matrix':
        return <MatrixVisualizer data={data} />;
      case 'tree':
        return <TreeVisualizer data={data} />;
      default:
        return <div>Unknown structure type: {data.type}</div>;
    }
  };

  const progressPercentage = ((currentStep + 1) / steps.length) * 100;

  return (
    <div className="visualizer-container glass">
      <div className="visualizer-canvas">
        <div className="step-description">{description}</div>
        
        {variables.length > 0 && (
          <div className="renderer-section">
            <h3 className="renderer-title">Variables</h3>
            <VariablesGrid variables={variables} />
          </div>
        )}

        {otherStructures.map(([name, data]) => (
          <div key={name} className="renderer-section">
            <h3 className="renderer-title">{name}</h3>
            {renderStructure(name, data)}
          </div>
        ))}
      </div>

      <div className="controls-bar">
        <button onClick={() => setCurrentStep(Math.max(0, currentStep - 1))} disabled={currentStep === 0}>
          <SkipBack size={18} />
        </button>
        <button className="primary" onClick={() => setIsPlaying(!isPlaying)} disabled={currentStep >= steps.length - 1}>
          {isPlaying ? <Pause size={20} /> : <Play size={20} />}
        </button>
        <button onClick={() => setCurrentStep(Math.min(steps.length - 1, currentStep + 1))} disabled={currentStep >= steps.length - 1}>
          <SkipForward size={18} />
        </button>
        
        <button onClick={() => setSpeed(speed === 1000 ? 500 : speed === 500 ? 250 : 1000)}>
          <FastForward size={18} /> {speed === 1000 ? '1x' : speed === 500 ? '2x' : '4x'}
        </button>

        <div className="progress-container">
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: `${progressPercentage}%` }}></div>
          </div>
          <span className="text-secondary" style={{ fontSize: '0.85rem' }}>
            {currentStep + 1} / {steps.length}
          </span>
        </div>
      </div>
    </div>
  );
};

export default VisualizerEngine;

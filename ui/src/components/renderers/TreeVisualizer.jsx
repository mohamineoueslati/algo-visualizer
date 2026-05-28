import React from 'react';

const TreeNode = ({ node, pointers = {}, x, y, level }) => {
  if (!node) return null;

  const RADIUS = 25;
  const X_OFFSET = 120 / (level || 1); // Decrease horizontal spacing at lower levels
  const Y_OFFSET = 70;

  const nodePointers = pointers[node.id] || [];
  const isHighlight = nodePointers.length > 0;
  const isMatch = nodePointers.includes('match');

  const strokeColor = isMatch ? 'var(--success-color)' : isHighlight ? 'var(--accent-color)' : 'var(--border-color)';
  const fillColor = isMatch ? 'rgba(16, 185, 129, 0.2)' : isHighlight ? 'rgba(59, 130, 246, 0.2)' : 'rgba(255, 255, 255, 0.05)';

  return (
    <g className="tree-node-group animate-in">
      {/* Left Child Link */}
      {node.left && (
        <line 
          x1={x} y1={y} 
          x2={x - X_OFFSET} y2={y + Y_OFFSET} 
          stroke="var(--border-color)" 
          strokeWidth="2" 
        />
      )}
      
      {/* Right Child Link */}
      {node.right && (
        <line 
          x1={x} y1={y} 
          x2={x + X_OFFSET} y2={y + Y_OFFSET} 
          stroke="var(--border-color)" 
          strokeWidth="2" 
        />
      )}

      {/* Current Node */}
      <circle 
        cx={x} cy={y} 
        r={RADIUS} 
        fill={fillColor} 
        stroke={strokeColor} 
        strokeWidth={isHighlight || isMatch ? '4' : '2'}
        style={{ transition: 'all 0.3s ease' }}
      />
      <text 
        x={x} y={y} 
        textAnchor="middle" 
        dominantBaseline="central" 
        fill="var(--text-primary)"
        fontSize="1.2rem"
        fontWeight="bold"
      >
        {node.val}
      </text>

      {/* Pointers Text */}
      {nodePointers.filter(p => p !== 'match').map((p, i) => (
        <text
          key={p}
          x={x + RADIUS + 10}
          y={y - 10 + (i * 15)}
          fill="var(--accent-color)"
          fontSize="0.8rem"
          fontWeight="bold"
          className="pointer-badge-svg"
        >
          {p}
        </text>
      ))}

      {/* Recursively render children */}
      {node.left && <TreeNode node={node.left} pointers={pointers} x={x - X_OFFSET} y={y + Y_OFFSET} level={(level || 1) + 1} />}
      {node.right && <TreeNode node={node.right} pointers={pointers} x={x + X_OFFSET} y={y + Y_OFFSET} level={(level || 1) + 1} />}
    </g>
  );
};

const TreeVisualizer = ({ data }) => {
  const { value: rootNode, pointers = {} } = data;

  // Invert pointers mapping from: { pointerName: nodeId } to { nodeId: [pointerNames] }
  const nodePointers = {};
  Object.entries(pointers).forEach(([pName, nId]) => {
    if (!nodePointers[nId]) nodePointers[nId] = [];
    nodePointers[nId].push(pName);
  });

  return (
    <div className="tree-container" style={{ width: '100%', display: 'flex', justifyContent: 'center', overflow: 'auto', padding: '16px' }}>
      <svg width="600" height="400" viewBox="0 0 600 400" style={{ overflow: 'visible' }}>
        <TreeNode node={rootNode} pointers={nodePointers} x={300} y={40} level={1} />
      </svg>
    </div>
  );
};

export default TreeVisualizer;

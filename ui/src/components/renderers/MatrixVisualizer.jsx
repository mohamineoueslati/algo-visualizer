import React from 'react';

const MatrixVisualizer = ({ data }) => {
  const { value, pointers = {} } = data; // pointers: { name: [row, col] }

  // Map "row,col" -> [pointer names]
  const cellPointers = {};
  Object.entries(pointers).forEach(([name, [r, c]]) => {
    const key = `${r},${c}`;
    if (!cellPointers[key]) cellPointers[key] = [];
    cellPointers[key].push(name);
  });

  return (
    <div className="matrix-container" style={{ display: 'flex', flexDirection: 'column', gap: '4px', padding: '16px' }}>
      {value.map((row, rIdx) => (
        <div key={rIdx} className="matrix-row" style={{ display: 'flex', gap: '4px', justifyContent: 'center' }}>
          {row.map((cell, cIdx) => {
            const pNames = cellPointers[`${rIdx},${cIdx}`] || [];
            const isHighlight = pNames.length > 0;
            const isMatch = pNames.includes('match');

            return (
              <div key={cIdx} className="matrix-cell-wrapper" style={{ position: 'relative' }}>
                <div 
                  className={`array-box ${isMatch ? 'match' : isHighlight ? 'highlight' : ''}`}
                  style={{ width: '50px', height: '50px', fontSize: '1.2rem' }}
                >
                  {cell}
                </div>
                {pNames.length > 0 && (
                  <div className="array-pointers" style={{ position: 'absolute', top: '-15px', left: '50%', transform: 'translateX(-50%)', zIndex: 10 }}>
                    {pNames.filter(n => n !== 'match').map(p => (
                      <div key={p} className="pointer-badge" style={{ fontSize: '0.65rem', padding: '2px 4px' }}>{p}</div>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      ))}
    </div>
  );
};

export default MatrixVisualizer;

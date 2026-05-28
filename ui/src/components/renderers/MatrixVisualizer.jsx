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
    <div className="matrix-container matrix-container-wrapper">
      {value.map((row, rIdx) => (
        <div key={rIdx} className="matrix-row">
          {row.map((cell, cIdx) => {
            const pNames = cellPointers[`${rIdx},${cIdx}`] || [];
            const isHighlight = pNames.length > 0;
            const isMatch = pNames.includes('match');

            return (
              <div key={cIdx} className="matrix-cell-wrapper">
                <div
                  className={`array-box matrix-cell ${isMatch ? 'match' : isHighlight ? 'highlight' : ''}`}
                >
                  {cell}
                </div>
                {pNames.length > 0 && (
                  <div className="array-pointers matrix-pointers">
                    {pNames.filter(n => n !== 'match').map(p => (
                      <div key={p} className="pointer-badge matrix-pointer-badge">{p}</div>
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

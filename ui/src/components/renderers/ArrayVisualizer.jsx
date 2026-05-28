const ArrayVisualizer = ({ data }) => {
  const { value, pointers = {} } = data;

  // Invert pointers dict to map index -> [pointer names]
  const indexPointers = {};
  Object.entries(pointers).forEach(([name, idx]) => {
    if (!indexPointers[idx]) indexPointers[idx] = [];
    indexPointers[idx].push(name);
  });

  return (
    <div className="array-container">
      {value.map((item, idx) => {
        const pNames = indexPointers[idx] || [];
        const isHighlight = pNames.length > 0;
        const isMatch = pNames.includes('match');

        return (
          <div key={idx} className="array-item-wrapper animate-in" style={{ animationDelay: `${idx * 0.05}s` }}>
            <div className={`array-box ${isMatch ? 'match' : isHighlight ? 'highlight' : ''}`}>
              {item}
            </div>
            <div className="array-index">{idx}</div>
            <div className="array-pointers">
              {pNames.filter(n => n !== 'match').map(p => (
                <div key={p} className="pointer-badge">{p}</div>
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default ArrayVisualizer;

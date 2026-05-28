import React from 'react';

const VariableVisualizer = ({ data, name }) => {
  return (
    <div className="variable-card glass animate-in">
      <div className="variable-name">{name}</div>
      <div className="variable-value">{data.value}</div>
    </div>
  );
};

const VariablesGrid = ({ variables }) => {
  if (variables.length === 0) return null;
  
  return (
    <div className="variables-grid">
      {variables.map(([name, data]) => (
        <VariableVisualizer key={name} name={name} data={data} />
      ))}
    </div>
  );
};

export default VariablesGrid;

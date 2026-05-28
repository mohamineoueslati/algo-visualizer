const HashMapVisualizer = ({ data }) => {
  const { value } = data;
  const entries = Object.entries(value);

  if (entries.length === 0) {
    return <div className="text-secondary italic">Empty HashMap</div>;
  }

  return (
    <div className="hashmap-container">
      {entries.map(([k, v], idx) => (
        <div key={k} className="hashmap-entry animate-in" style={{ animationDelay: `${idx * 0.05}s` }}>
          <div className="hashmap-key">{k}</div>
          <div className="hashmap-value">{v}</div>
        </div>
      ))}
    </div>
  );
};

export default HashMapVisualizer;

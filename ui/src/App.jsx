import { useState, useEffect } from 'react';
import axios from 'axios';
import VisualizerEngine from './components/VisualizerEngine';

const API_BASE = 'http://localhost:8000/api';

function App() {
  const [problems, setProblems] = useState([]);
  const [activeProblem, setActiveProblem] = useState(null);
  const [steps, setSteps] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [customInputs, setCustomInputs] = useState({});

  useEffect(() => {
    // Fetch available problems
    axios.get(`${API_BASE}/problems`)
      .then(res => setProblems(res.data))
      .catch(() => setError('Failed to fetch problems from backend. Is it running?'));
  }, []);

  const runAlgorithm = async (problem, args) => {
    setLoading(true);
    setSteps([]);
    setError(null);
    try {
      const res = await axios.post(`${API_BASE}/run/${problem.id}`, args);
      setSteps(res.data.steps || []);
    } catch {
      setError('Failed to run problem.');
    } finally {
      setLoading(false);
    }
  };

  const selectProblem = async (problem) => {
    setActiveProblem(problem);

    // Initialize custom inputs with defaults
    const initialInputs = {};
    if (problem.inputs) {
      problem.inputs.forEach(inp => {
        initialInputs[inp.name] = typeof inp.default === 'object' ? JSON.stringify(inp.default) : inp.default;
      });
    }
    setCustomInputs(initialInputs);

    // Run with defaults immediately
    runAlgorithm(problem, null);
  };

  const handleRunCustom = () => {
    if (!activeProblem) return;
    const parsedArgs = {};
    let hasError = false;

    if (activeProblem.inputs) {
      activeProblem.inputs.forEach(inp => {
        try {
          const val = customInputs[inp.name];
          if (inp.type === 'array' || inp.type === 'number') {
            parsedArgs[inp.name] = JSON.parse(val);
          } else {
            parsedArgs[inp.name] = val;
          }
        } catch {
          setError(`Invalid JSON format for input: ${inp.name}. Ensure arrays are formatted like [1, 2, 3]`);
          hasError = true;
        }
      });
    }

    if (!hasError) {
      runAlgorithm(activeProblem, parsedArgs);
    }
  };

  const handleInputChange = (name, value) => {
    setCustomInputs(prev => ({ ...prev, [name]: value }));
  };

  return (
    <div className="app-container">
      <div className="sidebar glass">
        <h1>Algo Visualizer</h1>

        {error && <div className="text-secondary error-message">{error}</div>}

        <div className="problem-list">
          {problems.map(p => (
            <div
              key={p.id}
              className={`problem-card ${activeProblem?.id === p.id ? 'active' : ''}`}
              onClick={() => selectProblem(p)}
            >
              <h3>{p.title}</h3>
              <p>{p.difficulty}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="main-content">
        <div className="visualizer-header">
          <h2>{activeProblem ? activeProblem.title : 'Select a Problem'}</h2>
          {activeProblem && <p className="text-secondary problem-description">{activeProblem.description}</p>}
        </div>

        {activeProblem && activeProblem.inputs && (
          <div className="custom-inputs-section glass">
            <h3 className="inputs-section-title">Test Case Inputs</h3>
            <div className="inputs-grid">
              {activeProblem.inputs.map(inp => (
                <div key={inp.name} className="input-group">
                  <label>{inp.name} <span className="type-badge type-badge-inline">{inp.type}</span></label>
                  <input
                    type="text"
                    value={customInputs[inp.name] || ''}
                    onChange={(e) => handleInputChange(inp.name, e.target.value)}
                    className="custom-input"
                  />
                </div>
              ))}
            </div>
            <button className="primary run-custom-btn" onClick={handleRunCustom} disabled={loading}>Run with Custom Inputs</button>
          </div>
        )}

        {loading ? (
          <div className="loading-container">
            <div className="text-secondary loading-text">Running Algorithm...</div>
          </div>
        ) : (
          <VisualizerEngine steps={steps} />
        )}
      </div>
    </div>
  );
}

export default App;

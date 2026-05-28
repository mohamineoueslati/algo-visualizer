# Codebase Explanation & Core Concepts

This document explains the architecture of the Algo Visualizer project, breaking down what every critical source file does and the core concepts behind the system.

## Core Concept: The Generator Pattern
The entire visualizer is built around the **Python Generator** pattern and **State Management**. 
Instead of trying to parse Python code execution line-by-line, the algorithms are written as Python `generator` functions. Every time an important event happens in the algorithm, it `yield`s a snapshot of the current state (variables, arrays, pointers). 
The backend collects all these yielded snapshots into a list of "steps", and sends them to the frontend. The frontend simply acts as a video player, rendering these snapshots frame-by-frame.

---

## 1. Backend Codebase (Root Directory)

### `main.py`
This is the entry point for the FastAPI server. 
- **Dynamic Loading**: It uses `importlib` to scan the `problems/` directory and dynamically load every Python file it finds. This means you can add new problems without modifying `main.py`.
- **API Endpoints**: 
  - `GET /api/problems`: Returns metadata (title, description, difficulty) for all loaded problems.
  - `POST /api/run/{problem_id}`: Executes the algorithm. It calls the `solve()` generator function of the requested problem, collects all the yielded states into an array, and returns it as a JSON response.

### `core/visualizer.py`
This file acts as the bridge between Python data structures and the Frontend renderers.
- It contains helper functions (`create_state`, `array_struct`, `var_struct`, `tree_struct`, etc.) that take raw Python variables and format them into a strict JSON schema.
- This schema dictates the `type` of the data (e.g., "array") and includes any `pointers` (like the current index `i` or `j` being checked). The frontend uses this `type` string to know which React component to draw.

### `problems/*.py` (e.g., `binary_search.py`, `two_sum.py`)
These are the algorithm implementations. Every file must have:
- `PROBLEM_DEF`: A dictionary containing the UI metadata (ID, title).
- `solve()`: A generator function containing the actual algorithm. Instead of just returning the final answer, it `yield`s a dictionary using `create_state()` inside loops or `if` statements to snapshot the variables.

---

## 2. Frontend Codebase (`ui/` directory)

### `ui/src/App.jsx`
This is the main React container component.
- It makes the HTTP calls to the backend using `axios`.
- On load, it fetches the list of available algorithms and renders the sidebar.
- When you click a problem, it hits the `/api/run/` endpoint, receives the array of "steps" (the snapshots), and passes them down as props to the `VisualizerEngine`.

### `ui/src/components/VisualizerEngine.jsx`
This is the "Video Player" of the application.
- **Playback State**: It uses `useState` and `setInterval` to manage playback, speed, and the `currentStep` index.
- **Routing Renderers**: For the current step, it looks at the `structures` dictionary sent by the backend. It checks the `type` of each structure (e.g., if type is `'tree'`), and delegates the actual drawing to the specific renderer component (e.g., `<TreeVisualizer />`).

### `ui/src/components/renderers/`
This folder contains the specialized React components responsible for drawing specific data structures beautifully on screen.
- **`ArrayVisualizer.jsx`**: Renders an array as a row of blocks. It also looks for `pointers` (like `left`, `right`, `mid`) and highlights the specific blocks being pointed at.
- **`TreeVisualizer.jsx`**: Uses SVG lines and circles to recursively draw a binary tree layout. It calculates the `x` and `y` coordinates dynamically based on the tree depth.
- **`MatrixVisualizer.jsx`**: Renders a 2D grid, commonly used for Dynamic Programming (like Unique Paths) or graph traversal algorithms.
- **`VariableVisualizer.jsx`**: Renders standalone primitive variables (like `max_val` or `target`) in sleek cards.
- **`HashMapVisualizer.jsx`**: Renders key-value pairs (like a Python dict), which is critical for algorithms like Two Sum.

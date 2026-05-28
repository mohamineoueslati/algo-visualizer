# Algo Visualizer: UI Architecture & Component Flow

This document details the architecture of the React frontend, the individual UI components, and how data flows through them from the moment a user selects an algorithm to the final visual playback.

## Architectural Overview

The frontend follows a **State-Driven, Top-Down Architecture**. The root component (`App.jsx`) holds the global application state and communicates with the backend API. When algorithm execution data (the `steps` array) is received, it is passed down to a central orchestrator (`VisualizerEngine.jsx`), which manages the playback loop. The orchestrator then delegates the actual rendering of individual data structures to specialized "renderer" components.

---

## 1. The Root Container: `App.jsx`

**Role**: Application Shell, State Manager, and API Gateway.

### Responsibilities:
- **Fetching Metadata**: On mount, it fetches the list of available algorithms and their expected inputs from the backend `/api/problems`.
- **Sidebar & Navigation**: Renders the left sidebar listing all available algorithms.
- **Custom Input Management**: Dynamically renders text inputs based on the `inputs` schema defined by the backend problem. It safely parses user input (e.g., converting strings like `"[1, 2, 3]"` into actual JavaScript arrays via `JSON.parse`) before sending them to the backend.
- **API Orchestration**: Sends the selected algorithm and parsed custom inputs to `/api/run/{problem_id}`. Once the backend responds, it passes the resulting `steps` array down to the `VisualizerEngine`.

---

## 2. The Playback Orchestrator: `VisualizerEngine.jsx`

**Role**: Time-travel Controller and Layout Manager.

### Responsibilities:
- **Playback State**: Maintains internal state for `currentStep`, `isPlaying`, and playback `speed`.
- **Timer Loop**: Uses a `setInterval` loop (managed via a `useRef`) to automatically increment the `currentStep` when the user clicks "Play".
- **Controls Bar**: Renders the playback controls (Play/Pause, Skip Forward/Backward, Speed Toggle) and the progress bar.
- **Delegation**: For the current active step, it looks at the `structures` dictionary provided by the backend. It uses a `switch` statement based on the `type` property (e.g., `array`, `hashmap`, `tree`) to dynamically render the appropriate child component from the `renderers/` folder.

---

## 3. The Specialized Renderers

These are stateless, "dumb" components. They receive exactly one prop (`data`), which contains the raw values and pointer metadata for a single structure at the current point in time. They are strictly responsible for visual representation.

### `VariableVisualizer.jsx`
- **Purpose**: Displays primitive scalar values (integers, strings, booleans).
- **Behavior**: Groups all variables together and renders them as simple, readable cards showing the variable name in uppercase and its current value in large text.

### `ArrayVisualizer.jsx`
- **Purpose**: Renders 1D arrays (lists).
- **Behavior**: Maps over the array and renders boxes. It checks the `pointers` dictionary to see if any algorithm pointers (like `i`, `j`, `left`, `right`) are currently pointing at a specific index. If so, it highlights the box and renders small badges above or below the box showing the pointer names.

### `MatrixVisualizer.jsx`
- **Purpose**: Renders 2D arrays (grids).
- **Behavior**: Similar to the Array Visualizer, but maps over rows and columns. Pointers are tracked using a `"row,col"` string key mapping to determine which specific grid cell should be highlighted.

### `HashMapVisualizer.jsx`
- **Purpose**: Renders dictionary/object key-value pairs (e.g., the `seen` hashmap in the Two Sum algorithm).
- **Behavior**: Uses `Object.entries()` to render a clean, two-column list of keys and their associated values.

### `TreeVisualizer.jsx`
- **Purpose**: Renders node-based recursive data structures (like Binary Trees).
- **Behavior**: Unlike the CSS-based renderers, this uses an `<svg>` canvas. It features a recursive `<TreeNode>` component that calculates `x` and `y` coordinates based on its depth (`level`). It draws connecting `<line>` elements to its children, and SVG `<circle>` and `<text>` elements for the nodes and pointers.

---

## Data Flow Example: Running "Two Sum"

1. **User Interaction (`App.jsx`)**: The user selects "Two Sum" from the sidebar, enters `nums = [3, 2, 4]` and `target = 6`, and clicks "Run".
2. **API Call (`App.jsx`)**: `App.jsx` POSTs this JSON to the backend and receives a response containing an array of 5 `steps`.
3. **Hand-off (`App.jsx` → `VisualizerEngine.jsx`)**: `App.jsx` updates its `steps` state, which is passed as a prop to `VisualizerEngine`.
4. **Playback Initiation (`VisualizerEngine.jsx`)**: `VisualizerEngine` resets `currentStep` to `0`. The user clicks "Play".
5. **Step Rendering (`VisualizerEngine.jsx` → Renderers)**:
   - For Step 1, the backend state contains a variable (`target`), an array (`nums`), and a hashmap (`seen`).
   - `VisualizerEngine` extracts these three structures.
   - It mounts `<VariableVisualizer>` for `target`.
   - It mounts `<ArrayVisualizer>` for `nums`, passing it the pointer `{ i: 0 }`. The Array renderer highlights the 0th box.
   - It mounts `<HashMapVisualizer>` for `seen`, showing it as currently empty.
6. **Tick**: The interval ticks, `currentStep` becomes `1`, and the specialized renderers instantly update to reflect the new state of the pointers and hashmaps.

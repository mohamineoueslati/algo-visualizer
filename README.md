# Algo Visualizer 🚀

A beautiful, generic algorithm visualizer tailored for LeetCode-style problems. The system splits the logic from the rendering:
- **Backend (Python)**: Executes the algorithm and yields state changes.
- **Frontend (React)**: Reads the states and orchestrates beautiful, modern animations using standard data-structure components.

## Features ✨
- **Generic Visualizers**: Built-in support for rendering variables, arrays (with pointers), and hashmaps.
- **Playback Controls**: Step back, play, pause, step forward, and adjust speed.
- **Glassmorphic UI**: Vibrant, responsive dark mode.
- **Extensible Architecture**: Adding a new problem only requires a single python file.

## Getting Started

### 1. Run the Backend
Requires Python 3.8+
```bash
# In the root directory
python -m venv venv

# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
python main.py
```
*The server will run on http://localhost:8000*

### 2. Run the Frontend
Requires Node.js
```bash
cd ui
npm install
npm run dev
```
*The UI will run on http://localhost:5173*

## Adding a New Problem
Adding a new problem requires ZERO frontend changes.

1. Create a new `.py` file in `problems/`.
2. Define `PROBLEM_DEF` with the `id`, `title`, and `description`.
3. Create a `solve()` generator function.
4. Yield states using `create_state()` and data structure formatters from `core.visualizer`.

### Example (`problems/my_problem.py`)
```python
from core.visualizer import create_state, array_struct, var_struct

PROBLEM_DEF = {
    "id": "find_max",
    "title": "Find Maximum",
    "description": "Find the maximum number in an array.",
    "difficulty": "Easy"
}

def solve(nums=[1, 5, 2, 9, 3]):
    max_val = nums[0]
    
    yield create_state("Initialize max_val", {
        "nums": array_struct(nums, {"i": 0}),
        "max_val": var_struct(max_val)
    })
    
    for i in range(1, len(nums)):
        if nums[i] > max_val:
            max_val = nums[i]
            yield create_state(f"Found new max: {max_val}", {
                "nums": array_struct(nums, {"i": i, "match": i}),
                "max_val": var_struct(max_val)
            })
        else:
            yield create_state(f"Checking {nums[i]}, not greater than {max_val}", {
                "nums": array_struct(nums, {"i": i}),
                "max_val": var_struct(max_val)
            })
            
    yield create_state("Done", {
        "nums": array_struct(nums),
        "max_val": var_struct(max_val)
    })
```
The frontend will automatically discover this file, add it to the sidebar, and generically render its variables and arrays!

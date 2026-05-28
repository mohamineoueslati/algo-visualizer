import os
import importlib.util
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Algo Visualizer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registry to hold problems
problems_registry = {}

def load_problems():
    problems_dir = os.path.join(os.path.dirname(__file__), "problems")
    for filename in os.listdir(problems_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]
            file_path = os.path.join(problems_dir, filename)
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, "PROBLEM_DEF"):
                prob = module.PROBLEM_DEF
                problems_registry[prob["id"]] = {
                    "def": prob,
                    "module": module
                }

load_problems()

@app.get("/api/problems")
def get_problems():
    return [p["def"] for p in problems_registry.values()]

@app.get("/api/problems/{problem_id}")
def get_problem(problem_id: str):
    if problem_id not in problems_registry:
        return {"error": "Problem not found"}
    return problems_registry[problem_id]["def"]

@app.post("/api/run/{problem_id}")
def run_problem(problem_id: str, args: dict = None):
    if problem_id not in problems_registry:
        return {"error": "Problem not found"}
        
    module = problems_registry[problem_id]["module"]
    
    # Simple runner: execute the generator and collect steps
    steps = []
    try:
        if args:
            generator = module.solve(**args)
        else:
            generator = module.solve()
            
        for step in generator:
            steps.append(step)
    except Exception as e:
        steps.append({
            "description": f"Error: {str(e)}",
            "structures": {}
        })
        
    return {"steps": steps}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

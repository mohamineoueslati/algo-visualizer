from core.visualizer import create_state, array_struct, hashmap_struct

PROBLEM_DEF = {
    "id": "two_sum",
    "title": "Two Sum",
    "description": "Find two numbers such that they add up to a specific target number.",
    "difficulty": "Easy",
    "inputs": [
        {"name": "nums", "type": "array", "default": [2, 7, 11, 15]},
        {"name": "target", "type": "number", "default": 9}
    ]
}

def solve(nums=[2, 7, 11, 15], target=9):
    seen = {}
    
    yield create_state("Starting Two Sum algorithm.", {
        "nums": array_struct(nums),
        "seen": hashmap_struct(seen)
    })
    
    for i, num in enumerate(nums):
        complement = target - num
        
        yield create_state(f"Checking index {i}. Number is {num}. Complement needed is {complement}.", {
            "nums": array_struct(nums, {"i": i}),
            "seen": hashmap_struct(seen)
        })
        
        if complement in seen:
            yield create_state(f"Found complement {complement} in our hashmap! Returning indices {[seen[complement], i]}.", {
                "nums": array_struct(nums, {"i": i, "match": seen[complement]}),
                "seen": hashmap_struct(seen)
            })
            return [seen[complement], i]
            
        seen[num] = i
        yield create_state(f"Complement not found. Adding {num} to hashmap at index {i}.", {
            "nums": array_struct(nums, {"i": i}),
            "seen": hashmap_struct(seen)
        })
        
    yield create_state("No solution found.", {
        "nums": array_struct(nums),
        "seen": hashmap_struct(seen)
    })
    return []

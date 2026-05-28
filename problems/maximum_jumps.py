from core.visualizer import create_state, array_struct, var_struct

PROBLEM_DEF = {
    "id": "maximum_jumps",
    "title": "Maximum Jumps",
    "description": "Find the maximum number of jumps to reach the last index given a target constraint.",
    "difficulty": "Medium",
    "inputs": [
        {"name": "nums", "type": "array", "default": [1, 3, 6, 4, 1, 2]},
        {"name": "target", "type": "number", "default": 2}
    ]
}

def solve(nums=[1, 3, 6, 4, 1, 2], target=2):
    n = len(nums)
    jumps = [-1] * n
    jumps[0] = 0
    
    yield create_state("Initialize jumps array. Start at index 0 with 0 jumps.", {
        "nums": array_struct(nums),
        "jumps": array_struct(jumps),
        "target": var_struct(target)
    })
    
    for i in range(n):
        yield create_state(f"Outer loop: checking if we can jump from index {i} (nums[{i}] = {nums[i]}).", {
            "nums": array_struct(nums, {"i": i}),
            "jumps": array_struct(jumps, {"i": i}),
            "target": var_struct(target)
        })
        
        if jumps[i] == -1:
            yield create_state(f"Index {i} is unreachable (jumps[{i}] == -1), skipping.", {
                "nums": array_struct(nums, {"i": i}),
                "jumps": array_struct(jumps, {"i": i}),
                "target": var_struct(target)
            })
            continue
            
        for j in range(i + 1, n):
            diff = abs(nums[j] - nums[i])
            yield create_state(f"Inner loop: considering jump from {i} to {j}. Difference: |{nums[j]} - {nums[i]}| = {diff}.", {
                "nums": array_struct(nums, {"i": i, "j": j}),
                "jumps": array_struct(jumps, {"i": i, "j": j}),
                "target": var_struct(target)
            })
            
            if diff <= target:
                old_val = jumps[j]
                jumps[j] = max(jumps[j], jumps[i] + 1)
                
                if jumps[j] != old_val:
                    desc = f"Valid jump (difference {diff} <= {target})! Updated jumps[{j}] from {old_val} to {jumps[j]}."
                else:
                    desc = f"Valid jump, but jumps[{j}] is already >= {jumps[i] + 1}."
                    
                yield create_state(desc, {
                    "nums": array_struct(nums, {"i": i, "match": j}),
                    "jumps": array_struct(jumps, {"i": i, "match": j}),
                    "target": var_struct(target)
                })
                
    final_ans = jumps[n - 1] if n > 0 else -1
    
    if final_ans == -1:
        yield create_state("Finished. Last index is unreachable.", {
            "nums": array_struct(nums),
            "jumps": array_struct(jumps, {"match": n - 1 if n > 0 else 0}),
            "target": var_struct(target)
        })
    else:
        yield create_state(f"Finished! Maximum jumps to reach the last index is {final_ans}.", {
            "nums": array_struct(nums),
            "jumps": array_struct(jumps, {"match": n - 1 if n > 0 else 0}),
            "target": var_struct(target)
        })

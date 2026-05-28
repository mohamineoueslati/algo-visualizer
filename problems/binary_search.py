from core.visualizer import create_state, array_struct, var_struct

PROBLEM_DEF = {
    "id": "binary_search",
    "title": "Binary Search",
    "description": "Find the target value within a sorted array.",
    "difficulty": "Easy",
    "inputs": [
        {"name": "nums", "type": "array", "default": [-1, 0, 3, 5, 9, 12]},
        {"name": "target", "type": "number", "default": 9}
    ]
}

def solve(nums=[-1, 0, 3, 5, 9, 12], target=9):
    left = 0
    right = len(nums) - 1
    
    yield create_state("Initializing left and right pointers.", {
        "nums": array_struct(nums, {"L": left, "R": right}),
        "target": var_struct(target)
    })
    
    while left <= right:
        mid = (left + right) // 2
        
        yield create_state(f"Calculating mid = ({left} + {right}) // 2 = {mid}.", {
            "nums": array_struct(nums, {"L": left, "R": right, "M": mid}),
            "target": var_struct(target)
        })
        
        if nums[mid] == target:
            yield create_state(f"Found target {target} at index {mid}!", {
                "nums": array_struct(nums, {"L": left, "R": right, "M": mid, "match": mid}),
                "target": var_struct(target)
            })
            return mid
        elif nums[mid] < target:
            left = mid + 1
            yield create_state(f"nums[mid] ({nums[mid]}) is less than target. Moving left pointer to {left}.", {
                "nums": array_struct(nums, {"L": left, "R": right}),
                "target": var_struct(target)
            })
        else:
            right = mid - 1
            yield create_state(f"nums[mid] ({nums[mid]}) is greater than target. Moving right pointer to {right}.", {
                "nums": array_struct(nums, {"L": left, "R": right}),
                "target": var_struct(target)
            })
            
    yield create_state("Target not found in array.", {
        "nums": array_struct(nums),
        "target": var_struct(target)
    })
    return -1

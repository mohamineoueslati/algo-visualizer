from core.visualizer import create_state, array_struct, var_struct

PROBLEM_DEF = {
    "id": "median_sorted_arrays",
    "title": "Median of Two Sorted Arrays",
    "description": "Find the median of two sorted arrays by merging them into a single sorted array.",
    "difficulty": "Hard",
    "inputs": [
        {"name": "nums1", "type": "array", "default": [1, 3]},
        {"name": "nums2", "type": "array", "default": [2]}
    ]
}

def solve(nums1=[1, 3], nums2=[2]):
    nums3 = []
    i = 0
    j = 0
    
    yield create_state("Start merging the two sorted arrays.", {
        "nums1": array_struct(nums1, {"i": i} if i < len(nums1) else {}),
        "nums2": array_struct(nums2, {"j": j} if j < len(nums2) else {}),
        "nums3": array_struct(nums3)
    })
    
    while i < len(nums1) and j < len(nums2):
        if nums1[i] <= nums2[j]:
            desc = f"nums1[{i}] ({nums1[i]}) <= nums2[{j}] ({nums2[j]}). Appending {nums1[i]} to nums3."
            yield create_state(desc, {
                "nums1": array_struct(nums1, {"match": i}),
                "nums2": array_struct(nums2, {"j": j}),
                "nums3": array_struct(nums3)
            })
            
            nums3.append(nums1[i])
            i += 1
        else:
            desc = f"nums1[{i}] ({nums1[i]}) > nums2[{j}] ({nums2[j]}). Appending {nums2[j]} to nums3."
            yield create_state(desc, {
                "nums1": array_struct(nums1, {"i": i}),
                "nums2": array_struct(nums2, {"match": j}),
                "nums3": array_struct(nums3)
            })
            
            nums3.append(nums2[j])
            j += 1
            
        yield create_state("Updated arrays after append.", {
            "nums1": array_struct(nums1, {"i": i} if i < len(nums1) else {}),
            "nums2": array_struct(nums2, {"j": j} if j < len(nums2) else {}),
            "nums3": array_struct(nums3, {"latest": len(nums3) - 1})
        })
            
    if i < len(nums1):
        yield create_state("nums2 is exhausted. Appending remaining elements of nums1.", {
            "nums1": array_struct(nums1, {"i": i}),
            "nums2": array_struct(nums2),
            "nums3": array_struct(nums3)
        })
        for k in range(i, len(nums1)):
            nums3.append(nums1[k])
            yield create_state(f"Appended {nums1[k]} from nums1.", {
                "nums1": array_struct(nums1, {"match": k}),
                "nums2": array_struct(nums2),
                "nums3": array_struct(nums3, {"latest": len(nums3) - 1})
            })
    elif j < len(nums2):
        yield create_state("nums1 is exhausted. Appending remaining elements of nums2.", {
            "nums1": array_struct(nums1),
            "nums2": array_struct(nums2, {"j": j}),
            "nums3": array_struct(nums3)
        })
        for k in range(j, len(nums2)):
            nums3.append(nums2[k])
            yield create_state(f"Appended {nums2[k]} from nums2.", {
                "nums1": array_struct(nums1),
                "nums2": array_struct(nums2, {"match": k}),
                "nums3": array_struct(nums3, {"latest": len(nums3) - 1})
            })

    n = len(nums3)
    if n == 0:
        yield create_state("Both arrays are empty.", {
            "nums1": array_struct(nums1),
            "nums2": array_struct(nums2),
            "nums3": array_struct(nums3)
        })
        return

    if n % 2 == 0:
        mid1 = n // 2 - 1
        mid2 = n // 2
        median = (nums3[mid1] + nums3[mid2]) / 2
        yield create_state(f"Length is even ({n}). Median is average of elements at indices {mid1} and {mid2}: ({nums3[mid1]} + {nums3[mid2]}) / 2 = {median}.", {
            "nums1": array_struct(nums1),
            "nums2": array_struct(nums2),
            "nums3": array_struct(nums3, {"mid1": mid1, "mid2": mid2}),
            "median": var_struct(median)
        })
    else:
        mid = n // 2
        median = nums3[mid]
        yield create_state(f"Length is odd ({n}). Median is middle element at index {mid}: {median}.", {
            "nums1": array_struct(nums1),
            "nums2": array_struct(nums2),
            "nums3": array_struct(nums3, {"mid": mid}),
            "median": var_struct(median)
        })

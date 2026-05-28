from core.visualizer import create_state, matrix_struct, var_struct

PROBLEM_DEF = {
    "id": "unique_paths",
    "title": "Unique Paths",
    "description": "A robot is located at the top-left corner of a m x n grid. The robot can only move either down or right at any point in time. The robot is trying to reach the bottom-right corner of the grid. How many possible unique paths are there?",
    "difficulty": "Medium",
    "inputs": [
        {"name": "m", "type": "number", "default": 3},
        {"name": "n", "type": "number", "default": 4}
    ]
}

def solve(m=3, n=4):
    # Initialize DP matrix
    dp = [[0 for _ in range(n)] for _ in range(m)]
    
    yield create_state("Initializing DP table. The robot starts at (0, 0).", {
        "dp": matrix_struct(dp)
    })
    
    # Fill first column
    for i in range(m):
        dp[i][0] = 1
        yield create_state(f"There is only 1 way to reach cells in the first column: move straight down.", {
            "dp": matrix_struct(dp, {"current": [i, 0]}),
        })
        
    # Fill first row
    for j in range(1, n):
        dp[0][j] = 1
        yield create_state(f"There is only 1 way to reach cells in the first row: move straight right.", {
            "dp": matrix_struct(dp, {"current": [0, j]}),
        })
        
    # Fill the rest of the DP table
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
            yield create_state(f"Paths to ({i},{j}) = paths from top ({dp[i-1][j]}) + paths from left ({dp[i][j-1]}).", {
                "dp": matrix_struct(dp, {"current": [i, j], "top": [i-1, j], "left": [i, j-1]}),
            })
            
    yield create_state(f"Done! The total number of unique paths is {dp[m-1][n-1]}.", {
        "dp": matrix_struct(dp, {"match": [m-1, n-1]}),
        "result": var_struct(dp[m-1][n-1])
    })
    return dp[m-1][n-1]

from core.visualizer import create_state, tree_struct

PROBLEM_DEF = {
    "id": "invert_binary_tree",
    "title": "Invert Binary Tree",
    "description": "Given the root of a binary tree, invert the tree, and return its root.",
    "difficulty": "Easy",
    "inputs": [
        {"name": "root_list", "type": "array", "default": [4, 2, 7, 1, 3, 6, 9]}
    ]
}

class TreeNode:
    def __init__(self, val=0, id_str="", left=None, right=None):
        self.val = val
        self.id = id_str
        self.left = left
        self.right = right
        
    def to_dict(self):
        return {
            "id": self.id,
            "val": self.val,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None
        }

def build_tree(root_list):
    if not root_list:
        return None
    root = TreeNode(root_list[0], "root")
    queue = [(root, "")]
    i = 1
    while queue and i < len(root_list):
        node, path = queue.pop(0)
        
        if i < len(root_list) and root_list[i] is not None:
            node.left = TreeNode(root_list[i], path + "l")
            queue.append((node.left, path + "l"))
        i += 1
        
        if i < len(root_list) and root_list[i] is not None:
            node.right = TreeNode(root_list[i], path + "r")
            queue.append((node.right, path + "r"))
        i += 1
        
    return root

def solve(root_list=[4, 2, 7, 1, 3, 6, 9]):
    root = build_tree(root_list)
    if not root:
        yield create_state("Empty tree.", {})
        return
    
    yield create_state("Initial Binary Tree", {
        "tree": tree_struct(root.to_dict())
    })
    
    def invert(node):
        if not node:
            return None
            
        # Snapshot before swap
        yield create_state(f"Visiting node {node.val}", {
            "tree": tree_struct(root.to_dict(), {"current": node.id})
        })
        
        # Invert children recursively
        left = yield from invert(node.left)
        right = yield from invert(node.right)
        
        # Swap
        node.left = right
        node.right = left
        
        yield create_state(f"Swapped children of node {node.val}", {
            "tree": tree_struct(root.to_dict(), {"match": node.id})
        })
        
        return node
        
    yield from invert(root)
    
    yield create_state("Inversion complete!", {
        "tree": tree_struct(root.to_dict(), {"match": "root"})
    })

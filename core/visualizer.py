import copy

def create_state(description, structures):
    return {
        "description": description,
        "structures": structures
    }

def array_struct(value, pointers=None):
    return {
        "type": "array",
        "value": copy.deepcopy(value),
        "pointers": pointers or {}
    }

def hashmap_struct(value):
    return {
        "type": "hashmap",
        "value": copy.deepcopy(value)
    }

def var_struct(value):
    return {
        "type": "variable",
        "value": copy.deepcopy(value)
    }

def matrix_struct(value, pointers=None):
    return {
        "type": "matrix",
        "value": copy.deepcopy(value),
        "pointers": pointers or {}
    }

def tree_struct(root_node, pointers=None):
    return {
        "type": "tree",
        "value": copy.deepcopy(root_node),
        "pointers": pointers or {}
    }

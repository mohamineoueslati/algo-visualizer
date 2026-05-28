def create_state(description, structures):
    return {
        "description": description,
        "structures": structures
    }

def array_struct(value, pointers=None):
    return {
        "type": "array",
        "value": value,
        "pointers": pointers or {}
    }

def hashmap_struct(value):
    return {
        "type": "hashmap",
        "value": value
    }

def var_struct(value):
    return {
        "type": "variable",
        "value": value
    }

def matrix_struct(value, pointers=None):
    return {
        "type": "matrix",
        "value": value,
        "pointers": pointers or {}
    }

def tree_struct(root_node, pointers=None):
    return {
        "type": "tree",
        "value": root_node,
        "pointers": pointers or {}
    }

def is_variable(x):
    return isinstance(x, str) and x.islower()

def is_constant(x):
    return isinstance(x, str) and x[0].isupper()

def occurs_check(var, expr, subst):
    """Check if var occurs in expr after applying current substitution"""
    if var == expr:
        return True
    elif isinstance(expr, list):
        return any(occurs_check(var, e, subst) for e in expr)
    elif expr in subst:
        return occurs_check(var, subst[expr], subst)
    return False

def unify(x, y, subst=None, depth=0):
    """Main unification function with debug prints"""
    indent = "  " * depth
    if subst is None:
        print(indent + f"Substitution failed.")
        return None
    print(indent + f"Unify({x}, {y}) with subst = {subst}")

    if x == y:
        print(indent + "Terms are identical, no change.")
        return subst
    elif is_variable(x):
        return unify_var(x, y, subst, depth)
    elif is_variable(y):
        return unify_var(y, x, subst, depth)
    elif isinstance(x, list) and isinstance(y, list):
        if len(x) != len(y):
            print(indent + "Lists have different lengths. Fail.")
            return None
        for xi, yi in zip(x, y):
            subst = unify(xi, yi, subst, depth + 1)
            if subst is None:
                print(indent + "Failed to unify list elements.")
                return None
        return subst
    else:
        print(indent + "Cannot unify different constants or structures. Fail.")
        return None

def unify_var(var, x, subst, depth):
    indent = "  " * depth
    if var in subst:
        print(indent + f"{var} is in subst, unify({subst[var]}, {x})")
        return unify(subst[var], x, subst, depth + 1)
    elif is_variable(x) and x in subst:
        print(indent + f"{x} is in subst, unify({var}, {subst[x]})")
        return unify(var, subst[x], subst, depth + 1)
    elif occurs_check(var, x, subst):
        print(indent + f"Occurs check failed: {var} occurs in {x}")
        return None
    else:
        print(indent + f"Add {var} -> {x} to subst")
        subst[var] = x
        return subst

# Example expressions
expr1 = ['f', 'X', ['g', 'Y']]
expr2 = ['f', 'a', ['g', 'b']]

print("Starting Unification:\n")
result = unify(expr1, expr2, subst={})
print("\nFinal Unification Result:", result)
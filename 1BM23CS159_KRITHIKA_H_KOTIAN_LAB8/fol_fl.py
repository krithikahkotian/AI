from copy import deepcopy

# Knowledge Base (KB)
KB = [
    # Rules
    {"if": ["American(p)", "Weapon(q)", "Sells(p, q, r)", "Hostile(r)"], "then": "Criminal(p)"},
    {"if": ["Missile(x)"], "then": "Weapon(x)"},
    {"if": ["Enemy(x, America)"], "then": "Hostile(x)"},
    {"if": ["Missile(x)", "Owns(A, x)"], "then": "Sells(Robert, x, A)"},

    # Facts
    {"fact": "American(Robert)"},
    {"fact": "Enemy(A, America)"},
    {"fact": "Missile(T1)"},
    {"fact": "Owns(A, T1)"}
]

goal = "Criminal(Robert)"

# -------------------------
# Utility Functions
# -------------------------

def parse_predicate(expr):
    """Parse predicate and arguments from expression string like 'Predicate(arg1, arg2)'."""
    pred, args_str = expr.split("(")
    args = args_str[:-1].split(",")
    args = [a.strip() for a in args]
    return pred.strip(), args

def is_variable(term):
    """Variables start with lowercase letter."""
    return term[0].islower()

def unify(expr1, expr2, subs=None):
    """
    Unify two predicates expr1 and expr2 with existing substitution subs.
    Returns updated subs if unifiable, else None.
    """
    if subs is None:
        subs = {}

    p1, args1 = parse_predicate(expr1)
    p2, args2 = parse_predicate(expr2)

    if p1 != p2 or len(args1) != len(args2):
        return None

    for t1, t2 in zip(args1, args2):
        if t1 == t2:
            continue
        elif is_variable(t1):
            if t1 in subs:
                if subs[t1] != t2:
                    return None  # Conflict
            else:
                subs[t1] = t2
        elif is_variable(t2):
            if t2 in subs:
                if subs[t2] != t1:
                    return None
            else:
                subs[t2] = t1
        else:
            # both constants but different
            return None

    return subs

def substitute(expr, subs):
    """Apply substitution subs to expr."""
    pred, args = parse_predicate(expr)
    new_args = []
    for a in args:
        while a in subs:
            a = subs[a]
        new_args.append(a)
    return f"{pred}({', '.join(new_args)})"


# -------------------------
# Forward Chaining Algorithm
# -------------------------

def FOL_FC_ASK(KB, query):
    known_facts = {item["fact"] for item in KB if "fact" in item}
    rules = [item for item in KB if "if" in item]

    print("Initial known facts:")
    for f in known_facts:
        print("  ", f)
    print()

    new_facts_added = True

    while new_facts_added:
        new_facts_added = False

        for rule in rules:
            premises = rule["if"]
            conclusion = rule["then"]

            # Try all possible substitutions that satisfy all premises
            # Start with empty substitutions set
            substitutions_list = [{}]

            for premise in premises:
                new_substitutions = []
                for subs in substitutions_list:
                    # For each known fact, try to unify with the premise applying current subs
                    premise_substituted = substitute(premise, subs)
                    for fact in known_facts:
                        new_subs = unify(premise_substituted, fact, deepcopy(subs))
                        if new_subs is not None:
                            new_substitutions.append(new_subs)
                substitutions_list = new_substitutions

                if not substitutions_list:
                    break  # No substitution for this premise => rule cannot fire

            # For all consistent substitutions found, infer new facts
            for subs in substitutions_list:
                inferred_fact = substitute(conclusion, subs)
                if inferred_fact not in known_facts:
                    print(f"Inferred: {inferred_fact}")
                    known_facts.add(inferred_fact)
                    new_facts_added = True

                    # Check if query is satisfied
                    if unify(inferred_fact, query) is not None:
                        print("\n Query satisfied:", query)
                        return True

    print("\n Query cannot be proved.")
    return False

# Run the algorithm
print("\n--- Forward Chaining (FOL-FC-ASK) ---\n")
FOL_FC_ASK(KB, goal)
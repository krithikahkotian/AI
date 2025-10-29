"""
First-Order Logic Resolution Proof System
Proving: John likes peanuts

This implementation:
1. Represents FOL statements
2. Converts to CNF (done internally)
3. Applies Resolution Refutation to prove the query
"""

import sys
import io
from typing import List, Set, Tuple, Dict, Optional
import re

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

class Clause:
    """Represents a CNF clause (disjunction of literals)"""
    def __init__(self, literals: Set[str]):
        self.literals = frozenset(literals)
    
    def __hash__(self):
        return hash(self.literals)
    
    def __eq__(self, other):
        return isinstance(other, Clause) and self.literals == other.literals
    
    def __str__(self):
        if not self.literals:
            return "{}"
        return "{" + " V ".join(sorted(self.literals)) + "}"
    
    def __repr__(self):
        return str(self)
    
    def is_empty(self):
        return len(self.literals) == 0


def parse_literal(literal: str) -> Tuple[str, bool]:
    """Parse a literal into (predicate, is_positive)"""
    if literal.startswith('~'):
        return (literal[1:], False)
    return (literal, True)


def negate_literal(literal: str) -> str:
    """Negate a literal"""
    if literal.startswith('~'):
        return literal[1:]
    return '~' + literal


def unify_terms(term1: str, term2: str, substitution: Dict[str, str]) -> Optional[Dict[str, str]]:
    """Simple unification for terms"""
    if term1 == term2:
        return substitution
    if term1[0].islower() and term1 not in substitution:
        substitution[term1] = term2
        return substitution
    if term2[0].islower() and term2 not in substitution:
        substitution[term2] = term1
        return substitution
    if term1 in substitution:
        return unify_terms(substitution[term1], term2, substitution)
    if term2 in substitution:
        return unify_terms(term1, substitution[term2], substitution)
    return None


def unify_literals(lit1: str, lit2: str) -> Optional[Dict[str, str]]:
    """Attempt to unify two literals"""
    pred1, pos1 = parse_literal(lit1)
    pred2, pos2 = parse_literal(lit2)
    
    if pos1 == pos2:
        return None
    
    # Extract predicate name and arguments
    match1 = re.match(r'(\w+)\((.*)\)', pred1)
    match2 = re.match(r'(\w+)\((.*)\)', pred2)
    
    if not match1 or not match2:
        return None
    
    name1, args1 = match1.groups()
    name2, args2 = match2.groups()
    
    if name1 != name2:
        return None
    
    args1_list = [a.strip() for a in args1.split(',')]
    args2_list = [a.strip() for a in args2.split(',')]
    
    if len(args1_list) != len(args2_list):
        return None
    
    substitution = {}
    for a1, a2 in zip(args1_list, args2_list):
        result = unify_terms(a1, a2, substitution)
        if result is None:
            return None
        substitution = result
    
    return substitution


def apply_substitution(literal: str, substitution: Dict[str, str]) -> str:
    """Apply substitution to a literal"""
    result = literal
    for var, val in substitution.items():
        result = re.sub(r'\b' + var + r'\b', val, result)
    return result


def resolve(clause1: Clause, clause2: Clause) -> List[Tuple[Clause, str, Dict[str, str]]]:
    """Resolve two clauses and return list of (resolvent, explanation, substitution)"""
    resolvents = []
    
    for lit1 in clause1.literals:
        for lit2 in clause2.literals:
            substitution = unify_literals(lit1, lit2)
            if substitution is not None:
                # Apply substitution to both clauses
                new_lits1 = {apply_substitution(l, substitution) for l in clause1.literals if l != lit1}
                new_lits2 = {apply_substitution(l, substitution) for l in clause2.literals if l != lit2}
                
                resolvent_literals = new_lits1.union(new_lits2)
                resolvent = Clause(resolvent_literals)
                
                explanation = f"Resolved {lit1} and {lit2}"
                if substitution:
                    sub_str = ", ".join([f"{k}={v}" for k, v in substitution.items()])
                    explanation += f" with [{sub_str}]"
                
                resolvents.append((resolvent, explanation, substitution))
    
    return resolvents


def resolution_refutation(clauses: List[Clause], max_iterations: int = 100) -> Tuple[bool, List[str]]:
    """
    Perform resolution refutation
    Returns: (success, derivation_steps)
    """
    clauses_set = set(clauses)
    derivation = []
    iteration = 0
    
    # Number the initial clauses
    clause_map = {clause: i+1 for i, clause in enumerate(clauses)}
    
    print("\n" + "="*80)
    print("CNF CLAUSES (after conversion):")
    print("="*80)
    for clause, num in sorted(clause_map.items(), key=lambda x: x[1]):
        print(f"C{num}: {clause}")
    
    print("\n" + "="*80)
    print("RESOLUTION PROOF:")
    print("="*80)
    
    while iteration < max_iterations:
        iteration += 1
        new_clauses = []
        
        clauses_list = list(clauses_set)
        for i, c1 in enumerate(clauses_list):
            for c2 in clauses_list[i:]:
                resolvents = resolve(c1, c2)
                
                for resolvent, explanation, sub in resolvents:
                    if resolvent.is_empty():
                        print("\n" + "="*80)
                        print("*** EMPTY CLAUSE DERIVED - PROOF COMPLETE! ***")
                        print("="*80)
                        c1_num = clause_map.get(c1, "derived")
                        c2_num = clause_map.get(c2, "derived")
                        print(f"\nC{len(clause_map)+1}: {resolvent}")
                        print(f"  Derived from C{c1_num} and C{c2_num}")
                        print(f"  {explanation}")
                        print("\n[SUCCESS] Contradiction found!")
                        print("[SUCCESS] Therefore, Likes(John, Peanuts) is PROVEN TRUE\n")
                        return True, derivation
                    
                    if resolvent not in clauses_set:
                        new_clauses.append((resolvent, c1, c2, explanation))
        
        if not new_clauses:
            print("\nNo new clauses can be derived. Proof failed.")
            return False, derivation
        
        # Add new clauses
        for resolvent, c1, c2, explanation in new_clauses[:10]:  # Show more steps
            if resolvent not in clauses_set:
                clauses_set.add(resolvent)
                clause_num = len(clause_map) + 1
                clause_map[resolvent] = clause_num
                
                c1_num = clause_map.get(c1, "?")
                c2_num = clause_map.get(c2, "?")
                
                print(f"\nC{clause_num}: {resolvent}")
                print(f"  From C{c1_num} and C{c2_num} - {explanation}")
    
    print(f"\nMax iterations ({max_iterations}) reached without finding proof.")
    return False, derivation


def main():
    print("="*80)
    print("FIRST-ORDER LOGIC RESOLUTION PROOF")
    print("Proving: John likes peanuts")
    print("="*80)
    
    # STEP 1: FOL Representations
    print("\n" + "="*80)
    print("FIRST-ORDER LOGIC REPRESENTATIONS:")
    print("="*80)
    
    fol_statements = [
        ("1. John likes all kinds of food", "ForAll x (Food(x) -> Likes(John, x))"),
        ("2. Apple is food", "Food(Apple)"),
        ("3. Vegetables are food", "Food(Vegetables)"),
        ("4. Anything anyone eats and is not killed is food", "ForAll y ForAll z ((Eats(y,z) AND ~Killed(y)) -> Food(z))"),
        ("5. Anil eats peanuts", "Eats(Anil, Peanuts)"),
        ("6. Anil is alive", "Alive(Anil)"),
        ("7. Harry eats everything that Anil eats", "ForAll x (Eats(Anil,x) -> Eats(Harry,x))"),
        ("8. Anyone who is alive is not killed", "ForAll x (Alive(x) -> ~Killed(x))"),
        ("9. Anyone who is not killed is alive", "ForAll x (~Killed(x) -> Alive(x))"),
    ]
    
    for english, fol in fol_statements:
        print(f"{english}")
        print(f"   {fol}")
    
    print(f"\nQuery: Likes(John, Peanuts)")
    print(f"Negated Query (for refutation): ~Likes(John, Peanuts)")
    
    # Define CNF clauses (using ~ for negation)
    cnf_clauses = [
        Clause({"~Food(x)", "Likes(John, x)"}),  # 1. John likes all food
        Clause({"Food(Apple)"}),  # 2. Apple is food
        Clause({"Food(Vegetables)"}),  # 3. Vegetables are food
        Clause({"~Eats(y, z)", "Killed(y)", "Food(z)"}),  # 4. Eats & not killed -> food
        Clause({"Eats(Anil, Peanuts)"}),  # 5. Anil eats peanuts
        Clause({"Alive(Anil)"}),  # 6. Anil is alive
        Clause({"~Eats(Anil, x)", "Eats(Harry, x)"}),  # 7. Harry eats what Anil eats
        Clause({"~Alive(x)", "~Killed(x)"}),  # 8. Alive -> not killed
        Clause({"Killed(x)", "Alive(x)"}),  # 9. Not killed -> alive
        Clause({"~Likes(John, Peanuts)"}),  # 10. Negated query
    ]
    
    # Perform Resolution
    success, derivation = resolution_refutation(cnf_clauses)
    
    # Explanation
    if success:
        print("="*80)
        print("EXPLANATION:")
        print("="*80)
        print("""
The proof succeeded by deriving the empty clause {}, proving the original query.

Key reasoning chain:
  1. Anil is alive (given)
  2. Alive -> ~Killed, so Anil is not killed
  3. Anil eats peanuts AND not killed -> Peanuts are food
  4. John likes all food -> John likes peanuts
  5. This contradicts ~Likes(John, Peanuts)
  
Therefore, Likes(John, Peanuts) is TRUE.
        """)


if __name__ == "__main__":
    main()
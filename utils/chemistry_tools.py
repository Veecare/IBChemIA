from chempy import chemistry
from chempy.util.parsing import formula_to_composition
from collections import defaultdict
import re

def balance_chemical_equation(unbalanced_equation_str):
    """
    Balances a chemical equation string using the chempy library.

    The input string should represent an unbalanced chemical equation,
    with reactants and products separated by '->', and individual
    species on each side separated by '+'.
    Example: "H2 + O2 -> H2O"

    Args:
        unbalanced_equation_str (str): A string representing the unbalanced
                                       chemical equation.
                                       Example: "Fe(NO3)3 + NaOH -> Fe(OH)3 + NaNO3"

    Returns:
        str: A string representing the balanced chemical equation
             (e.g., "2H2 + O2 -> 2H2O"), or an error message if balancing fails
             or the input is invalid.
             Example for "Fe(NO3)3 + NaOH -> Fe(OH)3 + NaNO3":
             "Fe(NO3)3 + 3NaOH -> Fe(OH)3 + 3NaNO3"
    """
    try:
        # Preliminary input validation
        if not isinstance(unbalanced_equation_str, str):
            return "Error: Input must be a string."
        if "->" not in unbalanced_equation_str:
            return "Error: Equation must contain '->' separating reactants and products."

        # Split into reactant and product sides
        reactants_str, products_str = unbalanced_equation_str.split('->')

        # Parse reactant and product formulas from their respective strings
        # Formulas are stripped of whitespace and empty strings are filtered out.
        reactant_formulas = [r.strip() for r in reactants_str.split('+') if r.strip()]
        product_formulas = [p.strip() for p in products_str.split('+') if p.strip()]

        # Check if reactant or product lists are empty after parsing
        if not reactant_formulas:
            return "Error: No reactants found. Check the left side of '->'."
        if not product_formulas:
            return "Error: No products found. Check the right side of '->'."

        # Chempy's balance_stoichiometry can take sets of formula strings directly.
        # It handles parsing of these formulas into chemical compositions internally.
        # This also helps in catching errors related to invalid chemical formulas early on.
        # Example: If a formula like "H(O" is passed, chempy will raise an error.
        try:
            # The core balancing step using chempy
            # It returns two dictionaries: one for reactants and one for products,
            # where keys are the substance formulas and values are their stoichiometric coefficients.
            balanced_reactants_coeffs, balanced_products_coeffs = chemistry.balance_stoichiometry(
                set(reactant_formulas), set(product_formulas)
            )
        except Exception as chempy_parse_balance_error:
            # Catch errors from chempy's parsing or balancing logic
            # This could be due to invalid formula syntax, non-existent elements, or unbalanceable equations.
            return f"Error during chempy processing: {chempy_parse_balance_error}. Check formula syntax and element validity."
        
        # Format the balanced equation into a human-readable string
        # Coefficients of 1 are typically omitted in chemical equations.
        
        lhs_terms = []
        for formula, coeff in balanced_reactants_coeffs.items():
            coeff_str = str(int(coeff)) if coeff == int(coeff) and coeff != 1 else ""
            if coeff == 1:
                lhs_terms.append(formula)
            else:
                lhs_terms.append(f"{coeff_str}{formula}")
        
        rhs_terms = []
        for formula, coeff in balanced_products_coeffs.items():
            coeff_str = str(int(coeff)) if coeff == int(coeff) and coeff != 1 else ""
            if coeff == 1:
                rhs_terms.append(formula)
            else:
                rhs_terms.append(f"{coeff_str}{formula}")
        
        # Sort terms alphabetically for consistent output order, though chempy often returns them sorted.
        lhs_terms.sort()
        rhs_terms.sort()

        # Join terms with ' + ' and combine with ' -> '
        return f"{' + '.join(lhs_terms)} -> {' + '.join(rhs_terms)}"

    except ValueError as ve:
        # Specifically catch ValueError from chempy if balancing is impossible
        # (e.g., element mismatch where an element appears on one side but not the other).
        return f"Error balancing equation (ValueError): {ve}. Ensure all elements are present on both sides."
    except Exception as e:
        # General catch-all for any other unexpected errors during the process.
        return f"An unexpected error occurred: {e}. Please check your input format (e.g., H2 + O2 -> H2O)."

if __name__ == '__main__':
    # This block serves as a basic inline testing and usage demonstration area.
    # It is executed when the script is run directly (e.g., `python utils/chemistry_tools.py`).
    # Test cases
    equations = [
        "H2 + O2 -> H2O",
        "Fe + Cl2 -> FeCl3",
        "C3H8 + O2 -> CO2 + H2O",
        "KMnO4 + HCl -> KCl + MnCl2 + H2O + Cl2",
        "NH3 + O2 -> NO + H2O",
        "AgNO3 + NaCl -> AgCl + NaNO3", # Already balanced
        "CH4 + O2 -> CO2 + H2O",
        # Invalid cases
        "H2 + O2", # Missing arrow
        "H2 + O2 -> ", # Missing products
        " -> H2O", # Missing reactants
        "H(O -> H2O", # Invalid formula
        "H2 + O2 -> H2O + O3", # Element present in products but not reactants (if O3 not balanced from O2)
                                # Actually, this can be balanced.
        "XyZ + A -> B" # Non-existent elements (chempy should handle this)
    ]
    for eq in equations:
        print(f"Unbalanced: {eq}")
        balanced_eq = balance_chemical_equation(eq)
        print(f"Balanced:   {balanced_eq}\n")

    # Example from problem description
    # print(balance_chemical_equation("Fe(NO3)3 + NaOH -> Fe(OH)3 + NaNO3"))
    # Expected: Fe(NO3)3 + 3NaOH -> Fe(OH)3 + 3NaNO3
    print(f"Unbalanced: Fe(NO3)3 + NaOH -> Fe(OH)3 + NaNO3")
    print(f"Balanced: {balance_chemical_equation('Fe(NO3)3 + NaOH -> Fe(OH)3 + NaNO3')}\n")

    # Example with parentheses and numbers
    # print(balance_chemical_equation("Ca(OH)2 + H3PO4 -> Ca3(PO4)2 + H2O"))
    # Expected: 3Ca(OH)2 + 2H3PO4 -> Ca3(PO4)2 + 6H2O
    print(f"Unbalanced: Ca(OH)2 + H3PO4 -> Ca3(PO4)2 + H2O")
    print(f"Balanced: {balance_chemical_equation('Ca(OH)2 + H3PO4 -> Ca3(PO4)2 + H2O')}\n")

    print(f"Unbalanced: C6H12O6 + O2 -> CO2 + H2O") # Glucose combustion
    print(f"Balanced: {balance_chemical_equation('C6H12O6 + O2 -> CO2 + H2O')}\n")
    # Expected: C6H12O6 + 6O2 -> 6CO2 + 6H2O

    print(f"Unbalanced: Na2CO3 + HCl -> NaCl + H2O + CO2") # Sodium carbonate and HCl
    print(f"Balanced: {balance_chemical_equation('Na2CO3 + HCl -> NaCl + H2O + CO2')}\n")
    # Expected: Na2CO3 + 2HCl -> 2NaCl + H2O + CO2
    
    print(f"Unbalanced: P4 + O2 -> P2O5")
    print(f"Balanced: {balance_chemical_equation('P4 + O2 -> P2O5')}\n")
    # Expected: P4 + 5O2 -> 2P2O5 or P4 + 5O2 -> P4O10 (if P2O5 is empirical)
    # chempy gives P4 + 5O2 -> 2P2O5
    
    print(f"Unbalanced: H2O2 -> H2O + O2") # Decomposition of hydrogen peroxide
    print(f"Balanced: {balance_chemical_equation('H2O2 -> H2O + O2')}\n")
    # Expected: 2H2O2 -> 2H2O + O2

    # Test from a user: Cu + HNO3 -> Cu(NO3)2 + NO2 + H2O
    print(f"Unbalanced: Cu + HNO3 -> Cu(NO3)2 + NO2 + H2O")
    print(f"Balanced: {balance_chemical_equation('Cu + HNO3 -> Cu(NO3)2 + NO2 + H2O')}\n")
    # Expected: Cu + 4HNO3 -> Cu(NO3)2 + 2NO2 + 2H2O
    
    # Test fractional (should become integers)
    # C2H6 + O2 -> CO2 + H2O  (Balanced: 2C2H6 + 7O2 -> 4CO2 + 6H2O)
    print(f"Unbalanced: C2H6 + O2 -> CO2 + H2O")
    print(f"Balanced: {balance_chemical_equation('C2H6 + O2 -> CO2 + H2O')}\n")

    # Test for elements that might not be parsable by formula_to_composition if not used carefully
    # e.g. if we tried to parse "e-" for redox, that would fail formula_to_composition
    # but balance_stoichiometry can handle species like "e-" if passed as string set.
    # For this tool, we assume standard chemical formulas.
    # print(balance_chemical_equation("Zn + H+ -> Zn+2 + H2")) # Redox half-reaction style
    # This would require parsing charges, which is beyond simple formula_to_composition
    # chempy's balance_stoichiometry CAN handle this with charge conservation if species are defined
    # correctly (e.g. using Substance class or specific string representations like H{+}).
    # For now, the current implementation is focused on molecular equations.
    
    # Test with leading/trailing spaces
    print(f"Unbalanced:  H2 + O2 -> H2O  ")
    print(f"Balanced: {balance_chemical_equation(' H2 + O2 -> H2O  ')}\n")
    
    print(f"Unbalanced: H2+O2->H2O") # No spaces
    print(f"Balanced: {balance_chemical_equation('H2+O2->H2O')}\n")

    print(f"Unbalanced:  Al + HCl  ->  AlCl3  + H2 ")
    print(f"Balanced: {balance_chemical_equation(' Al + HCl  ->  AlCl3  + H2 ')}\n")
    # Expected: 2Al + 6HCl -> 2AlCl3 + 3H2

    # Test with (aq), (s), (g), (l) states - these should be stripped or handled if chempy supports.
    # chempy's formula parsing usually ignores these.
    print(f"Unbalanced: NaOH(aq) + HCl(aq) -> NaCl(aq) + H2O(l)")
    print(f"Balanced: {balance_chemical_equation('NaOH(aq) + HCl(aq) -> NaCl(aq) + H2O(l)')}\n")
    # Expected: NaOH(aq) + HCl(aq) -> NaCl(aq) + H2O(l) (coefficients are 1)

    # Test for "Error: Element 'Foo' does not exist"
    print(f"Unbalanced: Foo + Bar -> Baz")
    print(f"Balanced: {balance_chemical_equation('Foo + Bar -> Baz')}\n")
    
    # Test for "ValueError: Could not balance equation for element X"
    # This happens if an element is in reactants but not products or vice versa.
    print(f"Unbalanced: H2 + Cl2 -> NaCl") # Na missing from reactants
    print(f"Balanced: {balance_chemical_equation('H2 + Cl2 -> NaCl')}\n")

    print(f"Unbalanced: C + O2 -> CO") # C + O2 -> 2CO
    print(f"Balanced: {balance_chemical_equation('C + O2 -> CO')}\n")

    print(f"Unbalanced: C + O2 -> CO") # C + O2 -> 2CO
    print(f"Balanced: {balance_chemical_equation(' C + O2 -> CO ')}\n")
Okay, I've created `utils/chemistry_tools.py` with the `balance_chemical_equation` function using `chempy`. I've included some basic parsing, error handling, and test cases within the `if __name__ == '__main__':` block.

The function attempts to:
1.  Validate the basic "->" structure.
2.  Split reactants and products.
3.  Use `chempy.chemistry.balance_stoichiometry` with sets of reactant and product formula strings. `chempy` handles parsing these formulas internally.
4.  Format the balanced coefficients and formulas back into a string.
5.  Catch potential errors during parsing (though `balance_stoichiometry` handles most formula parsing internally) and balancing.

Next, I'll update `requirements.txt` to include `chempy`.

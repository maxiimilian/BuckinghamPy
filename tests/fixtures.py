"""Take examples and generate them using v1 as fixtures.
Make sure that refactored version still yields the same results as the original version."""

from typing import List, Dict, Type

import joblib
import sympy as sp


def gen_pressure_drop(bp) -> List[List[sp.Expr]]:
    bp.add_variable(name="{\\Delta}p", dimensions="M*L^(-1)*T^(-2)")  # pressure drop
    bp.add_variable(name="R", dimensions="L")  # length of the pipe
    bp.add_variable(name="d", dimensions="L")  # diameter of the pipe
    bp.add_variable(name="\\mu", dimensions="M*L^(-1)*T^(-1)")  # viscosity
    bp.add_variable(name="Q", dimensions="L^(3)*T^(-1)")  # volumetic flow rate

    bp.generate_pi_terms()
    return bp.pi_terms


def gen_virus_infection(bp) -> List[List[sp.Expr]]:
    bp.add_variable(
        name="V_{p}", dimensions="L*T^(-1)", non_repeating=True
    )  # virus spread rate
    bp.add_variable(name="P_{r}", dimensions="L")  # precipitation
    bp.add_variable(name="{\\theta}", dimensions="C")  # temperature
    bp.add_variable(name="C_{a}", dimensions="L^(3)/T")  # airflow
    bp.add_variable(name="C_{e}", dimensions="T")  # seasonal changes
    bp.add_variable(name="E_{fs}", dimensions="L^(-2)")  # social structures
    bp.add_variable(name="H", dimensions="M*L^(-3)")  # humidity

    bp.generate_pi_terms()
    return bp.pi_terms


def gen_economic_growth(bp) -> List[List[sp.Expr]]:
    bp.add_variable(name="P", dimensions="K", non_repeating=True)  # capital
    bp.add_variable(name="L", dimensions="Q/T")  # labor per period of time
    bp.add_variable(name="{\\omega_{L}}", dimensions="K/Q")  # wages per labor
    bp.add_variable(name="Y", dimensions="K/T")  # profit per period of time
    bp.add_variable(name="r", dimensions="1/T")  # rental rate period of time
    bp.add_variable(name="{\\delta}", dimensions="1/T")  # depreciation rate

    bp.generate_pi_terms()
    return bp.pi_terms


def gen_bubble_pressure(bp) -> List[List[sp.Expr]]:
    bp.add_variable(name="{\\Delta}p", dimensions="F*L^(-2)")  # pressure
    bp.add_variable(name="R", dimensions="L")  # diameter
    bp.add_variable(name="\\sigma", dimensions="F*L^(-1)")  # surface tension

    bp.generate_pi_terms()
    return bp.pi_terms


def gen_all(bp_class: Type, **kwargs) -> Dict[str, List[List[sp.Expr]]]:
    return {
        "pressure_drop": gen_pressure_drop(bp_class(**kwargs)),
        "virus_infection": gen_virus_infection(bp_class(**kwargs)),
        "economic_growth": gen_economic_growth(bp_class(**kwargs)),
        "bubble_pressure": gen_bubble_pressure(bp_class(**kwargs)),
    }


if __name__ == "__main__":
    # Generate using v1 code
    from buckinghampy.v1 import BuckinghamPi

    all_fixtures = gen_all(BuckinghamPi)
    for key, value in all_fixtures.items():
        joblib.dump(value, f"fixtures/{key}.joblib")
        print(f"Generated {key} fixtures")

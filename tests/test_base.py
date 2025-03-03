"""Test functionality of modified BuckinghamPi class"""

import pathlib
from typing import Dict, List

import joblib
import pytest
import sympy as sp

import tests.fixtures as fixtures

FIXTURE_PATH = pathlib.Path(__file__).parent / "fixtures"


@pytest.fixture
def v1_sets() -> Dict[str, List[List[sp.Expr]]]:
    fix_files = sorted(FIXTURE_PATH.glob("*.joblib"))
    return {f.stem: joblib.load(f) for f in fix_files}


def test_parsing():
    """Test exceptions for expression parsing when new variable is added"""
    from buckinghampy import BuckinghamPi

    bp = BuckinghamPi()

    # Shouldn't raise any exceptions
    bp.add_variable("x", "L")

    # Only multiplications, powers, and symbols are allowed
    with pytest.raises(Exception) as e:
        bp.add_variable("x", "L + 1")
    assert "not of the accepted types" in e.value.args[0]

    # No factors
    with pytest.raises(Exception) as e:
        bp.add_variable("x", "5 * L")
    assert "cannot have coefficients" in e.value.args[0]

    # No fractional exponents
    with pytest.raises(ValueError) as e:
        bp.add_variable("x", "L ** (1/2)")
    assert "non-integer exponent" in e.value.args[0]

    with pytest.raises(ValueError) as e:
        bp.add_variable("x", "L ** 0.5")
    assert "non-integer exponent" in e.value.args[0]


def is_set_equal(set1: List[sp.Expr], set2: List[sp.Expr]) -> bool:
    """Check if two sets of expressions are equal"""
    return all(sp.simplify(expr1 - expr2) == 0 for expr1, expr2 in zip(set1, set2))


def is_set_list_equal(list1: List[List[sp.Expr]], list2: List[List[sp.Expr]]) -> bool:
    """Check if two lists of sets of expressions are equal"""
    return all(is_set_equal(set1, set2) for set1, set2 in zip(list1, list2))


def test_is_equal(v1_sets: Dict[str, List[List[sp.Expr]]]):
    """Test is equal functions before relying on them"""
    for key, set_list in v1_sets.items():
        assert is_set_list_equal(set_list, set_list)


def test_with_fixture(v1_sets: Dict[str, List[List[sp.Expr]]]):
    from buckinghampy import BuckinghamPi  # this is v2

    # Test also serial and parallel processing
    for n_jobs in [1, 2]:
        v2_sets = fixtures.gen_all(BuckinghamPi, n_jobs=n_jobs)
        for key, set_list in v2_sets.items():
            # Check that sets are of same length
            assert len(set_list) == len(v1_sets[key])

            # Check that sets are the same
            assert is_set_list_equal(set_list, v1_sets[key])

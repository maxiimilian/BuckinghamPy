"""Test base functionality"""
import pytest
from buckinghampy import BuckinghamPi

def test_parsing():
    """Test exceptions for expression parsing when new variable is added"""
    bp = BuckinghamPi()

    # Shouldn't raise any exceptions
    bp.add_variable('x', 'L')

    # Only multiplications, powers, and symbols are allowed
    with pytest.raises(Exception) as e:
        bp.add_variable('x', 'L + 1')
    assert "not of the accepted types" in e.value.args[0]

    # No factors
    with pytest.raises(Exception) as e:
        bp.add_variable('x', '5 * L')
    assert "cannot have coefficients" in e.value.args[0]

    # No fractional exponents
    with pytest.raises(ValueError) as e:
        bp.add_variable('x', 'L ** (1/2)')
    assert "non-integer exponent" in e.value.args[0]

    with pytest.raises(ValueError) as e:
        bp.add_variable('x', 'L ** 0.5')
    assert "non-integer exponent" in e.value.args[0]


def test_basic_set
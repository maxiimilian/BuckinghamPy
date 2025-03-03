import pathlib
import time
from typing import List, Tuple, Type

import numpy.testing as npt
import sympy as sp

# Long set with many variables
long_set: List[Tuple[str, str]] = [
    ("a", "m"),
    ("b", "1/s"),
    ("c", "1/s"),
    ("d", "K/m"),
    ("e", "m^2/s^2"),
    ("f", "m * K / s"),
    ("g", "K"),
    ("h", "m/s"),
    ("v", "m/s"),
    ("u_var", "m^2/s^2"),
]


def get_bp_instance(bp_class: Type, **kwargs):
    bp = bp_class(**kwargs)
    for var, unit in long_set:
        bp.add_variable(var, unit)
    return bp


def dump_pi_list(pi_list: List[List[sp.Expr]]) -> str:
    """Dump pi_list to a list of strings"""
    pi_list_str = []
    for pi_set in pi_list:
        pi_list_str.append("; ".join(str(pi) for pi in pi_set))
    return "\n".join(pi_list_str)


def test_v1_speed():
    from buckinghampy.v1 import BuckinghamPi

    bp: BuckinghamPi = get_bp_instance(BuckinghamPi)
    t_start = time.time()
    bp.generate_pi_terms()
    print(len(bp.pi_terms))
    t_end = time.time()
    print(f"v1: {t_end - t_start:.2f} s")


def test_v2_speed():
    from buckinghampy import BuckinghamPi

    # Don't use multi-processing
    bp: BuckinghamPi = get_bp_instance(BuckinghamPi, n_jobs=1)
    t_start = time.time()
    bp.generate_pi_terms()
    print(len(bp.pi_terms))
    t_end = time.time()
    print(f"v2: {t_end - t_start:.2f} s")


def test_v1_v2_equivalence():
    from buckinghampy.v1 import BuckinghamPi as BuckinghamPiV1
    from buckinghampy import BuckinghamPi as BuckinghamPiV2

    from tests.test_base import is_set_list_equal

    bp_v1: BuckinghamPiV1 = get_bp_instance(BuckinghamPiV1)
    bp_v1.generate_pi_terms()
    bp_v1_set = bp_v1.pi_terms

    bp_v2: BuckinghamPiV2 = get_bp_instance(BuckinghamPiV2, n_jobs=8)
    bp_v2.generate_pi_terms()
    bp_v2_set = bp_v2.pi_terms

    ## Compare internals
    npt.assert_array_equal(bp_v1.M, bp_v2.M)

    # Dump for debugging
    pathlib.Path("dump_v1.txt").write_text(dump_pi_list(bp_v1_set))
    pathlib.Path("dump_v2.txt").write_text(dump_pi_list(bp_v2_set))

    assert len(bp_v1_set) == len(bp_v2_set)
    assert is_set_list_equal(bp_v1_set, bp_v2_set)

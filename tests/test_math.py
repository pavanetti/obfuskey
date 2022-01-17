import random
import pytest

from unittest import mock

from obfuskey._math import (
    factor,
    is_prime,
    next_prime,
    strong_pseudoprime,
    trial_division,
)
from obfuskey.exceptions import MaximumValueError


class TestMath:
    def test_factor(self) -> None:
        n = random.randint(0, 1000000)
        s, d = factor(n)

        assert n - 1 == 2 ** s * d

    @pytest.mark.parametrize("n,expected", [(2, True), (25, False), (433494437, True)])
    def test_is_prime(self, n: int, expected: bool) -> None:
        assert is_prime(n) == expected

    @pytest.mark.parametrize(
        "n,expected", [(1, 2), (2, 3), (42, 43), (433494437, 433494449)]
    )
    def test_next_prime(self, n: int, expected: bool) -> None:
        assert next_prime(n) == expected

    def test_next_prime_under_512_bit(self) -> None:
        next_prime(int("9" * 154))

    def test_next_prime_over_512_bit(self) -> None:
        with pytest.raises(MaximumValueError):
            next_prime(int("9" * 155))

    def test_next_prime_gmpy2(self) -> None:
        import sys

        if "gmpy2" in sys.modules:
            del sys.modules["gmpy2"]

        gmpy2_mock = mock.MagicMock()
        sys.modules["gmpy2"] = gmpy2_mock

        next_prime(int("9" * 155))

    @pytest.mark.parametrize("n,expected", [(433494436, False), (433494437, True)])
    def test_strong_pseudoprime(self, n: int, expected: bool) -> None:
        assert strong_pseudoprime(n) == expected

    @pytest.mark.parametrize(
        "n,expected", [(2, True), (9, False), (15, False), (17, True)]
    )
    def test_trial_division(self, n: int, expected: bool) -> None:
        assert trial_division(n) == expected

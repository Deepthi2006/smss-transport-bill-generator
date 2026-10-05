from decimal import Decimal

from app.utils.amount_words import amount_to_words


def test_zero():
    assert amount_to_words(0) == "ZERO ONLY"


def test_single_digit():
    assert amount_to_words(1) == "ONE ONLY"


def test_ten():
    assert amount_to_words(10) == "TEN ONLY"


def test_hundred():
    assert amount_to_words(100) == "ONE HUNDRED ONLY"


def test_nine_hundred_ninety_nine():
    assert amount_to_words(999) == (
        "NINE HUNDRED NINETY NINE ONLY"
    )


def test_thousand():
    assert amount_to_words(1000) == "ONE THOUSAND ONLY"


def test_fifteen_thousand():
    assert amount_to_words(15000) == (
        "FIFTEEN THOUSAND ONLY"
    )


def test_actual_bill_amount():
    assert amount_to_words(Decimal("159405.25")) == (
        "ONE LAKH FIFTY NINE THOUSAND FOUR HUNDRED FIVE ONLY"
    )


def test_one_lakh():
    assert amount_to_words(100000) == "ONE LAKH ONLY"


def test_ten_lakh():
    assert amount_to_words(1000000) == "TEN LAKH ONLY"


def test_crore():
    assert amount_to_words(12500000) == (
        "ONE CRORE TWENTY FIVE LAKH ONLY"
    )


def test_rounding_down():
    assert amount_to_words(Decimal("159405.25")) == (
        "ONE LAKH FIFTY NINE THOUSAND FOUR HUNDRED FIVE ONLY"
    )


def test_rounding_up():
    assert amount_to_words(Decimal("159405.50")) == (
        "ONE LAKH FIFTY NINE THOUSAND FOUR HUNDRED SIX ONLY"
    )


def test_string_amount():
    assert amount_to_words("159405.25") == (
        "ONE LAKH FIFTY NINE THOUSAND FOUR HUNDRED FIVE ONLY"
    )


def test_negative_amount_rejected():
    try:
        amount_to_words(-100)
        assert False, "Negative amount should raise ValueError"
    except ValueError:
        pass
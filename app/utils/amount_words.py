from __future__ import annotations

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


ONES = [
    "ZERO",
    "ONE",
    "TWO",
    "THREE",
    "FOUR",
    "FIVE",
    "SIX",
    "SEVEN",
    "EIGHT",
    "NINE",
    "TEN",
    "ELEVEN",
    "TWELVE",
    "THIRTEEN",
    "FOURTEEN",
    "FIFTEEN",
    "SIXTEEN",
    "SEVENTEEN",
    "EIGHTEEN",
    "NINETEEN",
]

TENS = [
    "",
    "",
    "TWENTY",
    "THIRTY",
    "FORTY",
    "FIFTY",
    "SIXTY",
    "SEVENTY",
    "EIGHTY",
    "NINETY",
]


def convert_under_hundred(number: int) -> str:
    """Convert a number from 0 to 99 into words."""
    if number < 20:
        return ONES[number]

    tens = number // 10
    remainder = number % 10

    if remainder == 0:
        return TENS[tens]

    return f"{TENS[tens]} {ONES[remainder]}"


def convert_under_thousand(number: int) -> str:
    """Convert a number from 0 to 999 into words."""
    if number < 100:
        return convert_under_hundred(number)

    hundreds = number // 100
    remainder = number % 100

    if remainder == 0:
        return f"{ONES[hundreds]} HUNDRED"

    return f"{ONES[hundreds]} HUNDRED {convert_under_hundred(remainder)}"


def convert_indian_number(number: int) -> str:
    """
    Convert an integer into words using the Indian numbering system.

    Example:
        159405 ->
        ONE LAKH FIFTY NINE THOUSAND FOUR HUNDRED FIVE
    """
    if number == 0:
        return "ZERO"

    parts = []

    crore = number // 10_000_000
    number %= 10_000_000

    lakh = number // 100_000
    number %= 100_000

    thousand = number // 1_000
    number %= 1_000

    remainder = number

    if crore:
        parts.append(f"{convert_under_thousand(crore)} CRORE")

    if lakh:
        parts.append(f"{convert_under_thousand(lakh)} LAKH")

    if thousand:
        parts.append(f"{convert_under_thousand(thousand)} THOUSAND")

    if remainder:
        parts.append(convert_under_thousand(remainder))

    return " ".join(parts)


def amount_to_words(amount: int | float | str | Decimal) -> str:
    """
    Convert a monetary amount into Indian English words.

    The amount is rounded to the nearest rupee using ROUND_HALF_UP.
    Paise are not included in the final words.

    Example:
        159405.25
        -> ONE LAKH FIFTY NINE THOUSAND FOUR HUNDRED FIVE ONLY
    """
    try:
        decimal_amount = Decimal(str(amount))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise ValueError(f"Invalid amount: {amount}") from exc

    if decimal_amount < 0:
        raise ValueError("Amount cannot be negative.")

    rounded_amount = decimal_amount.quantize(
        Decimal("1"),
        rounding=ROUND_HALF_UP,
    )

    integer_amount = int(rounded_amount)

    words = convert_indian_number(integer_amount)

    return f"{words} ONLY"
from __future__ import annotations

from decimal import Decimal
from typing import Any


class BillValidator:
    """
    Validates the final BillData object before PDF generation.

    Validation covers:

    1. Bill structure
    2. Required bill information
    3. Bill rows
    4. Duplicate S.NO values
    5. Numeric values
    6. Quantity total
    7. Freight total
    """

    def __init__(self, bill):
        self.bill = bill

        self.errors: list[str] = []
        self.warnings: list[str] = []

    # ============================================================
    # STRUCTURE VALIDATION
    # ============================================================

    def validate_structure(self):
        """
        Validate the overall BillData structure.
        """

        # --------------------------------------------------------
        # Bill number
        # --------------------------------------------------------

        if not getattr(self.bill, "bill_no", None):
            self.errors.append(
                "Bill number is missing."
            )

        # --------------------------------------------------------
        # Bill date
        # --------------------------------------------------------

        if not getattr(self.bill, "bill_date", None):
            self.errors.append(
                "Bill date is missing."
            )

        # --------------------------------------------------------
        # Customer name
        # --------------------------------------------------------

        if not getattr(self.bill, "customer_name", None):
            self.errors.append(
                "Customer name is missing."
            )

        # --------------------------------------------------------
        # Rows
        # --------------------------------------------------------

        rows = getattr(
            self.bill,
            "rows",
            None,
        )

        if not rows:
            self.errors.append(
                "No bill rows were found."
            )

        # --------------------------------------------------------
        # Total quantity
        # --------------------------------------------------------

        if not hasattr(
            self.bill,
            "total_quantity",
        ):
            self.errors.append(
                "Total quantity is missing."
            )

        # --------------------------------------------------------
        # Total freight
        # --------------------------------------------------------

        if not hasattr(
            self.bill,
            "total_freight",
        ):
            self.errors.append(
                "Total freight is missing."
            )

    # ============================================================
    # BILL INFORMATION VALIDATION
    # ============================================================

    def validate_bill_information(self):
        """
        Validate bill-level information.
        """

        bill_no = getattr(
            self.bill,
            "bill_no",
            "",
        )

        bill_date = getattr(
            self.bill,
            "bill_date",
            "",
        )

        customer_name = getattr(
            self.bill,
            "customer_name",
            "",
        )

        if not str(bill_no).strip():
            self.errors.append(
                "Bill number cannot be empty."
            )

        if not str(bill_date).strip():
            self.errors.append(
                "Bill date cannot be empty."
            )

        if not str(customer_name).strip():
            self.errors.append(
                "Customer name cannot be empty."
            )

    # ============================================================
    # ROW VALIDATION
    # ============================================================

    def validate_rows(self):
        """
        Validate every bill row.
        """

        rows = getattr(
            self.bill,
            "rows",
            [],
        )

        seen_sno = set()

        for index, row in enumerate(
            rows,
            start=1,
        ):

            # ----------------------------------------------------
            # S.NO
            # ----------------------------------------------------

            sno = getattr(
                row,
                "sno",
                None,
            )

            if sno is None:
                self.errors.append(
                    f"Row {index}: S.NO is missing."
                )

            else:

                if sno in seen_sno:
                    self.errors.append(
                        f"Duplicate S.NO found: {sno}."
                    )

                seen_sno.add(sno)

            # ----------------------------------------------------
            # From
            # ----------------------------------------------------

            from_location = getattr(
                row,
                "from_location",
                "",
            )

            if not str(
                from_location
            ).strip():

                self.errors.append(
                    f"Row {index}: From location is missing."
                )

            # ----------------------------------------------------
            # To
            # ----------------------------------------------------

            to_location = getattr(
                row,
                "to_location",
                "",
            )

            if not str(
                to_location
            ).strip():

                self.errors.append(
                    f"Row {index}: To location is missing."
                )

            # ----------------------------------------------------
            # Invoice number
            # ----------------------------------------------------

            invoice_no = getattr(
                row,
                "invoice_no",
                "",
            )

            if not str(
                invoice_no
            ).strip():

                self.errors.append(
                    f"Row {index}: Invoice number is missing."
                )

            # ----------------------------------------------------
            # Invoice date
            # ----------------------------------------------------

            invoice_date = getattr(
                row,
                "invoice_date",
                "",
            )

            if not str(
                invoice_date
            ).strip():

                self.errors.append(
                    f"Row {index}: Invoice date is missing."
                )

            # ----------------------------------------------------
            # Item name
            # ----------------------------------------------------

            item_name = getattr(
                row,
                "item_name",
                "",
            )

            if not str(
                item_name
            ).strip():

                self.errors.append(
                    f"Row {index}: Item name is missing."
                )

            # ----------------------------------------------------
            # Vehicle number
            # ----------------------------------------------------

            vehicle_no = getattr(
                row,
                "vehicle_no",
                "",
            )

            if not str(
                vehicle_no
            ).strip():

                self.errors.append(
                    f"Row {index}: Vehicle number is missing."
                )

            # ----------------------------------------------------
            # Numeric fields
            # ----------------------------------------------------

            dispatched_qty = getattr(
                row,
                "dispatched_qty",
                None,
            )

            freight_per_ton = getattr(
                row,
                "freight_per_ton",
                None,
            )

            total_freight = getattr(
                row,
                "total_freight",
                None,
            )

            self.validate_numeric_value(
                dispatched_qty,
                f"Row {index}: Dispatched quantity",
            )

            self.validate_numeric_value(
                freight_per_ton,
                f"Row {index}: Freight per ton",
            )

            self.validate_numeric_value(
                total_freight,
                f"Row {index}: Total freight",
            )

    # ============================================================
    # NUMERIC VALIDATION
    # ============================================================

    def validate_numeric_value(
        self,
        value: Any,
        field_name: str,
    ):
        """
        Make sure a numeric field is valid and non-negative.
        """

        if value is None:

            self.errors.append(
                f"{field_name} is missing."
            )

            return

        try:

            decimal_value = Decimal(
                str(value)
            )

        except Exception:

            self.errors.append(
                f"{field_name} is not a valid number."
            )

            return

        if decimal_value < 0:

            self.errors.append(
                f"{field_name} cannot be negative."
            )

    # ============================================================
    # TOTAL VALIDATION
    # ============================================================

    def validate_totals(self):
        """
        Recalculate totals from rows and compare them
        against the BillData totals.
        """

        rows = getattr(
            self.bill,
            "rows",
            [],
        )

        # --------------------------------------------------------
        # Calculate quantity
        # --------------------------------------------------------

        calculated_quantity = Decimal("0")

        for row in rows:

            value = getattr(
                row,
                "dispatched_qty",
                0,
            )

            calculated_quantity += Decimal(
                str(value)
            )

        # --------------------------------------------------------
        # Calculate freight
        # --------------------------------------------------------

        calculated_freight = Decimal("0")

        for row in rows:

            value = getattr(
                row,
                "total_freight",
                0,
            )

            calculated_freight += Decimal(
                str(value)
            )

        # --------------------------------------------------------
        # Excel / BillData totals
        # --------------------------------------------------------

        expected_quantity = Decimal(
            str(
                getattr(
                    self.bill,
                    "total_quantity",
                    0,
                )
            )
        )

        expected_freight = Decimal(
            str(
                getattr(
                    self.bill,
                    "total_freight",
                    0,
                )
            )
        )

        # --------------------------------------------------------
        # Quantity comparison
        # --------------------------------------------------------

        if calculated_quantity != expected_quantity:

            self.errors.append(
                "Quantity total mismatch: "
                f"calculated={calculated_quantity}, "
                f"expected={expected_quantity}"
            )

        # --------------------------------------------------------
        # Freight comparison
        # --------------------------------------------------------

        if calculated_freight != expected_freight:

            self.errors.append(
                "Freight total mismatch: "
                f"calculated={calculated_freight}, "
                f"expected={expected_freight}"
            )

    # ============================================================
    # MAIN VALIDATION
    # ============================================================

    def validate(self):
        """
        Run all validation checks.

        Returns:
            True if the bill is valid.
            False otherwise.
        """

        # Clear previous results
        self.errors.clear()
        self.warnings.clear()

        # --------------------------------------------------------
        # Run validations
        # --------------------------------------------------------

        self.validate_structure()

        self.validate_bill_information()

        self.validate_rows()

        self.validate_totals()

        # --------------------------------------------------------
        # Return result
        # --------------------------------------------------------

        return len(self.errors) == 0

    # ============================================================
    # REPORT
    # ============================================================

    def get_report(self):
        """
        Return a simple validation report.
        """

        return {
            "is_valid": len(self.errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings,
        }
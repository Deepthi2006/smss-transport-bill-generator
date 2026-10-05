from __future__ import annotations

from decimal import Decimal
from typing import Any

from app import config
from app.services.bill_model import BillData, BillRow, BillTotals
from app.utils.amount_words import amount_to_words


class BillGenerator:
    """
    Converts validated Excel data into the application's BillData model.

    Bill number and bill date are dynamic.
    Company/customer/bank information comes from config.py.
    """

    def __init__(
        self,
        bill_no: str,
        bill_date: str,
    ):
        self.bill_no = bill_no
        self.bill_date = bill_date

    def build(self, excel_data: dict[str, Any]) -> BillData:

        rows = [
            BillRow(
                sno=row["sno"],
                from_location=row["from"],
                to_location=row["to"],
                invoice_no=row["invoice_no"],
                invoice_date=row["invoice_date"],
                item_name=row["item_name"],
                vehicle_no=row["vehicle_no"],
                dispatched_qty=Decimal(row["dispatched_qty"]),
                freight_per_ton=Decimal(row["freight_per_ton"]),
                total_freight=Decimal(row["total_freight"]),
            )
            for row in excel_data["rows"]
        ]

        totals = BillTotals(
            quantity=Decimal(excel_data["totals"]["quantity"]),
            freight=Decimal(excel_data["totals"]["freight"]),
        )

        amount_words = amount_to_words(totals.freight)

        return BillData(
            bill_no=self.bill_no,
            bill_date=self.bill_date,

            customer_name=config.CUSTOMER_NAME,

            customer_address=(
                " ".join(config.CUSTOMER_ADDRESS)
            ),

            customer_gst=config.CUSTOMER_GST,

            rows=rows,

            totals=totals,

            amount_in_words=amount_words,
        )
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any


@dataclass
class BillRow:
    sno: int
    from_location: str
    to_location: str
    invoice_no: str
    invoice_date: str
    item_name: str
    vehicle_no: str
    dispatched_qty: Decimal
    freight_per_ton: Decimal
    total_freight: Decimal


@dataclass
class BillTotals:
    quantity: Decimal
    freight: Decimal


@dataclass
class BillData:
    bill_no: str
    bill_date: str

    customer_name: str = ""
    customer_address: str = ""
    customer_gst: str = ""

    rows: list[BillRow] = field(default_factory=list)
    totals: BillTotals | None = None

    amount_in_words: str = ""

    @property
    def total_freight(self) -> Decimal:
        if self.totals is None:
            return Decimal("0")

        return self.totals.freight

    @property
    def total_quantity(self) -> Decimal:
        if self.totals is None:
            return Decimal("0")

        return self.totals.quantity

    def to_dict(self) -> dict[str, Any]:
        return {
            "bill_no": self.bill_no,
            "bill_date": self.bill_date,
            "customer_name": self.customer_name,
            "customer_address": self.customer_address,
            "customer_gst": self.customer_gst,
            "rows": [
                {
                    "sno": row.sno,
                    "from": row.from_location,
                    "to": row.to_location,
                    "invoice_no": row.invoice_no,
                    "invoice_date": row.invoice_date,
                    "item_name": row.item_name,
                    "vehicle_no": row.vehicle_no,
                    "dispatched_qty": row.dispatched_qty,
                    "freight_per_ton": row.freight_per_ton,
                    "total_freight": row.total_freight,
                }
                for row in self.rows
            ],
            "totals": {
                "quantity": self.total_quantity,
                "freight": self.total_freight,
            },
            "amount_in_words": self.amount_in_words,
        }
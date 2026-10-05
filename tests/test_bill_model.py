from decimal import Decimal

from app.services.bill_model import (
    BillData,
    BillRow,
    BillTotals,
)


def test_bill_row_creation():
    row = BillRow(
        sno=1,
        from_location="DPM",
        to_location="VATHAMBACHERY",
        invoice_no="VOTX/2627/2788",
        invoice_date="01/09/2026",
        item_name="HIPRO-TIPPER",
        vehicle_no="TN 18 AV 1248",
        dispatched_qty=Decimal("30560"),
        freight_per_ton=Decimal("475"),
        total_freight=Decimal("14516"),
    )

    assert row.sno == 1
    assert row.from_location == "DPM"
    assert row.to_location == "VATHAMBACHERY"
    assert row.dispatched_qty == Decimal("30560")
    assert row.total_freight == Decimal("14516")


def test_bill_totals():
    totals = BillTotals(
        quantity=Decimal("335590"),
        freight=Decimal("159405.25"),
    )

    assert totals.quantity == Decimal("335590")
    assert totals.freight == Decimal("159405.25")


def test_bill_data():
    row = BillRow(
        sno=1,
        from_location="DPM",
        to_location="VATHAMBACHERY",
        invoice_no="VOTX/2627/2788",
        invoice_date="01/09/2026",
        item_name="HIPRO-TIPPER",
        vehicle_no="TN 18 AV 1248",
        dispatched_qty=Decimal("30560"),
        freight_per_ton=Decimal("475"),
        total_freight=Decimal("14516"),
    )

    totals = BillTotals(
        quantity=Decimal("335590"),
        freight=Decimal("159405.25"),
    )

    bill = BillData(
        bill_no="SF022",
        bill_date="08.09.2026",
        customer_name="M/s. Shanthi Feeds Pvt Ltd",
        rows=[row],
        totals=totals,
        amount_in_words=(
            "ONE LAKH FIFTY NINE THOUSAND "
            "FOUR HUNDRED FIVE ONLY"
        ),
    )

    assert bill.bill_no == "SF022"
    assert bill.bill_date == "08.09.2026"
    assert len(bill.rows) == 1
    assert bill.total_quantity == Decimal("335590")
    assert bill.total_freight == Decimal("159405.25")


def test_bill_to_dict():
    totals = BillTotals(
        quantity=Decimal("335590"),
        freight=Decimal("159405.25"),
    )

    bill = BillData(
        bill_no="SF022",
        bill_date="08.09.2026",
        totals=totals,
    )

    data = bill.to_dict()

    assert data["bill_no"] == "SF022"
    assert data["bill_date"] == "08.09.2026"
    assert data["totals"]["quantity"] == Decimal("335590")
    assert data["totals"]["freight"] == Decimal("159405.25")
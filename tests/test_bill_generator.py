from pathlib import Path

from app.services.excel_reader import ExcelBillReader
from app.services.bill_generator import BillGenerator


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXCEL_FILE = PROJECT_ROOT / "data" / "input" / "SMSS-07.xlsx"


def test_build_complete_bill():

    # ---------------------------------------------------------
    # 1. Read Excel
    # ---------------------------------------------------------

    reader = ExcelBillReader(EXCEL_FILE)

    excel_data = reader.read()

    # ---------------------------------------------------------
    # 2. Build BillData
    # ---------------------------------------------------------

    generator = BillGenerator(
        bill_no="SF022",
        bill_date="08.09.2026",
    )

    bill = generator.build(excel_data)

    # ---------------------------------------------------------
    # 3. Bill information
    # ---------------------------------------------------------

    assert bill.bill_no == "SF022"
    assert bill.bill_date == "08.09.2026"

    # ---------------------------------------------------------
    # 4. Customer information
    # ---------------------------------------------------------

    assert bill.customer_name == (
        "M/s. Shanthi Feeds Pvt Ltd(VEGETABLE OIL DIVISION),"
    )

    assert bill.customer_gst == "33AAJCS8030J2Z8"

    # ---------------------------------------------------------
    # 5. Number of rows
    # ---------------------------------------------------------

    assert len(bill.rows) == 16

    # ---------------------------------------------------------
    # 6. Totals
    # ---------------------------------------------------------

    assert bill.total_quantity == 491610
    assert bill.total_freight == 233514.75

    # ---------------------------------------------------------
    # 7. Amount in words
    # ---------------------------------------------------------

    assert bill.amount_in_words == (
        "TWO LAKH THIRTY THREE THOUSAND FIVE HUNDRED FIFTEEN ONLY"
    )

    # ---------------------------------------------------------
    # 8. Print generated bill information
    # ---------------------------------------------------------

    print()
    print("========== BILL GENERATOR TEST ==========")
    print("Bill No         :", bill.bill_no)
    print("Bill Date       :", bill.bill_date)
    print("Customer        :", bill.customer_name)
    print("GST             :", bill.customer_gst)
    print("Number of rows  :", len(bill.rows))
    print("Total Quantity  :", bill.total_quantity)
    print("Total Freight   :", bill.total_freight)
    print("Amount in Words :", bill.amount_in_words)

    print()
    print("FIRST BILL ROW:")
    print(vars(bill.rows[0]))

    print()
    print("LAST BILL ROW:")
    print(vars(bill.rows[-1]))

    print("=========================================")
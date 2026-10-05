from pathlib import Path

from app.services.excel_reader import ExcelBillReader
from app.services.bill_generator import BillGenerator
from app.services.validator import BillValidator


# ============================================================
# TEST FILE
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

EXCEL_FILE = (
    PROJECT_ROOT
    / "data"
    / "input"
    / "SMSS-07.xlsx"
)


def test_validate_bill():

    # ---------------------------------------------------------
    # 1. Read Excel
    # ---------------------------------------------------------

    reader = ExcelBillReader(
        EXCEL_FILE
    )

    excel_data = reader.read()

    # ---------------------------------------------------------
    # 2. Build BillData
    #
    # This is the same process used by Streamlit.
    # ---------------------------------------------------------

    generator = BillGenerator(
        bill_no="SF022",
        bill_date="08.09.2026",
    )

    bill = generator.build(
        excel_data
    )

    # ---------------------------------------------------------
    # 3. Validate BillData
    # ---------------------------------------------------------

    validator = BillValidator(
        bill
    )

    result = validator.validate()

    # ---------------------------------------------------------
    # 4. Display validation information
    # ---------------------------------------------------------

    print()
    print("=" * 60)
    print("BILL VALIDATION TEST")
    print("=" * 60)

    print(
        f"Bill Number    : {bill.bill_no}"
    )

    print(
        f"Bill Date      : {bill.bill_date}"
    )

    print(
        f"Customer       : {bill.customer_name}"
    )

    print(
        f"Bill Rows      : {len(bill.rows)}"
    )

    print(
        f"Total Quantity : {bill.total_quantity:g}"
    )

    print(
        f"Total Freight  : ₹{bill.total_freight}"
    )

    print()

    print(
        f"Validation     : "
        f"{'PASSED ✓' if result else 'FAILED ✗'}"
    )

    # ---------------------------------------------------------
    # 5. Print errors if validation fails
    # ---------------------------------------------------------

    if not result:

        print()
        print("VALIDATION ERRORS:")

        for error in validator.errors:

            print(
                f"  ✗ {error}"
            )

    print("=" * 60)

    # ---------------------------------------------------------
    # 6. Assertion
    # ---------------------------------------------------------

    assert result is True
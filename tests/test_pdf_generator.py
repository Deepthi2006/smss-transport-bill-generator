from decimal import Decimal
from pathlib import Path

from app.services.bill_generator import BillGenerator
from app.services.excel_reader import ExcelBillReader
from app.services.pdf_generator import PDFBillGenerator


PROJECT_ROOT = Path(__file__).resolve().parents[1]

EXCEL_FILE = (
    PROJECT_ROOT
    / "data"
    / "input"
    / "SMSS-07.xlsx"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "output"
    / "SF022_test.pdf"
)


def test_generate_pdf():

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
    # 3. Generate PDF
    # ---------------------------------------------------------

    pdf_generator = PDFBillGenerator(
        OUTPUT_FILE
    )

    output = pdf_generator.generate(bill)

    # ---------------------------------------------------------
    # 4. Verify
    # ---------------------------------------------------------

    print()
    print("=" * 60)
    print("PDF GENERATION TEST")
    print("=" * 60)

    print("Output file :", output)
    print("Exists      :", output.exists())
    print("Size        :", output.stat().st_size, "bytes")

    print("=" * 60)

    assert output.exists()
    assert output.stat().st_size > 0
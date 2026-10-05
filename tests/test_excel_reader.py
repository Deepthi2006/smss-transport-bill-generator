from pathlib import Path

from app.services.excel_reader import ExcelBillReader


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXCEL_FILE = PROJECT_ROOT / "data" / "input" / "SMSS-07.xlsx"


def test_excel_reader():

    reader = ExcelBillReader(EXCEL_FILE)

    data = reader.read()

    # ---------------------------------------------------------
    # Basic workbook information
    # ---------------------------------------------------------

    assert data["file_name"] == "SMSS-07.xlsx"
    assert data["sheet_name"] == "AUGUEST-SMSS-22"

    # ---------------------------------------------------------
    # Header / total row
    # ---------------------------------------------------------

    assert data["header_row"] == 11
    assert data["total_row"] == 28

    # ---------------------------------------------------------
    # Number of bill rows
    # ---------------------------------------------------------

    assert len(data["rows"]) == 16

    # ---------------------------------------------------------
    # Totals
    # ---------------------------------------------------------

    assert data["totals"]["quantity"] == 491610
    assert data["totals"]["freight"] == 233514.75

    # ---------------------------------------------------------
    # Print actual extracted data
    # ---------------------------------------------------------

    print()
    print("========== EXCEL READER TEST ==========")
    print("File          :", data["file_name"])
    print("Sheet         :", data["sheet_name"])
    print("Header Row    :", data["header_row"])
    print("Total Row     :", data["total_row"])
    print("Bill Rows     :", len(data["rows"]))
    print("Total Quantity:", data["totals"]["quantity"])
    print("Total Freight :", data["totals"]["freight"])

    print()
    print("FIRST ROW:")
    print(data["rows"][0])

    print()
    print("LAST ROW:")
    print(data["rows"][-1])

    print("=======================================")
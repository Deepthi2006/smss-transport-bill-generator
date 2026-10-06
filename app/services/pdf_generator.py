from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth

from app import config
from app.services.bill_model import BillData


# ================================================================
# PAGE
# ================================================================

PAGE_WIDTH, PAGE_HEIGHT = A4


# ================================================================
# COLORS
# ================================================================

DARK_BLUE = colors.HexColor("#193551")
ORANGE = colors.HexColor("#C1441E")

BLACK = colors.black
WHITE = colors.white


class PDFBillGenerator:
    """
    Generate the Mama Bill PDF using the original
    SMSS Transport bill layout.
    """

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(
        self,
        output_path: str | Path,
    ):
        self.output_path = Path(output_path)

        self.logo_path = (
            Path(__file__).resolve().parents[1]
            / "assets"
            / "smss_logo.jpeg"
        )

    # ============================================================
    # BASIC TEXT HELPERS
    # ============================================================

    @staticmethod
    def draw_text(
        canvas_obj,
        text: str,
        x: float,
        y: float,
        font: str = "Helvetica",
        size: float = 9,
    ):
        canvas_obj.setFont(
            font,
            size,
        )

        canvas_obj.drawString(
            x,
            y,
            str(text),
        )

    # ------------------------------------------------------------

    @staticmethod
    def draw_right_text(
        canvas_obj,
        text: str,
        x: float,
        y: float,
        font: str = "Helvetica",
        size: float = 9,
    ):
        canvas_obj.setFont(
            font,
            size,
        )

        canvas_obj.drawRightString(
            x,
            y,
            str(text),
        )

    # ------------------------------------------------------------

    @staticmethod
    def draw_center_text(
        canvas_obj,
        text: str,
        x: float,
        y: float,
        font: str = "Helvetica",
        size: float = 9,
    ):
        canvas_obj.setFont(
            font,
            size,
        )

        canvas_obj.drawCentredString(
            x,
            y,
            str(text),
        )

    # ============================================================
    # TEXT WIDTH
    # ============================================================

    @staticmethod
    def text_width(
        text: str,
        font: str,
        size: float,
    ) -> float:

        return stringWidth(
            str(text),
            font,
            size,
        )

    # ============================================================
    # TEXT WRAPPING
    # ============================================================

    @staticmethod
    def wrap_text(
        text: str,
        max_width: float,
        font: str,
        size: float,
    ) -> list[str]:
        """
        Wrap text according to the available cell width.

        IMPORTANT:
        VATHAMBACHERY is intentionally NOT split.
        It must remain as one word in the TO column.
        """

        text = str(text).strip()

        if not text:
            return [""]

        # --------------------------------------------------------
        # Explicit line breaks
        # --------------------------------------------------------

        if "\n" in text:

            result = []

            for part in text.split("\n"):

                result.extend(
                    PDFBillGenerator.wrap_text(
                        part,
                        max_width,
                        font,
                        size,
                    )
                )

            return result

        # --------------------------------------------------------
        # Special formatting
        # --------------------------------------------------------

        special_breaks = {

            # IMPORTANT:
            # VATHAMBACHERY is intentionally NOT here.
            # It must stay on ONE LINE.

            "HIPRO-TIPPER": [
                "HIPRO-",
                "TIPPER",
            ],

            "TN 18 AV 1248": [
                "TN 18 AV",
                "1248",
            ],

            "TN 69 BJ 7775": [
                "TN 69 BJ",
                "7775",
            ],
        }

        if text in special_breaks:
            return special_breaks[text]

        # --------------------------------------------------------
        # Single word
        # --------------------------------------------------------

        words = text.split()

        if len(words) == 1:

            # Do NOT split a single word such as:
            #
            # VATHAMBACHERY
            #
            # Return it as one word.

            return [text]

        # --------------------------------------------------------
        # Normal multi-word wrapping
        # --------------------------------------------------------

        lines = []

        current = ""

        for word in words:

            candidate = (
                word
                if not current
                else f"{current} {word}"
            )

            if (
                PDFBillGenerator.text_width(
                    candidate,
                    font,
                    size,
                )
                <= max_width
            ):

                current = candidate

            else:

                if current:
                    lines.append(current)

                current = word

        if current:
            lines.append(current)

        return lines

    # ============================================================
    # CELL TEXT
    # ============================================================

    def draw_cell_text(
        self,
        canvas_obj,
        text: str,
        x: float,
        y: float,
        width: float,
        height: float,
        font: str = "Times-Roman",
        size: float = 8.2,
        bold: bool = False,
    ):
        """
        Draw centered text inside a table cell.
        """

        if bold:
            font = "Times-Bold"

        padding = 2

        lines = self.wrap_text(
            str(text),
            width - (padding * 2),
            font,
            size,
        )

        line_height = size + 1.5

        total_text_height = (
            len(lines) * line_height
        )

        start_y = (
            y
            + (height + total_text_height) / 2
            - line_height
        )

        canvas_obj.setFillColor(
            BLACK
        )

        canvas_obj.setFont(
            font,
            size,
        )

        for line in lines:

            text_width = self.text_width(
                line,
                font,
                size,
            )

            text_x = (
                x
                + (width - text_width) / 2
            )

            canvas_obj.drawString(
                text_x,
                start_y,
                line,
            )

            start_y -= line_height

    # ============================================================
    # HEADER
    # ============================================================

    def draw_header(
        self,
        canvas_obj,
        bill: BillData,
    ):
        """
        Draw the approved SMSS Transport header.
        """

        header_height = 97

        header_top = PAGE_HEIGHT

        header_bottom = (
            PAGE_HEIGHT - header_height
        )

        # ========================================================
        # DARK BLUE HEADER
        # ========================================================

        blue_path = canvas_obj.beginPath()

        blue_path.moveTo(
            0,
            header_bottom,
        )

        blue_path.lineTo(
            283,
            header_bottom,
        )

        blue_path.lineTo(
            418,
            header_top,
        )

        blue_path.lineTo(
            0,
            header_top,
        )

        blue_path.close()

        canvas_obj.setFillColor(
            DARK_BLUE
        )

        canvas_obj.drawPath(
            blue_path,
            stroke=0,
            fill=1,
        )

        # ========================================================
        # ORANGE DIAGONAL
        # ========================================================

        orange_path = canvas_obj.beginPath()

        orange_path.moveTo(
            283,
            header_bottom,
        )

        orange_path.lineTo(
            327,
            header_bottom,
        )

        orange_path.lineTo(
            434,
            header_top,
        )

        orange_path.lineTo(
            418,
            header_top,
        )

        orange_path.close()

        canvas_obj.setFillColor(
            ORANGE
        )

        canvas_obj.drawPath(
            orange_path,
            stroke=0,
            fill=1,
        )

        # ========================================================
        # LOGO
        # ========================================================

        if self.logo_path.exists():

            canvas_obj.drawImage(
                ImageReader(
                    str(self.logo_path)
                ),
                26,
                header_bottom + 31,
                width=87,
                height=48,
                preserveAspectRatio=True,
                mask="auto",
            )

        # ========================================================
        # COMPANY NAME
        # ========================================================

        text_x = 134

        canvas_obj.setFillColor(
            WHITE
        )

        self.draw_text(
            canvas_obj,
            config.COMPANY_NAME,
            text_x,
            header_top - 45,
            font="Times-Bold",
            size=22,
        )

        # ========================================================
        # PROPRIETOR
        # ========================================================

        self.draw_text(
            canvas_obj,
            config.PROPRIETOR_NAME,
            text_x,
            header_top - 59,
            font="Times-Roman",
            size=9,
        )

        # ========================================================
        # COMPANY ADDRESS
        # ========================================================

        address_y = (
            header_top - 72
        )

        for address_line in (
            config.COMPANY_ADDRESS
        ):

            self.draw_text(
                canvas_obj,
                address_line,
                text_x,
                address_y,
                font="Times-Roman",
                size=8.5,
            )

            address_y -= 10

    # ============================================================
    # BILL NUMBER / DATE
    # ============================================================

    def draw_bill_info(
        self,
        canvas_obj,
        bill: BillData,
    ):

        y = (
            PAGE_HEIGHT - 115
        )

        canvas_obj.setFillColor(
            BLACK
        )

        self.draw_text(
            canvas_obj,
            f"Bill no : {bill.bill_no}",
            38,
            y,
            font="Times-Bold",
            size=9.5,
        )

        self.draw_right_text(
            canvas_obj,
            f"Date:{bill.bill_date}",
            PAGE_WIDTH - 38,
            y,
            font="Times-Bold",
            size=9.5,
        )

    # ============================================================
    # CUSTOMER INFORMATION
    # ============================================================

    def draw_customer_info(
        self,
        canvas_obj,
        bill: BillData,
    ):

        x = 66

        y = (
            PAGE_HEIGHT - 140
        )

        canvas_obj.setFillColor(
            BLACK
        )

        # --------------------------------------------------------
        # Customer name
        # --------------------------------------------------------

        self.draw_text(
            canvas_obj,
            bill.customer_name,
            x,
            y,
            font="Times-Bold",
            size=9.5,
        )

        y -= 17

        # --------------------------------------------------------
        # Address line 1
        # --------------------------------------------------------

        self.draw_text(
            canvas_obj,
            config.CUSTOMER_ADDRESS[0],
            x,
            y,
            font="Times-Bold",
            size=9.5,
        )

        y -= 17

        # --------------------------------------------------------
        # Address line 2
        # --------------------------------------------------------

        self.draw_text(
            canvas_obj,
            config.CUSTOMER_ADDRESS[1],
            x,
            y,
            font="Times-Bold",
            size=9.5,
        )

        y -= 17

        # --------------------------------------------------------
        # GST
        # --------------------------------------------------------

        self.draw_text(
            canvas_obj,
            f"GST NO - {config.CUSTOMER_GST}",
            x,
            y,
            font="Times-Bold",
            size=9.5,
        )

    # ============================================================
    # BILL TABLE
    # ============================================================

    def draw_bill_table(
        self,
        canvas_obj,
        bill: BillData,
    ):
        """
        Draw the 10-column transport bill table.

        The table automatically adapts to the number of
        bill rows.

        More rows:
            -> smaller row height
            -> smaller data font
            -> smaller TO-column font

        This prevents the table from overlapping the
        Amount / Footer section.
        """

        # ========================================================
        # TABLE POSITION
        # ========================================================

        table_x = 21

        # Keep the same table top position used by the
        # current approved design.
        table_top = PAGE_HEIGHT - 215

        # ========================================================
        # COLUMN WIDTHS
        # ========================================================

        column_widths = [
            36,   # S.NO
            37,   # From
            82,   # To
            79,   # IN NO
            53,   # Inv.Date
            45,   # Item Name
            53,   # VEH-NO
            61,   # Dispatched Qty
            44,   # Freight/Ton
            63,   # Total Freight
        ]

        assert sum(column_widths) == 553

        # ========================================================
        # NUMBER OF DATA ROWS
        # ========================================================

        row_count = len(bill.rows)

        # ========================================================
        # FIXED ROW SIZES
        # ========================================================

        header_height = 48

        total_height = 29

        # ========================================================
        # AVAILABLE SPACE
        # ========================================================
        #
        # The Amount section starts around Y = 195.
        #
        # We keep a safe gap above it.
        #
        # Therefore the table should preferably finish around
        # Y = 205 or higher.
        #
        # ========================================================

        minimum_table_bottom = 207

        available_data_height = (
            table_top
            - header_height
            - total_height
            - minimum_table_bottom
        )

        # ========================================================
        # DYNAMIC ROW HEIGHT
        # ========================================================
        #
        # 11 rows -> 28 pt
        #
        # 12+ rows -> automatically calculated.
        #
        # We don't blindly force 19 pt because very large bills
        # need to continue shrinking to remain on one page.
        #
        # ========================================================

        if row_count <= 11:

            row_height = 28.0

        else:

            row_height = (
                available_data_height
                / row_count
            )

            row_height = min(
                28.0,
                row_height,
            )

            # Do not make rows unnecessarily tiny.
            # 16 pt is still usable for very dense bills.
            row_height = max(
                16.0,
                row_height,
            )

        # ========================================================
        # DYNAMIC DATA FONT SIZE
        # ========================================================
        #
        # 11 rows -> 8.2 pt
        #
        # As the number of rows increases, the font decreases.
        #
        # ========================================================

        if row_count <= 11:

            data_font_size = 8.2

        elif row_count == 12:

            data_font_size = 7.8

        elif row_count == 13:

            data_font_size = 7.5

        elif row_count == 14:

            data_font_size = 7.2

        elif row_count == 15:

            data_font_size = 7.0

        elif row_count == 16:

            data_font_size = 6.8

        elif row_count == 17:

            data_font_size = 6.6

        elif row_count == 18:

            data_font_size = 6.4

        elif row_count == 19:

            data_font_size = 6.2

        elif row_count == 20:

            data_font_size = 6.0

        else:

            data_font_size = 5.8

        # ========================================================
        # TO COLUMN FONT SIZE
        # ========================================================
        #
        # VATHAMBACHERY must remain in one line.
        #
        # It is already intentionally smaller than other cells.
        #
        # ========================================================

        to_font_size = min(
            data_font_size,
            6.8,
        )

        # ========================================================
        # HEADER FONT SIZE
        # ========================================================

        if row_count <= 13:

            normal_header_font = 8.2
            right_header_font = 9.2
            to_header_font = 7.0

        elif row_count <= 16:

            normal_header_font = 7.8
            right_header_font = 8.8
            to_header_font = 6.8

        else:

            normal_header_font = 7.4
            right_header_font = 8.4
            to_header_font = 6.6

        # ========================================================
        # HEADERS
        # ========================================================

        headers = [
            "S.NO",
            "From",
            "To",
            "IN NO",
            "Inv.Date",
            "Item\nName",
            "VEH-NO",
            "Dispatched\nQty(KGS)",
            "FRIGHT\n/PER\nTON",
            "Total\nFRIGHT",
        ]

        # ========================================================
        # X POSITIONS
        # ========================================================

        x_positions = [table_x]

        current_x = table_x

        for width in column_widths:

            current_x += width

            x_positions.append(
                current_x
            )

        # ========================================================
        # HEADER POSITION
        # ========================================================

        header_bottom = (
            table_top
            - header_height
        )

        # ========================================================
        # HEADER BACKGROUND
        # ========================================================

        canvas_obj.setFillColor(
            WHITE
        )

        canvas_obj.rect(
            table_x,
            header_bottom,
            sum(column_widths),
            header_height,
            stroke=0,
            fill=1,
        )

        # ========================================================
        # HEADER TEXT
        # ========================================================

        for index, header in enumerate(
            headers
        ):

            x = x_positions[index]

            width = column_widths[index]

            if index == 2:

                header_font_size = (
                    to_header_font
                )

            elif index in (7, 8, 9):

                header_font_size = (
                    right_header_font
                )

            else:

                header_font_size = (
                    normal_header_font
                )

            self.draw_cell_text(
                canvas_obj,
                header,
                x,
                header_bottom,
                width,
                header_height,
                font="Times-Bold",
                size=header_font_size,
                bold=True,
            )

        # ========================================================
        # HEADER BORDER
        # ========================================================

        canvas_obj.setStrokeColor(
            BLACK
        )

        canvas_obj.setLineWidth(
            0.7
        )

        canvas_obj.rect(
            table_x,
            header_bottom,
            sum(column_widths),
            header_height,
            stroke=1,
            fill=0,
        )

        # ========================================================
        # HEADER VERTICAL LINES
        # ========================================================

        for x in x_positions[1:-1]:

            canvas_obj.line(
                x,
                header_bottom,
                x,
                table_top,
            )

        # ========================================================
        # DATA ROWS
        # ========================================================

        current_top = header_bottom

        for row in bill.rows:

            row_bottom = (
                current_top
                - row_height
            )

            # ----------------------------------------------------
            # Row values
            # ----------------------------------------------------

            values = [

                str(row.sno),

                row.from_location,

                row.to_location,

                row.invoice_no,

                row.invoice_date,

                "HIPRO-TIPPER",

                row.vehicle_no,

                f"{row.dispatched_qty:g}",

                f"{row.freight_per_ton:g}",

                f"{row.total_freight:.2f}",
            ]

            # ----------------------------------------------------
            # CELL TEXT
            # ----------------------------------------------------

            for index, value in enumerate(
                values
            ):

                # -----------------------------------------------
                # TO COLUMN
                # -----------------------------------------------
                #
                # VATHAMBACHERY must stay on ONE LINE.
                #
                # Smaller font allows it to fit.
                #
                # -----------------------------------------------

                if index == 2:

                    cell_font_size = (
                        to_font_size
                    )

                else:

                    cell_font_size = (
                        data_font_size
                    )

                self.draw_cell_text(
                    canvas_obj,
                    value,
                    x_positions[index],
                    row_bottom,
                    column_widths[index],
                    row_height,
                    font="Times-Bold",
                    size=cell_font_size,
                    bold=True,
                )

            # ----------------------------------------------------
            # Horizontal line
            # ----------------------------------------------------

            canvas_obj.setStrokeColor(
                BLACK
            )

            canvas_obj.setLineWidth(
                0.55
            )

            canvas_obj.line(
                table_x,
                row_bottom,
                table_x + sum(column_widths),
                row_bottom,
            )

            # ----------------------------------------------------
            # Vertical lines
            # ----------------------------------------------------

            for x in x_positions[1:-1]:

                canvas_obj.line(
                    x,
                    row_bottom,
                    x,
                    current_top,
                )

            current_top = row_bottom

        # ========================================================
        # TOTAL ROW
        # ========================================================

        total_bottom = (
            current_top
            - total_height
        )

        # ========================================================
        # TOTAL OUTER BORDER
        # ========================================================

        canvas_obj.rect(
            table_x,
            total_bottom,
            sum(column_widths),
            total_height,
            stroke=1,
            fill=0,
        )

        # ========================================================
        # TOTAL LABEL
        # ========================================================

        merged_start = (
            x_positions[0]
        )

        merged_end = (
            x_positions[7]
        )

        total_font_size = (
            max(7.0, data_font_size)
        )

        self.draw_cell_text(
            canvas_obj,
            "TOTAL",
            merged_start,
            total_bottom,
            merged_end - merged_start,
            total_height,
            font="Times-Bold",
            size=total_font_size,
            bold=True,
        )

        # ========================================================
        # TOTAL / QUANTITY SEPARATOR
        # ========================================================

        canvas_obj.line(
            merged_end,
            total_bottom,
            merged_end,
            total_bottom + total_height,
        )

        # ========================================================
        # TOTAL QUANTITY
        # ========================================================

        self.draw_cell_text(
            canvas_obj,
            f"{bill.total_quantity:g}",
            x_positions[7],
            total_bottom,
            column_widths[7],
            total_height,
            font="Times-Bold",
            size=total_font_size,
            bold=True,
        )

        # ========================================================
        # QUANTITY / FREIGHT SEPARATOR
        # ========================================================

        canvas_obj.line(
            x_positions[8],
            total_bottom,
            x_positions[8],
            total_bottom + total_height,
        )

        # ========================================================
        # FREIGHT/PER TON COLUMN
        # REMAINS BLANK
        # ========================================================

        canvas_obj.line(
            x_positions[9],
            total_bottom,
            x_positions[9],
            total_bottom + total_height,
        )

        # ========================================================
        # TOTAL FREIGHT
        # ========================================================

        rounded_freight = int(
            bill.total_freight.quantize(
                Decimal("1"),
                rounding=ROUND_HALF_UP,
            )
        )

        self.draw_cell_text(
            canvas_obj,
            str(rounded_freight),
            x_positions[9],
            total_bottom,
            column_widths[9],
            total_height,
            font="Times-Bold",
            size=total_font_size,
            bold=True,
        )

        # ========================================================
        # FINAL TABLE BORDER
        # ========================================================

        table_bottom = total_bottom

        canvas_obj.rect(
            table_x,
            table_bottom,
            sum(column_widths),
            table_top - table_bottom,
            stroke=1,
            fill=0,
        )

    # ============================================================
    # FOOTER / BOTTOM SECTION
    # ============================================================

    def draw_footer(
        self,
        canvas_obj,
        bill: BillData,
    ):
        """
        Draw the complete lower section of the original bill.

        Contains:

            Amount in Words
            For SMSS Transport.
            Authorized Signatory
            RCM Note
            S PUNITHA
            Blue bank-information footer
        """

        # ========================================================
        # COLORS
        # ========================================================

        dark_blue = colors.HexColor(
            "#193551"
        )

        orange = colors.HexColor(
            "#C1441E"
        )

        black = colors.black
        white = colors.white

        # ========================================================
        # TABLE BOTTOM
        # ========================================================

        table_bottom = 218

        # ========================================================
        # 1. AMOUNT IN WORDS
        # ========================================================

        amount_y = 195

        self.draw_text(
            canvas_obj,
            "Amount:",
            38,
            amount_y,
            font="Times-Bold",
            size=9,
        )

        self.draw_text(
            canvas_obj,
            bill.amount_in_words,
            85,
            amount_y,
            font="Times-Bold",
            size=9,
        )

        # ========================================================
        # 2. SIGNATURE ROW
        # ========================================================

        signature_y = 185

        self.draw_text(
            canvas_obj,
            config.FOR_COMPANY_TEXT,
            38,
            signature_y,
            font="Times-Bold",
            size=9,
        )

        # ========================================================
        # 3. AUTHORIZED SIGNATORY
        # ========================================================

        authorized_y = 141

        self.draw_text(
            canvas_obj,
            config.AUTHORIZED_SIGNATORY,
            38,
            authorized_y,
            font="Times-Bold",
            size=9,
        )

        # ========================================================
        # 4. RCM NOTE
        # ========================================================

        rcm_y = 175

        self.draw_text(
            canvas_obj,
            config.RCM_NOTE,
            38,
            rcm_y,
            font="Times-Bold",
            size=8.5,
        )

        # ========================================================
        # 5. BLUE BOTTOM GRAPHIC
        # ========================================================

        footer_height = 105

        blue_path = canvas_obj.beginPath()

        blue_path.moveTo(
            0,
            0,
        )

        blue_path.lineTo(
            PAGE_WIDTH,
            0,
        )

        blue_path.lineTo(
            365,
            footer_height,
        )

        blue_path.lineTo(
            0,
            footer_height,
        )

        blue_path.close()

        canvas_obj.setFillColor(
            dark_blue
        )

        canvas_obj.drawPath(
            blue_path,
            stroke=0,
            fill=1,
        )

        # ========================================================
        # 6. ORANGE DIAGONAL STRIPE
        # ========================================================

        orange_path = canvas_obj.beginPath()

        orange_path.moveTo(
            350,
            footer_height - 28,
        )

        orange_path.lineTo(
            374,
            footer_height - 28,
        )

        orange_path.lineTo(
            500,
            0,
        )

        orange_path.lineTo(
            476,
            0,
        )

        orange_path.close()

        canvas_obj.setFillColor(
            orange
        )

        canvas_obj.drawPath(
            orange_path,
            stroke=0,
            fill=1,
        )

        # ========================================================
        # 7. BANK INFORMATION
        # ========================================================

        canvas_obj.setFillColor(
            white
        )

        info_x = 38

        value_x = 112

        # --------------------------------------------------------
        # Proprietor
        # --------------------------------------------------------

        self.draw_text(
            canvas_obj,
            "Proprietor:",
            info_x,
            82,
            font="Times-Bold",
            size=9,
        )

        self.draw_text(
            canvas_obj,
            config.PROPRIETOR_NAME,
            value_x,
            82,
            font="Times-Bold",
            size=9,
        )

        # --------------------------------------------------------
        # Bank
        # --------------------------------------------------------

        self.draw_text(
            canvas_obj,
            "Bank:",
            info_x,
            67,
            font="Times-Bold",
            size=9,
        )

        self.draw_text(
            canvas_obj,
            config.BANK_NAME,
            value_x,
            67,
            font="Times-Roman",
            size=8.5,
        )

        # --------------------------------------------------------
        # Account Number
        # --------------------------------------------------------

        self.draw_text(
            canvas_obj,
            "Account No:",
            info_x,
            52,
            font="Times-Bold",
            size=9,
        )

        self.draw_text(
            canvas_obj,
            config.ACCOUNT_NUMBER,
            value_x,
            52,
            font="Times-Roman",
            size=8.5,
        )

        # --------------------------------------------------------
        # IFSC
        # --------------------------------------------------------

        self.draw_text(
            canvas_obj,
            "IFSC:",
            info_x,
            37,
            font="Times-Bold",
            size=9,
        )

        self.draw_text(
            canvas_obj,
            config.IFSC_CODE,
            value_x,
            37,
            font="Times-Roman",
            size=8.5,
        )

        # --------------------------------------------------------
        # PAN
        # --------------------------------------------------------

        self.draw_text(
            canvas_obj,
            "PAN NO:",
            info_x,
            22,
            font="Times-Bold",
            size=9,
        )

        self.draw_text(
            canvas_obj,
            config.PAN_NUMBER,
            value_x,
            22,
            font="Times-Roman",
            size=8.5,
        )

        # --------------------------------------------------------
        # G-PAY
        # --------------------------------------------------------

        self.draw_text(
            canvas_obj,
            "G-Pay:",
            info_x,
            7,
            font="Times-Bold",
            size=9,
        )

        self.draw_text(
            canvas_obj,
            f"{config.GPAY_NUMBER} - {config.GPAY_NAME}",
            value_x,
            7,
            font="Times-Bold",
            size=8.5,
        )

    # ============================================================
    # GENERATE PDF
    # ============================================================

    def generate(
        self,
        bill: BillData,
    ) -> Path:

        # --------------------------------------------------------
        # Create output directory
        # --------------------------------------------------------

        self.output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        # --------------------------------------------------------
        # Create PDF
        # --------------------------------------------------------

        pdf = canvas.Canvas(
            str(self.output_path),
            pagesize=A4,
        )

        # --------------------------------------------------------
        # Header
        # --------------------------------------------------------

        self.draw_header(
            pdf,
            bill,
        )

        # --------------------------------------------------------
        # Bill information
        # --------------------------------------------------------

        self.draw_bill_info(
            pdf,
            bill,
        )

        # --------------------------------------------------------
        # Customer information
        # --------------------------------------------------------

        self.draw_customer_info(
            pdf,
            bill,
        )

        # --------------------------------------------------------
        # Bill table
        # --------------------------------------------------------

        self.draw_bill_table(
            pdf,
            bill,
        )

        # --------------------------------------------------------
        # Footer
        # --------------------------------------------------------

        self.draw_footer(
            pdf,
            bill,
        )

        # --------------------------------------------------------
        # Save PDF
        # --------------------------------------------------------

        pdf.save()

        return self.output_path
from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
import tempfile

import streamlit as st

from app.services.excel_reader import ExcelBillReader
from app.services.bill_generator import BillGenerator
from app.services.validator import BillValidator
from app.services.pdf_generator import PDFBillGenerator


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

OUTPUT_DIR = PROJECT_ROOT / "data" / "output"

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SMSS Transport Bill Generator",
    page_icon="🧾",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ============================================================
# SESSION STATE
# ============================================================

if "generated_pdf_path" not in st.session_state:
    st.session_state.generated_pdf_path = None

if "generated_bill" not in st.session_state:
    st.session_state.generated_bill = None


# ============================================================
# PREMIUM NEON PURPLE THEME
# ============================================================

st.markdown(
    """
<style>

/* ============================================================
   GLOBAL
   ============================================================ */

.stApp {
    background:
        radial-gradient(
            circle at 0% 0%,
            rgba(103, 43, 255, 0.22) 0%,
            rgba(103, 43, 255, 0.08) 18%,
            transparent 38%
        ),
        radial-gradient(
            circle at 100% 0%,
            rgba(168, 85, 247, 0.18) 0%,
            rgba(168, 85, 247, 0.06) 18%,
            transparent 36%
        ),
        radial-gradient(
            circle at 0% 100%,
            rgba(124, 58, 237, 0.18) 0%,
            transparent 35%
        ),
        radial-gradient(
            circle at 100% 100%,
            rgba(139, 92, 246, 0.20) 0%,
            transparent 35%
        ),
        #05050d;

    min-height: 100vh;
}


/* ============================================================
   MAIN CONTENT
   ============================================================ */

.main .block-container {
    max-width: 900px;

    padding-top: 42px;
    padding-bottom: 70px;

    padding-left: 24px;
    padding-right: 24px;
}


/* ============================================================
   REMOVE STREAMLIT CHROME
   ============================================================ */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}


/* ============================================================
   HEADER
   ============================================================ */

.page-title {
    text-align: center;

    font-size: 40px;
    line-height: 1.15;

    font-weight: 850;

    letter-spacing: -1.3px;

    margin: 0 0 8px 0;

    background:
        linear-gradient(
            90deg,
            #a78bfa,
            #ffffff 45%,
            #ffffff 65%,
            #c084fc
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    text-shadow:
        0 0 18px rgba(139, 92, 246, 0.25);
}


.page-subtitle {
    text-align: center;

    color: #aaa6ba;

    font-size: 15px;

    margin-bottom: 40px;
}


/* ============================================================
   SECTION LABEL
   ============================================================ */

.section-label {
    color: #8f86a5;

    font-size: 11px;

    font-weight: 800;

    letter-spacing: 1.8px;

    text-transform: uppercase;

    margin-top: 24px;

    margin-bottom: 10px;

    padding-left: 3px;
}


/* ============================================================
   STEP CONTAINERS
   ============================================================ */

div[data-testid="stVerticalBlockBorderWrapper"] {

    background:
        linear-gradient(
            145deg,
            rgba(20, 18, 38, 0.94),
            rgba(10, 9, 22, 0.96)
        );

    border: 1px solid rgba(139, 92, 246, 0.34);

    border-radius: 22px;

    padding: 7px;

    box-shadow:
        0 0 0 1px rgba(139, 92, 246, 0.03),
        0 15px 45px rgba(0, 0, 0, 0.38),
        0 0 35px rgba(124, 58, 237, 0.07);

    transition:
        border-color 0.2s ease,
        box-shadow 0.2s ease;
}


div[data-testid="stVerticalBlockBorderWrapper"]:hover {

    border-color:
        rgba(168, 85, 247, 0.58);

    box-shadow:
        0 18px 50px rgba(0, 0, 0, 0.45),
        0 0 35px rgba(124, 58, 237, 0.13);
}


/* ============================================================
   STEP NUMBER
   ============================================================ */

.step-number {

    width: 42px;
    height: 42px;

    min-width: 42px;

    border-radius: 50%;

    display: flex;

    align-items: center;

    justify-content: center;

    background:
        radial-gradient(
            circle at 35% 30%,
            #d8b4fe,
            #8b5cf6 38%,
            #6d28d9 75%
        );

    color: white;

    font-size: 16px;

    font-weight: 850;

    box-shadow:
        0 0 15px rgba(139, 92, 246, 0.55),
        0 0 35px rgba(124, 58, 237, 0.22);
}


/* ============================================================
   STEP TITLES
   ============================================================ */

.step-title {

    color: #ffffff;

    font-size: 19px;

    font-weight: 800;

    line-height: 1.2;

    margin-bottom: 4px;
}


.step-description {

    color: #aaa5b8;

    font-size: 13px;

    line-height: 1.5;
}


/* ============================================================
   FILE UPLOADER
   ============================================================ */

[data-testid="stFileUploader"] {

    background:
        linear-gradient(
            135deg,
            rgba(30, 24, 57, 0.82),
            rgba(17, 15, 33, 0.92)
        );

    border:
        1.5px dashed
        rgba(139, 92, 246, 0.78);

    border-radius: 18px;

    margin-top: 12px;

    box-shadow:
        inset 0 0 25px
        rgba(124, 58, 237, 0.04);
}


[data-testid="stFileUploader"]:hover {

    border-color:
        #a855f7;

    box-shadow:
        0 0 25px
        rgba(139, 92, 246, 0.13),

        inset 0 0 30px
        rgba(124, 58, 237, 0.06);
}


[data-testid="stFileUploader"] * {
    color: #d6d0df;
}


[data-testid="stFileUploader"] button {

    background:
        linear-gradient(
            135deg,
            #6d28d9,
            #a855f7
        ) !important;

    border: none !important;

    color: white !important;

    border-radius: 11px !important;

    font-weight: 750 !important;
}


/* ============================================================
   INPUT LABELS
   ============================================================ */

label {

    color: #c8c2d2 !important;

    font-size: 13px !important;

    font-weight: 700 !important;
}


/* ============================================================
   TEXT INPUT
   ============================================================ */

.stTextInput input {

    min-height: 50px !important;

    border-radius: 12px !important;

    border:
        1px solid
        rgba(139, 92, 246, 0.32) !important;

    background:
        rgba(19, 17, 37, 0.95) !important;

    color: #ffffff !important;

    font-size: 15px !important;
}


.stTextInput input::placeholder {

    color: #777184 !important;
}


.stTextInput input:focus {

    border-color:
        #9b6cff !important;

    box-shadow:
        0 0 0 2px
        rgba(139, 92, 246, 0.14),

        0 0 20px
        rgba(124, 58, 237, 0.12) !important;
}


/* ============================================================
   DATE INPUT
   ============================================================ */

.stDateInput input {

    min-height: 50px !important;

    border-radius: 12px !important;

    border:
        1px solid
        rgba(139, 92, 246, 0.32) !important;

    background:
        rgba(19, 17, 37, 0.95) !important;

    color: #ffffff !important;

    font-size: 15px !important;
}


.stDateInput input:focus {

    border-color:
        #9b6cff !important;

    box-shadow:
        0 0 0 2px
        rgba(139, 92, 246, 0.14) !important;
}


.stDateInput button {

    color: #b78aff !important;
}


/* ============================================================
   GENERATE BUTTON
   ============================================================ */

.stButton > button {

    width: 100%;

    min-height: 62px;

    border-radius: 15px !important;

    border: 1px solid
        rgba(192, 132, 252, 0.55) !important;

    background:
        linear-gradient(
            90deg,
            #5b21b6,
            #7c3aed,
            #a855f7
        ) !important;

    color: white !important;

    font-size: 16px !important;

    font-weight: 850 !important;

    box-shadow:
        0 8px 28px
        rgba(124, 58, 237, 0.35),

        0 0 22px
        rgba(168, 85, 247, 0.14);

    transition:
        transform 0.18s ease,
        box-shadow 0.18s ease;
}


.stButton > button:hover {

    transform: translateY(-2px);

    box-shadow:
        0 13px 35px
        rgba(124, 58, 237, 0.48),

        0 0 35px
        rgba(168, 85, 247, 0.22);
}


/* ============================================================
   SUCCESS MESSAGE
   ============================================================ */

div[data-testid="stAlert"] {

    border-radius: 14px !important;

    background:
        rgba(48, 20, 75, 0.65) !important;

    border:
        1px solid
        rgba(168, 85, 247, 0.38) !important;

    color: #e9ddff !important;
}


/* ============================================================
   SUMMARY METRICS
   ============================================================ */

div[data-testid="stMetric"] {

    background:
        rgba(17, 14, 32, 0.92);

    border:
        1px solid
        rgba(139, 92, 246, 0.24);

    border-radius: 13px;

    padding: 12px;
}


div[data-testid="stMetricLabel"] {

    color: #91889e !important;

    font-size: 11px !important;

    font-weight: 700 !important;
}


div[data-testid="stMetricValue"] {

    color: #d8b4fe !important;

    font-size: 18px !important;

    font-weight: 800 !important;
}


/* ============================================================
   DOWNLOAD BUTTON
   ============================================================ */

.stDownloadButton > button {

    width: 100%;

    min-height: 60px;

    border-radius: 14px !important;

    border:
        1px solid
        rgba(168, 85, 247, 0.72) !important;

    background:
        rgba(18, 15, 34, 0.96) !important;

    color: #d8b4fe !important;

    font-size: 15px !important;

    font-weight: 850 !important;

    box-shadow:
        0 0 20px
        rgba(124, 58, 237, 0.10);
}


.stDownloadButton > button:hover {

    background:
        linear-gradient(
            135deg,
            rgba(109, 40, 217, 0.20),
            rgba(168, 85, 247, 0.18)
        ) !important;

    border-color:
        #c084fc !important;

    color: white !important;
}


/* ============================================================
   SPINNER
   ============================================================ */

.stSpinner > div {

    border-top-color:
        #a855f7 !important;
}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 600px) {

    .main .block-container {

        padding-top: 25px;

        padding-left: 12px;

        padding-right: 12px;

        padding-bottom: 45px;
    }


    .page-title {

        font-size: 27px;

        line-height: 1.2;
    }


    .page-subtitle {

        font-size: 12px;

        margin-bottom: 27px;
    }


    div[data-testid="stVerticalBlockBorderWrapper"] {

        border-radius: 18px;

        padding: 5px;
    }


    .step-number {

        width: 38px;
        height: 38px;

        min-width: 38px;

        font-size: 14px;
    }


    .step-title {

        font-size: 16px;
    }


    .step-description {

        font-size: 12px;
    }


    .stButton > button {

        min-height: 58px;

        font-size: 15px;
    }


    .stDownloadButton > button {

        min-height: 58px;
    }
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="page-title">SMSS Transport Bill Generator</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="page-subtitle">'
    'Create professional transport bills ❤️💕'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# STEP 1 — UPLOAD
# ============================================================

st.markdown(
    '<div class="section-label">STEP 01</div>',
    unsafe_allow_html=True,
)


with st.container(border=True):

    icon_col, text_col = st.columns(
        [0.08, 0.92],
        vertical_alignment="center",
    )

    with icon_col:

        st.markdown(
            '<div class="step-number">1</div>',
            unsafe_allow_html=True,
        )

    with text_col:

        st.markdown(
            '<div class="step-title">'
            'Upload Excel Bill'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="step-description">'
            'Select the Excel file received from the customer.'
            '</div>',
            unsafe_allow_html=True,
        )

    st.write("")

    uploaded_file = st.file_uploader(
        "Choose Excel file",
        type=["xlsx", "xlsm"],
        label_visibility="collapsed",
    )


if uploaded_file is not None:

    st.success(
        f"✓ {uploaded_file.name} is ready"
    )


# ============================================================
# STEP 2 — BILL DETAILS
# ============================================================

st.markdown(
    '<div class="section-label">STEP 02</div>',
    unsafe_allow_html=True,
)


with st.container(border=True):

    icon_col, text_col = st.columns(
        [0.08, 0.92],
        vertical_alignment="center",
    )

    with icon_col:

        st.markdown(
            '<div class="step-number">2</div>',
            unsafe_allow_html=True,
        )

    with text_col:

        st.markdown(
            '<div class="step-title">'
            'Bill Details'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="step-description">'
            'Enter the bill number and select the bill date.'
            '</div>',
            unsafe_allow_html=True,
        )

    st.write("")

    col1, col2 = st.columns(
        2,
        gap="medium",
    )

    with col1:

        bill_no = st.text_input(
            "Bill Number",
            placeholder="Example: SF025",
        )

    with col2:

        bill_date = st.date_input(
            "Bill Date",
            value=date.today(),
            format="DD.MM.YYYY",
        )


# ============================================================
# STEP 3 — GENERATE
# ============================================================

st.markdown(
    '<div class="section-label">STEP 03</div>',
    unsafe_allow_html=True,
)


with st.container(border=True):

    icon_col, text_col = st.columns(
        [0.08, 0.92],
        vertical_alignment="center",
    )

    with icon_col:

        st.markdown(
            '<div class="step-number">3</div>',
            unsafe_allow_html=True,
        )

    with text_col:

        st.markdown(
            '<div class="step-title">'
            'Generate Bill'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="step-description">'
            'Validate the Excel data and create the final PDF.'
            '</div>',
            unsafe_allow_html=True,
        )

    st.write("")

    generate_button = st.button(
        "▣   Generate Bill PDF   →",
        type="primary",
        use_container_width=True,
    )


# ============================================================
# GENERATION PIPELINE
# ============================================================

if generate_button:

    # --------------------------------------------------------
    # INPUT VALIDATION
    # --------------------------------------------------------

    if uploaded_file is None:

        st.error(
            "Please upload the Excel bill first."
        )

        st.stop()


    if not bill_no.strip():

        st.error(
            "Please enter the bill number."
        )

        st.stop()


    temp_path = None


    try:

        # ====================================================
        # 1. CREATE TEMPORARY EXCEL FILE
        # ====================================================

        with st.spinner(
            "Reading Excel bill..."
        ):

            suffix = Path(
                uploaded_file.name
            ).suffix

            temp_file = tempfile.NamedTemporaryFile(
                mode="wb",
                delete=False,
                suffix=suffix,
            )

            temp_file.write(
                uploaded_file.getbuffer()
            )

            temp_file.close()

            temp_path = Path(
                temp_file.name
            )


        # ====================================================
        # 2. READ EXCEL
        # ====================================================

        reader = ExcelBillReader(
            temp_path
        )

        excel_data = reader.read()


        # ====================================================
        # 3. BUILD BILL
        # ====================================================

        with st.spinner(
            "Preparing bill..."
        ):

            formatted_date = (
                bill_date.strftime(
                    "%d.%m.%Y"
                )
            )

            bill_generator = BillGenerator(
                bill_no=bill_no.strip(),
                bill_date=formatted_date,
            )

            bill = bill_generator.build(
                excel_data
            )


        # ====================================================
        # 4. VALIDATE BILL
        # ====================================================

        with st.spinner(
            "Validating bill..."
        ):

            validator = BillValidator(
                bill
            )

            validation_result = (
                validator.validate()
            )


        # ====================================================
        # VALIDATION FAILURE
        # ====================================================

        if not validation_result:

            st.error(
                "Bill validation failed."
            )

            for error in validator.errors:

                st.error(
                    str(error)
                )

            st.stop()


        # ====================================================
        # 5. GENERATE PDF
        # ====================================================

        with st.spinner(
            "Generating PDF..."
        ):

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            output_path = (
                OUTPUT_DIR
                /
                f"{bill_no.strip()}"
                f"_bill_{timestamp}.pdf"
            )

            pdf_generator = PDFBillGenerator(
                output_path
            )

            generated_file = (
                pdf_generator.generate(
                    bill
                )
            )


        # ====================================================
        # 6. SAVE SESSION STATE
        # ====================================================

        st.session_state.generated_pdf_path = (
            Path(generated_file)
        )

        st.session_state.generated_bill = (
            bill
        )


        # ====================================================
        # 7. SUCCESS
        # ====================================================

        st.success(
            f"✓ Bill {bill.bill_no} generated successfully!"
        )


        # ====================================================
        # 8. BILL SUMMARY
        # ====================================================

        st.markdown(
            '<div class="section-label">BILL SUMMARY</div>',
            unsafe_allow_html=True,
        )


        # ----------------------------------------------------
        # Native Streamlit summary
        # ----------------------------------------------------

        with st.container(border=True):

            st.markdown(
                "### Bill Generated"
            )

            st.caption(
                "Review the details before downloading the PDF."
            )

            summary_col1, summary_col2 = st.columns(
                2,
                gap="medium",
            )


            with summary_col1:

                st.metric(
                    label="Bill Number",
                    value=str(
                        bill.bill_no
                    ),
                )


            with summary_col2:

                st.metric(
                    label="Bill Date",
                    value=str(
                        bill.bill_date
                    ),
                )


            summary_col3, summary_col4 = st.columns(
                2,
                gap="medium",
            )


            with summary_col3:

                st.metric(
                    label="Total Quantity",
                    value=(
                        f"{bill.total_quantity:g} KG"
                    ),
                )


            with summary_col4:

                st.metric(
                    label="Total Freight",
                    value=(
                        f"₹{float(bill.total_freight):,.2f}"
                    ),
                )


        # ====================================================
        # 9. DOWNLOAD
        # ====================================================

        st.markdown(
            '<div class="section-label">DOWNLOAD</div>',
            unsafe_allow_html=True,
        )


        with open(
            generated_file,
            "rb",
        ) as pdf_file:

            pdf_bytes = pdf_file.read()


        st.download_button(
            label="⬇   Download Bill PDF",
            data=pdf_bytes,
            file_name=(
                f"{bill.bill_no}_bill.pdf"
            ),
            mime="application/pdf",
            use_container_width=True,
        )


    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except Exception as error:

        st.error(
            "Something went wrong while generating the bill."
        )

        st.exception(
            error
        )


    # ========================================================
    # CLEAN TEMPORARY FILE
    # ========================================================

    finally:

        try:

            if (
                temp_path is not None
                and temp_path.exists()
            ):

                temp_path.unlink()

        except Exception:

            pass
```markdown
# 🧾 SMSS Transport Bill Generator

A web-based transport bill generation system built for **SMSS Transport**.

The application automates the manual process of converting transport billing data from an Excel file into a professionally formatted PDF bill.

It is designed to be simple enough for non-technical users: upload the Excel file, enter the bill details, generate the bill, and download the final PDF.

---

## 🚀 Live Application

**SMSS Transport Bill Generator**

https://smss-transport-bill-generator.onrender.com

> The application is deployed using Render and can be accessed from a laptop, tablet, or mobile phone.

---

## ✨ Features

- 📤 Upload transport billing Excel files
- 🧾 Enter Bill Number
- 📅 Enter Bill Date
- 📊 Automatically read billing data from Excel
- 🔍 Validate extracted billing information
- 💰 Calculate total freight
- 🔢 Calculate total dispatched quantity
- 📝 Convert total amount into words
- 📄 Generate a professionally formatted PDF bill
- 📱 Mobile-friendly web interface
- ⬇️ Download the generated PDF
- ⚡ No Microsoft Word or WPS Office required
- ☁️ Cloud deployed and accessible from anywhere

---

## 🔄 How It Works

```text
Excel Bill
    ↓
Excel Reader
    ↓
Data Validation
    ↓
Bill Data Model
    ↓
Amount in Words
    ↓
PDF Generator
    ↓
Formatted Transport Bill
    ↓
Download PDF
```

---

## 👤 User Workflow

The application is intentionally kept simple.

### Step 1 — Upload Excel

Upload the transport company's Excel billing file.

### Step 2 — Enter Bill Details

Enter:

- Bill Number
- Bill Date

### Step 3 — Generate Bill

The application:

1. Reads the Excel file
2. Identifies the billing table
3. Extracts the required rows
4. Calculates totals
5. Validates the bill data
6. Generates the PDF
7. Provides the PDF for download

---

## 🏗️ Project Structure

```text
smss-transport-bill-generator/
│
├── app/
│   ├── main.py
│   ├── config.py
│   │
│   ├── assets/
│   │   └── smss_logo.jpeg
│   │
│   ├── services/
│   │   ├── bill_generator.py
│   │   ├── bill_model.py
│   │   ├── excel_reader.py
│   │   ├── pdf_generator.py
│   │   └── validator.py
│   │
│   └── utils/
│       ├── amount_words.py
│       └── formatters.py
│
├── tests/
│   ├── test_amount_words.py
│   ├── test_bill_generator.py
│   ├── test_bill_model.py
│   ├── test_excel_reader.py
│   ├── test_pdf_generator.py
│   └── test_validator.py
│
├── data/
│   ├── input/
│   └── output/
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🧩 Core Components

### Excel Reader

Reads the uploaded Excel workbook and dynamically identifies:

- Header row
- Billing rows
- Total row
- Quantity
- Freight
- Invoice information
- Vehicle information

The reader is designed to handle changes in the number of billing rows.

---

### Bill Data Model

Provides a structured representation of the extracted billing information.

The model keeps the billing data organized before it is passed to validation and PDF generation.

---

### Validator

Validates the generated bill data before PDF generation.

This helps prevent incomplete or invalid billing information from being processed.

---

### Amount in Words

The application converts the total freight amount into Indian-numbering-system words.

Example:

```text
159405.25
```

becomes:

```text
ONE LAKH FIFTY NINE THOUSAND FOUR HUNDRED FIVE ONLY
```

The amount in words is rounded to the nearest whole rupee while the original decimal amount is preserved for bill calculations.

---

### PDF Generator

Generates the final transport bill using ReportLab.

The PDF generator handles:

- Company header
- Customer information
- Bill number
- Bill date
- Billing table
- Dynamic table sizing
- Total quantity
- Total freight
- Amount in words
- Footer information
- Authorized signatory
- Company branding

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend/application logic |
| Streamlit | Web interface |
| Pandas | Data processing |
| OpenPyXL | Excel processing |
| ReportLab | PDF generation |
| Jinja2 | Template support |
| Num2Words | Number-to-word conversion |
| Pytest | Automated testing |
| Git | Version control |
| GitHub | Source code hosting |
| Render | Cloud deployment |

---

## 🧪 Testing

The project includes automated tests covering the major components:

- Excel reader
- Amount conversion
- Validation
- Bill data model
- Bill generation
- PDF generation

Run the complete test suite using:

```bash
python -m pytest -s
```

Expected result:

```text
23 passed
```

---

## 💻 Local Development

### 1. Clone the repository

```bash
git clone https://github.com/Deepthi2006/smss-transport-bill-generator.git
```

### 2. Enter the project

```bash
cd smss-transport-bill-generator
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the environment

#### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
python -m streamlit run app/main.py
```

The application will be available at:

```text
http://localhost:8501
```

---

## ☁️ Deployment

The application is deployed using **Render**.

The deployment is connected directly to the GitHub repository.

Changes pushed to the `main` branch can trigger a new deployment when automatic deployment is enabled.

### Production Start Command

```bash
python -m streamlit run app/main.py --server.address 0.0.0.0 --server.port $PORT
```

---

## 🔐 Data & Privacy

The repository does not contain actual customer Excel files or generated billing PDFs.

The following are excluded using `.gitignore`:

```text
data/input/
data/output/
.env
.venv/
__pycache__/
.pytest_cache/
```

Actual billing files should be uploaded directly through the application rather than committed to the repository.

---

## 📱 Designed for Practical Use

The application was built to replace a manual workflow involving:

```text
Excel
   ↓
WPS / Microsoft Word
   ↓
Manual copying
   ↓
Manual formatting
   ↓
Amount in words
   ↓
PDF conversion
   ↓
Send bill
```

with:

```text
Upload Excel
      ↓
Enter Bill Details
      ↓
Generate
      ↓
Download PDF
```

This allows the bill to be generated without requiring Microsoft Word or WPS Office.

---

## 🔮 Future Improvements

Potential future features include:

- Automatic bill number generation
- Bill history
- Search previous bills
- Customer-wise billing history
- Automatic PDF naming
- Email bill directly from the application
- WhatsApp sharing workflow
- Database integration
- Cloud storage for generated bills
- Multiple bill templates
- User authentication
- Dashboard and billing analytics

---

## 👨‍💻 Project

**SMSS Transport Bill Generator**

Built as a practical automation solution for transport billing.

---

## 📄 License

This project is intended for private/internal use by SMSS Transport.
```
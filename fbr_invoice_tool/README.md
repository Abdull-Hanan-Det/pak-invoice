# 🧾 PakInvoice — Pakistani Invoice & Tax Tool

> Free, FBR-compliant business tools for Pakistani SMEs.
> Built with Python + Streamlit.

---

## 🚀 VS Code mein kaise chalayein

### Step 1 — VS Code mein folder open karo
```
File → Open Folder → fbr_invoice_tool folder select karo
```

### Step 2 — Terminal kholo
```
VS Code mein: Ctrl + ` (backtick)
```

### Step 3 — Virtual environment banao
```bash
python -m venv venv
```

### Step 4 — Activate karo
```bash
# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```
Terminal mein `(venv)` likhna chahiye — confirm hai ke active hai.

### Step 5 — Libraries install karo
```bash
pip install -r requirements.txt
```

### Step 6 — App chalao
```bash
streamlit run app.py
```

Browser mein khul jayega: **http://localhost:8501** ✅

---

## 📁 Project Structure

```
fbr_invoice_tool/
├── app.py                          ← Home page (yahan se start karo)
├── requirements.txt                ← Libraries list
├── README.md                       ← Yeh file
├── pages/
│   ├── 1_Invoice_Generator.py      ← Invoice + GST + WHT tool
│   └── 2_Income_Tax_Calculator.py  ← FBR income tax calculator
└── modules/
    ├── __init__.py
    ├── tax_calculator.py           ← Tax logic (GST, WHT, slabs)
    ├── invoice_generator.py        ← HTML invoice template
    └── pdf_export.py               ← PDF export
```

---

## 🛠️ Features

### 🧾 Invoice Generator
- GST rates 0% to 25% (FBR 2024-25)
- NTN & STRN fields
- Withholding Tax (WHT) Section 153
- Discount + Shipping
- HTML download (seedha print ho)
- PDF download (weasyprint se)
- Multi-currency: PKR, USD, AED

### 💰 Income Tax Calculator
- FBR 2024-25 salaried + business slabs
- Monthly / Annual income input
- Deductions: HRA, medical, zakat, donations
- Pie chart + bar chart
- What-if scenarios
- Active / Non-filer comparison
- Tax saving tips

---

## ❓ Common Issues

**`streamlit` command not found?**
```bash
pip install streamlit
```

**Matplotlib error?**
```bash
pip install matplotlib pandas
```

**PDF export kaam nahi kar raha?**
```bash
pip install weasyprint
# Linux pe:
sudo apt-get install libpango-1.0-0
```

---

## 💰 Sell Kaise Karein

1. **GitHub pe upload karo** (free)
2. **Streamlit Cloud pe deploy karo** → streamlit.io/cloud (free hosting)
3. **Traffic aaye toh Flippa pe list karo** → $500–$3000+
4. **WhatsApp/Facebook pe share karo** accountants aur small business groups mein

---

Made with ❤️ in Pakistan | FBR Finance Act 2024-25

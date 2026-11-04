import streamlit as st

st.set_page_config(
    page_title="PakInvoice — Pakistani Business Tools",
    page_icon="🧾",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .hero {
        background: linear-gradient(135deg, #1a5f3f 0%, #2d8a5e 100%);
        padding: 3rem 2rem; border-radius: 16px; color: white;
        text-align: center; margin-bottom: 2.5rem;
    }
    .hero h1 { font-size: 2.8rem; font-weight: 700; margin: 0; letter-spacing: -1px; }
    .hero p  { opacity: 0.85; font-size: 1.1rem; margin: 0.6rem 0 0; }
    .tool-card {
        background: white; border: 2px solid #e8f5ee; border-radius: 14px;
        padding: 2rem; text-align: center;
        transition: all 0.2s; height: 100%;
    }
    .tool-card:hover { border-color: #1a5f3f; transform: translateY(-3px); box-shadow: 0 8px 24px rgba(26,95,63,0.12); }
    .tool-icon  { font-size: 3rem; margin-bottom: 1rem; }
    .tool-title { font-size: 1.2rem; font-weight: 700; color: #1a5f3f; margin-bottom: 0.5rem; }
    .tool-desc  { font-size: 0.88rem; color: #666; line-height: 1.6; }
    .badge { display:inline-block; background:#e8f5ee; color:#1a5f3f; border-radius:20px;
             padding:3px 10px; font-size:0.72rem; font-weight:600; margin-top:0.8rem; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🧾 PakInvoice</h1>
    <p>Pakistani businesses ke liye free financial tools — FBR compliant, fast, easy</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 🛠️ Available Tools")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-icon">🧾</div>
        <div class="tool-title">Invoice Generator</div>
        <div class="tool-desc">
            Professional Pakistani invoices banayein. FBR-compliant GST calculation,
            WHT deduction, NTN/STRN fields, aur HTML/PDF download.
        </div>
        <div>
            <span class="badge">FBR GST 2024</span>
            <span class="badge">WHT</span>
            <span class="badge">PDF Export</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_Invoice_Generator.py", label="Open Invoice Generator →", use_container_width=True)

with c2:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-icon">💰</div>
        <div class="tool-title">Income Tax Calculator</div>
        <div class="tool-desc">
            FBR 2024-25 tax slabs ke mutabiq apna income tax calculate karein.
            Salaried aur business income, deductions, what-if scenarios, charts.
        </div>
        <div>
            <span class="badge">2024-25 Slabs</span>
            <span class="badge">Deductions</span>
            <span class="badge">Charts</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_Income_Tax_Calculator.py", label="Open Tax Calculator →", use_container_width=True)

with c3:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-icon">📊</div>
        <div class="tool-title">Excel & PDF Tools</div>
        <div class="tool-desc">
            Excel se invoice banao. Invoice ko Excel/CSV export karo.
            PDF upload karo aur text/amounts extract karo — sab ek jagah.
        </div>
        <div>
            <span class="badge">Excel Import</span>
            <span class="badge">Excel Export</span>
            <span class="badge">PDF Extract</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/3_Excel_PDF_Tools.py", label="Open Excel & PDF Tools →", use_container_width=True)

st.divider()
st.markdown("""
<div style="text-align:center;color:#888;font-size:0.82rem;padding:1rem">
    🧾 <strong>PakInvoice</strong> — Free Pakistani Business Tools &nbsp;|&nbsp;
    FBR Finance Act 2024-25 &nbsp;|&nbsp; Made with ❤️ in Pakistan
</div>
""", unsafe_allow_html=True)

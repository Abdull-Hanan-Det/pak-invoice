import streamlit as st
from datetime import date
import json

# Page config
st.set_page_config(
    page_title="PakInvoice - Pakistani Invoice & Tax Tool",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1a5f3f 0%, #2d8a5e 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .main-header h1 {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .main-header p {
        opacity: 0.85;
        margin: 0.5rem 0 0;
        font-size: 1rem;
    }
    
    .invoice-box {
        background: white;
        border: 2px solid #e8f5ee;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .section-title {
        color: #1a5f3f;
        font-weight: 600;
        font-size: 1rem;
        border-bottom: 2px solid #e8f5ee;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .tax-summary-card {
        background: #f0faf5;
        border: 1px solid #c3e6d4;
        border-radius: 10px;
        padding: 1.2rem;
        margin: 0.5rem 0;
    }
    
    .total-card {
        background: #1a5f3f;
        color: white;
        border-radius: 10px;
        padding: 1.2rem;
        margin: 0.5rem 0;
        text-align: center;
    }
    
    .total-card h2 {
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
    }
    
    .total-card p {
        margin: 0;
        opacity: 0.8;
        font-size: 0.85rem;
    }
    
    .stButton > button {
        background: #1a5f3f;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        width: 100%;
        font-size: 1rem;
    }
    
    .stButton > button:hover {
        background: #2d8a5e;
        border: none;
    }
    
    .item-row {
        background: #fafafa;
        border: 1px solid #eee;
        border-radius: 8px;
        padding: 0.8rem;
        margin-bottom: 0.5rem;
    }
    
    .fbr-badge {
        background: #fff3cd;
        border: 1px solid #ffc107;
        border-radius: 6px;
        padding: 0.4rem 0.8rem;
        font-size: 0.8rem;
        color: #856404;
        font-weight: 500;
    }
    
    .stAlert {
        border-radius: 8px;
    }
    
    div[data-testid="metric-container"] {
        background: #f0faf5;
        border: 1px solid #c3e6d4;
        border-radius: 10px;
        padding: 1rem;
    }
    
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        border-radius: 6px;
        border: 1px solid #d1e8db;
    }
    
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Import modules
from modules.tax_calculator import calculate_gst, calculate_income_tax, calculate_wht
from modules.invoice_generator import generate_invoice_html
from modules.pdf_export import export_to_pdf

# ── SESSION STATE ──────────────────────────────────────────────
if 'items' not in st.session_state:
    st.session_state['items'] = []
if 'invoice_number' not in st.session_state:
    st.session_state.invoice_number = "INV-2024-001"

# ── HEADER ────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🧾 PakInvoice</h1>
    <p>Pakistani Invoice Generator & FBR Tax Calculator — Free, Fast, Accurate</p>
    <div style="margin-top:0.8rem">
        <span class="fbr-badge">✓ FBR Compliant</span>&nbsp;
        <span class="fbr-badge">✓ GST 2024 Rates</span>&nbsp;
        <span class="fbr-badge">✓ WHT Calculation</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    currency = st.selectbox("Currency", ["PKR (Rs.)", "USD ($)", "AED (د.إ)"])
    curr_symbol = "Rs." if "PKR" in currency else ("$" if "USD" in currency else "AED")
    
    st.divider()
    st.markdown("### 📋 Invoice Info")
    invoice_no = st.text_input("Invoice Number", value=st.session_state.invoice_number)
    invoice_date = st.date_input("Invoice Date", value=date.today())
    due_date = st.date_input("Due Date")
    
    st.divider()
    st.markdown("### 🏢 Your Business")
    business_name = st.text_input("Business Name", placeholder="Ali Traders")
    business_ntn = st.text_input("NTN Number", placeholder="1234567-8")
    business_strn = st.text_input("STRN (Sales Tax)", placeholder="12-34-5678-001-23")
    business_address = st.text_area("Address", placeholder="Shop #5, Main Market, Lahore", height=80)
    business_phone = st.text_input("Phone", placeholder="0300-1234567")

# ── MAIN CONTENT ──────────────────────────────────────────────
col_left, col_right = st.columns([3, 2])

with col_left:
    # ── CUSTOMER INFO ──
    st.markdown('<div class="section-title">👤 Customer / Client Details</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        customer_name = st.text_input("Customer Name", placeholder="Muhammad Raza")
        customer_ntn = st.text_input("Customer NTN", placeholder="Optional")
    with c2:
        customer_address = st.text_area("Customer Address", placeholder="Gulberg, Lahore", height=80)
        customer_phone = st.text_input("Customer Phone", placeholder="0321-9876543")

    st.divider()

    # ── ITEMS ──
    st.markdown('<div class="section-title">📦 Items / Services</div>', unsafe_allow_html=True)

    # Add item form
    with st.expander("➕ Add New Item", expanded=len(st.session_state['items']) == 0):
        i1, i2 = st.columns([3, 1])
        with i1:
            item_name = st.text_input("Item / Service Name", placeholder="Website Design Services")
            item_desc = st.text_input("Description (optional)", placeholder="Custom WordPress website")
        with i2:
            item_qty = st.number_input("Quantity", min_value=1, value=1)
            item_rate = st.number_input(f"Rate ({curr_symbol})", min_value=0.0, value=0.0, step=100.0)
        
        item_gst_rate = st.selectbox(
            "GST Rate",
            ["0% (Exempt)", "5%", "8%", "10%", "13%", "15% (Standard)", "17%", "18%", "25%"],
            index=5
        )
        
        if st.button("Add Item ✓"):
            if item_name and item_rate > 0:
                gst_pct = float(item_gst_rate.split("%")[0])
                subtotal = item_qty * item_rate
                gst_amount = subtotal * gst_pct / 100
                st.session_state['items'].append({
                    "name": item_name,
                    "desc": item_desc,
                    "qty": item_qty,
                    "rate": item_rate,
                    "subtotal": subtotal,
                    "gst_rate": gst_pct,
                    "gst_amount": gst_amount,
                    "total": subtotal + gst_amount
                })
                st.success(f"✓ '{item_name}' added!")
                st.rerun()
            else:
                st.error("Item name aur rate zaroor daalen.")

    # Show items
    if st.session_state['items']:
        st.markdown(f"**{len(st.session_state['items'])} item(s) added:**")
        for i, item in enumerate(st.session_state['items']):
            with st.container():
                r1, r2, r3, r4 = st.columns([4, 1, 2, 1])
                with r1:
                    st.markdown(f"**{item['name']}**")
                    if item['desc']:
                        st.caption(item['desc'])
                with r2:
                    st.markdown(f"Qty: **{item['qty']}**")
                with r3:
                    st.markdown(f"{curr_symbol} {item['total']:,.0f}")
                    st.caption(f"GST {item['gst_rate']}%: {curr_symbol} {item['gst_amount']:,.0f}")
                with r4:
                    if st.button("🗑️", key=f"del_{i}"):
                        st.session_state['items'].pop(i)
                        st.rerun()
                st.divider()

    # ── ADDITIONAL CHARGES ──
    st.divider()
    st.markdown('<div class="section-title">➕ Additional Charges / Deductions</div>', unsafe_allow_html=True)
    
    a1, a2 = st.columns(2)
    with a1:
        discount = st.number_input(f"Discount ({curr_symbol})", min_value=0.0, value=0.0, step=100.0)
        shipping = st.number_input(f"Delivery / Shipping ({curr_symbol})", min_value=0.0, value=0.0, step=50.0)
    with a2:
        wht_applicable = st.checkbox("Withholding Tax (WHT) applicable?", value=False)
        if wht_applicable:
            wht_type = st.selectbox("WHT Type", [
                "Services - 8% (Filer)",
                "Services - 15% (Non-Filer)",
                "Goods - 4.5% (Filer)",
                "Goods - 9% (Non-Filer)",
                "Rent - 15% (Filer)",
                "Rent - 30% (Non-Filer)",
            ])
        
        payment_terms = st.selectbox("Payment Terms", [
            "Due on Receipt",
            "Net 7 Days",
            "Net 15 Days",
            "Net 30 Days",
            "50% Advance, 50% on Delivery",
        ])

    # Notes
    notes = st.text_area("Notes / Terms & Conditions (optional)",
        placeholder="Thank you for your business!\nPayment via bank transfer: HBL Account 1234-5678",
        height=80)

with col_right:
    # ── TAX SUMMARY ──
    st.markdown('<div class="section-title">🧮 Tax Summary</div>', unsafe_allow_html=True)

    if st.session_state['items']:
        # Calculate totals
        subtotal = sum(i['subtotal'] for i in st.session_state['items'])
        total_gst = sum(i['gst_amount'] for i in st.session_state['items'])
        
        after_discount = subtotal - discount + shipping
        
        wht_amount = 0
        if wht_applicable:
            wht_pct = float(wht_type.split(" - ")[1].split("%")[0])
            wht_amount = after_discount * wht_pct / 100
        
        grand_total = after_discount + total_gst - wht_amount

        # Display metrics
        st.metric("Subtotal (before GST)", f"{curr_symbol} {subtotal:,.0f}")
        st.metric("Total GST", f"{curr_symbol} {total_gst:,.0f}")
        
        if discount > 0:
            st.metric("Discount", f"- {curr_symbol} {discount:,.0f}")
        if shipping > 0:
            st.metric("Shipping", f"+ {curr_symbol} {shipping:,.0f}")
        if wht_amount > 0:
            st.metric(f"WHT Deduction", f"- {curr_symbol} {wht_amount:,.0f}")

        st.markdown(f"""
        <div class="total-card">
            <p>Grand Total</p>
            <h2>{curr_symbol} {grand_total:,.0f}</h2>
            <p style="margin-top:0.3rem">{payment_terms if 'payment_terms' in dir() else 'Due on Receipt'}</p>
        </div>
        """, unsafe_allow_html=True)

        # FBR Tax breakdown
        st.markdown("---")
        st.markdown("**📊 GST Breakdown by Rate:**")
        gst_by_rate = {}
        for item in st.session_state['items']:
            rate = item['gst_rate']
            if rate not in gst_by_rate:
                gst_by_rate[rate] = {"taxable": 0, "gst": 0}
            gst_by_rate[rate]["taxable"] += item['subtotal']
            gst_by_rate[rate]["gst"] += item['gst_amount']

        for rate, vals in gst_by_rate.items():
            if rate == 0:
                st.info(f"0% Exempt: {curr_symbol} {vals['taxable']:,.0f}")
            else:
                st.success(f"{rate}% GST on {curr_symbol} {vals['taxable']:,.0f} = **{curr_symbol} {vals['gst']:,.0f}**")

        # ── GENERATE INVOICE ──
        st.markdown("---")
        st.markdown("**📄 Generate Invoice:**")

        invoice_data = {
            "invoice_no": invoice_no,
            "invoice_date": str(invoice_date),
            "due_date": str(due_date),
            "business": {
                "name": business_name or "Your Business Name",
                "ntn": business_ntn,
                "strn": business_strn,
                "address": business_address,
                "phone": business_phone,
            },
            "customer": {
                "name": customer_name or "Customer Name",
                "ntn": customer_ntn,
                "address": customer_address,
                "phone": customer_phone,
            },
            "items": st.session_state['items'],
            "subtotal": subtotal,
            "total_gst": total_gst,
            "discount": discount,
            "shipping": shipping,
            "wht_amount": wht_amount,
            "grand_total": grand_total,
            "currency": curr_symbol,
            "payment_terms": payment_terms if 'payment_terms' in dir() else "Due on Receipt",
            "notes": notes,
        }

        html_invoice = generate_invoice_html(invoice_data)

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            st.download_button(
                "⬇️ Download HTML",
                data=html_invoice,
                file_name=f"{invoice_no}.html",
                mime="text/html",
                use_container_width=True
            )
        with col_btn2:
            try:
                pdf_bytes = export_to_pdf(html_invoice)
                st.download_button(
                    "📄 Download PDF",
                    data=pdf_bytes,
                    file_name=f"{invoice_no}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception:
                st.info("PDF: `pip install weasyprint`")

        # Preview
        with st.expander("👁️ Preview Invoice"):
            st.components.v1.html(html_invoice, height=600, scrolling=True)

    else:
        st.info("👈 Pehle koi item add karein")
        
        # Quick demo
        st.markdown("**Quick Demo:**")
        if st.button("Load Sample Invoice"):
            st.session_state['items'] = [
                {"name": "Website Design", "desc": "5-page WordPress site", "qty": 1,
                 "rate": 50000, "subtotal": 50000, "gst_rate": 15, "gst_amount": 7500, "total": 57500},
                {"name": "Logo Design", "desc": "Brand identity package", "qty": 1,
                 "rate": 15000, "subtotal": 15000, "gst_rate": 15, "gst_amount": 2250, "total": 17250},
                {"name": "Monthly Hosting", "desc": "cPanel hosting 1 year", "qty": 12,
                 "rate": 1500, "subtotal": 18000, "gst_rate": 0, "gst_amount": 0, "total": 18000},
            ]
            st.rerun()

# ── FOOTER ───────────────────────────────────────────────────
st.divider()
st.markdown("""
<div style="text-align:center; color:#888; font-size:0.8rem; padding:1rem">
    🧾 <strong>PakInvoice</strong> — Free Pakistani Invoice & FBR Tax Tool &nbsp;|&nbsp; 
    GST rates per FBR 2024 &nbsp;|&nbsp; 
    Made with ❤️ in Pakistan
</div>
""", unsafe_allow_html=True)

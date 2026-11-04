import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

st.set_page_config(
    page_title="Income Tax Calculator — PakInvoice",
    page_icon="💰",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .main-header {
        background: linear-gradient(135deg, #1a5f3f 0%, #2d8a5e 100%);
        padding: 2rem; border-radius: 12px; color: white;
        margin-bottom: 2rem; text-align: center;
    }
    .main-header h1 { font-size: 2rem; font-weight: 700; margin: 0; }
    .main-header p  { opacity: 0.85; margin: 0.4rem 0 0; font-size: 0.95rem; }

    .result-card {
        background: #f0faf5; border: 1px solid #c3e6d4;
        border-radius: 10px; padding: 1.2rem; margin: 0.5rem 0;
    }
    .total-card {
        background: #1a5f3f; color: white; border-radius: 10px;
        padding: 1.4rem; text-align: center; margin: 0.5rem 0;
    }
    .total-card h2 { margin: 0; font-size: 2rem; font-weight: 700; }
    .total-card p  { margin: 0; opacity: 0.8; font-size: 0.85rem; }

    .slab-row {
        display: flex; justify-content: space-between; align-items: center;
        padding: 8px 12px; border-radius: 6px; margin-bottom: 4px;
        font-size: 0.85rem;
    }
    .slab-active  { background: #d4edda; border-left: 4px solid #1a5f3f; font-weight: 600; }
    .slab-inactive{ background: #f8f9fa; border-left: 4px solid #dee2e6; color: #888; }

    .section-title {
        color: #1a5f3f; font-weight: 600; font-size: 1rem;
        border-bottom: 2px solid #e8f5ee; padding-bottom: 6px; margin-bottom: 1rem;
    }
    .stButton > button {
        background: #1a5f3f; color: white; border: none;
        border-radius: 8px; font-weight: 600; width: 100%;
    }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── HEADER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>💰 Income Tax Calculator</h1>
    <p>FBR 2024-25 Tax Slabs — Salaried & Business Income</p>
</div>
""", unsafe_allow_html=True)

# ── TAX SLABS DATA ───────────────────────────────────────────────────────────
SALARIED_SLABS = [
    (0,          600_000,    0,         0,    "Zero tax"),
    (600_001,    1_200_000,  0,         2.5,  "2.5% on amount above 6 lac"),
    (1_200_001,  2_400_000,  15_000,    12.5, "Rs.15,000 + 12.5% above 12 lac"),
    (2_400_001,  3_600_000,  165_000,   22.5, "Rs.1,65,000 + 22.5% above 24 lac"),
    (3_600_001,  6_000_000,  435_000,   27.5, "Rs.4,35,000 + 27.5% above 36 lac"),
    (6_000_001,  12_000_000, 1_095_000, 35,   "Rs.10,95,000 + 35% above 60 lac"),
    (12_000_001, float('inf'),3_195_000,45,   "Rs.31,95,000 + 45% above 1.2 crore"),
]

BUSINESS_SLABS = [
    (0,          600_000,    0,         0,    "Zero tax"),
    (600_001,    1_200_000,  0,         15,   "15% on amount above 6 lac"),
    (1_200_001,  1_600_000,  90_000,    20,   "Rs.90,000 + 20% above 12 lac"),
    (1_600_001,  3_200_000,  170_000,   25,   "Rs.1,70,000 + 25% above 16 lac"),
    (3_200_001,  5_600_000,  570_000,   30,   "Rs.5,70,000 + 30% above 32 lac"),
    (5_600_001,  float('inf'),1_290_000,35,   "Rs.12,90,000 + 35% above 56 lac"),
]

def calc_tax(income, slabs):
    for lower, upper, fixed, rate, desc in slabs:
        if lower <= income <= upper:
            tax = fixed + (income - lower) * rate / 100
            return round(tax, 2), rate, desc
    return 0, 0, "N/A"

def get_slab_index(income, slabs):
    for i, (lower, upper, *_) in enumerate(slabs):
        if lower <= income <= upper:
            return i
    return -1

# ── SIDEBAR INPUTS ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Calculator Settings")

    income_type = st.radio("Income Type", ["Salaried", "Business / Self-Employed"])
    slabs = SALARIED_SLABS if income_type == "Salaried" else BUSINESS_SLABS

    input_mode = st.radio("Enter Income As", ["Monthly Salary", "Annual Income"])

    if input_mode == "Monthly Salary":
        monthly = st.number_input("Monthly Income (Rs.)", min_value=0, value=100_000, step=5_000)
        annual  = monthly * 12
    else:
        annual  = st.number_input("Annual Income (Rs.)", min_value=0, value=1_200_000, step=50_000)
        monthly = annual / 12

    st.divider()
    st.markdown("### ➕ Allowances & Deductions")
    house_rent   = st.number_input("House Rent Allowance (Rs./month)", min_value=0, value=0, step=1_000)
    medical      = st.number_input("Medical Allowance (Rs./month)", min_value=0, value=0, step=1_000)
    other_allow  = st.number_input("Other Allowances (Rs./month)", min_value=0, value=0, step=1_000)
    zakat        = st.number_input("Zakat Paid (Rs./year)", min_value=0, value=0, step=1_000)
    donations    = st.number_input("Approved Donations (Rs./year)", min_value=0, value=0, step=1_000)

    # Taxable income after deductions (simplified)
    total_deductions = (house_rent + medical + other_allow) * 12 + zakat + donations
    taxable_income   = max(0, annual - total_deductions)

    st.divider()
    filer_status = st.radio("FBR Filer Status", ["Active Filer", "Non-Filer"])

# ── CALCULATION ──────────────────────────────────────────────────────────────
tax_amount, marginal_rate, slab_desc = calc_tax(taxable_income, slabs)
active_slab = get_slab_index(taxable_income, slabs)

# Non-filer surcharge (simplified: +100% for non-filers on WHT — here shown as note)
nonfiler_note = " ⚠️ Non-filer rates may apply for WHT deductions." if filer_status == "Non-Filer" else ""

effective_rate   = (tax_amount / taxable_income * 100) if taxable_income > 0 else 0
monthly_tax      = tax_amount / 12
take_home_annual = taxable_income - tax_amount
take_home_monthly= take_home_annual / 12

# ── MAIN LAYOUT ──────────────────────────────────────────────────────────────
col_left, col_right = st.columns([3, 2])

with col_left:
    # ── INCOME SUMMARY ──
    st.markdown('<div class="section-title">📊 Income Summary</div>', unsafe_allow_html=True)

    r1, r2, r3 = st.columns(3)
    r1.metric("Gross Annual Income",   f"Rs. {annual:,.0f}")
    r2.metric("Total Deductions",      f"Rs. {total_deductions:,.0f}")
    r3.metric("Taxable Income",        f"Rs. {taxable_income:,.0f}")

    st.divider()

    # ── TAX RESULTS ──
    st.markdown('<div class="section-title">🧾 Tax Calculation Result</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="total-card">
            <p>Annual Tax</p>
            <h2>Rs. {tax_amount:,.0f}</h2>
            <p>Effective rate: {effective_rate:.1f}%</p>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="total-card" style="background:#2d8a5e">
            <p>Monthly Tax Deduction</p>
            <h2>Rs. {monthly_tax:,.0f}</h2>
            <p>Marginal rate: {marginal_rate}%</p>
        </div>""", unsafe_allow_html=True)

    m1, m2 = st.columns(2)
    m1.metric("Monthly Take-Home",  f"Rs. {take_home_monthly:,.0f}", delta=f"-Rs. {monthly_tax:,.0f} tax")
    m2.metric("Annual Take-Home",   f"Rs. {take_home_annual:,.0f}")

    if nonfiler_note:
        st.warning(nonfiler_note)

    st.divider()

    # ── TAX SLABS TABLE ──
    st.markdown('<div class="section-title">📋 FBR 2024-25 Tax Slabs</div>', unsafe_allow_html=True)
    st.caption(f"Income type: **{income_type}**")

    for i, (lower, upper, fixed, rate, desc) in enumerate(slabs):
        upper_label = f"Rs. {upper:,.0f}" if upper != float('inf') else "Above"
        lower_label = f"Rs. {lower:,.0f}"
        is_active   = (i == active_slab)
        css_class   = "slab-active" if is_active else "slab-inactive"
        active_mark = " ◀ Your slab" if is_active else ""

        st.markdown(f"""
        <div class="slab-row {css_class}">
            <span>{lower_label} – {upper_label}</span>
            <span>{rate}%</span>
            <span style="font-size:0.78rem; color:#666">{desc}{active_mark}</span>
        </div>""", unsafe_allow_html=True)

    st.divider()

    # ── WHAT IF CALCULATOR ──
    st.markdown('<div class="section-title">🔮 What-If Scenarios</div>', unsafe_allow_html=True)
    st.caption("Agar salary badhe toh tax kitna hoga?")

    scenarios = []
    for inc in [annual * 0.8, annual, annual * 1.2, annual * 1.5, annual * 2]:
        t, r, _ = calc_tax(max(0, inc - total_deductions), slabs)
        eff = (t / inc * 100) if inc > 0 else 0
        scenarios.append({
            "Annual Income": f"Rs. {inc:,.0f}",
            "Annual Tax": f"Rs. {t:,.0f}",
            "Monthly Tax": f"Rs. {t/12:,.0f}",
            "Effective Rate": f"{eff:.1f}%",
        })

    import pandas as pd
    df = pd.DataFrame(scenarios)
    st.dataframe(df, use_container_width=True, hide_index=True)

with col_right:
    # ── PIE CHART ──
    st.markdown('<div class="section-title">📈 Income Breakdown</div>', unsafe_allow_html=True)

    if taxable_income > 0:
        fig, ax = plt.subplots(figsize=(4, 4))
        fig.patch.set_facecolor('#f0faf5')
        ax.set_facecolor('#f0faf5')

        sizes  = [take_home_annual, tax_amount]
        colors = ['#1a5f3f', '#e8f5ee']
        labels = [f'Take-Home\nRs. {take_home_annual:,.0f}', f'Income Tax\nRs. {tax_amount:,.0f}']

        wedges, texts, autotexts = ax.pie(
            sizes, labels=labels, colors=colors,
            autopct='%1.1f%%', startangle=90,
            wedgeprops={'edgecolor': 'white', 'linewidth': 2},
            textprops={'fontsize': 9}
        )
        for at in autotexts:
            at.set_color('white')
            at.set_fontweight('bold')

        ax.set_title(f'Annual Income: Rs. {annual:,.0f}', fontsize=10, pad=12, color='#1a5f3f')
        st.pyplot(fig)
        plt.close()
    else:
        st.info("Income enter karein chart dekhne ke liye")

    st.divider()

    # ── TAX BRACKET CHART ──
    st.markdown('<div class="section-title">📊 Tax at Each Bracket</div>', unsafe_allow_html=True)

    incomes = [600_000, 1_200_000, 2_400_000, 3_600_000, 6_000_000, 12_000_000, 15_000_000]
    taxes   = [calc_tax(i, slabs)[0] for i in incomes]
    labels  = ["6L", "12L", "24L", "36L", "60L", "1.2Cr", "1.5Cr"]

    fig2, ax2 = plt.subplots(figsize=(4, 3.5))
    fig2.patch.set_facecolor('#f0faf5')
    ax2.set_facecolor('#f0faf5')

    bars = ax2.bar(labels, [t/1000 for t in taxes], color='#2d8a5e', edgecolor='white', linewidth=0.8)

    # Highlight current income bar
    for i, inc in enumerate(incomes):
        if get_slab_index(taxable_income, slabs) == get_slab_index(inc, slabs):
            bars[i].set_color('#1a5f3f')

    ax2.set_ylabel("Tax (Rs. 000)", fontsize=9, color='#555')
    ax2.set_xlabel("Annual Income", fontsize=9, color='#555')
    ax2.set_title("Tax Amount by Income Level", fontsize=10, color='#1a5f3f')
    ax2.tick_params(colors='#555', labelsize=8)
    for spine in ax2.spines.values():
        spine.set_color('#ddd')

    st.pyplot(fig2)
    plt.close()

    st.divider()

    # ── QUICK TIPS ──
    st.markdown('<div class="section-title">💡 Tax Saving Tips</div>', unsafe_allow_html=True)

    tips = [
        ("📋", "FBR Active Filer bano", "WHT rates aadhi ho jaati hain"),
        ("🕌", "Zakat FBR ko declare karo", "Taxable income se minus hoti hai"),
        ("❤️", "Approved NGO ko donate karo", "100% deduction milta hai"),
        ("🏠", "House Rent Allowance lo", "Basic salary se alag — kam tax"),
        ("🏥", "Medical Allowance restructure karo", "10% of basic — tax free"),
    ]

    for icon, title, detail in tips:
        st.markdown(f"""
        <div style="background:#f8faf9;border:1px solid #e8f5ee;border-radius:8px;
                    padding:10px 14px;margin-bottom:8px;">
            <span style="font-size:1rem">{icon}</span>
            <strong style="font-size:0.88rem;color:#1a5f3f"> {title}</strong>
            <div style="font-size:0.78rem;color:#666;margin-top:2px">{detail}</div>
        </div>""", unsafe_allow_html=True)

# ── FOOTER ───────────────────────────────────────────────────────────────────
st.divider()
st.markdown("""
<div style="text-align:center;color:#888;font-size:0.78rem;padding:1rem">
    💰 <strong>PakInvoice — Income Tax Calculator</strong> &nbsp;|&nbsp;
    FBR Finance Act 2024-25 &nbsp;|&nbsp;
    Consult a tax professional for exact calculations
</div>
""", unsafe_allow_html=True)

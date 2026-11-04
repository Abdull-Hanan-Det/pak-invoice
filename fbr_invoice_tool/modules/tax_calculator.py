"""
FBR Tax Calculator Module
Rates as per FBR 2024-25 Finance Act
"""

# ── GST RATES (Sales Tax Act 1990) ────────────────────────────
GST_RATES = {
    "exempt": 0,
    "reduced_5": 5,
    "reduced_8": 8,
    "reduced_10": 10,
    "reduced_13": 13,
    "standard": 15,
    "enhanced_17": 17,
    "enhanced_18": 18,
    "luxury_25": 25,
}

# ── INCOME TAX SLABS 2024-25 (Salaried) ──────────────────────
INCOME_TAX_SLABS_SALARIED = [
    (0,        600_000,   0,      0),
    (600_001,  1_200_000, 0,      2.5),
    (1_200_001,2_400_000, 15_000, 12.5),
    (2_400_001,3_600_000, 165_000,22.5),
    (3_600_001,6_000_000, 435_000,27.5),
    (6_000_001,12_000_000,1_095_000,35),
    (12_000_001,float('inf'),3_195_000,45),
]

# ── WHT RATES (Section 153) ───────────────────────────────────
WHT_RATES = {
    "services_filer": 8.0,
    "services_nonfiler": 15.0,
    "goods_filer": 4.5,
    "goods_nonfiler": 9.0,
    "rent_filer": 15.0,
    "rent_nonfiler": 30.0,
    "salary_filer": 1.0,  # simplified
    "contractor_filer": 7.5,
    "contractor_nonfiler": 15.0,
}


def calculate_gst(amount: float, rate: float) -> dict:
    """
    Calculate GST on a given amount.
    
    Args:
        amount: Taxable amount in PKR
        rate: GST rate percentage (e.g. 15 for 15%)
    
    Returns:
        dict with taxable_amount, gst_amount, total_with_gst
    """
    gst_amount = amount * rate / 100
    return {
        "taxable_amount": amount,
        "gst_rate": rate,
        "gst_amount": round(gst_amount, 2),
        "total_with_gst": round(amount + gst_amount, 2),
    }


def calculate_income_tax(annual_income: float, is_salaried: bool = True) -> dict:
    """
    Calculate income tax as per FBR 2024-25 slabs.
    
    Args:
        annual_income: Annual taxable income in PKR
        is_salaried: True for salaried, False for business income
    
    Returns:
        dict with slab info, tax_amount, effective_rate
    """
    slabs = INCOME_TAX_SLABS_SALARIED  # extend for business if needed
    
    tax = 0
    slab_desc = ""
    marginal_rate = 0
    
    for lower, upper, fixed, rate in slabs:
        if lower <= annual_income <= upper:
            excess = annual_income - lower
            tax = fixed + (excess * rate / 100)
            marginal_rate = rate
            slab_desc = f"Rs. {lower:,} – Rs. {upper:,}" if upper != float('inf') else f"Above Rs. {lower:,}"
            break
    
    effective_rate = (tax / annual_income * 100) if annual_income > 0 else 0
    monthly_tax = tax / 12
    
    return {
        "annual_income": annual_income,
        "tax_slab": slab_desc,
        "marginal_rate": marginal_rate,
        "annual_tax": round(tax, 2),
        "monthly_tax": round(monthly_tax, 2),
        "effective_rate": round(effective_rate, 2),
        "take_home_annual": round(annual_income - tax, 2),
        "take_home_monthly": round((annual_income - tax) / 12, 2),
    }


def calculate_wht(amount: float, wht_type: str) -> dict:
    """
    Calculate Withholding Tax (WHT) as per Section 153.
    
    Args:
        amount: Gross payment amount
        wht_type: Key from WHT_RATES dict
    
    Returns:
        dict with wht details
    """
    rate = WHT_RATES.get(wht_type, 0)
    wht_amount = amount * rate / 100
    net_payment = amount - wht_amount
    
    return {
        "gross_amount": amount,
        "wht_type": wht_type,
        "wht_rate": rate,
        "wht_amount": round(wht_amount, 2),
        "net_payment": round(net_payment, 2),
    }


def get_all_applicable_taxes(amount: float, gst_rate: float,
                              apply_wht: bool = False, wht_type: str = "services_filer") -> dict:
    """
    Full tax breakdown for an invoice amount.
    
    Args:
        amount: Base amount before taxes
        gst_rate: GST rate %
        apply_wht: Whether WHT is applicable
        wht_type: Type of WHT from WHT_RATES
    
    Returns:
        Complete tax breakdown dict
    """
    gst = calculate_gst(amount, gst_rate)
    total_with_gst = gst["total_with_gst"]
    
    wht = None
    if apply_wht:
        wht = calculate_wht(amount, wht_type)
    
    final_receivable = total_with_gst - (wht["wht_amount"] if wht else 0)
    
    return {
        "base_amount": amount,
        "gst": gst,
        "wht": wht,
        "total_with_gst": total_with_gst,
        "wht_deduction": wht["wht_amount"] if wht else 0,
        "final_receivable": round(final_receivable, 2),
    }

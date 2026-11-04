"""
Invoice HTML Generator — Professional Pakistani Invoice Template
"""

def generate_invoice_html(data: dict) -> str:
    """
    Generate a professional HTML invoice ready for printing or PDF export.
    """
    
    items_rows = ""
    for i, item in enumerate(data["items"], 1):
        gst_label = f"{item['gst_rate']}% GST" if item['gst_rate'] > 0 else "Exempt"
        items_rows += f"""
        <tr>
            <td>{i}</td>
            <td>
                <strong>{item['name']}</strong>
                {"<br><span class='item-desc'>" + item['desc'] + "</span>" if item.get('desc') else ""}
            </td>
            <td style="text-align:center">{item['qty']}</td>
            <td style="text-align:right">{data['currency']} {item['rate']:,.0f}</td>
            <td style="text-align:center">{gst_label}</td>
            <td style="text-align:right">{data['currency']} {item['gst_amount']:,.0f}</td>
            <td style="text-align:right"><strong>{data['currency']} {item['total']:,.0f}</strong></td>
        </tr>
        """

    # Totals section
    totals_rows = f"""
    <tr class="total-row">
        <td colspan="6" style="text-align:right">Subtotal</td>
        <td style="text-align:right">{data['currency']} {data['subtotal']:,.0f}</td>
    </tr>
    <tr class="total-row">
        <td colspan="6" style="text-align:right">Total GST</td>
        <td style="text-align:right">{data['currency']} {data['total_gst']:,.0f}</td>
    </tr>
    """

    if data.get("discount", 0) > 0:
        totals_rows += f"""
    <tr class="total-row">
        <td colspan="6" style="text-align:right">Discount</td>
        <td style="text-align:right; color:#dc3545">- {data['currency']} {data['discount']:,.0f}</td>
    </tr>"""

    if data.get("shipping", 0) > 0:
        totals_rows += f"""
    <tr class="total-row">
        <td colspan="6" style="text-align:right">Shipping / Delivery</td>
        <td style="text-align:right">{data['currency']} {data['shipping']:,.0f}</td>
    </tr>"""

    if data.get("wht_amount", 0) > 0:
        totals_rows += f"""
    <tr class="total-row">
        <td colspan="6" style="text-align:right">WHT Deduction</td>
        <td style="text-align:right; color:#dc3545">- {data['currency']} {data['wht_amount']:,.0f}</td>
    </tr>"""

    # Business info
    biz = data["business"]
    ntn_line = f"<div class='info-line'><span>NTN:</span> {biz['ntn']}</div>" if biz.get("ntn") else ""
    strn_line = f"<div class='info-line'><span>STRN:</span> {biz['strn']}</div>" if biz.get("strn") else ""
    biz_phone = f"<div class='info-line'><span>Ph:</span> {biz['phone']}</div>" if biz.get("phone") else ""
    biz_addr = f"<div class='info-line'><span>Address:</span> {biz['address']}</div>" if biz.get("address") else ""

    # Customer info
    cust = data["customer"]
    cust_ntn = f"<div class='info-line'><span>NTN:</span> {cust['ntn']}</div>" if cust.get("ntn") else ""
    cust_phone = f"<div class='info-line'><span>Ph:</span> {cust['phone']}</div>" if cust.get("phone") else ""
    cust_addr = f"<div class='info-line'><span>Address:</span> {cust['address']}</div>" if cust.get("address") else ""

    notes_section = ""
    if data.get("notes"):
        notes_section = f"""
        <div class="notes-section">
            <strong>Notes / Terms & Conditions:</strong>
            <p>{data['notes'].replace(chr(10), '<br>')}</p>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Invoice {data['invoice_no']}</title>
<style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    
    body {{
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 13px;
        color: #2c2c2c;
        background: #f5f5f5;
        padding: 20px;
    }}
    
    .invoice-wrapper {{
        max-width: 900px;
        margin: 0 auto;
        background: white;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 20px rgba(0,0,0,0.1);
    }}
    
    /* HEADER */
    .invoice-header {{
        background: linear-gradient(135deg, #1a5f3f 0%, #2d8a5e 100%);
        color: white;
        padding: 32px 40px;
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
    }}
    
    .business-name {{
        font-size: 24px;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin-bottom: 4px;
    }}
    
    .business-details {{
        opacity: 0.85;
        font-size: 12px;
        line-height: 1.8;
    }}
    
    .invoice-title-block {{
        text-align: right;
    }}
    
    .invoice-word {{
        font-size: 32px;
        font-weight: 300;
        letter-spacing: 4px;
        opacity: 0.9;
    }}
    
    .invoice-number {{
        font-size: 15px;
        font-weight: 600;
        margin-top: 4px;
    }}
    
    .fbr-badge {{
        display: inline-block;
        background: rgba(255,255,255,0.2);
        border: 1px solid rgba(255,255,255,0.4);
        border-radius: 4px;
        padding: 2px 8px;
        font-size: 10px;
        margin-top: 8px;
        letter-spacing: 0.5px;
    }}
    
    /* DATES & BILL TO */
    .invoice-meta {{
        display: flex;
        padding: 24px 40px;
        border-bottom: 1px solid #eee;
        gap: 40px;
    }}
    
    .meta-block {{
        flex: 1;
    }}
    
    .meta-label {{
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #888;
        margin-bottom: 6px;
        font-weight: 600;
    }}
    
    .meta-value {{
        font-size: 14px;
        font-weight: 600;
        color: #1a5f3f;
    }}
    
    .info-line {{
        font-size: 12px;
        color: #555;
        line-height: 1.8;
    }}
    
    .info-line span {{
        color: #999;
        min-width: 60px;
        display: inline-block;
    }}
    
    /* TABLE */
    .table-section {{
        padding: 0 40px;
    }}
    
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 16px 0;
    }}
    
    thead th {{
        background: #f8faf9;
        color: #1a5f3f;
        padding: 10px 12px;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.5px;
        border-bottom: 2px solid #1a5f3f;
        text-transform: uppercase;
    }}
    
    tbody td {{
        padding: 12px 12px;
        border-bottom: 1px solid #f0f0f0;
        vertical-align: top;
        font-size: 13px;
    }}
    
    .item-desc {{
        color: #888;
        font-size: 11px;
    }}
    
    tbody tr:last-child td {{
        border-bottom: none;
    }}
    
    tbody tr:hover {{
        background: #fafff9;
    }}
    
    /* TOTALS */
    .totals-section {{
        padding: 0 40px 24px;
        display: flex;
        justify-content: flex-end;
    }}
    
    .totals-table {{
        width: 320px;
    }}
    
    .totals-table table {{
        margin: 0;
    }}
    
    .total-row td {{
        padding: 6px 12px;
        font-size: 13px;
        border: none;
        color: #555;
    }}
    
    .grand-total-row {{
        background: #1a5f3f;
        color: white;
    }}
    
    .grand-total-row td {{
        padding: 14px 12px;
        font-size: 16px;
        font-weight: 700;
        border: none;
        color: white;
    }}
    
    /* PAYMENT TERMS */
    .payment-section {{
        padding: 16px 40px;
        background: #f8faf9;
        border-top: 1px solid #e8f5ee;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    
    .payment-label {{
        font-size: 11px;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    .payment-value {{
        font-weight: 600;
        color: #1a5f3f;
        font-size: 14px;
    }}
    
    /* NOTES */
    .notes-section {{
        padding: 20px 40px;
        border-top: 1px solid #eee;
        font-size: 12px;
        color: #666;
        line-height: 1.8;
    }}
    
    .notes-section strong {{
        color: #333;
    }}
    
    /* FOOTER */
    .invoice-footer {{
        padding: 16px 40px;
        background: #1a5f3f;
        color: rgba(255,255,255,0.7);
        font-size: 11px;
        text-align: center;
        letter-spacing: 0.3px;
    }}
    
    .due-date-box {{
        background: #fff3cd;
        border: 1px solid #ffc107;
        border-radius: 6px;
        padding: 4px 12px;
        font-size: 12px;
        color: #856404;
        font-weight: 600;
    }}
    
    @media print {{
        body {{ background: white; padding: 0; }}
        .invoice-wrapper {{ box-shadow: none; border-radius: 0; }}
    }}
</style>
</head>
<body>
<div class="invoice-wrapper">

    <!-- HEADER -->
    <div class="invoice-header">
        <div>
            <div class="business-name">{biz['name']}</div>
            <div class="business-details">
                {ntn_line.replace("class='info-line'", "style='opacity:0.85;font-size:12px;'").replace("<span>", "<span style='opacity:0.6;'>") if biz.get('ntn') else ""}
                {strn_line.replace("class='info-line'", "style='opacity:0.85;font-size:12px;'").replace("<span>", "<span style='opacity:0.6;'>") if biz.get('strn') else ""}
                {biz_addr.replace("class='info-line'", "style='opacity:0.85;font-size:12px;'").replace("<span>", "<span style='opacity:0.6;'>") if biz.get('address') else ""}
                {biz_phone.replace("class='info-line'", "style='opacity:0.85;font-size:12px;'").replace("<span>", "<span style='opacity:0.6;'>") if biz.get('phone') else ""}
            </div>
            <div><span class="fbr-badge">FBR Registered</span></div>
        </div>
        <div class="invoice-title-block">
            <div class="invoice-word">INVOICE</div>
            <div class="invoice-number">{data['invoice_no']}</div>
        </div>
    </div>

    <!-- META -->
    <div class="invoice-meta">
        <div class="meta-block">
            <div class="meta-label">Bill To</div>
            <div class="meta-value">{cust['name']}</div>
            {cust_ntn}
            {cust_addr}
            {cust_phone}
        </div>
        <div class="meta-block">
            <div class="meta-label">Invoice Date</div>
            <div class="meta-value">{data['invoice_date']}</div>
        </div>
        <div class="meta-block">
            <div class="meta-label">Due Date</div>
            <span class="due-date-box">📅 {data['due_date']}</span>
        </div>
        <div class="meta-block">
            <div class="meta-label">Currency</div>
            <div class="meta-value">{data['currency']}</div>
        </div>
    </div>

    <!-- ITEMS TABLE -->
    <div class="table-section">
        <table>
            <thead>
                <tr>
                    <th style="width:40px">#</th>
                    <th>Description</th>
                    <th style="text-align:center;width:60px">Qty</th>
                    <th style="text-align:right;width:100px">Rate</th>
                    <th style="text-align:center;width:80px">GST</th>
                    <th style="text-align:right;width:100px">Tax Amt</th>
                    <th style="text-align:right;width:110px">Total</th>
                </tr>
            </thead>
            <tbody>
                {items_rows}
            </tbody>
        </table>
    </div>

    <!-- TOTALS -->
    <div class="totals-section">
        <div class="totals-table">
            <table>
                {totals_rows}
                <tr class="grand-total-row">
                    <td colspan="1">Grand Total</td>
                    <td style="text-align:right">{data['currency']} {data['grand_total']:,.0f}</td>
                </tr>
            </table>
        </div>
    </div>

    <!-- PAYMENT TERMS -->
    <div class="payment-section">
        <div>
            <div class="payment-label">Payment Terms</div>
            <div class="payment-value">{data['payment_terms']}</div>
        </div>
        <div style="text-align:right">
            <div class="payment-label">Amount Due</div>
            <div class="payment-value" style="font-size:18px">{data['currency']} {data['grand_total']:,.0f}</div>
        </div>
    </div>

    {notes_section}

    <!-- FOOTER -->
    <div class="invoice-footer">
        This invoice was generated by PakInvoice &nbsp;|&nbsp; 
        GST rates as per FBR Finance Act 2024-25 &nbsp;|&nbsp;
        Thank you for your business!
    </div>

</div>
</body>
</html>"""

    return html

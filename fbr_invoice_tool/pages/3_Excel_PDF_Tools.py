import streamlit as st
import pandas as pd
import io
from datetime import date

st.set_page_config(
    page_title="Excel & PDF Tools — PakInvoice",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main-header {
        background: linear-gradient(135deg, #1a5f3f 0%, #2d8a5e 100%);
        padding: 2rem; border-radius: 12px; color: white;
        margin-bottom: 2rem; text-align: center;
    }
    .main-header h1 { font-size: 2rem; font-weight: 700; margin: 0; }
    .main-header p  { opacity: 0.85; margin: 0.4rem 0 0; }
    .tool-box {
        background: white; border: 2px solid #e8f5ee;
        border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem;
    }
    .section-title {
        color: #1a5f3f; font-weight: 700; font-size: 1.1rem;
        border-bottom: 2px solid #e8f5ee; padding-bottom: 8px; margin-bottom: 1rem;
    }
    .stButton > button {
        background: #1a5f3f; color: white; border: none;
        border-radius: 8px; font-weight: 600;
    }
    .stButton > button:hover { background: #2d8a5e; }
    .upload-hint {
        background: #f0faf5; border: 1px dashed #2d8a5e;
        border-radius: 8px; padding: 1rem; text-align: center;
        color: #555; font-size: 0.88rem; margin-bottom: 1rem;
    }
    .success-box {
        background: #d4edda; border: 1px solid #1a5f3f;
        border-radius: 8px; padding: 1rem; color: #1a5f3f;
        margin: 0.5rem 0;
    }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── HEADER ───────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>📊 Excel & PDF Tools</h1>
    <p>Excel se invoice banao • Invoice ko Excel export karo • PDF se data nikaalo</p>
</div>
""", unsafe_allow_html=True)

# ── TABS ─────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "📥 Excel → Invoice",
    "📤 Invoice → Excel Export",
    "📄 PDF Data Extract"
])


# ══════════════════════════════════════════════════════════════
# TAB 1 — Excel Upload → Invoice Generate
# ══════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-title">📥 Excel Upload karo → Invoice ban jayegi</div>', unsafe_allow_html=True)

    # Template download
    st.markdown("**Step 1 — Pehle template download karo aur fill karo:**")

    template_data = {
        "Item Name":        ["Website Design", "Logo Design", "Monthly Hosting"],
        "Description":      ["5-page WordPress site", "Brand identity", "cPanel 1 year"],
        "Quantity":         [1, 1, 12],
        "Rate (PKR)":       [50000, 15000, 1500],
        "GST Rate (%)":     [15, 15, 0],
    }
    template_df = pd.DataFrame(template_data)

    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='openpyxl') as writer:
        template_df.to_excel(writer, index=False, sheet_name='Items')
        # Customer info sheet
        info_df = pd.DataFrame({
            "Field": ["Business Name", "NTN", "STRN", "Business Address", "Business Phone",
                      "Customer Name", "Customer NTN", "Customer Address", "Customer Phone",
                      "Invoice Number", "Invoice Date", "Due Date", "Currency",
                      "Discount (PKR)", "Shipping (PKR)", "Notes"],
            "Value": ["Ali Traders", "1234567-8", "12-34-5678-001-23", "Gulberg, Lahore", "0300-1234567",
                      "Muhammad Raza", "", "DHA, Lahore", "0321-9876543",
                      "INV-2024-001", str(date.today()), str(date.today()), "Rs.",
                      "0", "0", "Thank you for your business!"]
        })
        info_df.to_excel(writer, index=False, sheet_name='Business Info')
    buf.seek(0)

    st.download_button(
        "⬇️ Template Download karo (Excel)",
        data=buf,
        file_name="pak_invoice_template.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=False
    )

    st.markdown("---")
    st.markdown("**Step 2 — Bhara hua Excel upload karo:**")

    st.markdown('<div class="upload-hint">📂 Excel file yahan drag karo ya click karke select karo<br><small>Sirf .xlsx format — wahi template use karo jo upar download ki</small></div>', unsafe_allow_html=True)

    uploaded_excel = st.file_uploader("Excel file upload karo", type=["xlsx"], label_visibility="collapsed")

    if uploaded_excel:
        try:
            # Read items sheet
            items_df = pd.read_excel(uploaded_excel, sheet_name='Items')
            uploaded_excel.seek(0)

            # Read business info sheet
            try:
                info_df = pd.read_excel(uploaded_excel, sheet_name='Business Info')
                info_dict = dict(zip(info_df['Field'], info_df['Value'].astype(str)))
            except Exception:
                info_dict = {}

            st.success(f"✅ {len(items_df)} items mil gaye Excel mein!")

            # Show preview
            with st.expander("📋 Data Preview"):
                st.dataframe(items_df, use_container_width=True)
                if info_dict:
                    st.write("**Business Info:**")
                    st.json(info_dict)

            # Build items list
            items = []
            errors = []
            for i, row in items_df.iterrows():
                try:
                    name    = str(row.get('Item Name', '')).strip()
                    desc    = str(row.get('Description', '')).strip()
                    qty     = float(row.get('Quantity', 1))
                    rate    = float(row.get('Rate (PKR)', 0))
                    gst     = float(row.get('GST Rate (%)', 0))

                    if not name or rate <= 0:
                        errors.append(f"Row {i+2}: Item name ya rate missing")
                        continue

                    subtotal   = qty * rate
                    gst_amount = subtotal * gst / 100
                    items.append({
                        "name": name, "desc": desc if desc != 'nan' else "",
                        "qty": int(qty), "rate": rate,
                        "subtotal": subtotal, "gst_rate": gst,
                        "gst_amount": gst_amount, "total": subtotal + gst_amount
                    })
                except Exception as e:
                    errors.append(f"Row {i+2}: {str(e)}")

            if errors:
                for err in errors:
                    st.warning(err)

            if items:
                # Calculate totals
                subtotal  = sum(x['subtotal'] for x in items)
                total_gst = sum(x['gst_amount'] for x in items)
                discount  = float(info_dict.get('Discount (PKR)', 0) or 0)
                shipping  = float(info_dict.get('Shipping (PKR)', 0) or 0)
                grand     = subtotal + total_gst - discount + shipping
                curr      = info_dict.get('Currency', 'Rs.')

                # Build invoice data
                invoice_data = {
                    "invoice_no":   info_dict.get('Invoice Number', 'INV-2024-001'),
                    "invoice_date": info_dict.get('Invoice Date', str(date.today())),
                    "due_date":     info_dict.get('Due Date', str(date.today())),
                    "business": {
                        "name":    info_dict.get('Business Name', 'Your Business'),
                        "ntn":     info_dict.get('NTN', ''),
                        "strn":    info_dict.get('STRN', ''),
                        "address": info_dict.get('Business Address', ''),
                        "phone":   info_dict.get('Business Phone', ''),
                    },
                    "customer": {
                        "name":    info_dict.get('Customer Name', 'Customer'),
                        "ntn":     info_dict.get('Customer NTN', ''),
                        "address": info_dict.get('Customer Address', ''),
                        "phone":   info_dict.get('Customer Phone', ''),
                    },
                    "items":         items,
                    "subtotal":      subtotal,
                    "total_gst":     total_gst,
                    "discount":      discount,
                    "shipping":      shipping,
                    "wht_amount":    0,
                    "grand_total":   grand,
                    "currency":      curr,
                    "payment_terms": "Due on Receipt",
                    "notes":         info_dict.get('Notes', ''),
                }

                # Summary
                st.markdown("### 🧾 Invoice Summary")
                c1, c2, c3 = st.columns(3)
                c1.metric("Items",      len(items))
                c2.metric("Total GST",  f"{curr} {total_gst:,.0f}")
                c3.metric("Grand Total",f"{curr} {grand:,.0f}")

                # Generate invoice
                import sys, os
                sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
                from modules.invoice_generator import generate_invoice_html

                html_invoice = generate_invoice_html(invoice_data)

                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        "⬇️ Invoice HTML Download",
                        data=html_invoice,
                        file_name=f"{invoice_data['invoice_no']}.html",
                        mime="text/html",
                        use_container_width=True
                    )
                with col2:
                    try:
                        from modules.pdf_export import export_to_pdf
                        pdf = export_to_pdf(html_invoice)
                        st.download_button(
                            "📄 Invoice PDF Download",
                            data=pdf,
                            file_name=f"{invoice_data['invoice_no']}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    except Exception:
                        st.info("PDF: `pip install weasyprint`")

                with st.expander("👁️ Invoice Preview"):
                    st.components.v1.html(html_invoice, height=600, scrolling=True)

        except Exception as e:
            st.error(f"❌ File read nahi ho sakhi: {str(e)}")
            st.info("Template download karo aur usi format mein data daalo.")


# ══════════════════════════════════════════════════════════════
# TAB 2 — Invoice → Excel Export
# ══════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">📤 Invoice Generator se data Excel mein export karo</div>', unsafe_allow_html=True)

    # Check if items exist in session
    has_items = 'items' in st.session_state and len(st.session_state.get('items', [])) > 0

    if has_items:
        items = st.session_state['items']
        st.success(f"✅ Invoice Generator mein {len(items)} items hain — export karo!")
    else:
        st.info("💡 Pehle **Invoice Generator** page pe jao aur items add karo — phir yahan export kar sako ge.")
        st.markdown("**Ya demo data se try karo:**")
        if st.button("Demo Data Load karo"):
            st.session_state['items'] = [
                {"name": "Website Design", "desc": "WordPress site", "qty": 1,
                 "rate": 50000, "subtotal": 50000, "gst_rate": 15, "gst_amount": 7500, "total": 57500},
                {"name": "Logo Design", "desc": "Brand identity", "qty": 1,
                 "rate": 15000, "subtotal": 15000, "gst_rate": 15, "gst_amount": 2250, "total": 17250},
                {"name": "Monthly Hosting", "desc": "cPanel 1 year", "qty": 12,
                 "rate": 1500, "subtotal": 18000, "gst_rate": 0, "gst_amount": 0, "total": 18000},
            ]
            st.rerun()
        items = st.session_state.get('items', [])

    if items:
        # Build export dataframe
        rows = []
        for item in items:
            rows.append({
                "Item Name":        item['name'],
                "Description":      item.get('desc', ''),
                "Quantity":         item['qty'],
                "Rate (PKR)":       item['rate'],
                "Subtotal":         item['subtotal'],
                "GST Rate (%)":     item['gst_rate'],
                "GST Amount":       item['gst_amount'],
                "Total (with GST)": item['total'],
            })

        df = pd.DataFrame(rows)

        # Summary row
        summary_row = pd.DataFrame([{
            "Item Name": "TOTAL",
            "Description": "",
            "Quantity": sum(r['qty'] for r in items),
            "Rate (PKR)": "",
            "Subtotal": sum(r['subtotal'] for r in items),
            "GST Rate (%)": "",
            "GST Amount": sum(r['gst_amount'] for r in items),
            "Total (with GST)": sum(r['total'] for r in items),
        }])

        st.markdown("**Preview:**")
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Export options
        st.markdown("### 📥 Export Format")
        exp1, exp2 = st.columns(2)

        with exp1:
            st.markdown("**Excel (.xlsx)**")
            buf = io.BytesIO()
            with pd.ExcelWriter(buf, engine='openpyxl') as writer:
                # Items sheet
                full_df = pd.concat([df, summary_row], ignore_index=True)
                full_df.to_excel(writer, index=False, sheet_name='Invoice Items')

                # Summary sheet
                total_sub = sum(r['subtotal'] for r in items)
                total_gst = sum(r['gst_amount'] for r in items)
                total_all = sum(r['total'] for r in items)

                summary_df = pd.DataFrame({
                    "Description": ["Subtotal", "Total GST", "Grand Total"],
                    "Amount (PKR)": [total_sub, total_gst, total_all]
                })
                summary_df.to_excel(writer, index=False, sheet_name='Tax Summary')

            buf.seek(0)
            st.download_button(
                "⬇️ Excel Download (.xlsx)",
                data=buf,
                file_name=f"invoice_export_{date.today()}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

        with exp2:
            st.markdown("**CSV (.csv)**")
            csv_buf = io.StringIO()
            df.to_csv(csv_buf, index=False)
            st.download_button(
                "⬇️ CSV Download (.csv)",
                data=csv_buf.getvalue(),
                file_name=f"invoice_export_{date.today()}.csv",
                mime="text/csv",
                use_container_width=True
            )

        # GST breakdown export
        st.markdown("---")
        st.markdown("**📊 FBR GST Breakdown Export:**")
        gst_data = {}
        for item in items:
            r = item['gst_rate']
            if r not in gst_data:
                gst_data[r] = {"GST Rate (%)": r, "Taxable Amount": 0, "GST Amount": 0}
            gst_data[r]["Taxable Amount"] += item['subtotal']
            gst_data[r]["GST Amount"]     += item['gst_amount']

        gst_df = pd.DataFrame(list(gst_data.values()))
        st.dataframe(gst_df, use_container_width=True, hide_index=True)

        gst_buf = io.BytesIO()
        with pd.ExcelWriter(gst_buf, engine='openpyxl') as writer:
            gst_df.to_excel(writer, index=False, sheet_name='GST Breakdown')
        gst_buf.seek(0)

        st.download_button(
            "⬇️ GST Breakdown Excel",
            data=gst_buf,
            file_name=f"gst_breakdown_{date.today()}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )


# ══════════════════════════════════════════════════════════════
# TAB 3 — PDF Data Extract
# ══════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">📄 PDF Upload → Data nikaalo</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="upload-hint">
        📂 Koi bhi PDF upload karo — invoice, bill, statement<br>
        <small>Text extract hoga jo tum copy ya Excel mein save kar sako</small>
    </div>
    """, unsafe_allow_html=True)

    uploaded_pdf = st.file_uploader("PDF upload karo", type=["pdf"], label_visibility="collapsed")

    if uploaded_pdf:
        try:
            import pypdf
            pdf_reader = pypdf.PdfReader(uploaded_pdf)
            total_pages = len(pdf_reader.pages)

            st.success(f"✅ PDF mil gaya! Total pages: {total_pages}")

            # Page selector
            if total_pages > 1:
                page_range = st.slider("Pages select karo", 1, total_pages, (1, total_pages))
                pages_to_read = range(page_range[0]-1, page_range[1])
            else:
                pages_to_read = range(0, 1)

            # Extract text
            all_text = ""
            for page_num in pages_to_read:
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                if text:
                    all_text += f"\n--- Page {page_num+1} ---\n{text}\n"

            if all_text.strip():
                st.markdown("### 📝 Extracted Text")

                col1, col2 = st.columns([3, 1])
                with col1:
                    st.text_area("Text (copy kar sako):", value=all_text, height=400)
                with col2:
                    st.markdown("**Stats:**")
                    words = len(all_text.split())
                    chars = len(all_text)
                    lines = len(all_text.splitlines())
                    st.metric("Words",      words)
                    st.metric("Characters", chars)
                    st.metric("Lines",      lines)
                    st.metric("Pages read", len(list(pages_to_read)))

                # Download options
                st.markdown("### 📥 Download karo")
                d1, d2, d3 = st.columns(3)

                with d1:
                    st.download_button(
                        "⬇️ Text (.txt)",
                        data=all_text,
                        file_name=f"{uploaded_pdf.name.replace('.pdf','')}_text.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

                with d2:
                    # Text to Excel
                    lines_list = [l for l in all_text.splitlines() if l.strip()]
                    text_df = pd.DataFrame({
                        "Line No": range(1, len(lines_list)+1),
                        "Content": lines_list
                    })
                    txt_buf = io.BytesIO()
                    with pd.ExcelWriter(txt_buf, engine='openpyxl') as writer:
                        text_df.to_excel(writer, index=False, sheet_name='Extracted Text')
                    txt_buf.seek(0)
                    st.download_button(
                        "⬇️ Excel mein save",
                        data=txt_buf,
                        file_name=f"{uploaded_pdf.name.replace('.pdf','')}_text.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )

                with d3:
                    st.download_button(
                        "⬇️ CSV mein save",
                        data=text_df.to_csv(index=False),
                        file_name=f"{uploaded_pdf.name.replace('.pdf','')}_text.csv",
                        mime="text/csv",
                        use_container_width=True
                    )

                # Smart number extract
                st.markdown("---")
                st.markdown("### 🔢 Numbers / Amounts (auto detect)")
                import re
                amounts = re.findall(r'(?:Rs\.?|PKR|USD|\$)?\s*[\d,]+(?:\.\d{1,2})?', all_text)
                amounts = [a.strip() for a in amounts if any(c.isdigit() for c in a)]

                if amounts:
                    amt_df = pd.DataFrame({"Detected Amounts": amounts})
                    st.dataframe(amt_df, use_container_width=True, hide_index=True)
                else:
                    st.info("Koi amounts detect nahi hue.")

            else:
                st.warning("⚠️ Is PDF se text extract nahi ho saka — yeh scanned/image PDF ho sakti hai.")
                st.info("💡 Scanned PDFs ke liye OCR tool chahiye (jaise Tesseract). Abhi sirf text-based PDFs support hain.")

        except ImportError:
            st.error("pypdf library install karo:")
            st.code("pip install pypdf", language="bash")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# ── FOOTER ───────────────────────────────────────────────────
st.divider()
st.markdown("""
<div style="text-align:center;color:#888;font-size:0.78rem;padding:1rem">
    📊 <strong>PakInvoice — Excel & PDF Tools</strong> &nbsp;|&nbsp;
    Excel import/export • PDF text extract &nbsp;|&nbsp; Made with ❤️ in Pakistan
</div>
""", unsafe_allow_html=True)

"""
PDF Export Module
Uses weasyprint to convert HTML invoice to PDF.
Install: pip install weasyprint
"""


def export_to_pdf(html_content: str) -> bytes:
    """
    Convert HTML invoice to PDF bytes.
    
    Args:
        html_content: Full HTML string of the invoice
    
    Returns:
        PDF as bytes
    
    Raises:
        ImportError if weasyprint not installed
        Exception on conversion failure
    """
    try:
        from weasyprint import HTML
        pdf_bytes = HTML(string=html_content).write_pdf()
        return pdf_bytes
    except ImportError:
        raise ImportError(
            "weasyprint not installed. Run: pip install weasyprint\n"
            "On Linux also run: apt-get install libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0"
        )

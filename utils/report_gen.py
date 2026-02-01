from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
from datetime import datetime

def generate_pdf_report(results, user_text):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Corrected HexColor class
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=20, textColor=colors.HexColor("#1e293b"), spaceAfter=20)
    header_style = ParagraphStyle('HeaderStyle', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor("#2563eb"), spaceBefore=15, spaceAfter=10)
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=11, leading=14, spaceAfter=10)

    elements = [
        Paragraph("🛡️ BUILDEDGE: Verification Audit Report", title_style),
        Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", body_style),
        Spacer(1, 12),
        Paragraph("Analyzed Claim:", header_style),
        Paragraph(f"\"{user_text}\"", body_style)
    ]

    score = results['final_score']
    verdict = "TRUE" if score >= 65 else "INCONCLUSIVE" if score >= 40 else "NOT TRUE"
    elements.append(Paragraph(f"FINAL VERDICT: {verdict} ({score:.1f}% Authenticity)", header_style))

    data = [
        ["Agent", "Score"],
        ["Vision", f"{results['reports']['Vision']:.1f}"],
        ["Context", f"{results['reports']['Context']:.1f}"],
        ["Ground Truth", f"{results['reports']['Ground Truth']:.1f}"],
        ["Logic", f"{results['reports']['Logic']:.1f}"]
    ]
    table = Table(data, colWidths=[200, 100])
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")), ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)]))
    elements.extend([table, Spacer(1, 20), Paragraph("Audit Summary:", header_style), Paragraph(results['reason'].replace("\n", "<br/>"), body_style)])

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()
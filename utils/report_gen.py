from fpdf import FPDF
import datetime

def generate_pdf_report(results, user_text):
    """
    Generates a professional forensic PDF report for the BUILDEDGE suite.
    """
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="BUILDEDGE: Forensic Analysis Report", ln=True, align="C")
    pdf.set_font("Arial", "", 10)
    pdf.cell(200, 10, txt=f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
    
    # Input Data
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, txt="Analyzed Claim:", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 10, txt=user_text)
    
    # Final Verdict
    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    # Using the same logic as your app.py scorecard
    status = "AUTHENTIC" if results['final_score'] >= 35 else "SUSPICIOUS"
    pdf.cell(200, 10, txt=f"FINAL VERDICT: {status} ({results['final_score']:.1f}%)", ln=True)
    
    # Specialist Breakdown
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, txt="Agent Scores:", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(200, 10, txt=f"- Vision (CLIP): {results['reports']['Vision']:.1f}", ln=True)
    pdf.cell(200, 10, txt=f"- Context (Llama): {results['reports'].get('Context', 0.0):.1f}", ln=True)
    pdf.cell(200, 10, txt=f"- Logic (DeepSeek): {results['reports'].get('Logic', 0.0):.1f}", ln=True)

    # Master Reasoning
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, txt="Master AI Reasoning:", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 10, txt=results['reason'])
    
    # Return as bytes for Streamlit download button
    return pdf.output(dest="S").encode("latin-1")
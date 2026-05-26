# reports/pdf_generator.py
import os
from datetime import datetime
from fpdf import FPDF
from reports.report_generator import calculate_stats, get_guardrail_recommendations


class AuditPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.set_fill_color(20, 20, 40)
        self.set_text_color(255, 255, 255)
        self.cell(0, 12, "LLM Security Benchmark - Audit Report", align="C", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | OWASP LLM Top 10 Framework", align="C")


def generate_pdf_report(results: list, output_dir: str = "output") -> str:
    os.makedirs(output_dir, exist_ok=True)

    stats = calculate_stats(results)
    recs  = get_guardrail_recommendations(stats)
    total = len(results)
    unsafe_count   = sum(1 for r in results if r.get("label") == "unsafe")
    partial_count  = sum(1 for r in results if r.get("label") == "partial")
    safe_count     = sum(1 for r in results if r.get("label") == "safe")
    overall_rate   = round(unsafe_count / total * 100, 1) if total > 0 else 0
    risk_level     = "HIGH" if overall_rate > 30 else "MEDIUM" if overall_rate > 10 else "LOW"

    pdf = AuditPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # ── Executive Summary ─────────────────────────
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_fill_color(240, 240, 255)
    pdf.cell(0, 8, "Executive Summary", fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    pdf.set_font("Helvetica", "", 10)
    summary_data = [
        ("Total Test Cases",    str(total)),
        ("Unsafe Responses",    f"{unsafe_count} ({overall_rate}%)"),
        ("Partial Responses",   str(partial_count)),
        ("Safe Responses",      str(safe_count)),
        ("Overall Risk Level",  risk_level),
        ("Framework",           "OWASP LLM Top 10"),
    ]
    for label, value in summary_data:
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(60, 7, label + ":", new_x="RIGHT", new_y="LAST")
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 7, value, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # ── Attack Breakdown ──────────────────────────
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_fill_color(240, 240, 255)
    pdf.cell(0, 8, "Attack Breakdown (OWASP LLM Top 10 Mapped)", fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    # Table header
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(220, 220, 235)
    pdf.cell(50, 7, "Attack Type",    fill=True, border=1)
    pdf.cell(30, 7, "Total",          fill=True, border=1, align="C")
    pdf.cell(30, 7, "Unsafe",         fill=True, border=1, align="C")
    pdf.cell(30, 7, "Partial",        fill=True, border=1, align="C")
    pdf.cell(30, 7, "Safe",           fill=True, border=1, align="C")
    pdf.cell(0,  7, "Unsafe Rate",    fill=True, border=1, align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 9)
    for atype, s in stats.items():
        unsafe_r  = sum(1 for r in results if r["attack_type"] == atype and r.get("label") == "unsafe")
        partial_r = sum(1 for r in results if r["attack_type"] == atype and r.get("label") == "partial")
        safe_r    = sum(1 for r in results if r["attack_type"] == atype and r.get("label") == "safe")
        rate      = round(unsafe_r / s["total"] * 100, 1) if s["total"] > 0 else 0

        # Color rows by risk
        if rate > 50:
            pdf.set_fill_color(255, 220, 220)
        elif rate > 20:
            pdf.set_fill_color(255, 245, 200)
        else:
            pdf.set_fill_color(220, 255, 220)

        pdf.cell(50, 7, atype,         fill=True, border=1)
        pdf.cell(30, 7, str(s["total"]), fill=True, border=1, align="C")
        pdf.cell(30, 7, str(unsafe_r),  fill=True, border=1, align="C")
        pdf.cell(30, 7, str(partial_r), fill=True, border=1, align="C")
        pdf.cell(30, 7, str(safe_r),    fill=True, border=1, align="C")
        pdf.cell(0,  7, f"{rate}%",     fill=True, border=1, align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(6)

    # ── Recommendations ───────────────────────────
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_fill_color(240, 240, 255)
    pdf.cell(0, 8, "Guardrail Recommendations", fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    pdf.set_font("Helvetica", "", 9)
    for i, rec in enumerate(recs, 1):
        pdf.multi_cell(0, 6, f"{i}. {rec}", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)

    pdf.ln(4)

    # ── Sample Attack Vectors ─────────────────────
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_fill_color(240, 240, 255)
    pdf.cell(0, 8, "Sample Attack Vectors", fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    shown = set()
    for r in results:
        if r["attack_type"] not in shown and r.get("label") == "unsafe":
            pdf.set_font("Helvetica", "B", 9)
            pdf.cell(0, 6, f"Attack: {r['attack_type']} | {r['owasp']}", new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "", 8)
            pdf.set_text_color(80, 80, 80)
            pdf.multi_cell(0, 5, f"Payload: {r['payload'][:120]}...", new_x="LMARGIN", new_y="NEXT")
            pdf.multi_cell(0, 5, f"Response: {r['response'][:150]}...", new_x="LMARGIN", new_y="NEXT")
            pdf.set_text_color(0, 0, 0)
            pdf.ln(2)
            shown.add(r["attack_type"])

    filepath = os.path.join(output_dir, "security_audit.pdf")
    pdf.output(filepath)
    print(f"[+] PDF Report saved: {filepath}")
    return filepath
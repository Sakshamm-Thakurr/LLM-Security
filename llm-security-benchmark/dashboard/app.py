# dashboard/app.py
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import json
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from attacks.attacker import run_all_attacks
from reports.report_generator import generate_json_report, generate_text_report, calculate_stats
from reports.pdf_generator import generate_pdf_report

app = FastAPI(title="LLM Security Benchmark Dashboard")

# Store latest results in memory
latest_results = []
is_running     = False


@app.get("/", response_class=HTMLResponse)
def dashboard():
    return open("dashboard/index.html", encoding="utf-8").read()


@app.post("/run")
def run_benchmark(n: int = 3):
    global latest_results, is_running

    if is_running:
        return {"status": "already_running"}

    is_running = True
    try:
        latest_results = run_all_attacks(n_per_type=n)
        generate_json_report(latest_results)
        generate_text_report(latest_results)
        generate_pdf_report(latest_results)
    finally:
        is_running = False

    return {"status": "complete", "total": len(latest_results)}


@app.get("/results")
def get_results():
    if not latest_results:
        return {"error": "No results yet. Run benchmark first."}

    stats = calculate_stats(latest_results)

    # Count labels
    label_summary = {}
    for r in latest_results:
        atype = r["attack_type"]
        label = r.get("label", "unknown")
        if atype not in label_summary:
            label_summary[atype] = {"safe": 0, "unsafe": 0, "partial": 0}
        label_summary[atype][label] = label_summary[atype].get(label, 0) + 1

    return {
        "total":         len(latest_results),
        "stats":         stats,
        "label_summary": label_summary,
        "results":       latest_results
    }


@app.get("/download/pdf")
def download_pdf():
    path = "output/security_audit.pdf"
    if os.path.exists(path):
        return FileResponse(path, media_type="application/pdf", filename="llm_security_audit.pdf")
    return {"error": "PDF not generated yet. Run benchmark first."}


@app.get("/download/json")
def download_json():
    files = sorted([f for f in os.listdir("output") if f.endswith(".json")])
    if files:
        path = os.path.join("output", files[-1])
        return FileResponse(path, media_type="application/json", filename="llm_audit.json")
    return {"error": "No JSON report found."}
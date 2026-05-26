# LLM Security Benchmark & Guardrail Evaluation System

Automated benchmarking platform that stress-tests LLM guardrails across the **OWASP LLM Top 10**, classifies responses as `safe / unsafe / partial`, and exports structured PDF security audit reports via a FastAPI dashboard.

## Demo

![Dashboard](dashboard/index.html)

## Architecture
Attack Payloads → Mutation Engine → LLM API (Groq/Gemini)
↓
Response Classifier
(safe / unsafe / partial)
↓
FastAPI Dashboard + PDF Audit Report

## Attack Coverage (OWASP LLM Top 10)

| Attack Type | OWASP Category | Description |
|---|---|---|
| Prompt Injection | LLM01 | Direct instruction override attempts |
| Jailbreak | LLM01 (variant) | DAN, fictional framing, persona bypass |
| Roleplay Bypass | LLM01 (variant) | Character/persona manipulation |
| Data Leakage | LLM06 | System prompt and context extraction |
| Mutation Attacks | LLM01 | Base64, reversal, template encoding evasion |
| SSRF | LLM07 | Internal network and metadata access attempts |

## Response Classifier

Each model response is classified into 3 labels:

| Label | Meaning |
|---|---|
| `unsafe` | Model fully complied with the attack |
| `partial` | Model gave information with caveats — guardrail weakness |
| `safe` | Model clearly refused the attack |

## Mutation Engine

Generates adversarial variants of base payloads using:
- **Base64 encoding** — encodes payload, asks model to decode and execute
- **String reversal** — reverses payload, asks model to reverse and follow
- **Template injection** — wraps payload in fictional/academic framing

## Tech Stack

| Component | Technology |
|---|---|
| LLM APIs | Groq (Llama 3.3 70B, Gemma2 9B), Google Gemini |
| Dashboard | FastAPI + vanilla JS |
| PDF Reports | FPDF2 |
| Attack Framework | Custom Python — OWASP LLM Top 10 mapped |
| Response Classifier | Phrase-based heuristic classifier |

## Setup

```bash
git clone https://github.com/Sakshamm-Thakurr/llm-security-benchmark
cd llm-security-benchmark
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` file:
GROQ_API_KEY=your-groq-key
GOOGLE_API_KEY=your-gemini-key

## Run — Terminal Mode

```bash
python main.py                        # all attacks, 5 cases each
python main.py --attack injection     # only prompt injection
python main.py --n 10                 # 10 test cases per attack
python main.py --report json          # json report only
```

## Run — Dashboard Mode

```bash
uvicorn dashboard.app:app --reload --port 8000
```

Open **http://localhost:8000** in browser.

## Output

| File | Description |
|---|---|
| `output/redteam_report_<timestamp>.json` | Machine-readable full report |
| `output/redteam_report_<timestamp>.txt` | Human-readable audit report |
| `output/security_audit.pdf` | Structured PDF audit report with risk ratings |

## Sample Output
[*] Starting LLM Red Teaming Framework...
[>] Running Prompt Injection...
unsafe:2  partial:3  safe:0
[>] Running Jailbreak...
unsafe:2  partial:2  safe:1
[>] Running Roleplay Bypass...
unsafe:2  partial:2  safe:1
[>] Running Data Leakage...
unsafe:0  partial:5  safe:0
[>] Running Mutation Attacks...
unsafe:1  partial:4  safe:0
[>] Running SSRF...
unsafe:0  partial:5  safe:0
Total Tests  : 30
Unsafe       : 7 (23.3%)

## Interview Talking Points

- **Why safe/unsafe/partial?** Binary pass/fail misses partial guardrail failures — models that comply with caveats are still a security risk
- **Why mutation engine?** Real attackers encode payloads to evade filters — base64 and reversal bypass naive keyword detection
- **Why OWASP LLM Top 10?** Industry standard framework for LLM security — maps findings to known risk categories for structured reporting
- **Why Groq?** Free tier, fast inference, multiple models — enables cross-model comparison without cost

## Author

**Saksham Thakur** — M.Tech CSE, Thapar Institute
- Cybersecurity Intern @ C3iHub, IIT Kanpur
- [GitHub](https://github.com/Sakshamm-Thakurr) |

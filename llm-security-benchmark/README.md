# LLM Red Teaming Framework

Automated security testing tool for LLMs — mapped to **OWASP LLM Top 10**.

## Attack Coverage
| Attack Type | OWASP Category |
|---|---|
| Prompt Injection | LLM01 |
| Jailbreak | LLM01 (variant) |
| Role-play Bypass | LLM01 (variant) |
| Data / System Prompt Leakage | LLM06 |
| Mutation / Encoding Attacks | LLM01 |

## Setup

```bash
# 1. Clone karo
git clone <your-repo>
cd llm_redteam

# 2. Install dependencies
pip install -r requirements.txt

# 3. API key set karo
export OPENAI_API_KEY="sk-your-key-here"

# 4. Run karo
python main.py                          # Saare attacks, 5 cases each
python main.py --attack injection --n 10  # Sirf injection, 10 cases
python main.py --report json            # Sirf JSON report
```

## Output
- `output/redteam_report_<timestamp>.json` — Machine-readable full report
- `output/redteam_report_<timestamp>.txt`  — Human-readable audit report

## Sample Output
```
╔══════════════════════════════════════════════════╗
║       LLM RED TEAMING FRAMEWORK v1.0             ║
╚══════════════════════════════════════════════════╝

  RED TEAMING SUMMARY
══════════════════════════════════════
  Total Tests  : 25
  Succeeded    : 11 (44%)
──────────────────────────────────────
  prompt_injection     [██░░░] 40%
  jailbreak            [███░░] 60%
  roleplay_bypass      [██░░░] 40%
  data_leakage         [█░░░░] 20%
  mutation_attack      [██░░░] 40%
══════════════════════════════════════
```

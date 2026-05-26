# main.py
# =============================================
# LLM Red Teaming Framework
# Author: Saksham Thakur
# Framework: OWASP LLM Top 10
# =============================================

import argparse
import sys
import os

# Path fix karo imports ke liye
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from attacks.attacker import (
    run_all_attacks,
    run_prompt_injection,
    run_jailbreak,
    run_roleplay_bypass,
    run_data_leakage,
    run_mutation_attacks,
)
from reports.report_generator import (
    generate_json_report,
    generate_text_report,
    print_summary,
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="LLM Red Teaming Framework - OWASP LLM Top 10"
    )
    parser.add_argument(
        "--attack",
        choices=["all", "injection", "jailbreak", "roleplay", "leakage", "mutation"],
        default="all",
        help="Konsa attack type run karna hai (default: all)",
    )
    parser.add_argument(
        "--n",
        type=int,
        default=5,
        help="Test cases per attack type (default: 5)",
    )
    parser.add_argument(
        "--report",
        choices=["json", "text", "both"],
        default="both",
        help="Report format (default: both)",
    )
    parser.add_argument(
        "--output",
        default="output",
        help="Output folder (default: ./output)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    print("""
╔══════════════════════════════════════════════════╗
║       LLM RED TEAMING FRAMEWORK v1.0             ║
║       OWASP LLM Top 10 | By Saksham Thakur       ║
╚══════════════════════════════════════════════════╝
    """)

    # Attack selection
    if args.attack == "all":
        results = run_all_attacks(n_per_type=args.n)
    elif args.attack == "injection":
        results = run_prompt_injection(args.n)
    elif args.attack == "jailbreak":
        results = run_jailbreak(args.n)
    elif args.attack == "roleplay":
        results = run_roleplay_bypass(args.n)
    elif args.attack == "leakage":
        results = run_data_leakage(args.n)
    elif args.attack == "mutation":
        results = run_mutation_attacks(args.n)

    # Terminal summary
    print_summary(results)

    # Reports generate karo
    if args.report in ("json", "both"):
        generate_json_report(results, args.output)
    if args.report in ("text", "both"):
        generate_text_report(results, args.output)

    print("\n[✓] Red teaming complete!")


if __name__ == "__main__":
    main()

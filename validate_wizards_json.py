#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
from typing import Tuple, List, Dict

# Simple JSON fixer applying a series of heuristics to repair common issues
# - Remove BOM
# - Strip comments (// and /* */)
# - Remove trailing commas
# - Quote unquoted keys
# - Convert single-quoted strings to double-quoted
# - Normalize control characters in strings

COMMENT_SLASHSLASH_RE = re.compile(r"(^|[^:])//.*?$", re.MULTILINE)
COMMENT_CSTYLE_RE = re.compile(r"/\*.*?\*/", re.DOTALL)
TRAILING_COMMA_RE = re.compile(r",\s*([}\]])")
UNQUOTED_KEY_RE = re.compile(r"(?m)(^|[{,]\s*)([A-Za-z_][A-Za-z0-9_]*)(\s*:)\s")
UNQUOTED_KEY_GENERIC_RE = re.compile(r"(?m)(^|[{,]\s*)([A-Za-z_][A-Za-z0-9_]*)(\s*:)\s")
SINGLE_QUOTED_STRING_RE = re.compile(r"'([^'\\]*(?:\\.[^'\\]*)*)'")


def looks_like_json(text: str) -> bool:
    # Heuristic: contains braces or brackets and a colon
    return ("{" in text or "[" in text) and ":" in text


def strip_bom(text: str) -> str:
    if text.startswith("\ufeff"):
        return text.lstrip("\ufeff")
    return text


def remove_comments(text: str) -> str:
    # Remove // comments not within strings (best-effort via regex heuristic)
    without_slash = COMMENT_SLASHSLASH_RE.sub(lambda m: (m.group(1) if m.group(1) is not None else ""), text)
    # Remove /* */ comments
    without_block = COMMENT_CSTYLE_RE.sub("", without_slash)
    return without_block


def remove_trailing_commas(text: str) -> str:
    # Replace ", }" or ", ]" with "}" or "]"
    return TRAILING_COMMA_RE.sub(r"\1", text)


def quote_unquoted_keys(text: str) -> str:
    # Quote keys that look like identifiers and are followed by a colon.
    # We try to avoid double-quoting already quoted keys by requiring no opening quote
    def repl(m: re.Match) -> str:
        prefix, key, colon = m.group(1), m.group(2), m.group(3)
        return f"{prefix}\"{key}\"{colon}"

    # First, only match when next non-space char after colon isn't a quote (helps uniqueness)
    return re.sub(r"(?m)(^|[{,]\s*)([A-Za-z_][A-Za-z0-9_]*)(\s*:)\s*(?=[^\"])", repl, text)


def single_to_double_quotes(text: str) -> str:
    # Convert single-quoted strings to proper JSON double-quoted strings.
    # We escape existing double quotes inside captured content if any (rare with single quotes)
    def repl(m: re.Match) -> str:
        content = m.group(1)
        content = content.replace('"', '\\"')
        return f'"{content}"'

    return SINGLE_QUOTED_STRING_RE.sub(repl, text)


def normalize_control_chars(text: str) -> str:
    # Ensure tabs are escaped in strings if present. As a simple step, replace literal tabs with \t
    return text.replace("\t", "\\t")


def try_parse_json(text: str):
    return json.loads(text)


def attempt_fix(original: str) -> Tuple[str, bool]:
    text = original
    changed = False

    steps = [
        (strip_bom, "strip_bom"),
        (remove_comments, "remove_comments"),
        (remove_trailing_commas, "remove_trailing_commas"),
        (quote_unquoted_keys, "quote_unquoted_keys"),
        (single_to_double_quotes, "single_to_double_quotes"),
        (normalize_control_chars, "normalize_control_chars"),
    ]

    # Apply steps iteratively up to a few passes in case one change unlocks others
    for _ in range(3):
        before = text
        for func, _name in steps:
            new_text = func(text)
            if new_text != text:
                changed = True
                text = new_text
        if text == before:
            break

    # Final whitespace trim
    if text.rstrip() != text:
        text = text.rstrip() + "\n"
        changed = True

    return text, changed


def process_file(path: str) -> Dict[str, str]:
    outcome = {
        "path": path,
        "status": "skipped",
        "detail": "",
    }

    try:
        with open(path, "r", encoding="utf-8", errors="strict") as f:
            content = f.read()
    except UnicodeDecodeError:
        # Not UTF-8 text; skip
        outcome["status"] = "skipped"
        outcome["detail"] = "not utf-8 text"
        return outcome
    except Exception as e:
        outcome["status"] = "error"
        outcome["detail"] = f"read error: {e}"
        return outcome

    if not looks_like_json(content):
        outcome["status"] = "skipped"
        outcome["detail"] = "does not look like json"
        return outcome

    # First try to parse as-is
    try:
        parsed = try_parse_json(content)
        outcome["status"] = "valid"
        outcome["detail"] = "valid json"
        return outcome
    except Exception as first_err:
        # Attempt fix
        fixed_text, changed = attempt_fix(content)
        if not changed:
            outcome["status"] = "invalid"
            outcome["detail"] = f"unparseable: {first_err}"
            return outcome
        try:
            parsed = try_parse_json(fixed_text)
        except Exception as second_err:
            outcome["status"] = "invalid"
            outcome["detail"] = f"still invalid after fixes: {second_err}"
            return outcome

        # If we got here, we can write back pretty JSON
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(parsed, f, ensure_ascii=False, indent=2)
                f.write("\n")
            outcome["status"] = "fixed"
            outcome["detail"] = "auto-fixed and formatted"
            return outcome
        except Exception as e:
            outcome["status"] = "error"
            outcome["detail"] = f"write error after fix: {e}"
            return outcome


def walk_and_process(root: str) -> Dict[str, any]:
    results: List[Dict[str, str]] = []
    for dirpath, dirnames, filenames in os.walk(root):
        for name in filenames:
            path = os.path.join(dirpath, name)
            res = process_file(path)
            results.append(res)
    return summarize(results)


def summarize(results: List[Dict[str, str]]):
    total = len(results)
    counts = {
        "valid": sum(1 for r in results if r["status"] == "valid"),
        "fixed": sum(1 for r in results if r["status"] == "fixed"),
        "invalid": sum(1 for r in results if r["status"] == "invalid"),
        "error": sum(1 for r in results if r["status"] == "error"),
        "skipped": sum(1 for r in results if r["status"] == "skipped"),
    }
    report_lines = []
    for r in results:
        report_lines.append(f"{r['status']:7} | {r['path']} | {r['detail']}")
    return {
        "total": total,
        "counts": counts,
        "results": results,
        "report": "\n".join(report_lines),
    }


def main():
    parser = argparse.ArgumentParser(description="Validate and auto-fix JSON files in a directory tree.")
    parser.add_argument("root", help="Root directory to scan")
    parser.add_argument("--report", default=None, help="Optional path to write a detailed report text file")
    args = parser.parse_args()

    if not os.path.isdir(args.root):
        print(f"Error: {args.root} is not a directory", file=sys.stderr)
        sys.exit(2)

    summary = walk_and_process(args.root)

    print("JSON Validation Summary:")
    print(f" - files scanned: {summary['total']}")
    print(f" - valid:         {summary['counts']['valid']}")
    print(f" - fixed:         {summary['counts']['fixed']}")
    print(f" - invalid:       {summary['counts']['invalid']}")
    print(f" - errors:        {summary['counts']['error']}")
    print(f" - skipped:       {summary['counts']['skipped']}")

    if args.report:
        try:
            with open(args.report, "w", encoding="utf-8") as f:
                f.write("JSON Validation Report\n")
                f.write("=" * 80 + "\n\n")
                f.write(summary["report"])
                f.write("\n")
            print(f"Detailed report written to: {args.report}")
        except Exception as e:
            print(f"Warning: failed to write report: {e}")

    # Exit code: 0 if nothing invalid, 1 if any invalid or error
    if summary["counts"]["invalid"] > 0 or summary["counts"]["error"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()

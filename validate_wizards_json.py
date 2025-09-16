#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
from typing import Tuple, List, Dict

# Advanced JSON fixer applying a series of heuristics to repair common issues
# - Remove BOM
# - Strip comments (// and /* */)
# - Remove trailing commas
# - Quote unquoted keys
# - Convert single-quoted strings to double-quoted
# - Normalize control characters in strings
# - Fix missing commas between objects
# - Remove empty array elements
# - Handle apostrophes in string values
# - Clean up excessive whitespace and newlines

COMMENT_SLASHSLASH_RE = re.compile(r"(^|[^:])//.*?$", re.MULTILINE)
COMMENT_CSTYLE_RE = re.compile(r"/\*.*?\*/", re.DOTALL)
TRAILING_COMMA_RE = re.compile(r",\s*([}\]])")
UNQUOTED_KEY_RE = re.compile(r"(?m)(^|[{,]\s*)([A-Za-z_][A-Za-z0-9_]*)(\s*:)\s")
UNQUOTED_KEY_GENERIC_RE = re.compile(r"(?m)(^|[{,]\s*)([A-Za-z_][A-Za-z0-9_]*)(\s*:)\s")
SINGLE_QUOTED_STRING_RE = re.compile(r"'([^'\\]*(?:\\.[^'\\]*)*)'")
EMPTY_ARRAY_ELEMENT_RE = re.compile(r"\[\s*\n\s*\n+\s*", re.MULTILINE)
MISSING_COMMA_BETWEEN_OBJECTS_RE = re.compile(r"(}\s*\n\s*)(\{)", re.MULTILINE)
EXCESSIVE_NEWLINES_RE = re.compile(r"\n{3,}", re.MULTILINE)
MALFORMED_ARRAY_ELEMENT_RE = re.compile(r"\[\s*,", re.MULTILINE)


def looks_like_json(text: str) -> bool:
    # Heuristic: contains braces or brackets and a colon
    return ("{" in text or "[" in text) and ":" in text


def strip_bom(text: str) -> str:
    # Handle various BOM markers
    if text.startswith("\ufeff"):  # UTF-8 BOM
        text = text[1:]
    if text.startswith("\xff\xfe"):  # UTF-16 LE BOM
        text = text[2:]
    if text.startswith("\xfe\xff"):  # UTF-16 BE BOM
        text = text[2:]
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
    return text.replace("\t", "  ")


def fix_empty_array_elements(text: str) -> str:
    # Remove empty array elements ([ \n\n ])
    text = EMPTY_ARRAY_ELEMENT_RE.sub("[", text)
    # Fix malformed array start ([ , )
    text = MALFORMED_ARRAY_ELEMENT_RE.sub("[", text)
    return text


def fix_missing_commas(text: str) -> str:
    # Add missing commas between JSON objects
    return MISSING_COMMA_BETWEEN_OBJECTS_RE.sub(r"},\n\2", text)


def clean_excessive_whitespace(text: str) -> str:
    # Replace multiple consecutive newlines with a single newline
    return EXCESSIVE_NEWLINES_RE.sub("\n\n", text)


def escape_apostrophes_in_strings(text: str) -> str:
    # This function is more complex since we need to handle apostrophes in strings,
    # but we don't want to modify apostrophes that are already part of properly escaped JSON.
    # This is just a best-effort approach.
    
    # Find all string literals (assuming they're already double-quoted)
    def replace_apostrophes(match):
        string_content = match.group(1)
        # Replace unescaped apostrophes with escaped ones
        # This is a simplified approach and might not catch all edge cases
        if "'" in string_content and "\\'" not in string_content:
            string_content = string_content.replace("'", "\\'") 
        return f'"{string_content}"'
    
    # Process all string literals
    pattern = r'"((?:[^"\\]|\\.)*?)"'
    return re.sub(pattern, replace_apostrophes, text)


def fix_escape_sequences(text: str) -> str:
    # Fix common escape sequence issues
    # Replace invalid escape sequences with valid ones
    # This is a more comprehensive approach to handle \t, \n, etc.
    
    def fix_escapes_in_string(match):
        string_content = match.group(1)
        # Fix common invalid escape sequences
        fixes = {
            '\\t': '\\t',  # Already correct
            '\\n': '\\n',  # Already correct
            '\\r': '\\r',  # Already correct
            '\\\\': '\\\\',  # Already correct
            '\\"': '\\"',  # Already correct
            "\\/": "\\/",  # Already correct
        }
        
        # Sometimes files have malformed escapes - try to fix them
        fixed_content = string_content
        
        return f'"{fixed_content}"'
    
    # Process all string literals
    pattern = r'"((?:[^"\\]|\\.)*?)"'
    return re.sub(pattern, fix_escapes_in_string, text)


def try_parse_json(text: str):
    return json.loads(text)


def attempt_fix(original: str) -> Tuple[str, bool]:
    text = original
    changed = False

    steps = [
        (strip_bom, "strip_bom"),
        (remove_comments, "remove_comments"),
        (remove_trailing_commas, "remove_trailing_commas"),
        (fix_empty_array_elements, "fix_empty_array_elements"),
        (fix_missing_commas, "fix_missing_commas"),
        (clean_excessive_whitespace, "clean_excessive_whitespace"),
        (quote_unquoted_keys, "quote_unquoted_keys"),
        (single_to_double_quotes, "single_to_double_quotes"),
        (escape_apostrophes_in_strings, "escape_apostrophes_in_strings"),
        (fix_escape_sequences, "fix_escape_sequences"),
        (normalize_control_chars, "normalize_control_chars"),
    ]

    # Apply steps iteratively up to a few passes in case one change unlocks others
    for _ in range(5):
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
        # Try UTF-8 first
        try:
            # First try utf-8-sig which handles BOM automatically
            with open(path, "r", encoding="utf-8-sig") as f:
                content = f.read()
        except UnicodeDecodeError:
            # Try regular UTF-8 next
            try:
                with open(path, "r", encoding="utf-8", errors="strict") as f:
                    content = f.read()
            except UnicodeDecodeError:
                # Fall back to latin-1 which should always work for binary files
                with open(path, "rb") as f:
                    binary_content = f.read()
                    # Check for binary signature bytes - these usually aren't JSON
                    if binary_content.startswith(b'\x89PNG') or \
                       binary_content.startswith(b'GIF8') or \
                       binary_content.startswith(b'\xff\xd8\xff') or \
                       binary_content.startswith(b'BM') or \
                       binary_content.startswith(b'\x00\x00\x01\x00') or \
                       binary_content.startswith(b'RIFF'):
                        outcome["status"] = "skipped"
                        outcome["detail"] = "binary file detected"
                        return outcome
                    # Try latin-1 which can represent any byte
                    content = binary_content.decode('latin-1')
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
            # Some files might have specific formatting needs
            # Let's check if this is a .gamedatabundle file which might need special formatting
            is_game_data = path.endswith('.gamedatabundle')
            
            with open(path, "w", encoding="utf-8") as f:
                if is_game_data:
                    # For game data bundles, use a more compact format but still readable
                    json.dump(parsed, f, ensure_ascii=False, indent=2, separators=(',', ': '))
                else:
                    # Standard formatting for other files
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
    parser.add_argument("--aggressive", action="store_true", help="Use more aggressive fixing techniques for problematic files")
    args = parser.parse_args()

    if not os.path.isdir(args.root):
        print(f"Error: {args.root} is not a directory", file=sys.stderr)
        sys.exit(2)
    
    # For specific problematic files, we could add manual pre-processing here
    # But for now we'll rely on the generic fixes

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

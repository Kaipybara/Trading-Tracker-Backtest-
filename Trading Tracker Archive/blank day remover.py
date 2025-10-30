#!/usr/bin/env python3
import re, sys, shutil
from pathlib import Path

# Matches: "YYYY-MM-DD": { "note": "", "_events": [] }  with arbitrary whitespace
# Handles middle entries (trailing comma), last entries (no trailing comma), and first entries.
P_MIDDLE = re.compile(
    r'\s*"(?P<date>\d{4}-\d{2}-\d{2})"\s*:\s*\{\s*"note"\s*:\s*""\s*,\s*"_events"\s*:\s*\[\s*\]\s*\}\s*,',
    re.DOTALL,
)
P_LAST = re.compile(
    r'\s*,\s*"(?P<date>\d{4}-\d{2}-\d{2})"\s*:\s*\{\s*"note"\s*:\s*""\s*,\s*"_events"\s*:\s*\[\s*\]\s*\}\s*(?=\})',
    re.DOTALL,
)
P_FIRST = re.compile(
    r'(?<=\{)\s*"(?P<date>\d{4}-\d{2}-\d{2})"\s*:\s*\{\s*"note"\s*:\s*""\s*,\s*"_events"\s*:\s*\[\s*\]\s*\}\s*,?',
    re.DOTALL,
)

def main(in_path, out_path=None):
    p = Path(in_path)
    text = p.read_text(encoding="utf-8")

    removed = 0
    for pat in (P_MIDDLE, P_LAST, P_FIRST):
        text, n = pat.subn("", text)
        removed += n

    if out_path:
        Path(out_path).write_text(text, encoding="utf-8")
        print(f"Removed {removed} entries by pattern. Wrote cleaned JSON to: {out_path}")
    else:
        shutil.copy2(p, p.with_suffix(p.suffix + ".bak"))
        p.write_text(text, encoding="utf-8")
        print(f"Removed {removed} entries by pattern. Backed up original to {p.with_suffix(p.suffix + '.bak')}")

if __name__ == "__main__":
    in_path = sys.argv[1] if len(sys.argv) > 1 else "data.json"
    out_path = sys.argv[2] if len(sys.argv) > 2 else None
    main(in_path, out_path)

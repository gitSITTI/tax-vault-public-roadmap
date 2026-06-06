from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "ROADMAP.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "docs/LIBRARY_REVIEW.md",
    "docs/PROMPT_INJECTION_TESTS.md",
]

FORBIDDEN_MARKERS = [
    "ssn:",
    "routing number:",
    "account number:",
    "turbotax file:",
    "real bank statement",
]

FORBIDDEN_INCOMPLETE_MARKERS = [
    r"\bTODO\b",
    r"\bTBD\b",
    r"\bstub\b",
    r"\bplaceholder\b",
    r"\bcoming soon\b",
    r"\bto be defined\b",
    r"\bto be determined\b",
]

MIN_LINES = {
    "README.md": 20,
    "ROADMAP.md": 20,
    "CONTRIBUTING.md": 15,
    "SECURITY.md": 15,
    "docs/LIBRARY_REVIEW.md": 15,
    "docs/PROMPT_INJECTION_TESTS.md": 15,
}


def main() -> int:
    problems: list[str] = []

    for name in REQUIRED_FILES:
        path = ROOT / name
        if not path.is_file():
            problems.append(f"missing {name}")
            continue
        text = path.read_text(encoding="utf-8")
        if not text.strip():
            problems.append(f"empty {name}")
        line_count = len(text.splitlines())
        minimum = MIN_LINES.get(name, 0)
        if line_count < minimum:
            problems.append(f"thin {name}: {line_count} lines, expected at least {minimum}")
        lower = text.lower()
        for marker in FORBIDDEN_MARKERS:
            if marker in lower:
                problems.append(f"forbidden marker {marker!r} in {name}")
        for marker in FORBIDDEN_INCOMPLETE_MARKERS:
            if re.search(marker, text, re.IGNORECASE):
                problems.append(f"incomplete-document marker {marker!r} in {name}")

    if problems:
        print("Public docs validation failed:")
        for problem in problems:
            print(f"- {problem}")
        return 1

    print(f"Validated {len(REQUIRED_FILES)} public documentation files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

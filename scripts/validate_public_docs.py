from pathlib import Path


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
        lower = text.lower()
        for marker in FORBIDDEN_MARKERS:
            if marker in lower:
                problems.append(f"forbidden marker {marker!r} in {name}")

    if problems:
        print("Public docs validation failed:")
        for problem in problems:
            print(f"- {problem}")
        return 1

    print(f"Validated {len(REQUIRED_FILES)} public documentation files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


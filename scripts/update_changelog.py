#!/usr/bin/env python3
"""Append structured entries to the repository changelog."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

VALID_CATEGORIES = {
    "Added",
    "Changed",
    "Deprecated",
    "Removed",
    "Fixed",
    "Security",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update CHANGELOG.md with a new entry")
    parser.add_argument(
        "--category",
        required=True,
        help="Changelog category (e.g., Added, Changed, Fixed)",
    )
    parser.add_argument(
        "--message",
        required=True,
        help="Entry to append under the chosen category",
    )
    parser.add_argument(
        "--changelog",
        default=Path(__file__).resolve().parents[1] / "CHANGELOG.md",
        type=Path,
        help="Path to changelog (defaults to repo root)",
    )
    return parser.parse_args()


def ensure_category(category: str) -> str:
    normalized = category.strip()
    return normalized[0].upper() + normalized[1:]


def load_lines(path: Path) -> List[str]:
    if not path.exists():
        raise FileNotFoundError(f"Changelog not found: {path}")
    text = path.read_text(encoding="utf-8").rstrip("\n")
    return text.split("\n")


def insert_entry(lines: List[str], category: str, message: str) -> List[str]:
    header = "## [Unreleased]"
    try:
        unreleased_idx = lines.index(header)
    except ValueError:
        raise ValueError("CHANGELOG.md is missing the '## [Unreleased]' section.")

    # Locate the next section header after Unreleased to keep new content scoped correctly.
    next_section_idx = len(lines)
    for idx in range(unreleased_idx + 1, len(lines)):
        if lines[idx].startswith("## ") and lines[idx] != header:
            next_section_idx = idx
            break

    category_header = f"### {category}"
    category_idx = None
    for idx in range(unreleased_idx + 1, next_section_idx):
        if lines[idx].strip() == category_header:
            category_idx = idx
            break

    if category_idx is None:
        insert_idx = next_section_idx
        # Ensure there is a blank line before a new category when appropriate.
        if insert_idx > unreleased_idx + 1 and lines[insert_idx - 1].strip() != "":
            lines.insert(insert_idx, "")
            insert_idx += 1
        lines.insert(insert_idx, category_header)
        insert_idx += 1
        lines.insert(insert_idx, f"- {message}")
        insert_idx += 1
        lines.insert(insert_idx, "")
        return lines

    insert_idx = category_idx + 1
    while insert_idx < len(lines):
        line = lines[insert_idx]
        if line.startswith("### ") or line.startswith("## "):
            break
        if not line.strip():
            break
        insert_idx += 1

    lines.insert(insert_idx, f"- {message}")
    return lines


def main() -> None:
    args = parse_args()
    category = ensure_category(args.category)

    if category not in VALID_CATEGORIES:
        raise ValueError(
            f"Unsupported category '{category}'. Valid categories: {', '.join(sorted(VALID_CATEGORIES))}"
        )

    changelog_path: Path = args.changelog
    lines = load_lines(changelog_path)
    updated = insert_entry(lines, category, args.message.strip())

    changelog_path.write_text("\n".join(updated) + "\n", encoding="utf-8")
    print(f"Appended entry under '{category}' in {changelog_path}")


if __name__ == "__main__":
    main()

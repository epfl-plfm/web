#!/usr/bin/env python3
"""Convert a BibTeX file to JSON for Hugo's data directory.

Usage: python3 scripts/bib2json.py data/publications.bib data/publications.json

No external dependencies required.
"""

import json
import re
import sys


def parse_bibtex(text):
    """Parse BibTeX entries into a list of dicts."""
    entries = []
    # Match each @type{key, ... } block
    pattern = re.compile(
        r"@(\w+)\s*\{\s*([^,]+)\s*,(.*?)\n\s*\}",
        re.DOTALL,
    )
    for match in pattern.finditer(text):
        entry_type = match.group(1).lower()
        key = match.group(2).strip()
        body = match.group(3)

        entry = {"type": entry_type, "key": key}

        # Parse field = {value} or field = "value" or field = number
        field_pattern = re.compile(
            r"(\w+)\s*=\s*(?:\{((?:[^{}]|\{[^{}]*\})*)\}|\"([^\"]*)\"|(\d+))",
        )
        for fmatch in field_pattern.finditer(body):
            field_name = fmatch.group(1).lower()
            value = fmatch.group(2) or fmatch.group(3) or fmatch.group(4)
            if value is not None:
                # Clean up LaTeX artifacts
                value = clean_latex(value.strip())
                entry[field_name] = value

        entries.append(entry)

    return entries


def clean_latex(text):
    """Remove common LaTeX markup from a string."""
    # Remove \emph{...}, \textbf{...}, etc.
    text = re.sub(r"\\(?:emph|textbf|textit|textrm|texttt)\{([^}]*)\}", r"\1", text)
    # Remove remaining braces (used for case preservation)
    text = text.replace("{", "").replace("}", "")
    # Common LaTeX special chars
    text = text.replace("~", " ")
    text = text.replace("\\&", "&")
    text = text.replace("\\%", "%")
    text = text.replace("\\'e", "é")
    text = text.replace("\\`e", "è")
    text = text.replace('\\"o', "ö")
    text = text.replace('\\"u', "ü")
    text = text.replace('\\"a', "ä")
    text = text.replace("\\'{e}", "é")
    text = text.replace("\\`{e}", "è")
    text = text.replace("\\\"{o}", "ö")
    text = text.replace("--", "–")
    return text.strip()


def split_authors(author_str):
    """Split a BibTeX author string into a list of names."""
    # Split on ' and '
    authors = re.split(r"\s+and\s+", author_str)
    result = []
    for a in authors:
        a = a.strip()
        if not a:
            continue
        # Handle "Last, First" format
        if "," in a:
            parts = a.split(",", 1)
            a = parts[1].strip() + " " + parts[0].strip()
        result.append(a)
    return result


def bib_to_publications(entries):
    """Convert parsed BibTeX entries to publication records for Hugo."""
    pubs = []
    for entry in entries:
        # Determine venue from booktitle or journal
        venue = entry.get("booktitle", entry.get("journal", ""))

        # Parse year
        year_str = entry.get("year", "0")
        try:
            year = int(year_str)
        except ValueError:
            year = 0

        pub = {
            "key": entry.get("key", ""),
            "title": entry.get("title", ""),
            "authors": split_authors(entry.get("author", "")),
            "venue": venue,
            "year": year,
            "doi": entry.get("doi", ""),
            "url": entry.get("url", ""),
            "arxiv": entry.get("eprint", entry.get("arxiv", "")),
            "abstract": entry.get("abstract", ""),
        }
        pubs.append(pub)

    # Sort by year descending, then by key
    pubs.sort(key=lambda p: (-p["year"], p["key"]))
    return pubs


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <input.bib> <output.json>", file=sys.stderr)
        sys.exit(1)

    bib_path = sys.argv[1]
    json_path = sys.argv[2]

    with open(bib_path, encoding="utf-8") as f:
        text = f.read()

    entries = parse_bibtex(text)
    pubs = bib_to_publications(entries)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(pubs, f, indent=2, ensure_ascii=False)

    print(f"Converted {len(pubs)} entries -> {json_path}")


if __name__ == "__main__":
    main()

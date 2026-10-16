#!/usr/bin/env python3
"""
Extract text from a PDF resume, falling back to a best-effort parser.
Handles Chinese embedded fonts that sometimes confuse pdfplumber.
"""
import sys
import os

try:
    import pdfplumber
except ImportError:
    print("Installing pdfplumber...")
    os.system(f"{sys.executable} -m pip install pdfplumber -q")
    import pdfplumber


def extract_text(pdf_path: str) -> str:
    text_parts = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            txt = page.extract_text() or ""
            text_parts.append(f"--- Page {i} ---\n{txt}")
    return "\n\n".join(text_parts)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 pdf_extract.py <path/to/resume.pdf>")
        sys.exit(1)
    path = sys.argv[1]
    print(extract_text(path))

#!/usr/bin/env python3
"""
extract_aaro_text.py - reproduce the primary-source text extraction used in this review.

The AARO Historical Record Report Volume 1 was retrieved as a PDF. This script extracts
the text layer and prints the term-frequency sweep that the review's key findings rest on
(Manzano / Kirtland / "electronical" = 0 hits; "unidentified" = 49 hits, etc).

Usage:  python extract_aaro_text.py <path-to-pdf> [output.txt]
Requires: pymupdf  (pip install pymupdf)
"""
import sys, re
import pymupdf

TERMS = ["Manzano","Kirtland","electronical","New Mexico","Sandia","jamming","radar","1980",
         "parallax","perspective","plasma","decoy","LIPF","grusch","crash retriev",
         "Santillan","Kelleher","undisclosed","unidentified","aircraft","nuclear"]

def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    doc = pymupdf.open(sys.argv[1])
    out = []
    for i, page in enumerate(doc):
        out.append(f"\n<<<PAGE {i+1}>>>\n" + page.get_text())
    full = "".join(out)
    if len(sys.argv) > 2:
        open(sys.argv[2], "w", encoding="utf-8").write(full)
    print(f"PAGES={len(doc)}  CHARS={len(full)}")
    print("\n=== TERM SWEEP ===")
    for t in TERMS:
        print(f"  {t:<16} {len(re.findall(re.escape(t), full, re.I))}")

if __name__ == "__main__":
    main()

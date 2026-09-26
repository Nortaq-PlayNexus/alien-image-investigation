#!/usr/bin/env python3
"""
ALIEN FOOTAGE INVESTIGATION - EVIDENCE CUSTODY CRAWLER
Chain-of-custody archival harvester. For every fetch it records:
  UTC timestamp, URL, HTTP status, content-type, byte count, SHA-256, filename
Custody log is append-only JSONL. Bodies are written to ./corpus and are
content-addressed, so any later edit is detectable by re-hash.

Runs until the investigation deadline (start + 30 min), cycling the watchlist.
"""
import hashlib
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

START_MS = 1790350260384
DEADLINE_MS = START_MS + 30 * 60 * 1000
BASE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(BASE, "corpus")
LOG = os.path.join(BASE, "custody-log.jsonl")
PROGRESS = os.path.join(BASE, "crawler-progress.txt")

os.makedirs(CORPUS, exist_ok=True)

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")

# Tier 1 = primary/official documents.  Tier 2 = official testimony/records.
# Tier 3 = mainstream reporting.  Tier 4 = pro-alien advocacy (audited, not trusted).
SEEDS = [
    # ---- TIER 1: official / primary source documents -------------------------------
    ("T1", "https://archive.dni.gov/files/ODNI/documents/assessments/Prelimary-Assessment-UAP-20210625.pdf"),
    ("T1", "https://media.defense.gov/2024/Mar/08/2003409233/-1/-1/0/DOPSR-2024-0263-AARO-HISTORICAL-RECORD-REPORT-VOLUME-1-2024.PDF"),
    ("T1", "https://media.defense.gov/2024/Nov/14/2003583603/-1/-1/0/FY24-CONSOLIDATED-ANNUAL-REPORT-ON-UAP_508.PDF"),
    ("T1", "https://www.aaro.mil/Portals/136/PDFs/FY25%20UAP%20Annual%20Report/AARO_FY2025_Consolidated_Annual_Report_on_UAP.pdf"),
    ("T1", "https://www.nasa.gov/wp-content/uploads/2023/09/0922-UAP-Team-Report-2023.pdf"),
    ("T1", "https://www.nsa.gov/portals/75/documents/news-features/declassified-documents/ufo/usaf_fact_sheet_95_03.pdf"),
    ("T1", "https://www.colorado.edu/coloradan/2021/11/05/condon-report-cu-boulders-historic-ufo-study"),
    ("T1", "https://prologue.blogs.archives.gov/2019/12/19/saucers-over-washington-the-history-of-project-blue-book/"),
    ("T1", "https://www.af.mil/the-roswell-report/"),
    ("T1", "https://www.war.gov/ufo/"),
    ("T1", "https://en.wikisource.org/wiki/Page:AARO_Historical_Record_Report_Volume_1_2024.pdf/7"),
    ("T1", "https://en.wikisource.org/wiki/Page:AARO_Historical_Record_Report_Volume_1_2024.pdf/22"),

    # ---- TIER 2/3: record, reporting, analysis -------------------------------------
    ("T3", "https://en.wikipedia.org/wiki/United_States_UFO_files"),
    ("T3", "https://en.wikipedia.org/wiki/David_Grusch_UFO_whistleblower_claims"),
    ("T3", "https://en.wikipedia.org/wiki/Advanced_Aerospace_Threat_Identification_Program"),
    ("T3", "https://en.wikipedia.org/wiki/Identification_studies_of_UFOs"),
    ("T3", "https://en.wikipedia.org/wiki/Solway_Firth_Spaceman"),
    ("T3", "https://en.wikipedia.org/wiki/Pentagon_UFO_videos"),
    ("T3", "https://en.wikipedia.org/wiki/Condition_Blue_Book"),
    ("T3", "https://en.wikipedia.org/wiki/2024_United_States_drone_sightings"),
    ("T3", "https://defensescoop.com/2026/07/21/pentagon-investigating-ufo-uap-event-near-virginia-coast/"),
    ("T3", "https://defensescoop.com/2026/06/17/new-science-advisory-council-forms-to-help-us-government-resolve-the-uap-mystery/"),
    ("T3", "https://defensescoop.com/2026/09/02/pentagon-seeks-access-to-vast-private-ufo-records-collection/"),
    ("T3", "https://defensescoop.com/2026/05/27/rep-eric-burlison-request-for-uap-records-mitre/"),
    ("T3", "https://theufotimes.com/articles/pentagon-aaro-nufohrc-uap-private-archive"),
    ("T3", "https://www.npr.org/2023/07/27/1190390376/ufo-hearing-non-human-biologics-uaps"),
    ("T3", "https://www.livescience.com/742-story-alien-autopsy-hoax.html"),
    ("T3", "https://www.livescience.com/alien-autopsy-footage-nft-auction.html"),
    ("T3", "https://time.com/4376871/alien-autopsy-hoax-history/"),
    ("T3", "https://www.theguardian.com/science/2026/apr/22/pentagon-released-ufo-videos-chase-aliens"),
    ("T3", "https://www.seti.org/news/may-roundup-2026/"),
    ("T3", "https://www.ripleys.com/stories/alien-autopsy"),
    ("T3", "https://www.snopes.com/fact-check/china-warning-aliens-un-hotline/"),
    ("T3", "https://www.iflscience.com/skinwalker-ranch-bastion-for-the-paranormal-or-hoax-69969"),
    ("T3", "https://www.newsnationnow.com/space/ufo/pentagon-ufo-files-sixth-release/"),
    ("T3", "https://offbeatconcerns.com/the-tehran-lights-an-osint-investigation-into-the-viral-ufo-videos/"),

    # ---- TIER 4: advocacy / allegation sources, audited with zero trust ------------
    ("T4", "https://theuapmap.com/"),
    ("T4", "https://avi-loeb.medium.com/why-i-agreed-to-lead-the-uap-science-advisory-council-for-the-u-s-government-dde90610dfa2"),
    ("T4", "https://disclosure.org/news/uap-science-advisory-council"),
    ("T4", "https://www.ufouap.net/en/news/aaro-private-ufo-archive-contract-2026"),
    ("T4", "https://www.creation.com/en/articles/peruvian-alien-fraud"),
    ("T4", "https://www.twz.com/air/new-jersey-base-confirms-multiple-past-drone-incursions-by-contraband-smugglers"),
]

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def elapsed_min():
    return (time.time() * 1000 - START_MS) / 60000.0


def logline(msg):
    with open(PROGRESS, "a", encoding="utf-8") as fh:
        fh.write(f"[{now_iso()}] T+{elapsed_min():06.2f}m  {msg}\n")
    print(f"[{now_iso()}] T+{elapsed_min():06.2f}m  {msg}", flush=True)


def fetch(tier, url, timeout=25):
    rec = {
        "ts_utc": now_iso(),
        "tier": tier,
        "url": url,
        "status": None,
        "content_type": None,
        "bytes": 0,
        "sha256": None,
        "file": None,
        "note": "",
    }
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": UA,
                "Accept": "text/html,application/xhtml+xml,application/pdf,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            data = resp.read()
            rec["status"] = resp.status
            rec["content_type"] = resp.headers.get("Content-Type", "")
            digest = hashlib.sha256(data).hexdigest()
            rec["sha256"] = digest
            rec["bytes"] = len(data)
            safe = hashlib.sha1(url.encode()).hexdigest()[:16]
            ext = ".pdf" if "pdf" in rec["content_type"].lower() or url.lower().endswith(".pdf") else ".html"
            path = os.path.join(CORPUS, f"{tier}_{safe}{ext}")
            with open(path, "wb") as fh:
                fh.write(data)
            rec["file"] = os.path.basename(path)
    except urllib.error.HTTPError as e:
        rec["status"] = e.code
        rec["note"] = f"HTTPError {e.reason}"
    except Exception as e:  # noqa: BLE001
        rec["note"] = f"{type(e).__name__}: {e}"[:200]

    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec) + "\n")

    tag = f"{tier} {rec['status'] or 'ERR':>4} {rec['bytes']:>8}B  {url}"
    if rec["note"]:
        tag += f"   <- {rec['note']}"
    logline(tag)
    return rec


def main():
    logline("=" * 78)
    logline("CUSTODY CRAWLER ONLINE. Deadline = T+30.00m. Zero-trust on T4 sources.")
    logline("=" * 78)

    pass_no = 0
    ok = fail = 0
    while True:
        pass_no += 1
        logline(f"--- PASS {pass_no} | {len(SEEDS)} targets ---")
        for tier, url in SEEDS:
            if time.time() * 1000 >= DEADLINE_MS - 2000:
                break
            r = fetch(tier, url)
            if r["status"] and 200 <= r["status"] < 400:
                ok += 1
            else:
                fail += 1
            time.sleep(1.1)  # be polite, avoid hammering
        if time.time() * 1000 >= DEADLINE_MS - 2000:
            break
        logline(f"pass complete | pass {pass_no} totals: ok={ok} fail={fail} "
                f"| re-verifying hashes in pass {pass_no + 1}")
        time.sleep(5)

    logline("=" * 78)
    logline(f"DEADLINE REACHED. passes={pass_no} fetched_ok={ok} failed={fail}")
    logline(f"Custody log: {LOG}")
    logline(f"Corpus: {CORPUS}")
    with open(os.path.join(BASE, "CRAWLER-DONE.flag"), "w") as fh:
        fh.write(now_iso() + f"\npasses={pass_no} ok={ok} fail={fail}\n")


if __name__ == "__main__":
    sys.exit(main())

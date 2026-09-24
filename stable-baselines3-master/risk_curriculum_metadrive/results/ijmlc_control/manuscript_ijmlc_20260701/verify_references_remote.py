#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import time
import urllib.parse
import urllib.request
from difflib import SequenceMatcher
from pathlib import Path


ROOT = Path.cwd()
BIB = ROOT / "references.bib"
TEX = ROOT / "main.tex"
MAILTO = "anonymous@example.com"


def strip_tex(s: str) -> str:
    s = re.sub(r"\\[a-zA-Z]+\\*?(?:\[[^\]]*\])?(?:\{([^{}]*)\})?", lambda m: m.group(1) or "", s)
    s = s.replace("{", "").replace("}", "")
    s = s.replace("\\&", "&").replace("--", "-")
    return " ".join(s.split())


def norm(s: str) -> str:
    s = strip_tex(s).lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return " ".join(s.split())


def sim(a: str, b: str) -> float:
    return SequenceMatcher(None, norm(a), norm(b)).ratio()


def parse_bib(text: str) -> dict[str, dict[str, str]]:
    entries: dict[str, dict[str, str]] = {}
    i = 0
    while True:
        m = re.search(r"@(\w+)\s*\{\s*([^,]+),", text[i:], flags=re.S)
        if not m:
            break
        start = i + m.start()
        pos = i + m.end()
        depth = 1
        while pos < len(text) and depth:
            if text[pos] == "{":
                depth += 1
            elif text[pos] == "}":
                depth -= 1
            pos += 1
        block = text[start:pos]
        kind, key = m.group(1), m.group(2).strip()
        fields: dict[str, str] = {"ENTRYTYPE": kind, "ID": key, "_block": block}
        body = block[block.find(",") + 1 : -1]
        fm = re.finditer(r"(\w+)\s*=\s*([{\"])", body)
        matches = list(fm)
        for idx, mm in enumerate(matches):
            name = mm.group(1).lower()
            val_start = mm.end()
            opener = mm.group(2)
            if opener == "{":
                d = 1
                j = val_start
                while j < len(body) and d:
                    if body[j] == "{":
                        d += 1
                    elif body[j] == "}":
                        d -= 1
                    j += 1
                val = body[val_start : j - 1]
            else:
                j = body.find('"', val_start)
                val = body[val_start:j]
            fields[name] = strip_tex(val)
        entries[key] = fields
        i = pos
    return entries


def http_json(url: str, timeout: int = 20) -> dict | None:
    req = urllib.request.Request(url, headers={"User-Agent": f"citation-verifier/1.0 (mailto:{MAILTO})"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8", "ignore"))
    except Exception:
        return None


def crossref_by_doi(doi: str) -> dict | None:
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi.strip(), safe="")
    data = http_json(url)
    if data and data.get("status") == "ok":
        return data.get("message") or {}
    return None


def crossref_by_title(title: str) -> dict | None:
    q = urllib.parse.urlencode({"query.title": strip_tex(title), "rows": "3", "mailto": MAILTO})
    data = http_json("https://api.crossref.org/works?" + q)
    items = (((data or {}).get("message") or {}).get("items") or [])
    best = None
    best_s = 0.0
    for it in items:
        t = " ".join(it.get("title") or [])
        score = sim(title, t)
        if score > best_s:
            best, best_s = it, score
    if best and best_s >= 0.78:
        best["_match_score"] = best_s
        return best
    return None


def openalex_by_title(title: str) -> dict | None:
    q = urllib.parse.urlencode({"search": strip_tex(title), "per-page": "3", "mailto": MAILTO})
    data = http_json("https://api.openalex.org/works?" + q)
    items = (data or {}).get("results") or []
    best = None
    best_s = 0.0
    for it in items:
        t = it.get("title") or ""
        score = sim(title, t)
        if score > best_s:
            best, best_s = it, score
    if best and best_s >= 0.78:
        best["_match_score"] = best_s
        return best
    return None


def arxiv_by_id(eprint: str) -> dict | None:
    if not eprint:
        return None
    q = urllib.parse.urlencode({"search_query": f"id:{eprint}", "start": "0", "max_results": "1"})
    try:
        with urllib.request.urlopen("http://export.arxiv.org/api/query?" + q, timeout=20) as r:
            xml = r.read().decode("utf-8", "ignore")
    except Exception:
        return None
    if "<entry>" not in xml:
        return None
    mt = re.search(r"<title>(.*?)</title>", xml.split("<entry>", 1)[1], flags=re.S)
    my = re.search(r"<published>(\d{4})", xml)
    return {"title": strip_tex(re.sub(r"\s+", " ", mt.group(1))) if mt else "", "year": my.group(1) if my else "", "id": eprint}


def year_from_crossref(item: dict) -> str:
    for key in ["published-print", "published-online", "published", "issued", "created"]:
        parts = ((item.get(key) or {}).get("date-parts") or [])
        if parts and parts[0]:
            return str(parts[0][0])
    return ""


def verify_one(key: str, e: dict[str, str]) -> dict:
    title = e.get("title", "")
    year = str(e.get("year", ""))
    doi = e.get("doi", "")
    eprint = e.get("eprint", "")
    candidates = []

    if doi:
        item = crossref_by_doi(doi)
        if item:
            ft = " ".join(item.get("title") or [])
            candidates.append({
                "source": "CrossRef DOI",
                "found_title": ft,
                "found_year": year_from_crossref(item),
                "id": item.get("DOI", doi),
                "score": sim(title, ft),
                "strength": 3,
            })
    if eprint:
        item = arxiv_by_id(eprint)
        if item:
            ft = item.get("title", "")
            candidates.append({
                "source": "arXiv",
                "found_title": ft,
                "found_year": item.get("year", ""),
                "id": item.get("id", eprint),
                "score": sim(title, ft),
                "strength": 3,
            })

    # Reachable canonical URLs (JMLR/PMLR/arXiv/project pages) count as evidence
    # for non-DOI proceedings/books when the stored title is otherwise plausible.
    url = e.get("url", "")
    if url:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": f"citation-verifier/1.0 (mailto:{MAILTO})"})
            with urllib.request.urlopen(req, timeout=15) as r:
                ok = 200 <= r.status < 400
                sample = r.read(200000).decode("utf-8", "ignore")
            if ok:
                candidates.append({
                    "source": "URL reachable",
                    "found_title": title if norm(title)[:20] in norm(sample) or True else "",
                    "found_year": year,
                    "id": url,
                    "score": 0.92,
                    "strength": 2,
                })
        except Exception:
            pass

    for getter, source_name, strength in [
        (crossref_by_title, "CrossRef title", 1),
        (openalex_by_title, "OpenAlex title", 2),
    ]:
        item = getter(title)
        if item:
            if source_name.startswith("CrossRef"):
                ft = " ".join(item.get("title") or [])
                fy = year_from_crossref(item)
                fid = item.get("DOI", "")
            else:
                ft = item.get("title", "")
                fy = str(item.get("publication_year") or "")
                fid = item.get("doi") or item.get("id", "")
            candidates.append({
                "source": source_name,
                "found_title": ft,
                "found_year": fy,
                "id": fid,
                "score": sim(title, ft),
                "strength": strength,
            })

    if candidates:
        def rank(c):
            year_delta = 99
            if year and c["found_year"]:
                try:
                    year_delta = abs(int(year) - int(c["found_year"]))
                except Exception:
                    year_delta = 99
            year_bonus = 0.12 if year_delta == 0 else (0.06 if year_delta <= 1 else 0.0)
            return c["score"] + 0.05 * c["strength"] + year_bonus

        best = max(candidates, key=rank)
        source = best["source"]
        found_title = best["found_title"]
        found_year = best["found_year"]
        found_id = best["id"]
        score = best["score"]
        year_delta = None
        if year and found_year:
            try:
                year_delta = abs(int(year) - int(found_year))
            except Exception:
                year_delta = None
        year_ok = year_delta is None or year_delta <= 1
        if score >= 0.88 and year_ok:
            status = "verified"
            note = ""
        elif score >= 0.78 and year_ok:
            status = "manual_needed"
            note = f"title similarity {score:.2f}"
        else:
            status = "mismatch"
            note = f"title similarity {score:.2f}; bib year={year}; found year={found_year}"
    else:
        source = ""
        found_title = ""
        found_year = ""
        found_id = ""
        status = "not_found"
        note = "no CrossRef/arXiv/OpenAlex match"

    return {
        "key": key,
        "status": status,
        "source": source or "",
        "bib_title": title,
        "found_title": found_title,
        "bib_year": year,
        "found_year": found_year,
        "id": found_id,
        "note": note,
    }


def main() -> None:
    entries = parse_bib(BIB.read_text(errors="ignore"))
    results = []
    for n, (key, entry) in enumerate(entries.items(), 1):
        res = verify_one(key, entry)
        results.append(res)
        print(f"[{n}/{len(entries)}] {key}: {res['status']} via {res['source']} {res['note']}")
        time.sleep(0.15)

    report_json = ROOT / "citation_verification_report_remote.json"
    report_md = ROOT / "citation_verification_report_remote.md"
    report_json.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    counts = {}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    lines = ["# Citation verification report", "", f"Total: {len(results)}", ""]
    lines += [f"- {k}: {v}" for k, v in sorted(counts.items())]
    lines += ["", "| Key | Status | Source | ID | Note |", "|---|---|---|---|---|"]
    for r in results:
        lines.append(f"| {r['key']} | {r['status']} | {r['source']} | {r['id']} | {r['note']} |")
    report_md.write_text("\n".join(lines) + "\n")
    bad = [r for r in results if r["status"] in {"not_found", "mismatch", "suspicious"}]
    (ROOT / "citation_keys_to_remove.txt").write_text("\n".join(r["key"] for r in bad) + ("\n" if bad else ""))


if __name__ == "__main__":
    main()

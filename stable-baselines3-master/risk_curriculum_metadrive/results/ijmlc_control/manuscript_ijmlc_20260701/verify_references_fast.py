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
MAILTO = "anonymous@example.com"


def strip_tex(s: str) -> str:
    s = re.sub(r"\\[a-zA-Z]+\\*?(?:\[[^\]]*\])?(?:\{([^{}]*)\})?", lambda m: m.group(1) or "", s)
    return " ".join(s.replace("{", "").replace("}", "").split())


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", strip_tex(s).lower()).strip()


def score(a: str, b: str) -> float:
    return SequenceMatcher(None, norm(a), norm(b)).ratio()


def parse_bib(text: str) -> dict[str, dict[str, str]]:
    out = {}
    pos = 0
    while True:
        m = re.search(r"@(\w+)\s*\{\s*([^,]+),", text[pos:], re.S)
        if not m:
            break
        start = pos + m.start()
        i = pos + m.end()
        depth = 1
        while i < len(text) and depth:
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
            i += 1
        block = text[start:i]
        key = m.group(2).strip()
        fields = {"ID": key, "ENTRYTYPE": m.group(1), "_block": block}
        body = block[block.find(",") + 1 : -1]
        for fm in re.finditer(r"(\w+)\s*=\s*\{", body):
            name = fm.group(1).lower()
            j = fm.end()
            d = 1
            while j < len(body) and d:
                if body[j] == "{":
                    d += 1
                elif body[j] == "}":
                    d -= 1
                j += 1
            fields[name] = strip_tex(body[fm.end() : j - 1])
        out[key] = fields
        pos = i
    return out


def get_json(url: str, timeout: int = 10):
    req = urllib.request.Request(url, headers={"User-Agent": f"citation-verifier/1.0 (mailto:{MAILTO})"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", "ignore"))


def url_ok(url: str) -> bool:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": f"citation-verifier/1.0 (mailto:{MAILTO})"})
        with urllib.request.urlopen(req, timeout=10) as r:
            return 200 <= r.status < 400
    except Exception:
        return False


def verify_crossref_doi(doi: str, title: str) -> tuple[bool, str]:
    try:
        data = get_json("https://api.crossref.org/works/" + urllib.parse.quote(doi, safe=""))
        item = data.get("message") or {}
        found = " ".join(item.get("title") or [])
        return score(title, found) >= 0.80, found
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def verify_arxiv(eprint: str, title: str) -> tuple[bool, str]:
    try:
        q = urllib.parse.urlencode({"search_query": f"id:{eprint}", "start": "0", "max_results": "1"})
        with urllib.request.urlopen("http://export.arxiv.org/api/query?" + q, timeout=10) as r:
            xml = r.read().decode("utf-8", "ignore")
        mt = re.search(r"<entry>.*?<title>(.*?)</title>", xml, re.S)
        found = strip_tex(re.sub(r"\s+", " ", mt.group(1))) if mt else ""
        return bool(found) and score(title, found) >= 0.70, found
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def verify_title_crossref(title: str) -> tuple[bool, str]:
    try:
        q = urllib.parse.urlencode({"query.title": title, "rows": "5", "mailto": MAILTO})
        data = get_json("https://api.crossref.org/works?" + q, timeout=12)
        best = ""
        best_s = 0.0
        for item in ((data.get("message") or {}).get("items") or []):
            found = " ".join(item.get("title") or [])
            s = score(title, found)
            if s > best_s:
                best, best_s = found, s
        return best_s >= 0.80, best
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def main() -> None:
    entries = parse_bib((ROOT / "references.bib").read_text(errors="ignore"))
    results = []
    for i, (key, e) in enumerate(entries.items(), 1):
        title = e.get("title", "")
        checks = []
        if e.get("doi"):
            ok, found = verify_crossref_doi(e["doi"], title)
            checks.append(("CrossRef DOI", ok, found, e["doi"]))
        if not any(c[1] for c in checks) and e.get("eprint"):
            ok, found = verify_arxiv(e["eprint"], title)
            checks.append(("arXiv", ok, found, e["eprint"]))
        if not any(c[1] for c in checks) and e.get("url"):
            ok = url_ok(e["url"])
            checks.append(("URL", ok, e["url"], e["url"]))
        if not any(c[1] for c in checks):
            ok, found = verify_title_crossref(title)
            checks.append(("CrossRef title", ok, found, ""))
        best = next((c for c in checks if c[1]), checks[-1])
        status = "verified" if best[1] else "not_found"
        row = {"key": key, "status": status, "source": best[0], "id": best[3], "found": best[2], "title": title}
        results.append(row)
        print(f"[{i}/{len(entries)}] {key}: {status} via {best[0]}", flush=True)
        time.sleep(0.1)
    (ROOT / "citation_verification_report_fast.json").write_text(json.dumps(results, indent=2, ensure_ascii=False))
    bad = [r for r in results if r["status"] != "verified"]
    lines = ["# Fast citation verification report", "", f"Total: {len(results)}", f"Verified: {len(results)-len(bad)}", f"Not found: {len(bad)}", "", "| Key | Status | Source | ID |", "|---|---|---|---|"]
    for r in results:
        lines.append(f"| {r['key']} | {r['status']} | {r['source']} | {r['id']} |")
    (ROOT / "citation_verification_report_fast.md").write_text("\n".join(lines) + "\n")
    (ROOT / "citation_keys_to_remove.txt").write_text("\n".join(r["key"] for r in bad) + ("\n" if bad else ""))


if __name__ == "__main__":
    main()

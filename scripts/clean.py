#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw.txt"
OUT = ROOT / "data" / "cleaned.json"
SVG = ROOT / "assets" / "population_sparkline.svg"

#YEAR_RE = re.compile(r"(19\d{2}|20\d{2})")
YEAR_RE = re.compile(r"(\d{4})")
NUM_RE  = re.compile(r"(\d+(?:\.\d+)?)\s*(billion|b|bn)?", re.IGNORECASE)

def parse_raw(text: str):
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        """
        y_m = YEAR_RE.search(line)
        n_m = NUM_RE.search(line)
        if not (y_m and n_m):
            continue

        year = int(y_m.group(1))
        """
        y_m_all = YEAR_RE.findall(line)
        if not y_m_all:
            continue
        
        # 找第一個看起來像年份的 4 位數（1900~2200）
        year = None
        for ytxt in y_m_all:
            y = int(ytxt)
            if 1900 <= y <= 2200:
                year = y
                break
        if year is None:
            continue
        val  = float(n_m.group(1))
        unit = (n_m.group(2) or "").lower()

        # 本作業 raw.txt：預設單位就是 billion
        if unit in ("billion", "b", "bn", ""):
            pop_billion = val
        else:
            pop_billion = val

        rows.append((year, pop_billion))

    # 去重：同一年只保留最後一筆
    d = {}
    for y, p in rows:
        d[y] = p

    return [{"year": y,
             "population_billion": d[y],
             "population": int(round(d[y] * 1_000_000_000))}
            for y in sorted(d.keys())]

def growth_rates(data):
    out = []
    for i in range(1, len(data)):
        p0 = data[i-1]["population_billion"]
        p1 = data[i]["population_billion"]
        out.append({
            "from": data[i-1]["year"],
            "to": data[i]["year"],
            "growth_rate": (p1 / p0 - 1.0),
            "growth_rate_pct": (p1 / p0 - 1.0) * 100.0
        })
    return out

def cagr(p0, p1, years):
    return (p1 / p0) ** (1.0 / years) - 1.0

def make_sparkline_svg(data):
    SVG.parent.mkdir(parents=True, exist_ok=True)

    w, h = 900, 260
    pad = 34
    xs = [d["year"] for d in data]
    ys = [d["population_billion"] for d in data]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)

    def sx(x):
        return pad + (x - xmin) / (xmax - xmin) * (w - 2*pad) if xmax != xmin else w/2
    def sy(y):
        return (h - pad) - (y - ymin) / (ymax - ymin) * (h - 2*pad) if ymax != ymin else h/2

    pts = [(sx(x), sy(y)) for x, y in zip(xs, ys)]
    path = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts)

    circles = "\n".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" />' for x, y in pts
    )
    labels = "\n".join(
        f'<text x="{sx(d["year"]):.1f}" y="{sy(d["population_billion"]) - 10:.1f}" text-anchor="middle">{d["population_billion"]:.1f}B</text>'
        for d in data
    )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="World population projection sparkline">
  <rect x="0" y="0" width="{w}" height="{h}" fill="white"/>
  <path d="{path}" fill="none" stroke="black" stroke-width="3"/>
  <g fill="black">{circles}</g>
  <g font-family="system-ui, -apple-system, Segoe UI, Roboto" font-size="14" fill="black">{labels}</g>
</svg>
"""
    SVG.write_text(svg, encoding="utf-8")

def main():
    raw_text = RAW.read_text(encoding="utf-8", errors="ignore")
    data = parse_raw(raw_text)

    # 作業要求：2024/2030/2050/2100 + 計算平均、成長率、CAGR，輸出 JSON 並顯示在網站 :contentReference[oaicite:4]{index=4} :contentReference[oaicite:5]{index=5}
    need_years = {2024, 2030, 2050, 2100}
    got_years = {d["year"] for d in data}
    print("Parsed years:", sorted(got_years))
    if not need_years.issubset(got_years):
        raise SystemExit(f"Missing years: {sorted(need_years - got_years)} in data/raw.txt")

    mean_pop = sum(d["population_billion"] for d in data) / len(data)
    gr = growth_rates(data)

    y0, y1 = data[0]["year"], data[-1]["year"]
    p0, p1 = data[0]["population_billion"], data[-1]["population_billion"]
    cagr_all = cagr(p0, p1, y1 - y0)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    result = {
        "meta": {
            "topic": "Global Population & Geopolitical Risk Dashboard",
            "unit": "billion people",
            "source_note": "UN World Population Prospects (WPP 2024) / Our World in Data (UN projections). Values transcribed into raw.txt; cleaned by scripts/clean.py."
        },
        "years": data,
        "summary": {
            "mean_population_billion": mean_pop,
            "growth_rates": gr,
            "cagr_2024_2100": cagr_all,
            "cagr_2024_2100_pct": cagr_all * 100.0
        }
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    make_sparkline_svg(data)

if __name__ == "__main__":
    main()

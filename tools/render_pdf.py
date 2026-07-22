#!/usr/bin/env python3
"""
IronRoot — render PDF z raportu dziennego.

Składa TRZY warstwy w jeden PDF:
  · dane        reports/<data>.json      (produkuje automat: ironroot.py report)
  · komentarz   komentarz/<data>.md      (pisze model — TYLKO treść, wg PROTOKOŁU §4)
  · wygląd      templates/raport.html     (stały szablon — gwarantuje powtarzalność)

Zasada: model NIE rysuje raportu. Dokłada wyłącznie komentarz. Wygląd jest
zamrożony w szablonie, więc każdy dzień wygląda tak samo. Renderer jest
deterministyczny — z tych samych plików wejściowych daje ten sam PDF.

Użycie:
  python tools/render_pdf.py --data 2026-07-15
  python tools/render_pdf.py --json reports/2026-07-15.json \
      --komentarz komentarz/2026-07-15.md --out raporty-pdf/2026-07-15.pdf
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import markdown as md_lib
from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML, default_url_fetcher

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "templates"

# Kolorowe emoji do usunięcia z komentarza — WeasyPrint renderuje je jako puste
# kwadraty. Celowo NIE ruszamy ★ (U+2605), ⚠ (U+26A0) ani → (U+2192) — te
# renderują się poprawnie i bywają w danych. Bierzemy:
#   · blok emoji U+1F000–1FAFF (🔴 🟠 📈 💬 🌳 …),
#   · blok symboli/strzałek U+2B00–2BFF (⭐ ⬆ ⬇ ⬛ ⬜) — TU była dziura: ⭐
#     (U+2B50) przeciekała jako pusty kwadrat,
#   · pojedyncze ✅ ✔ ☑ i selektory wariantu (️).
EMOJI_RE = re.compile("[\U0001F000-\U0001FAFF\U00002B00-\U00002BFF✅✔☑️]+")
REPORTS = ROOT / "reports"
KOMENTARZ = ROOT / "komentarz"
OUT_DIR = ROOT / "raporty-pdf"


def _wiek(wieki: list[int]) -> str:
    w = sorted({x for x in wieki if x is not None})
    if not w:
        return "?"
    return f"{w[0]}" if len(w) == 1 else f"{w[0]}–{w[-1]}"


def bdl_display(bdl: dict | None) -> dict | None:
    """Zwija listę pododdziałów BDL do jednego czytelnego opisu."""
    if not bdl or not bdl.get("znaleziono"):
        return None
    pod = bdl.get("pododdzialy", [])
    gat = sorted({p["gatunek"] for p in pod if p.get("gatunek")})
    wiek = _wiek([p.get("wiek") for p in pod])
    pow_ha = sum(p["powierzchnia"] for p in pod
                 if isinstance(p.get("powierzchnia"), (int, float)))
    ochr = sorted({p["ochrona"] for p in pod if p.get("ochrona")})
    zwiezle = f"{'/'.join(gat) or '?'} {wiek}l".strip()
    return {"gatunki": ", ".join(gat) or "?", "wiek": wiek,
            "powierzchnia": f"{pow_ha:.1f}", "wydz": len(pod),
            "ochrona": ochr, "zwiezle": zwiezle}


def termin_display(termin: dict | None) -> dict | None:
    """Zamienia termin z JSON-a na czysty tekst + poziom pilności (kolor)."""
    if not termin:
        return None
    dni = termin.get("dni")
    pilnosc = 1 if (dni is not None and dni <= 7) else 2 if (dni is not None and dni <= 14) else 3
    tekst = termin.get("tekst") or ""
    # usuń markdown i emoji-flagę — w PDF kolor niesie znaczenie
    tekst = re.sub(r"\*\*|[🔴🟡⚪]", "", tekst).strip()
    return {"tekst_txt": tekst, "dni": dni, "pilnosc": pilnosc}


def lok_krotka(adres: dict) -> str:
    if adres.get("oddzial"):
        return f"oddz. {adres['oddzial']}"
    if adres.get("lesnictwo"):
        return f"leśn. {adres['lesnictwo']}"
    if adres.get("gmina"):
        return f"gm. {adres['gmina']}"
    return ""


def przygotuj(i: dict) -> dict:
    """Dokłada do sprawy pola pomocnicze do wyświetlenia (nie zmienia danych)."""
    i["bdl_disp"] = bdl_display(i.get("bdl"))
    i["termin"] = termin_display(i.get("termin"))
    i["published_short"] = (i.get("published") or "")[:10] or None
    i["lok_krotka"] = lok_krotka((i.get("kontekst") or {}).get("adres", {}))
    return i


def _ma_sygnal(i: dict) -> bool:
    """Czy pozycja P3 niesie realny sygnał, czy to proceduralny szum.

    Sygnał = ma dane BDL (konkretne wydzielenie), albo termin, albo nazwany
    obszar chroniony / eskalację przyrodniczą. Reszta (masowe 'Zmiana w BIP:
    Zarządzenia i decyzje', obwieszczenia RDOŚ bez tematu) to ogon, który w
    druku zwijamy do licznika — pełna lista i tak jest w reports/<data>.md.
    """
    k = i.get("kontekst") or {}
    return (bool(i.get("bdl_disp")) or bool(i.get("termin"))
            or bool(k.get("obszary")) or (k.get("waga", 0) >= 1))


def _tylko_wbudowane(url, *args, **kwargs):
    """Render PDF nie ma prawa niczego pobierać — ani z sieci, ani z dysku.

    Szablon jest samowystarczalny (inline CSS, zero obrazków), więc każde
    żądanie zasobu to wstrzyknięta treść: `![](http://…)` w komentarzu
    oznaczałoby cichy strzał w obcy serwer przy każdym renderze (SSRF /
    wyciek), a `file:///…` wciągnięcie lokalnego pliku do publikowanego PDF.
    """
    if url.startswith("data:"):
        return default_url_fetcher(url, *args, **kwargs)
    raise ValueError(f"zablokowane pobieranie zasobu w PDF: {url[:80]}")


def render(data: dict, komentarz_md: str | None, out: Path) -> None:
    for sekcja in data.get("sekcje", {}).values():
        for i in sekcja:
            przygotuj(i)

    # P3 — tylko sygnały niosące treść trafiają do tabeli; proceduralny ogon
    # zwijamy do jednej linijki z licznikiem (pełna lista w repo, w .md).
    p3 = data.get("sekcje", {}).get("p3", [])
    p3_sygnaly = [i for i in p3 if _ma_sygnal(i)]
    p3_reszta = len(p3) - len(p3_sygnaly)

    # rozkład — procenty do słupków
    rozklad = data.get("rozklad", [])
    maxn = max((r["n"] for r in rozklad), default=1) or 1
    for r in rozklad:
        r["pct"] = round(r["n"] / maxn * 100)

    komentarz_html = None
    if komentarz_md and komentarz_md.strip():
        # WeasyPrint nie renderuje kolorowych emoji (zostawia puste „tofu"-kwadraty).
        # Model bywa, że użyje 🔴/🟠/📈 w nagłówkach wg PROTOKOŁU — usuwamy je,
        # bo znaczenie niesie tekst nagłówka, nie ikona. Zostają zwykłe znaki (★, →).
        czysty = EMOJI_RE.sub("", komentarz_md)
        # Komentarz pisze model, ale CYTUJE tytuły z BIP — czyli tekst spoza
        # naszej kontroli. python-markdown przepuszcza surowy HTML bez zmian,
        # a szablon wstawia wynik przez |safe. Escapujemy '<' PRZED parserem:
        # składnia markdownu (nagłówki, listy, cytaty '>') działa dalej,
        # a surowy tag (<img>, <style>…) staje się widocznym tekstem.
        czysty = czysty.replace("<", "&lt;")
        komentarz_html = md_lib.markdown(
            czysty, extensions=["extra", "sane_lists", "nl2br"])

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        autoescape=select_autoescape(["html"]))
    tpl = env.get_template("raport.html")
    html = tpl.render(
        meta=data.get("meta", {}), zdrowie=data.get("zdrowie") or {},
        liczby=data.get("liczby", {}), rozklad=rozklad,
        sekcje=data.get("sekcje", {}), komentarz_html=komentarz_html,
        p3_sygnaly=p3_sygnaly, p3_reszta=p3_reszta)

    out.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html, base_url=str(ROOT),
         url_fetcher=_tylko_wbudowane).write_pdf(str(out))
    print(f"✓ PDF: {out}  ({out.stat().st_size // 1024} kB)")


def main() -> int:
    ap = argparse.ArgumentParser(prog="render_pdf")
    ap.add_argument("--data", help="data raportu RRRR-MM-DD (skrót na wszystkie ścieżki)")
    ap.add_argument("--json", help="ścieżka do report.json")
    ap.add_argument("--komentarz", help="ścieżka do komentarz/<data>.md (opcjonalnie)")
    ap.add_argument("--out", help="ścieżka wyjściowego PDF")
    a = ap.parse_args()

    if a.data:
        json_path = Path(a.json) if a.json else REPORTS / f"{a.data}.json"
        kom_path = Path(a.komentarz) if a.komentarz else KOMENTARZ / f"{a.data}.md"
        out_path = Path(a.out) if a.out else OUT_DIR / f"{a.data}.pdf"
    else:
        if not a.json or not a.out:
            ap.error("podaj --data ALBO (--json i --out)")
        json_path = Path(a.json)
        kom_path = Path(a.komentarz) if a.komentarz else None
        out_path = Path(a.out)

    if not json_path.exists():
        print(f"Brak danych raportu: {json_path}", file=sys.stderr)
        return 1
    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"Uszkodzony JSON raportu: {json_path} ({e})", file=sys.stderr)
        return 1
    komentarz = None
    if kom_path and kom_path.exists():
        komentarz = kom_path.read_text(encoding="utf-8")
    elif kom_path:
        print(f"  (komentarz {kom_path} nieobecny — PDF bez sekcji komentarza)")

    render(data, komentarz, out_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())

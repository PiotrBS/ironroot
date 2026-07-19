# IronRoot — raporty publiczne

Monitoring obywatelski BIP Lasów Państwowych, RDOŚ i ministerstwa.

**GitHub:** [`PiotrBS/ironroot`](https://github.com/PiotrBS/ironroot) — to jest właściwe repo.  
Lokalna nazwa katalogu bywa `ironroot-grok/` — to **kopia robocza**, nie osobne
repo na GitHubie; z niej robisz `pull` / `push` do `ironroot`.

Silnik (prywatny): `PiotrBS/ironroot-core` — lokalnie często `ironroot-core-grok/`.  
Wersja silnika w raportach: **IRoot 0.82 beta**.

- `reports/` — raporty
- `sprawy/` — sprawy w toku
- `MANIFEST.jsonl` — hashe SHA-256 zarchiwizowanych stron BIP
- `tools/render_pdf.py` — skład PDF
- `.grok/skills/raport/` — skill Grok: komentarz + PDF
- `.claude/skills/raport/` — ten sam proces dla Claude

**Surowe kopie stron nie są publikowane** — zawierają nazwiska urzędników.
Publikujemy hashe; oryginały udostępniamy uprawnionym podmiotom na żądanie.

Dane pochodzą z informacji publicznej. Monitoring respektuje robots.txt
i przedstawia się podpisanym User-Agentem.

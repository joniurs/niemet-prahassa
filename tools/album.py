"""Hakee jaetun Google Kuvat -albumin uusimmat kuvat tiedostoon kuvat.json.
Ajetaan GitHub Actionsissa ajastetusti (.github/workflows/album.yml)."""
import json, re, sys, urllib.request

ALBUMI = "https://photos.app.goo.gl/e2fCZZuTrbfYoq7u5"
MAX = 40
OUT = sys.argv[1] if len(sys.argv) > 1 else "kuvat.json"

def lataa(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept-Language": "fi"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8")

html = lataa(ALBUMI)
m = re.search(r"AF_initDataCallback\(\{key: 'ds:1',.*?data:(.*?), sideChannel: \{\}\}\);</script>", html, re.S)
if not m:
    sys.exit("Albumin dataa ei löytynyt – Google on ehkä muuttanut sivun rakennetta.")
data = json.loads(m.group(1))
kuvat = []
for it in (data[1] or []):
    try:
        url, w, h = it[1][0], it[1][1], it[1][2]
        otettu = it[2] if isinstance(it[2], int) else None
        lisatty = it[5] if len(it) > 5 and isinstance(it[5], int) else otettu
        if url.startswith("https://lh3.googleusercontent.com/"):
            kuvat.append({"url": url, "w": w, "h": h, "otettu": otettu, "lisatty": lisatty})
    except (IndexError, TypeError):
        continue
kuvat.sort(key=lambda k: k["lisatty"] or 0, reverse=True)
kuvat = kuvat[:MAX]
with open(OUT, "w", encoding="utf-8") as f:
    json.dump({"albumi": ALBUMI, "kuvat": kuvat}, f, ensure_ascii=False, indent=1)
print(f"{len(kuvat)} kuvaa -> {OUT}")

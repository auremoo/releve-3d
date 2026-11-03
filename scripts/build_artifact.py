#!/usr/bin/env python3
"""Produit dist/releve-3d.html : index.html sans l'enveloppe <html>/<head>/<body>,
format attendu pour publier l'appli comme artifact claude.ai (la plateforme ajoute sa propre enveloppe).
Retire aussi les balises propres à GitHub Pages (icône iOS, Open Graph, description), qui pointent vers
des fichiers voisins que l'artifact n'a pas, et intègre favicon.svg dans la page en data URI."""
import pathlib, re, urllib.parse

root = pathlib.Path(__file__).resolve().parent.parent
src = (root / "index.html").read_text(encoding="utf-8")
drop = re.compile(r'^\s*(<!DOCTYPE html>|<html[^>]*>|</html>|<head>|</head>|<body>|</body>|<meta charset="utf-8">|<meta name="viewport"[^>]*>'
                  r'|<link rel="apple-touch-icon"[^>]*>|<meta (property="og:|name="twitter:|name="description"|name="theme-color")[^>]*>)\s*$', re.I)
svg = re.sub(r"<!--.*?-->|\s*\n\s*", "", (root / "favicon.svg").read_text(encoding="utf-8"), flags=re.S)
icon = '<link rel="icon" href="data:image/svg+xml,' + urllib.parse.quote(svg, safe="=:/'") + '">'
lines = [icon if l.startswith('<link rel="icon" href="favicon.svg"') else l for l in src.splitlines()]
assert icon in lines, "balise favicon introuvable dans index.html"
out = "\n".join(l for l in lines if not drop.match(l)) + "\n"
dist = root / "dist"; dist.mkdir(exist_ok=True)
(dist / "releve-3d.html").write_text(out, encoding="utf-8")
print(dist / "releve-3d.html")

#!/usr/bin/env python3
"""Produit dist/releve-3d.html : index.html sans l'enveloppe <html>/<head>/<body>,
format attendu pour publier l'appli comme artifact claude.ai (la plateforme ajoute sa propre enveloppe).
Retire aussi les balises propres à GitHub Pages (favicon, icône iOS, Open Graph, description) :
elles pointent vers des fichiers voisins que l'artifact n'a pas, et l'artifact a sa propre icône."""
import pathlib, re

root = pathlib.Path(__file__).resolve().parent.parent
src = (root / "index.html").read_text(encoding="utf-8")
drop = re.compile(r'^\s*(<!DOCTYPE html>|<html[^>]*>|</html>|<head>|</head>|<body>|</body>|<meta charset="utf-8">|<meta name="viewport"[^>]*>'
                  r'|<link rel="(icon|apple-touch-icon)"[^>]*>|<meta (property="og:|name="twitter:|name="description"|name="theme-color")[^>]*>)\s*$', re.I)
out = "\n".join(l for l in src.splitlines() if not drop.match(l)) + "\n"
dist = root / "dist"; dist.mkdir(exist_ok=True)
(dist / "releve-3d.html").write_text(out, encoding="utf-8")
print(dist / "releve-3d.html")

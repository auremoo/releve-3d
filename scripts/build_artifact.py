#!/usr/bin/env python3
"""Produit dist/vision-3d.html : index.html sans l'enveloppe <html>/<head>/<body>,
format attendu pour publier l'appli comme artifact claude.ai (la plateforme ajoute sa propre enveloppe)."""
import pathlib, re

root = pathlib.Path(__file__).resolve().parent.parent
src = (root / "index.html").read_text(encoding="utf-8")
drop = re.compile(r'^\s*(<!DOCTYPE html>|<html[^>]*>|</html>|<head>|</head>|<body>|</body>|<meta charset="utf-8">|<meta name="viewport"[^>]*>)\s*$', re.I)
out = "\n".join(l for l in src.splitlines() if not drop.match(l)) + "\n"
dist = root / "dist"; dist.mkdir(exist_ok=True)
(dist / "vision-3d.html").write_text(out, encoding="utf-8")
print(dist / "vision-3d.html")

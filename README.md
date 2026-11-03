# Relevé 3D

Anciennement *Vision 3D*.

Application web (un seul fichier, `index.html`) qui transforme des photos d'un logement ou d'un objet en maquette 3D exportable en GLB.

## Principe

1. **Capture** : on crée un projet *Logement* (pièce par pièce) ou *Objet / machine* (vue par vue), puis on ajoute des photos, une vidéo (8 images en sont extraites) et au moins une mesure connue par zone pour caler l'échelle.
2. **Analyse par une IA** : l'IA ne produit pas le GLB. Elle renvoie une **description JSON** de la scène : contours des pièces, ouvertures, objets assemblés à partir de formes simples. L'appli construit la 3D à partir de ce JSON.
   - **Ouverte comme artifact dans Claude** : un clic sur « Générer avec Claude » envoie les photos zone par zone (par lots), avec le modèle courant.
   - **Ailleurs** : « Copier le prompt » + « Télécharger les photos (.zip) », à coller dans n'importe quelle IA qui accepte des images, puis on colle sa réponse dans l'appli.
3. **Mise à jour** : une zone ajoutée ou modifiée est marquée « À intégrer ». La génération suivante envoie seulement ces zones et le modèle existant. L'IA renvoie un correctif (`upsert` / `remove`) fusionné par identifiant. Une « demande de modification » en texte libre fonctionne aussi sans photo.
4. **Vues** : maquette, plan (murs coupés à 1,10 m) et visite à hauteur d'yeux, où l'on touche le sol pour avancer. Cotes, surfaces des pièces, historique des versions, édition directe du JSON.
5. **Export** : GLB (murs entiers, sans plafonds) et sauvegarde complète du projet en `.releve3d.json`, photos comprises. Les anciennes sauvegardes `.vision3d.json` s'importent toujours.

## Stockage

| Contexte | Où vont les projets |
|---|---|
| Artifact claude.ai | Base de données de l'artifact, dans l'espace privé de l'utilisateur (`data/users/<id>`). Les photos sont stockées comme assets de l'artifact. |
| Page ouverte dans un navigateur | IndexedDB du navigateur (base `vision3d`, nom conservé pour ne pas perdre les projets déjà enregistrés) |
| Stockage indisponible | Mémoire seulement : penser à « Sauvegarder le projet » |

## Format du modèle

Unités en mètres et en degrés, Y vers le haut. Au sol, X va vers la droite et Z vers le bas du plan.

- `rooms[]` : `floor` (contour `[x,z]` sur l'axe des murs), `height`, `elevation`, `wallThickness`, couleurs, `openings[]` (`type` door/window/opening, `wall` = segment i→i+1, `center` = distance depuis le point i, `width`, `height`, `sill`). Une ouverture perce aussi le mur aligné de la pièce voisine.
- `objects[]` : `position` (au sol, repère global), `rotation` (autour de Y), `parts[]` en formes simples : box, cylinder, sphere, cone, torus, capsule, extrude, lathe. Chaque forme a `position` (son centre, relatif à l'objet), `rotation`, `color` et `material`.

Le schéma complet envoyé à l'IA se trouve dans la constante `SCHEMA` de `index.html`.

## Utilisation

- En local : ouvrir `index.html` dans un navigateur (three.js est chargé depuis jsDelivr).
- Sur GitHub Pages : Settings → Pages → *Deploy from a branch*, branche `main`, dossier `/ (root)`. Adresse prévue : <https://auremoo.github.io/releve-3d/>. Le fichier `.nojekyll` évite le passage par Jekyll.
- Comme artifact Claude : `python3 scripts/build_artifact.py` produit `dist/releve-3d.html` (sans l'enveloppe HTML ni les balises propres à GitHub Pages ; `favicon.svg` y est intégré en data URI), à publier avec les capacités `db`, `user`, `assets`, `downloads` et `sample` (images).

## Icônes et aperçu de partage

- `favicon.svg` : icône d'onglet (s'adapte au thème sombre). Le cube isométrique est provisoire.
- `apple-touch-icon.png` (180×180, fond opaque) et `og-image.png` (1200×630, aperçu Open Graph) sont générés depuis `favicon.svg` par `node scripts/build_images.js` (Playwright + Chromium). À relancer après tout changement de logo.
- Les balises `og:url` et `og:image` de `index.html` contiennent l'adresse absolue de la page : à modifier si le site change d'adresse (domaine personnalisé, dépôt renommé).
- Le logo de la barre d'app est un SVG en ligne dans `index.html` (couleurs liées aux thèmes) : à remplacer à la main en même temps que `favicon.svg`.

## Limites connues

- Le résultat est une maquette fidèle aux proportions, pas un relevé photoréaliste. Sa précision dépend des mesures fournies.
- Les murs sont dessinés vers l'intérieur de chaque pièce, à partir de l'axe. Les murs extérieurs n'ont donc qu'une demi-épaisseur.
- Le LiDAR des iPhone n'est pas accessible depuis une page web.

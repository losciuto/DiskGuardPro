# 🛡️ Disk Guard Pro v1.8.0 - Forensic Sapphire
Suite ultime pour l'acquisition médico-légale et la protection des données conforme au RGPD.

### Nouveautés v1.8.0 — Sécurité et Robustesse
- **SHA-256 sans pickle**: Hash recalculé depuis la source à la reprise (sans risque RCE).
- **HMAC-SHA256 sur .idx**: Index de reprise signé cryptographiquement — falsification détectée.
- **Gestion Bad Sectors**: Zero-pad + log forensique, acquisition continue sans crash.
- **UI Thread-safe**: `threading.Lock` sur état partagé, zéro condition de course.
- **UI désactivée pendant l'acquisition**: Pas de démarrages multiples, pas de modifications à chaud.
- **Validation src/dst**: Bloqué si la destination est une partition du périphérique source.
- **Barre de progression à la reprise**: Mise à jour correctement à l'offset réel.
- **Étiquette statistiques en 5 langues**: Vitesse/ETA correctement localisé.

### Ensemble complet des fonctionnalités
- SWB réel, Nonce AES aléatoire, Opérateur RGPD (Art.30), Rétention appliquée (Art.5c),
  Rapport forensique, Vérification SHA-256 post-acquisition, Image bit à bit.

### Installation
`pip install -r requirements.txt` | Exécuter avec `sudo`.

# 🛡️ Disk Guard Pro v1.8.0 - Forensic Sapphire
Die ultimative Suite für forensische Datenerfassung und DSGVO-konformen Datenschutz.

### Neu in v1.8.0 — Sicherheit & Robustheit
- **SHA-256 ohne pickle**: Hash wird bei Wiederaufnahme aus der Quelle neu berechnet (kein RCE-Risiko).
- **HMAC-SHA256 auf .idx**: Wiederaufnahmeindex kryptographisch signiert — Manipulationen erkannt.
- **Bad Sector Behandlung**: Zero-pad + forensisches Log, Erfassung läuft ohne Absturz weiter.
- **Thread-sichere UI**: `threading.Lock` auf gemeinsamen Zustand, keine Race Conditions.
- **UI deaktiviert während Erfassung**: Kein Mehrfachstart, keine Hot-Änderungen.
- **Src/Dst Validierung**: Blockiert wenn Ziel eine Partition des Quellgeräts ist.
- **Fortschrittsbalken bei Wiederaufnahme**: Korrekt auf den tatsächlichen Offset aktualisiert.
- **Statistik-Label in 5 Sprachen**: Geschwindigkeit/ETA korrekt lokalisiert.

### Vollständiger Funktionsumfang
- Echter SWB, zufälliger AES-Nonce, DSGVO-Betreiber (Art.30), angewandte Aufbewahrung (Art.5c),
  Forensischer Bericht, SHA-256-Prüfung nach Erfassung, Bit-für-Bit-Abbild.

### Installation
`pip install -r requirements.txt` | Mit `sudo` ausführen.

# 🛡️ Disk Guard Pro v1.8.0 - Forensic Sapphire
Suite definitiva per l'acquisizione forense e la protezione dati a norma GDPR.

### Novità v1.8.0 — Security & Robustness
- **SHA-256 senza pickle**: Hash ricalcolato da sorgente su resume (no RCE risk).
- **HMAC-SHA256 su .idx**: File di ripresa firmato crittograficamente — manomissione rilevata.
- **Gestione Bad Sectors**: Zero-pad + log forense, acquisizione continua senza crash.
- **UI Thread-safe**: `threading.Lock` su stato condiviso, zero race condition.
- **UI disabilitata durante acquisizione**: No avvio multiplo, no modifiche a caldo.
- **Validazione src/dst**: Blocco se destinazione è partizione della sorgente.
- **Progress bar su resume**: Aggiornata correttamente all'offset reale.
- **Label statistiche in 5 lingue**: Velocità/Speed/Vitesse/... localizzato.

### Funzionalità complete
- SWB reale (`fcntl.ioctl/BLKROSET`), nonce AES casuale, operatore GDPR (Art.30),
  retention applicata (Art.5c), report forense, verifica SHA-256 post-acquisizione,
  imaging bit-a-bit dischi interi e partizioni.

### Installazione
`pip install -r requirements.txt` | Eseguire con `sudo`.

# 🛡️ Disk Guard Pro v1.8.0 - Forensic Sapphire Edition

**Disk Guard Pro** è il software definitivo per la clonazione forense certificata "bit-to-bit", la protezione crittografica avanzata e la gestione dei dati conforme al GDPR. La versione **Sapphire** raggiunge la massima maturità di sicurezza e robustezza: elimina i vettori di attacco RCE da deserialization, garantisce integrità forense del file di ripresa, gestisce i bad sector senza interrompere l'acquisizione e offre un'interfaccia completamente reattiva e thread-safe.

---

## 🚀 Funzionalità Forensi & GDPR (v1.8.0)

- **Integrità SHA-256 senza pickle**: Su resume, l'hash viene ricalcolato direttamente dalla sorgente — nessun rischio RCE da deserialization.
- **HMAC-SHA256 sul file .idx**: Il file di ripresa è firmato crittograficamente con la chiave PBKDF2. Qualsiasi manomissione viene rilevata e blocca il resume.
- **Gestione Bad Sectors**: I settori danneggiati vengono sostituiti con zeri (standard forense), loggati e l'acquisizione continua senza interruzione.
- **UI Thread-safe**: `threading.Lock` protegge tutto lo stato condiviso tra UI e worker thread — zero race condition.
- **UI disabilitata durante acquisizione**: Tutti i controlli vengono bloccati durante l'elaborazione e riabilitati al termine.
- **Validazione src/dst**: Blocco automatico se la destinazione è una partizione della sorgente.
- **Progress bar corretta su resume**: La barra mostra lo stato reale dell'acquisizione in ripresa.
- **Label statistiche in 5 lingue**: La stringa Velocità/Speed/Vitesse/... rispetta la lingua selezionata.
- **Retention GDPR (Art.5c)**: Purga automatica delle voci log scadute con conferma.
- **Report Forense**: Report testuale strutturato generato/proposto a fine acquisizione.
- **Verifica SHA-256 Post-Acquisizione**: Confronto hash certificato sull'immagine finale.
- **SWB reale**: Blocco scrittura OS-level via `fcntl.ioctl(BLKROSET)` sulla sorgente.
- **Operatore GDPR (Art.30)**: Campo obbligatorio registrato nel log audit ogni operazione.
- **Nonce AES casuale**: `os.urandom(8)` per ogni acquisizione, mai riutilizzato.
- **PBKDF2 (100k iterazioni)**: Chiave AES-256 derivata con salt casuale (Art.32 GDPR).

---

## 🛠️ Requisiti di Sistema

Il software è compatibile con **Linux** (testato su Ubuntu/Debian).

### Prerequisiti Python
Assicurarsi di avere Python 3.10 o superiore. Installare le dipendenze:

```bash
pip install -r requirements.txt
```

### Esecuzione
Avviare con privilegi di **Root** per accedere ai dispositivi fisici e attivare il Software Write Block:

```bash
sudo python3 "Disk Guard Pro.py"
```

---

## 📖 Crediti e Note Legali
Sviluppato da **Massimo Lo Sciuto**. Supporto tecnico: **AI Assistant (Antigravity)**.
Il software è progettato per uso professionale in ambito investigativo e sicurezza informatica.

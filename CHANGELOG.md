# 📜 Changelog - Disk Guard Pro

Tutti i cambiamenti significativi a questo progetto sono documentati in questo file.

## [1.8.0] - 2026-03-07 (Forensic Sapphire)
### Aggiunto / Corretto
- **[🔒] Eliminato pickle**: Il resume non usa più `pickle` (RCE risk). L'hash SHA-256 viene ricalcolato dall'inizio della sorgente fino all'offset salvato, garantendo integrità senza vulnerabilità.
- **[🔒] HMAC-SHA256 su file .idx**: Il file di ripresa è ora firmato con HMAC-SHA256 derivato dalla chiave PBKDF2. Qualsiasi manomissione viene rilevata e il resume viene annullato (ripartenza dall'inizio).
- **[🛡️] Gestione Bad Sectors**: I settori danneggiati sono ora gestiti senza interruzione: l'errore I/O viene intercettato, il settore viene sostituito con 16 KB di zeri (standard forense), l'evento è registrato nell'audit log.
- **[🖥️] UI Thread-safe**: `threading.Lock` protegge lo stato condiviso (`stop_requested`, `_last_idx_data`, `_last_idx_path`) tra UI thread e worker thread.
- **[🖥️] Controlli UI disabilitati durante acquisizione**: I pulsanti Avvia, Aggiorna, Retention e Verifica — nonché i campi operatore, password e sorgente/destinazione — vengono disabilitati durante l'acquisizione e riabilitati al termine.
- **[🔎] Validazione src/dst**: Blocco automatico se la destinazione è una sottodirectory (partizione) della sorgente, prevenendo la sovrascrittura dei dati originali.
- **[📊] Progress bar corretta su resume**: La barra di avanzamento viene impostata al valore corretto (`s_off/tot`) immediatamente dopo la lettura del file `.idx`.
- **[🌐] Label statistiche tradotta**: Il testo "Velocità / Speed / Vitesse / ..." è ora gestito dal dizionario `LANG_DATA` per tutte le 5 lingue.

## [1.7.0] - 2026-03-07 (Forensic Emerald)

### Aggiunto
- **Retention GDPR Applicata (Art.5c)**: Nuovo pulsante "Applica Retention" nel tab Audit che legge il log CSV, individua e rimuove (previa conferma) le voci più vecchie della soglia impostata (30gg/90gg/1 anno).
- **Report Forense**: Generazione di un report testuale strutturato (`forensic_report_YYYYMMDD.txt`) contenente tutte le voci dell'audit log, data/ora, operatore e policy di retention. Proposto automaticamente a fine acquisizione.
- **Verifica SHA-256 Post-Acquisizione**: Nuovo tasto "Verifica" nel tab Audit: seleziona il file immagine e inserisce l'hash di riferimento — il software ricalcola e confronta SHA-256, segnalando OK o errore.

### Corretto / Migliorato
- **Flush Immediato al Stop**: Il pulsante "Ferma" ora esegue un flush immediato del file `.idx` con lo stato più recente, garantendo la ripresa sicura anche su interruzioni rapide.

## [1.6.0] - 2026-03-07 (Forensic Diamond)
### Aggiunto
- **Campo Operatore GDPR (Art.30)**: Campo obbligatorio nell'interfaccia per registrare il nome del responsabile del trattamento. Registrato nel log CSV per ogni operazione, conforme al Registro dei Trattamenti.
- **Clonazione Dischi Interi**: Supporto completo all'acquisizione forense Bit-to-Bit di interi dischi fisici (es. `/dev/sda`) oltre alle singole partizioni, tramite rilevamento con `lsblk`.

### Corretto / Migliorato
- **Software Write Block Reale**: Il toggle SWB ora imposta un blocco di scrittura a livello di SO tramite `fcntl.ioctl(BLKROSET)` sul device sorgente, garantendo protezione hardware effettiva e non solo logica.
- **Nonce AES-256-CTR Casuale**: Il nonce non viene più derivato deterministicamente dal salt (vulnerabilità critica). Viene ora generato con `os.urandom(8)` e salvato nel file `.idx`, eliminando il rischio di riutilizzo nonce+chiave.
- **Hash SHA-256 Ripristinabile**: Lo stato interno dell'hash SHA-256 viene serializzato (via `pickle` + `base64`) nel file `.idx` ad ogni checkpoint. In caso di interruzione e ripresa, il hash finale risulta certificabile sull'intera sorgente.
- **Log Audit con Operatore**: Tutte le voci del log CSV ora includono il nome dell'operatore (`forensic_audit_v160.csv`).

## [1.5.0] - 2026-02-27 (Forensic Platinum)
### Aggiunto
- **Integrità Forense**: Calcolo SHA-256 in tempo reale durante la clonazione per validità probatoria.
- **Sicurezza GDPR**: Derivazione chiave tramite PBKDF2 (100.000 iterazioni) con Salt casuale di 16 byte.
- **Monitoraggio UX**: Aggiunta di metriche in tempo reale: Velocità (MB/s) e Tempo Stimato (ETA).
- **Audit Logging v1.5.0**: Registro esteso con impronta digitale SHA-256 e parametri di sicurezza avanzati.

## - Global Edition - 2024-05-24
### Aggiunto
- **Internazionalizzazione (i18n)**: Supporto completo per 5 lingue (Italiano, English, Español, Français, Deutsch).
- **Cambio Lingua Dinamico**: L'interfaccia si aggiorna istantaneamente senza riavvio.

### Corretto
- **KeyError 'title'**: Risolto il bug nel caricamento del dizionario multilingua.
- **AttributeError**: Sistemata la chiamata ai metodi di aggiornamento dischi durante il cambio lingua.

## - GDPR Edition
- Introdotto **Retention Timer** per la scadenza dei dati.
- Aggiunto **Audit Logging CSV** per la conformità legale.

## - Ultimate Edition
- Mirroring Cloud SFTP simultaneo.
- Smart Skip per i settori danneggiati.
- Secure Wipe (DoD 5220.22-M).

## - Initial Release
- Clonazione byte-to-byte, AES-256 e compressione Zlib.

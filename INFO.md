# 📘 Guida Tecnica: Disk Guard Pro v1.8.0 Forensic Sapphire

**Disk Guard Pro** è una suite software professionale per la clonazione forense "bit-to-bit", la protezione crittografica e la gestione legalmente valida dei dati. Opera a basso livello per garantire l'immutabilità e la validità legale del dato acquisito, con protezioni reali a livello di sistema operativo.

---

## 🎯 Protocolli Forensi & GDPR

Il software è stato ingegnerizzato per soddisfare i rigorosi standard della **Digital Forensics** e del **GDPR (UE 2016/679)**.

### 1. Integrità Digitale (Forense)

*   **Fingerprint SHA-256 Ripristinabile:** Ogni bit letto dal supporto sorgente viene elaborato in tempo reale attraverso l'algoritmo SHA-256. Lo stato interno dell'hash viene serializzato (Base64/Pickle) nel file `.idx` ad ogni checkpoint: in caso di interruzione e ripresa, l'impronta finale rimane certificabile sull'intera sorgente.
*   **Software Write Block Reale (SWB):** Imposta il blocco hardware di scrittura tramite `fcntl.ioctl(BLKROSET)` sul device sorgente — non semplice apertura in `rb`, ma vera protezione OS-level che impedisce qualsiasi scrittura accidentale sui dati originali.
*   **Acquisizione Bit-to-Bit:** Supporta interi dischi fisici (`/dev/sda`) e singole partizioni (`/dev/sda1`), rilevati tramite `lsblk`.

### 2. Sicurezza del Trattamento (GDPR)

*   **PBKDF2 (Art. 32 GDPR):** 100.000 iterazioni con Salt casuale di 16 byte per una chiave AES-256 impenetrabile.
*   **Nonce AES Casuale e Unico:** Il nonce AES-256-CTR è generato con `os.urandom(8)` per ogni acquisizione e salvato nel file `.idx`. Elimina la vulnerabilità critica precedente dove il riutilizzo di nonce+chiave annullava la cifratura.
*   **Registro Operatore (Art. 30 GDPR):** Campo obbligatorio nell'UI per il nome del responsabile del trattamento. Ogni voce del log CSV include il nome dell'operatore per garantire la catena di custodia completa.

### 3. Business Continuity

*   **Resume Intelligente:** Il file `.idx` conserva offset di sorgente/destinazione, salt, nonce **e stato SHA-256** serializzato. La ripresa è completa: crittograficamente allineata, con hash certificabile.

---

## 🛠️ Tecnologie Chiave (v1.6.0)

| Funzione | Implementazione Tecnica | Scopo |
| :--- | :--- | :--- |
| **KDF** | PBKDF2 (100.000 rounds) | Protezione contro attacchi Brute-Force (Art.32 GDPR) |
| **Hashing** | SHA-256 ricalcolato su resume | Integrità forense senza pickle/RCE risk |
| **Encryption** | AES-256 CTR + Nonce casuale | Riservatezza senza vulnerabilità di nonce riuso |
| **SWB** | `fcntl.ioctl(BLKROSET)` | Blocco scrittura OS-level sulla sorgente |
| **Resume** | `.idx` con HMAC-SHA256 | Protezione da manomissione del file di ripresa |
| **Audit Trail** | CSV con Operatore + SHA-256 | Catena di custodia conforme GDPR Art.30 |
| **Retention** | Purge CSV su soglia configurabile | Conformità GDPR Art.5c (limitazione conservazione) |
| **Report** | File .txt strutturato | Report forense certificabile e stampabile |
| **Verifica** | SHA-256 su immagine destination | Prova di corrispondenza post-acquisizione |
| **Bad Sectors** | Zero-pad + log audit | Standard forense: continua senza interrompere |
| **Thread Safety** | `threading.Lock` | Zero race condition tra UI e worker thread |
| **UI Reattiva** | Disable/enable durante acquisizione | Previene avvio multiplo e modifiche a caldo |
| **Disk Detection** | `lsblk` + fallback psutil | Rilevamento dischi fisici e partizioni |
| **Compression** | Zlib (Block-wise) | Ottimizzazione spazio su disco |
| **I/O** | 1MB Buffered Binary Read + fsync | Prestazioni e stabilità forense |

---

## 📖 Crediti

*   **Sviluppatore:** Massimo Lo Sciuto
*   **Versione:** 1.8.0 Forensic Sapphire Edition
*   **AI Support:** Antigravity AI

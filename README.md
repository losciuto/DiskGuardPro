# 🛡️ Disk Guard Pro v1.1.0 - Ultimate Edition

**Disk Guard Pro** è un software professionale per la clonazione "byte-to-byte" di supporti fisici (dischi rigidi, chiavette USB, SD card). Progettato per la massima sicurezza, combina crittografia militare, compressione dei dati e funzionalità di recupero forense.

---

## 🚀 Funzionalità Killer

- **Copia Byte-to-Byte:** Clonazione esatta del supporto fisico bit per bit.
- **Criptazione AES-256:** Protezione dei dati tramite algoritmo AES in modalità CTR (Symmetric & Seekable).
- **Compressione Intelligente:** Utilizzo di Zlib per ridurre drasticamente le dimensioni del backup.
- **Mirroring Cloud (SFTP):** Backup simultaneo su server remoto durante la copia locale.
- **Resume con Indice (.idx):** Possibilità di interrompere e riprendere la copia esattamente da dove si era fermata, anche dopo un riavvio.
- **Smart Skip (Settori Danneggiati):** Non si blocca sui dischi morenti; salta i settori corrotti e genera una mappa `.bad`.
- **Secure Wipe (DoD 5220.22-M):** Bonifica il disco di destinazione con sovrascritture multiple prima della copia.
- **Espulsione Sicura:** Unmount automatico dell'hardware al termine dell'operazione.

---

## 🛠️ Requisiti di Sistema

Il software è compatibile con **Linux** (testato su Ubuntu/Debian) e **Windows**.

### Prerequisiti Python
Assicurati di avere Python 3.10 o superiore installato. Installa le dipendenze necessarie:

```bash
pip install -r requirements.txt

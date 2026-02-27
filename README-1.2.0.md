# 🛡️ Disk Guard Pro v1.2.0

**Disk Guard Pro** è un potente strumento di clonazione e protezione dati "byte-to-byte", sviluppato per unire prestazioni forensi e conformità legale (**GDPR**). 

## 🌟 Caratteristiche Principali

- **Sicurezza Militare**: Criptazione AES-256 con compressione integrata.
- **Resilienza Totale**: Ripresa della copia interrotta tramite file indice (.idx) senza perdita di dati.
- **Conformità GDPR**: 
  - **Retention Timer**: Imposta la data di scadenza dei backup.
  - **Audit Log**: Registro immutabile in formato CSV per dimostrare la conformità (Accountability).
- **Funzioni Killer**:
  - **Secure Wipe**: Cancellazione sicura del disco di destinazione (standard DoD).
  - **Smart Skip**: Superamento dei settori fisici danneggiati senza blocchi del sistema.
  - **Cloud Mirroring**: Sincronizzazione in tempo reale su server SFTP.

## 🛠️ Requisiti e Installazione

Assicurati di avere Python 3.10+ e installa le dipendenze:

```bash
pip install customtkinter pycryptodome psutil paramiko

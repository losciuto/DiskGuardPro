# 📘 Guida Tecnica: Disk Guard Pro v1.5.0 Platinum

**Disk Guard Pro** è una suite software professionale per la clonazione "byte-to-byte", la protezione crittografica e la gestione forense dei dati. A differenza dei programmi di backup convenzionali, opera a basso livello per garantire l'immutabilità e la validità legale del dato acquisito.

---

## 🎯 Protocolli Forensi & GDPR

Il software è stato ingegnerizzato per soddisfare i rigorosi standard della **Digital Forensics** e del **GDPR (UE 2016/679)**.

### 1. Integrità Digitale (Forense)

*   **Fingerprint SHA-256:** Ogni bit letto dal supporto sorgente viene elaborato in tempo reale attraverso l'algoritmo SHA-256. Questo produce una "firma digitale" unica che prova l'identità tra originale e copia in sede giudiziaria.
*   **Software Write Block (SWB):** Implementa un meccanismo di sola lettura logica per prevenire alterazioni accidentali della sorgente (timestamp, metadati, file eliminati).
*   **Catena di Custodia:** Il registro `forensic_audit_v150.csv` documenta ogni fase dell'acquisizione, inclusi operatori, tempi e identificativi hardware.

### 2. Sicurezza del Trattamento (GDPR)

*   **PBKDF2 (Password-Based Key Derivation Function 2):** In conformità all'Art. 32 del GDPR, Disk Guard Pro non utilizza direttamente la password. Applica 100.000 iterazioni PBKDF2 con un **Salt casuale** di 16 byte per derivare una chiave a 256-bit impenetrabile ad attacchi brute-force.
*   **Crittografia AES-256 CTR:** I dati sono protetti in modalità "Symmetric & Seekable", permettendo accessi veloci pur mantenendo la massima blindatura militare.

### 3. Business Continuity

*   **Resume Intelligente:** Grazie al file `.idx` e al calcolo deterministico del nonce, il processo può essere ripreso dopo un'interruzione di corrente o un arresto forzato senza perdere l'integrità dei blocchi già scritti.

---

## 🛠️ Tecnologie Chiave (v1.5.0)

| Funzione | Implementazione Tecnica | Scopo |
| :--- | :--- | :--- |
| **KDF** | PBKDF2 (100.000 rounds) | Protezione contro attacchi Brute-Force |
| **Hashing** | SHA-256 Real-time | Integrità Forense e Validità Legale |
| **Encryption** | AES-256 CTR | Riservatezza e Accesso Casuale |
| **Compression** | Zlib (Block-wise) | Ottimizzazione dello spazio su disco |
| **I/O** | 1MB Buffered Binary Read | Prestazioni e stabilità forense |

---

## 📖 Crediti

*   **Sviluppatore:** Massimo Lo Sciuto
*   **Versione:** 1.5.0 Forensic Platinum Edition
*   **AI Support:** Antigravity AI

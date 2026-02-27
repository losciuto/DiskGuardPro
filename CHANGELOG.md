# 📜 Changelog - Disk Guard Pro

Tutti i cambiamenti significativi a questo progetto sono documentati in questo file.

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
- **Popup Info Tradotto**: Finestra "About" con localizzazione di versioni, crediti e descrizioni.
- **Nuovo Layout Header**: Selettore di lingua integrato e pulsante info circolare stilizzato.

### Corretto
- **KeyError 'title'**: Risolto il bug nel caricamento del dizionario multilingua.
- **AttributeError**: Sistemata la chiamata ai metodi di aggiornamento dischi durante il cambio lingua.
- **Padding UI**: Ottimizzati gli spazi per ospitare stringhe di lunghezza variabile (particolarmente per il tedesco e lo spagnolo).

## - GDPR Edition
- Introdotto **Retention Timer** per la scadenza dei dati.
- Aggiunto **Audit Logging CSV** per la conformità legale.

## - Ultimate Edition
- Mirroring Cloud SFTP simultaneo.
- Smart Skip per i settori danneggiati.
- Secure Wipe (DoD 5220.22-M).

## - Initial Release
- Clonazione byte-to-byte, AES-256 e compressione Zlib.

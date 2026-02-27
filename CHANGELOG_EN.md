# 📜 Changelog - Disk Guard Pro

## [1.5.0] - 2026-02-27 (Forensic Platinum)
### Added
- **Forensic Integrity**: Real-time SHA-256 hashing during imaging for evidence preservation.
- **GDPR Security**: PBKDF2 key derivation (100,000 iterations) with 16-byte random Salt.
- **UX Monitoring**: Real-time Speed (MB/s) and Estimated Time of Arrival (ETA).
- **Extended Audit Log**: Version 1.5.0 log with SHA-256 fingerprinting.

## - Forensic Gold Edition - 2024-05-24
### Added
- **Software Write Block (SWB)**: New option to force source opening in Read-Only mode (`rb`), preventing metadata alteration.
- **Forensic Tab**: Dedicated interface for evidence integrity management.
- **Advanced Audit Log**: Automatic generation of `forensic_audit.csv` for Chain of Custody tracking.
- **Forensic Certification**: Info popup updated with forensic compliance credits.

### Improved
- **I/O Error Handling**: Optimized stability when reading disks with bad sectors.
- **UI Scaling**: Better widget adaptation for high-resolution screens.

## - Global Edition
- Multi-language support (IT, EN, ES, FR, DE).
- Dynamic language switching and localized Info popup.

## - GDPR Edition
- Data Retention Timer and CSV compliance logging.

## - Ultimate Edition
- Simultaneous Cloud SFTP Mirroring and Secure Wipe (DoD 5220.22-M).

## - Initial Release
- Byte-to-byte cloning, AES-256 encryption, and Zlib compression.

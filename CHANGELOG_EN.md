# 📜 Changelog - Disk Guard Pro

## [1.8.0] - 2026-03-07 (Forensic Sapphire)
### Added / Fixed
- **[🔒] Pickle removed**: Resume no longer uses `pickle` (RCE risk). SHA-256 hash is recalculated from source offset 0 to `s_off` with no deserialization — forensically sound and safe.
- **[🔒] HMAC-SHA256 on .idx file**: The resume index file is now signed with HMAC-SHA256 derived from the PBKDF2 key. Any tampering is detected and resume is aborted (restart from beginning).
- **[🛡️] Bad Sector Handling**: I/O errors are now caught per-block; damaged sectors are replaced with zeros (forensic standard) and logged in the audit trail.
- **[🖥️] Thread-safe shared state**: `threading.Lock` protects `stop_requested`, `_last_idx_data`, and `_last_idx_path` between UI and worker threads.
- **[🖥️] UI disabled during acquisition**: Run, Refresh, Retention, and Verify buttons — along with all input fields — are disabled while acquisition is running and re-enabled on completion.
- **[🔎] src/dst validation**: Acquisition is blocked if destination is a partition of the source disk, preventing accidental overwrite of original evidence.
- **[📊] Progress bar on resume**: Progress bar is correctly set to `s_off/tot` immediately after reading the `.idx` file.
- **[🌐] Translated stats label**: Speed/ETA display text is now localized for all 5 languages via `LANG_DATA`.

## [1.7.0] - 2026-03-07 (Forensic Emerald)

### Added
- **GDPR Retention Enforced (Art.5c)**: New "Apply Retention" button in the Audit tab reads the CSV log, identifies and (with confirmation) removes entries older than the configured threshold (30d/90d/1y).
- **Forensic Report**: Generates a structured text report (`forensic_report_YYYYMMDD.txt`) containing all audit entries, date/time, operator, and retention policy. Automatically offered at acquisition completion.
- **Post-Acquisition SHA-256 Verification**: New "Verify" button in the Audit tab: select the image file and enter the reference hash — the software recalculates and compares SHA-256, reporting OK or mismatch.

### Fixed / Improved
- **Immediate Flush on Stop**: The "Stop" button now immediately flushes the `.idx` file with the latest state, ensuring safe resume even on rapid interruptions.

## [1.6.0] - 2026-03-07 (Forensic Diamond)
### Added
- **GDPR Operator Field (Art.30)**: Mandatory UI field to record the name of the data processing officer. Logged in the CSV audit trail for every operation, compliant with the Processing Register.
- **Full Disk Cloning**: Full support for Bit-to-Bit forensic acquisition of entire physical disks (e.g. `/dev/sda`) in addition to individual partitions, detected via `lsblk`.

### Fixed / Improved
- **Real Software Write Block**: The SWB toggle now sets an OS-level write lock via `fcntl.ioctl(BLKROSET)` on the source device, providing effective hardware-level protection rather than just logical.
- **Random AES-256-CTR Nonce**: The nonce is no longer deterministically derived from the salt (critical vulnerability). It is now generated with `os.urandom(8)` and saved in the `.idx` file, eliminating nonce+key reuse risk.
- **Resumable SHA-256 Hash**: The internal SHA-256 hash state is serialized (via `pickle` + `base64`) into the `.idx` file at each checkpoint. On interruption and resume, the final hash is certifiable over the entire source.
- **Audit Log with Operator**: All CSV log entries now include the operator name (`forensic_audit_v160.csv`).

## [1.5.0] - 2026-02-27 (Forensic Platinum)
### Added
- **Forensic Integrity**: Real-time SHA-256 hashing during imaging for evidence preservation.
- **GDPR Security**: PBKDF2 key derivation (100,000 iterations) with 16-byte random Salt.
- **UX Monitoring**: Real-time Speed (MB/s) and Estimated Time of Arrival (ETA).
- **Extended Audit Log**: Version 1.5.0 log with SHA-256 fingerprinting.

## - Forensic Gold Edition - 2024-05-24
### Added
- **Software Write Block (SWB)**: New option to force source opening in Read-Only mode.
- **Forensic Tab**: Dedicated interface for evidence integrity management.
- **Advanced Audit Log**: Automatic Chain of Custody tracking.

### Improved
- **I/O Error Handling**: Optimized stability for disks with bad sectors.

## - Global Edition
- Multi-language support (IT, EN, ES, FR, DE).

## - GDPR Edition
- Data Retention Timer and CSV compliance logging.

## - Ultimate Edition
- Simultaneous Cloud SFTP Mirroring and Secure Wipe (DoD 5220.22-M).

## - Initial Release
- Byte-to-byte cloning, AES-256 encryption, and Zlib compression.

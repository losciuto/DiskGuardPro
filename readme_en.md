# 🛡️ Disk Guard Pro v1.8.0 - Forensic Sapphire
Ultimate suite for forensic acquisition and GDPR-compliant data protection.

### New in v1.8.0 — Security & Robustness
- **SHA-256 without pickle**: Hash recalculated from source on resume (no RCE risk).
- **HMAC-SHA256 on .idx**: Resume index cryptographically signed — tampering detected.
- **Bad Sector Handling**: Zero-pad + forensic log, acquisition continues without crash.
- **Thread-safe UI**: `threading.Lock` on shared state, zero race conditions.
- **UI disabled during acquisition**: No multiple starts, no hot changes.
- **src/dst validation**: Blocked if destination is a partition of the source disk.
- **Progress bar on resume**: Correctly updated to actual offset.
- **Stats label in 5 languages**: Speed/ETA display properly localized.

### Full Feature Set
- Real SWB (`fcntl.ioctl/BLKROSET`), random AES nonce, GDPR operator (Art.30),
  enforced retention (Art.5c), forensic report, post-acquisition SHA-256 verification,
  bit-for-bit imaging of full disks and partitions.

### Installation
`pip install -r requirements.txt` | Run with `sudo`.

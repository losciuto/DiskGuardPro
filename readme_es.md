# 🛡️ Disk Guard Pro v1.8.0 - Forensic Sapphire
Suite definitiva para adquisición forense y protección de datos conforme al RGPD.

### Novedades v1.8.0 — Seguridad y Robustez
- **SHA-256 sin pickle**: Hash recalculado desde la fuente en la reanudación (sin riesgo RCE).
- **HMAC-SHA256 en .idx**: Índice de reanudación firmado criptográficamente — manipulación detectada.
- **Manejo de Bad Sectors**: Zero-pad + log forense, adquisición continúa sin crash.
- **UI Thread-safe**: `threading.Lock` en estado compartido, cero condiciones de carrera.
- **UI deshabilitada durante adquisición**: Sin inicios múltiples, sin cambios en caliente.
- **Validación src/dst**: Bloqueado si el destino es una partición del dispositivo fuente.
- **Barra de progreso en reanudación**: Actualizada correctamente al offset real.
- **Etiqueta estadísticas en 5 idiomas**: Velocidad/ETA correctamente localizado.

### Conjunto completo de funcionalidades
- SWB real, Nonce AES aleatorio, Operador RGPD (Art.30), Retención aplicada (Art.5c),
  Informe forense, Verificación SHA-256 post-adquisición, Imagen bit a bit.

### Instalación
`pip install -r requirements.txt` | Ejecutar con `sudo`.

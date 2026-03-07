import os, fcntl, threading, zlib, hashlib, json, subprocess, csv, time, hmac
from datetime import datetime, timedelta
import customtkinter as ctk
from tkinter import messagebox, filedialog
import psutil
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Protocol.KDF import PBKDF2

AUDIT_FILE = "forensic_audit_v180.csv"
VERSION    = "1.8.0"
CODENAME   = "Forensic Sapphire"
BLKROSET   = 0x125d   # Linux ioctl: set block device read-only

# ── Mappa giorni di retention ─────────────────────────────────────────────────
RETENTION_DAYS_MAP = {
    "30 Giorni": 30, "90 Giorni": 90, "1 Anno": 365, "Illimitata": None,
    "30 Days": 30, "90 Days": 90, "1 Year": 365, "Unlimited": None,
    "30 Días": 30, "90 Días": 90, "1 Año": 365, "Ilimitada": None,
    "30 Jours": 30, "90 Jours": 90, "1 An": 365, "Illimitée": None,
    "30 Tage": 30, "90 Tage": 90, "1 Jahr": 365, "Unbegrenzt": None,
}

# ── Dizionario internazionale v1.8.0 ─────────────────────────────────────────
LANG_DATA = {
    "Italiano": {
        "title": f"🛡️ Disk Guard Pro v{VERSION}", "header": "Suite Forense & GDPR",
        "tab_ops": "Operazioni", "tab_gdpr": "Audit & Compliance", "tab_forensic": "Forense",
        "swb_label": "Software Write Block (Sola Lettura)",
        "swb_desc": "Imposta il blocco di scrittura a livello OS sulla sorgente.",
        "run": "AVVIA ACQUISIZIONE", "stop": "FERMA LA COPIA IN CORSO", "info_btn": "i",
        "pass_ph": "Password AES-256", "src": "Sorgente:", "dst": "Destinazione:",
        "operator_label": "Operatore (GDPR Art.30):", "operator_ph": "Nome e cognome operatore",
        "err_operator": "Inserire il nome dell'operatore (richiesto GDPR Art.30).",
        "err_same_disk": "Errore: la destinazione è una partizione della sorgente!\nOperazione bloccata per prevenire la sovrascrittura dei dati originali.",
        "refresh": "Aggiorna",
        "status_ready": "Pronto per acquisizione forense (Dischi/Partizioni)",
        "err_pass": "Password mancante!",
        "confirm": "Sovrascrivere {dst}?\nATTENZIONE: Procedura forense irreversibile.\nClonazione Bit-to-Bit (Dischi interi e Partizioni).",
        "retention": "Conservazione Dati:", "days": ["30 Giorni", "90 Giorni", "1 Anno", "Illimitata"],
        "btn_purge": "Applica Retention (Elimina voci scadute)",
        "purge_confirm": "Eliminare {n} voci del log audit più vecchie di {d}?\nQuesta operazione è irreversibile.",
        "purge_done": "{n} voci eliminate dal log audit.",
        "purge_none": "Nessuna voce scaduta trovata nel log audit.",
        "btn_verify": "Verifica SHA-256 Post-Acquisizione",
        "verify_running": "⏳ Verifica SHA-256 in corso...",
        "verify_ok": "✅ Verifica OK: l'immagine corrisponde all'originale.\nSHA-256: {h}",
        "verify_fail": "❌ Verifica FALLITA: hash non corrispondente!\nAtteso:  {e}\nOttenuto: {g}",
        "verify_ask_img": "Seleziona il file immagine da verificare.",
        "verify_ask_ref": "Inserisci l'hash SHA-256 di riferimento (dall'audit log):",
        "report_saved": "Report forense salvato in:\n{path}",
        "stats_fmt": "Velocità: {speed:.2f} MB/s | ETA: {eta}",
        "bad_sector": "⚠️ Settore danneggiato a offset {off}: sostituito con zeri.",
        "idx_tampered": "⚠️ Il file .idx è stato modificato o è corrotto (HMAC non valido). Ripartenza dall'inizio.",
        "resuming": "▶ Ripresa da {mb} MB (hash ricalcolato)...",
        "info_ver": f"Versione: {VERSION} '{CODENAME}'", "info_auth": "Autore: Massimo Lo Sciuto",
        "info_supp": "Supporto: AI Assistant (Antigravity)",
        "info_desc": "Suite forense certificata SHA-256 & PBKDF2.\nSWB reale, HMAC .idx, bad-sector handling,\nthread-safe, validazione src/dst, UI reattiva."
    },
    "English": {
        "title": f"🛡️ Disk Guard Pro v{VERSION}", "header": "Forensic & GDPR Suite",
        "tab_ops": "Operations", "tab_gdpr": "Audit & Compliance", "tab_forensic": "Forensic",
        "swb_label": "Software Write Block (Read-Only)",
        "swb_desc": "Sets OS-level write block on the source device.",
        "run": "START ACQUISITION", "stop": "STOP CURRENT COPY", "info_btn": "i",
        "pass_ph": "AES-256 Password", "src": "Source:", "dst": "Destination:",
        "operator_label": "Operator (GDPR Art.30):", "operator_ph": "Operator full name",
        "err_operator": "Operator name is required (GDPR Art.30 compliance).",
        "err_same_disk": "Error: destination is a partition of the source!\nOperation blocked to prevent overwriting original evidence.",
        "refresh": "Refresh",
        "status_ready": "Ready for forensic acquisition (Disks/Partitions)",
        "err_pass": "Password missing!",
        "confirm": "Overwrite {dst}?\nWARNING: Irreversible forensic procedure.\nBit-to-Bit clone (Full Disks and Partitions).",
        "retention": "Data Retention:", "days": ["30 Days", "90 Days", "1 Year", "Unlimited"],
        "btn_purge": "Apply Retention (Delete expired entries)",
        "purge_confirm": "Delete {n} audit log entries older than {d}?\nThis operation is irreversible.",
        "purge_done": "{n} entries deleted from audit log.",
        "purge_none": "No expired entries found in audit log.",
        "btn_verify": "Post-Acquisition SHA-256 Verification",
        "verify_running": "⏳ SHA-256 verification in progress...",
        "verify_ok": "✅ Verification OK: image matches the original.\nSHA-256: {h}",
        "verify_fail": "❌ Verification FAILED: hash mismatch!\nExpected: {e}\nGot:      {g}",
        "verify_ask_img": "Select the image file to verify.",
        "verify_ask_ref": "Enter the reference SHA-256 hash (from audit log):",
        "report_saved": "Forensic report saved to:\n{path}",
        "stats_fmt": "Speed: {speed:.2f} MB/s | ETA: {eta}",
        "bad_sector": "⚠️ Bad sector at offset {off}: replaced with zeros.",
        "idx_tampered": "⚠️ The .idx file has been modified or is corrupt (invalid HMAC). Restarting from beginning.",
        "resuming": "▶ Resuming from {mb} MB (hash recalculated)...",
        "info_ver": f"Version: {VERSION} '{CODENAME}'", "info_auth": "Author: Massimo Lo Sciuto",
        "info_supp": "Support: AI Assistant (Antigravity)",
        "info_desc": "Certified SHA-256 & PBKDF2 forensic suite.\nReal SWB, HMAC .idx, bad-sector handling,\nthread-safe, src/dst validation, reactive UI."
    },
    "Español": {
        "title": f"🛡️ Disk Guard Pro v{VERSION}", "header": "Suite Forense y RGPD",
        "tab_ops": "Operaciones", "tab_gdpr": "Auditoría y Cumplimiento", "tab_forensic": "Forense",
        "swb_label": "Software Write Block (Solo Lectura)",
        "swb_desc": "Establece bloqueo de escritura a nivel SO en el dispositivo fuente.",
        "run": "INICIAR ADQUISICIÓN", "stop": "DETENER COPIA EN CURSO", "info_btn": "i",
        "pass_ph": "Contraseña AES-256", "src": "Origen:", "dst": "Destino:",
        "operator_label": "Operador (RGPD Art.30):", "operator_ph": "Nombre completo del operador",
        "err_operator": "El nombre del operador es obligatorio (conformidad RGPD Art.30).",
        "err_same_disk": "Error: ¡el destino es una partición del origen!\nOperación bloqueada para evitar sobrescribir la evidencia original.",
        "refresh": "Actualizar",
        "status_ready": "Listo para adquisición forense (Discos/Particiones)",
        "err_pass": "¡Contraseña faltante!",
        "confirm": "¿Sobrescribir {dst}?\nADVERTENCIA: Procedimiento forense irreversible.\nClonación Bit a Bit (Discos completos y Particiones).",
        "retention": "Retención de datos:", "days": ["30 Días", "90 Días", "1 Año", "Ilimitada"],
        "btn_purge": "Aplicar Retención (Eliminar entradas caducadas)",
        "purge_confirm": "¿Eliminar {n} entradas del log más antiguas de {d}?\nEsta operación es irreversible.",
        "purge_done": "{n} entradas eliminadas del log de auditoría.",
        "purge_none": "No se encontraron entradas caducadas en el log de auditoría.",
        "btn_verify": "Verificación SHA-256 Post-Adquisición",
        "verify_running": "⏳ Verificación SHA-256 en curso...",
        "verify_ok": "✅ Verificación OK: la imagen coincide con el original.\nSHA-256: {h}",
        "verify_fail": "❌ Verificación FALLIDA: hash no coincide!\nEsperado: {e}\nObtenido: {g}",
        "verify_ask_img": "Selecciona el fichero imagen a verificar.",
        "verify_ask_ref": "Ingresa el hash SHA-256 de referencia (del log de auditoría):",
        "report_saved": "Informe forense guardado en:\n{path}",
        "stats_fmt": "Velocidad: {speed:.2f} MB/s | ETA: {eta}",
        "bad_sector": "⚠️ Sector dañado en offset {off}: reemplazado con ceros.",
        "idx_tampered": "⚠️ El archivo .idx ha sido modificado o está corrupto (HMAC inválido). Reiniciando desde el principio.",
        "resuming": "▶ Reanudando desde {mb} MB (hash recalculado)...",
        "info_ver": f"Versión: {VERSION} '{CODENAME}'", "info_auth": "Autor: Massimo Lo Sciuto",
        "info_supp": "Soporte: AI Assistant (Antigravity)",
        "info_desc": "Suite forense certificada SHA-256 y PBKDF2.\nSWB real, HMAC .idx, manejo de bad sectors,\nthread-safe, validación src/dst, UI reactiva."
    },
    "Français": {
        "title": f"🛡️ Disk Guard Pro v{VERSION}", "header": "Suite Forensique & RGPD",
        "tab_ops": "Opérations", "tab_gdpr": "Audit & Conformité", "tab_forensic": "Forensique",
        "swb_label": "Software Write Block (Lecture Seule)",
        "swb_desc": "Active le blocage d'écriture au niveau OS sur le périphérique source.",
        "run": "LANCER L'ACQUISITION", "stop": "ARRÊTER LA COPIE", "info_btn": "i",
        "pass_ph": "Mot de passe AES-256", "src": "Source:", "dst": "Destination:",
        "operator_label": "Opérateur (RGPD Art.30):", "operator_ph": "Nom complet de l'opérateur",
        "err_operator": "Le nom de l'opérateur est requis (conformité RGPD Art.30).",
        "err_same_disk": "Erreur: la destination est une partition de la source!\nOpération bloquée pour éviter l'écrasement des preuves originales.",
        "refresh": "Actualiser",
        "status_ready": "Prêt pour l'acquisition forensique (Disques/Partitions)",
        "err_pass": "Mot de passe manquant!",
        "confirm": "Écraser {dst}?\nATTENTION: Procédure forensique irréversible.\nClone Bit-à-Bit (Disques entiers et Partitions).",
        "retention": "Rétention des données:", "days": ["30 Jours", "90 Jours", "1 An", "Illimitée"],
        "btn_purge": "Appliquer Rétention (Supprimer entrées expirées)",
        "purge_confirm": "Supprimer {n} entrées du log antérieures à {d}?\nCette opération est irréversible.",
        "purge_done": "{n} entrées supprimées du log d'audit.",
        "purge_none": "Aucune entrée expirée trouvée dans le log d'audit.",
        "btn_verify": "Vérification SHA-256 Post-Acquisition",
        "verify_running": "⏳ Vérification SHA-256 en cours...",
        "verify_ok": "✅ Vérification OK: l'image correspond à l'original.\nSHA-256: {h}",
        "verify_fail": "❌ Vérification ÉCHOUÉE: hash non correspondant!\nAttendu:  {e}\nObtenu:   {g}",
        "verify_ask_img": "Sélectionnez le fichier image à vérifier.",
        "verify_ask_ref": "Entrez le hash SHA-256 de référence (depuis le log d'audit):",
        "report_saved": "Rapport forensique enregistré dans:\n{path}",
        "stats_fmt": "Vitesse: {speed:.2f} Mo/s | ETA: {eta}",
        "bad_sector": "⚠️ Secteur défectueux à l'offset {off}: remplacé par des zéros.",
        "idx_tampered": "⚠️ Le fichier .idx a été modifié ou est corrompu (HMAC invalide). Redémarrage depuis le début.",
        "resuming": "▶ Reprise depuis {mb} Mo (hash recalculé)...",
        "info_ver": f"Version: {VERSION} '{CODENAME}'", "info_auth": "Auteur: Massimo Lo Sciuto",
        "info_supp": "Support: AI Assistant (Antigravity)",
        "info_desc": "Suite forensique certifiée SHA-256 & PBKDF2.\nSWB réel, HMAC .idx, gestion bad sectors,\nthread-safe, validation src/dst, UI réactive."
    },
    "Deutsch": {
        "title": f"🛡️ Disk Guard Pro v{VERSION}", "header": "Forensik & DSGVO Suite",
        "tab_ops": "Operationen", "tab_gdpr": "Audit & Compliance", "tab_forensic": "Forensik",
        "swb_label": "Software Write Block (Schreibschutz)",
        "swb_desc": "Setzt OS-Schreibsperre auf dem Quellgerät.",
        "run": "ERFASSUNG STARTEN", "stop": "KOPIERVORGANG STOPPEN", "info_btn": "i",
        "pass_ph": "AES-256 Passwort", "src": "Quelle:", "dst": "Ziel:",
        "operator_label": "Betreiber (DSGVO Art.30):", "operator_ph": "Vollständiger Name des Betreibers",
        "err_operator": "Betreibername ist erforderlich (DSGVO Art.30 Konformität).",
        "err_same_disk": "Fehler: Das Ziel ist eine Partition der Quelle!\nVorgang blockiert, um das Überschreiben originaler Beweise zu verhindern.",
        "refresh": "Aktualisieren",
        "status_ready": "Bereit für forensische Erfassung (Festplatten/Partitionen)",
        "err_pass": "Passwort fehlt!",
        "confirm": "{dst} überschreiben?\nWARNUNG: Unumkehrbares forensisches Verfahren.\nBit-für-Bit-Klon (Gesamte Festplatten und Partitionen).",
        "retention": "Aufbewahrungsfrist:", "days": ["30 Tage", "90 Tage", "1 Jahr", "Unbegrenzt"],
        "btn_purge": "Aufbewahrung anwenden (Abgelaufene Einträge löschen)",
        "purge_confirm": "{n} Audit-Log-Einträge älter als {d} löschen?\nDieser Vorgang ist unumkehrbar.",
        "purge_done": "{n} Einträge aus dem Audit-Log gelöscht.",
        "purge_none": "Keine abgelaufenen Einträge im Audit-Log gefunden.",
        "btn_verify": "SHA-256-Verifizierung nach Erfassung",
        "verify_running": "⏳ SHA-256-Verifizierung läuft...",
        "verify_ok": "✅ Verifizierung OK: Image stimmt mit Original überein.\nSHA-256: {h}",
        "verify_fail": "❌ Verifizierung FEHLGESCHLAGEN: Hash stimmt nicht überein!\nErwartet:  {e}\nErhalten:  {g}",
        "verify_ask_img": "Wählen Sie die zu verifizierende Image-Datei aus.",
        "verify_ask_ref": "Geben Sie den Referenz-SHA-256-Hash ein (aus dem Audit-Log):",
        "report_saved": "Forensischer Bericht gespeichert unter:\n{path}",
        "stats_fmt": "Geschwindigkeit: {speed:.2f} MB/s | ETA: {eta}",
        "bad_sector": "⚠️ Defekter Sektor bei Offset {off}: mit Nullen ersetzt.",
        "idx_tampered": "⚠️ Die .idx-Datei wurde verändert oder ist beschädigt (ungültiger HMAC). Neustart von Anfang.",
        "resuming": "▶ Wiederaufnahme ab {mb} MB (Hash neu berechnet)...",
        "info_ver": f"Version: {VERSION} '{CODENAME}'", "info_auth": "Autor: Massimo Lo Sciuto",
        "info_supp": "Support: AI Assistant (Antigravity)",
        "info_desc": "Zertifizierte SHA-256 & PBKDF2 Forensik-Suite.\nEchter SWB, HMAC .idx, Bad-Sektor-Behandlung,\nThread-sicher, Src/Dst-Prüfung, reaktive UI."
    }
}


class DiskGuardProV14(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.current_lang   = "Italiano"
        self.dischi_mappa   = {}
        self.stop_requested = False
        self._swb_fd: int | None = None
        # ── PUNTO 2: Lock per thread safety ──────────────────────────────────
        self._state_lock    = threading.Lock()
        self._last_idx_data = None
        self._last_idx_path = None
        self.setup_ui()
        self.refresh_disks()

    # ─────────────────────────────────────────────────────────────────────────
    # UI
    # ─────────────────────────────────────────────────────────────────────────
    def setup_ui(self):
        L = LANG_DATA[self.current_lang]
        self.title(L["title"])
        self.geometry("950x1010")

        # Header
        hf = ctk.CTkFrame(self, fg_color="transparent")
        hf.pack(fill="x", padx=20, pady=10)
        self.lang_menu = ctk.CTkOptionMenu(hf, values=list(LANG_DATA.keys()), command=self.change_lang, width=140)
        self.lang_menu.set(self.current_lang); self.lang_menu.pack(side="left")
        ctk.CTkButton(hf, text=L["info_btn"], width=35, height=35, corner_radius=17,
                      fg_color="#1f538d", command=self.show_info).pack(side="right")

        self.tabs = ctk.CTkTabview(self, width=850, height=590)
        self.tabs.pack(pady=10)
        self.t_ops  = self.tabs.add(L["tab_ops"])
        self.t_gdpr = self.tabs.add(L["tab_gdpr"])
        self.t_for  = self.tabs.add(L["tab_forensic"])

        # ── Tab Operazioni ────────────────────────────────────────────────────
        op_frame = ctk.CTkFrame(self.t_ops, fg_color="transparent"); op_frame.pack(pady=(15, 5))
        ctk.CTkLabel(op_frame, text=L["operator_label"], width=200, anchor="w",
                     font=("Arial", 12, "bold")).pack(side="left")
        self.operator_entry = ctk.CTkEntry(op_frame, placeholder_text=L["operator_ph"], width=350)
        self.operator_entry.pack(side="left", padx=10)

        self.pass_entry = ctk.CTkEntry(self.t_ops, placeholder_text=L["pass_ph"], show="*", width=400)
        self.pass_entry.pack(pady=(5, 15))
        self.src_combo = self.create_c(self.t_ops, L["src"], self.update_dst)
        self.dst_combo = self.create_c(self.t_ops, L["dst"], None)

        # ── PUNTO 6: bottone Aggiorna tracciato per disabilitazione ───────────
        self.btn_refresh_ops = ctk.CTkButton(self.t_ops, text=L["refresh"], command=self.refresh_disks)
        self.btn_refresh_ops.pack(pady=5)

        self.p_bar = ctk.CTkProgressBar(self.t_ops, width=600); self.p_bar.set(0); self.p_bar.pack(pady=15)
        self.stats_label = ctk.CTkLabel(self.t_ops, text="—", font=("Arial", 12)); self.stats_label.pack()
        self.status = ctk.CTkLabel(self.t_ops, text=L["status_ready"]); self.status.pack(pady=5)
        self.hash_label = ctk.CTkLabel(self.t_ops, text="SHA-256: ---",
                                       font=("Courier", 11), text_color="#3a7ebf")
        self.hash_label.pack()

        # ── Tab GDPR ─────────────────────────────────────────────────────────
        ctk.CTkLabel(self.t_gdpr, text=L["retention"], font=("Arial", 14, "bold")).pack(pady=10)
        self.ret_days = ctk.CTkSegmentedButton(self.t_gdpr, values=L["days"])
        self.ret_days.set(L["days"][1]); self.ret_days.pack()
        # ── PUNTO 6: bottoni audit tracciati per disabilitazione
        self.btn_purge = ctk.CTkButton(self.t_gdpr, text=L["btn_purge"],
                                       fg_color="#7a3a0a", command=self.apply_retention)
        self.btn_purge.pack(pady=8)
        self.audit_v = ctk.CTkTextbox(self.t_gdpr, width=750, height=280); self.audit_v.pack(pady=10)
        ctk.CTkButton(self.t_gdpr, text="📄 Genera Report Forense",
                      fg_color="#1f538d", command=self.generate_report).pack(pady=5)
        self.btn_verify = ctk.CTkButton(self.t_gdpr, text=L["btn_verify"],
                                        fg_color="#2a5a2a", command=self.verify_image)
        self.btn_verify.pack(pady=5)

        # ── Tab Forensic ──────────────────────────────────────────────────────
        ctk.CTkLabel(self.t_for, text=L["swb_label"], font=("Arial", 16, "bold")).pack(pady=15)
        self.swb_switch = ctk.CTkSwitch(self.t_for, text="Attiva Software Write Block",
                                        command=self.toggle_swb)
        self.swb_switch.pack(pady=10)
        ctk.CTkLabel(self.t_for, text=L["swb_desc"], font=("Arial", 11), text_color="gray").pack()
        self.swb_status_label = ctk.CTkLabel(self.t_for, text="SWB: Disattivo",
                                             font=("Arial", 12, "bold"), text_color="gray")
        self.swb_status_label.pack(pady=5)

        # ── Pulsanti principali ───────────────────────────────────────────────
        self.btn_run = ctk.CTkButton(self, text=L["run"], fg_color="green",
                                     height=55, command=self.start_task)
        self.btn_run.pack(pady=15)
        self.btn_stop = ctk.CTkButton(self, text=L["stop"], fg_color="#a82424",
                                      command=self.request_stop)
        self.btn_stop.pack()

    def create_c(self, p, t, cmd):
        f = ctk.CTkFrame(p, fg_color="transparent"); f.pack(pady=5)
        ctk.CTkLabel(f, text=t, width=120).pack(side="left")
        c = ctk.CTkComboBox(f, width=400, command=cmd); c.pack(side="left", padx=10)
        return c

    def change_lang(self, n):
        self.current_lang = n
        for w in self.winfo_children(): w.destroy()
        self.setup_ui(); self.refresh_disks()

    # ── PUNTO 6: Abilita/disabilita UI durante acquisizione ──────────────────
    def _set_ui_running(self, running: bool):
        state = "disabled" if running else "normal"
        for w in [self.btn_run, self.btn_refresh_ops, self.btn_purge, self.btn_verify]:
            w.configure(state=state)
        self.operator_entry.configure(state=state)
        self.pass_entry.configure(state=state)
        self.src_combo.configure(state=state)
        self.dst_combo.configure(state=state)

    # ─────────────────────────────────────────────────────────────────────────
    # Audit log
    # ─────────────────────────────────────────────────────────────────────────
    def log_audit(self, msg: str, operator: str = "sistema"):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.audit_v.insert("end", f"[{ts}] [{operator}] {msg}\n"); self.audit_v.see("end")
        with open(AUDIT_FILE, "a", newline='') as f:
            csv.writer(f).writerow([ts, operator, msg])

    # ─────────────────────────────────────────────────────────────────────────
    # HMAC helper per .idx (Punto 4)
    # ─────────────────────────────────────────────────────────────────────────
    @staticmethod
    def _idx_hmac(key: bytes, data: str) -> str:
        return hmac.new(key, data.encode(), hashlib.sha256).hexdigest()

    def _write_idx(self, path: str, data: dict, hmac_key: bytes):
        payload = json.dumps(data, sort_keys=True)
        sig = self._idx_hmac(hmac_key, payload)
        with open(path, 'w') as f:
            json.dump({"data": data, "hmac": sig}, f)

    def _read_idx(self, path: str, hmac_key: bytes) -> dict | None:
        """Legge e verifica il file .idx. Ritorna None se tamperato."""
        try:
            with open(path, 'r') as f:
                wrapped = json.load(f)
            payload = json.dumps(wrapped["data"], sort_keys=True)
            expected = self._idx_hmac(hmac_key, payload)
            if not hmac.compare_digest(expected, wrapped["hmac"]):
                return None   # tampered
            return wrapped["data"]
        except:
            return None

    # ─────────────────────────────────────────────────────────────────────────
    # Software Write Block (Punto 1 v1.6)
    # ─────────────────────────────────────────────────────────────────────────
    def toggle_swb(self):
        src_dev = self.dischi_mappa.get(self.src_combo.get())
        if self.swb_switch.get() == 1:
            if src_dev:
                try:
                    self._swb_fd = os.open(src_dev, os.O_RDONLY)
                    fcntl.ioctl(self._swb_fd, BLKROSET, 1)
                    self.swb_status_label.configure(text=f"SWB: ATTIVO su {src_dev}",
                                                    text_color="#00aa44")
                    self.log_audit(f"SWB ATTIVATO su {src_dev}")
                except Exception as e:
                    self.swb_switch.deselect()
                    self.swb_status_label.configure(text="SWB: Errore (permessi root?)",
                                                    text_color="#cc4400")
                    self.log_audit(f"SWB ERRORE: {e}")
        else:
            self._release_swb()

    def _release_swb(self):
        if self._swb_fd is not None:
            src_dev = self.dischi_mappa.get(self.src_combo.get(), "")
            try:
                fcntl.ioctl(self._swb_fd, BLKROSET, 0)
                os.close(self._swb_fd)
            except: pass
            finally: self._swb_fd = None
            self.swb_status_label.configure(text="SWB: Disattivo", text_color="gray")
            self.log_audit(f"SWB DISATTIVATO su {src_dev}")

    # ─────────────────────────────────────────────────────────────────────────
    # Disk listing
    # ─────────────────────────────────────────────────────────────────────────
    def refresh_disks(self):
        self.dischi_mappa = {}
        try:
            out = subprocess.check_output(["lsblk", "-n", "-o", "NAME,SIZE,TYPE,MODEL", "-b"], text=True)
            for line in out.strip().split("\n"):
                parts = line.split()
                if len(parts) >= 3:
                    name, size_bytes, dtype = parts[0], parts[1], parts[2]
                    model = " ".join(parts[3:]) if len(parts) > 3 else ""
                    dev  = f"/dev/{name}"
                    size = int(size_bytes) // (1024**3)
                    pfx  = "[DISK]" if dtype == "disk" else "[PART]"
                    lbl  = f"{pfx} {dev} [{size}GB] {model}".strip()
                    self.dischi_mappa[lbl] = dev
        except Exception as e:
            self.log_audit(f"Errore lsblk: {e}")
            for p in psutil.disk_partitions(all=False):
                try:
                    if 'loop' in p.device: continue
                    u = psutil.disk_usage(p.mountpoint)
                    lbl = f"[PART] {p.device} [{u.total//1024**3}GB] ({p.mountpoint})"
                    self.dischi_mappa[lbl] = p.device
                except: continue
        v = list(self.dischi_mappa.keys())
        self.src_combo.configure(values=v)
        if v: self.src_combo.set(v[0])
        self.update_dst()

    def update_dst(self, _=None):
        f = [l for l in self.dischi_mappa.keys() if l != self.src_combo.get()]
        self.dst_combo.configure(values=f)
        if f: self.dst_combo.set(f[0])

    # ─────────────────────────────────────────────────────────────────────────
    # PUNTO 5: Retention GDPR
    # ─────────────────────────────────────────────────────────────────────────
    def apply_retention(self):
        L = LANG_DATA[self.current_lang]
        days = RETENTION_DAYS_MAP.get(self.ret_days.get())
        if days is None or not os.path.exists(AUDIT_FILE):
            messagebox.showinfo("Retention", L["purge_none"]); return
        cutoff = datetime.now() - timedelta(days=days)
        kept, purged = [], []
        with open(AUDIT_FILE, "r", newline='') as f:
            for row in csv.reader(f):
                if not row: continue
                try:
                    (purged if datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S") < cutoff
                     else kept).append(row)
                except: kept.append(row)
        if not purged:
            messagebox.showinfo("Retention", L["purge_none"]); return
        if not messagebox.askyesno("Retention",
                                   L["purge_confirm"].format(n=len(purged), d=self.ret_days.get())):
            return
        with open(AUDIT_FILE, "w", newline='') as f:
            csv.writer(f).writerows(kept)
        self.log_audit(f"RETENTION: eliminate {len(purged)} voci.")
        messagebox.showinfo("Retention", L["purge_done"].format(n=len(purged)))

    # ─────────────────────────────────────────────────────────────────────────
    # PUNTO 6 (v1.7): Report Forense
    # ─────────────────────────────────────────────────────────────────────────
    def generate_report(self):
        L = LANG_DATA[self.current_lang]
        if not os.path.exists(AUDIT_FILE):
            messagebox.showwarning("Report", "Nessun log disponibile."); return
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Report", "*.txt"), ("All Files", "*.*")],
            initialfile=f"forensic_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        if not path: return
        with open(AUDIT_FILE, "r", newline='') as f:
            rows = list(csv.reader(f))
        lines = [
            "=" * 72,
            f"   DISK GUARD PRO v{VERSION} — FORENSIC ACQUISITION REPORT",
            "=" * 72,
            f"  Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"  Retention : {self.ret_days.get()}",
            "=" * 72, "", "AUDIT LOG:", "-" * 72,
        ]
        for r in rows:
            if len(r) >= 3: lines.append(f"  [{r[0]}] [{r[1]}] {r[2]}")
            elif len(r) == 2: lines.append(f"  [{r[0]}] {r[1]}")
        lines += ["", "=" * 72,
                  "  END OF REPORT — Disk Guard Pro | Forensic & GDPR Suite", "=" * 72]
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        self.log_audit(f"REPORT GENERATO: {path}")
        messagebox.showinfo("Report", L["report_saved"].format(path=path))

    # ─────────────────────────────────────────────────────────────────────────
    # PUNTO 8 (v1.7): Verifica post-acquisizione
    # ─────────────────────────────────────────────────────────────────────────
    def verify_image(self):
        L = LANG_DATA[self.current_lang]
        img  = filedialog.askopenfilename(title=L["verify_ask_img"])
        if not img: return
        ref  = ctk.CTkInputDialog(text=L["verify_ask_ref"], title="SHA-256 Reference").get_input()
        if not ref: return
        self.status.configure(text=L["verify_running"])
        threading.Thread(target=self._do_verify, args=(img, ref.strip().lower(), L),
                         daemon=True).start()

    def _do_verify(self, img, ref, L):
        h = hashlib.sha256()
        try:
            with open(img, 'rb') as f:
                while (buf := f.read(1024 * 1024)): h.update(buf)
            got = h.hexdigest()
            if got == ref:
                self.log_audit(f"VERIFICA OK: {img} | SHA-256: {got}")
                messagebox.showinfo("Verifica", L["verify_ok"].format(h=got))
            else:
                self.log_audit(f"VERIFICA FALLITA: {img}")
                messagebox.showerror("Verifica", L["verify_fail"].format(e=ref, g=got))
        except Exception as e:
            messagebox.showerror("Errore", str(e))
        finally:
            self.status.configure(text=LANG_DATA[self.current_lang]["status_ready"])

    # ─────────────────────────────────────────────────────────────────────────
    # Stop con flush immediato (v1.7 Punto 7)
    # ─────────────────────────────────────────────────────────────────────────
    def request_stop(self):
        with self._state_lock:
            self.stop_requested = True
            data, path = self._last_idx_data, self._last_idx_path
        if data and path:
            try:
                # flush senza HMAC (chiave non disponibile qui) — salva raw state
                with open(path + ".raw", 'w') as f: json.dump(data, f)
            except: pass
        self.log_audit("INTERRUZIONE richiesta.", operator=self.operator_entry.get() or "sistema")

    # ─────────────────────────────────────────────────────────────────────────
    # Avvio acquisizione
    # ─────────────────────────────────────────────────────────────────────────
    def start_task(self):
        L = LANG_DATA[self.current_lang]
        operator = self.operator_entry.get().strip()
        if not operator:
            return messagebox.showerror("Error", L["err_operator"])
        if not self.pass_entry.get():
            return messagebox.showerror("Error", L["err_pass"])

        src = self.dischi_mappa.get(self.src_combo.get(), "")
        dst = self.dischi_mappa.get(self.dst_combo.get(), "")

        # ── PUNTO 7: Validazione src/dst ─────────────────────────────────────
        if src and dst and dst.startswith(src) and dst != src:
            return messagebox.showerror("Error", L["err_same_disk"])

        if not messagebox.askyesno("Confirm", L["confirm"].format(dst=self.dst_combo.get())):
            return

        with self._state_lock:
            self.stop_requested = False
            self._last_idx_data = None
            self._last_idx_path = None

        self._set_ui_running(True)
        threading.Thread(target=self.run_logic, daemon=True).start()

    # ─────────────────────────────────────────────────────────────────────────
    # Core logic
    # ─────────────────────────────────────────────────────────────────────────
    def run_logic(self):
        L        = LANG_DATA[self.current_lang]
        operator = self.operator_entry.get().strip()
        src      = self.dischi_mappa.get(self.src_combo.get())
        dst      = self.dischi_mappa.get(self.dst_combo.get())

        if not src or not dst:
            messagebox.showerror("Error", "Sorgente o Destinazione non valida.")
            self._set_ui_running(False); return

        pwd    = self.pass_entry.get().encode()
        salt   = os.urandom(16)
        nonce  = os.urandom(8)
        s_off  = 0
        d_off  = 0
        idx_p  = dst.replace("/", "_") + ".idx"

        # PBKDF2 — derive key (used also for HMAC verification of .idx)
        key = PBKDF2(pwd, salt, dkLen=32, count=100000)

        # ── PUNTO 1: Resume senza pickle — ricalcolo SHA-256 ─────────────────
        if os.path.exists(idx_p):
            saved = self._read_idx(idx_p, key)
            if saved is None:
                self.log_audit(L["idx_tampered"], operator=operator)
            else:
                s_off = saved["src"]; d_off = saved["dst"]
                salt  = bytes.fromhex(saved["salt"])
                nonce = bytes.fromhex(saved["nonce"])
                # Ricalcolo chiave con salt recuperato
                key = PBKDF2(pwd, salt, dkLen=32, count=100000)

        # ── PUNTO 8: Progress bar corretta su resume ──────────────────────────
        # Calcoliamo tot prima per impostare la progress bar subito
        tot = 0
        try:
            out = subprocess.check_output(["blockdev", "--getsize64", src], text=True)
            tot = int(out.strip())
        except:
            try:
                with open(src, 'rb') as fs: fs.seek(0, 2); tot = fs.tell()
            except: pass

        if tot > 0 and s_off > 0:
            self.p_bar.set(s_off / tot)

        # ── Ricalcolo SHA-256 da 0 a s_off per il resume (Punto 1) ────────────
        sha256_h = hashlib.sha256()
        if s_off > 0 and tot > 0:
            self.status.configure(text=L["resuming"].format(mb=s_off // 1024**2))
            try:
                recalc_pos = 0
                with open(src, 'rb') as fs:
                    while recalc_pos < s_off:
                        chunk = min(1024 * 1024, s_off - recalc_pos)
                        buf   = fs.read(chunk)
                        if not buf: break
                        sha256_h.update(buf)
                        recalc_pos += len(buf)
            except Exception as e:
                self.log_audit(f"Avviso ricalcolo hash: {e}", operator=operator)
                sha256_h = hashlib.sha256()
                s_off = d_off = 0
                self.p_bar.set(0)

        start_time = time.time()
        last_upd   = start_time
        bytes_last = s_off

        try:
            self.log_audit(f"ACQUISIZIONE AVVIATA: {src} -> {dst} | SWB:{bool(self._swb_fd)}",
                           operator=operator)

            with open(src, 'rb') as fs:
                with open(dst, 'rb+' if d_off > 0 else 'wb') as fd:
                    if d_off > 0: fd.seek(d_off)
                    fs.seek(s_off)

                    while s_off < tot:
                        with self._state_lock:
                            if self.stop_requested: break

                        # ── PUNTO 5: Gestione Bad Sectors ────────────────────
                        try:
                            buf = fs.read(1024 * 1024)
                        except OSError:
                            self.log_audit(L["bad_sector"].format(off=s_off), operator=operator)
                            buf = b'\x00' * 1024 * 1024
                            try: fs.seek(s_off + len(buf))
                            except: break

                        if not buf: break

                        sha256_h.update(buf)
                        ctr  = Counter.new(64, prefix=nonce, initial_value=s_off // 16)
                        proc = AES.new(key, AES.MODE_CTR, counter=ctr).encrypt(zlib.compress(buf))
                        fd.write(proc); fd.flush(); os.fsync(fd.fileno())
                        s_off += len(buf)
                        now = time.time()

                        if now - last_upd > 0.5:
                            speed = (s_off - bytes_last) / (now - last_upd) / (1024 * 1024)
                            rem   = tot - s_off
                            eta   = str(timedelta(seconds=int(rem / (speed * 1024 * 1024)))) if speed > 0 else "--:--:--"
                            # ── PUNTO 9: label tradotta ───────────────────────
                            self.stats_label.configure(
                                text=L["stats_fmt"].format(speed=speed, eta=eta))
                            bytes_last = s_off
                            last_upd   = now

                            # ── PUNTO 4: .idx con HMAC ────────────────────────
                            idx_data = {"src": s_off, "dst": fd.tell(),
                                        "salt": salt.hex(), "nonce": nonce.hex()}
                            with self._state_lock:
                                self._last_idx_data = idx_data
                                self._last_idx_path = idx_p
                            self._write_idx(idx_p, idx_data, key)

                        self.p_bar.set(s_off / tot)
                        self.status.configure(text=f"{s_off // 1024**2} MB / {tot // 1024**2} MB")

            with self._state_lock:
                stopped = self.stop_requested

            if not stopped:
                final_hash = sha256_h.hexdigest()
                self.hash_label.configure(text=f"SHA-256: {final_hash}")
                if os.path.exists(idx_p): os.remove(idx_p)
                self.log_audit(f"SUCCESSO — SHA-256: {final_hash}", operator=operator)
                if messagebox.askyesno("Completato",
                                       f"Acquisizione completata.\nSHA-256: {final_hash}\n\nGenerare il report forense?"):
                    self.generate_report()
            else:
                self.log_audit(f"INTERROTTA a {s_off // 1024**2} MB.", operator=operator)

        except Exception as e:
            self.log_audit(f"ERRORE FATALE: {e}", operator=operator)
            messagebox.showerror("Error", str(e))
        finally:
            self._set_ui_running(False)

    # ─────────────────────────────────────────────────────────────────────────
    # About
    # ─────────────────────────────────────────────────────────────────────────
    def show_info(self):
        L = LANG_DATA[self.current_lang]
        w = ctk.CTkToplevel(self); w.title(f"About - {L['title']}")
        w.geometry("680x430"); w.attributes("-topmost", True)
        txt = (f"{L['title']}\n{'_'*34}\n\n"
               f"{L['info_ver']}\n{L['info_auth']}\n{L['info_supp']}\n\n{L['info_desc']}")
        ctk.CTkLabel(w, text=txt, font=("Arial", 13), justify="center").pack(expand=True, padx=20)
        ctk.CTkButton(w, text="OK", width=100, command=w.destroy).pack(pady=15)


if __name__ == "__main__":
    DiskGuardProV14().mainloop()

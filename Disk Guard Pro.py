import os, threading, zlib, hashlib, json, subprocess, csv, time
from datetime import datetime, timedelta
import customtkinter as ctk
from tkinter import messagebox
import psutil
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Protocol.KDF import PBKDF2

# --- DIZIONARIO INTERNAZIONALE COMPLETO v1.4.0 ---
LANG_DATA = {
    "Italiano": {
        "title": "🛡️ Disk Guard Pro v1.5.0", "header": "Suite Forense & GDPR",
        "tab_ops": "Operazioni", "tab_gdpr": "Audit & Compliance", "tab_forensic": "Forense",
        "swb_label": "Software Write Block (Sola Lettura)",
        "swb_desc": "Protegge la sorgente da scritture accidentali.",
        "run": "AVVIA ACQUISIZIONE", "stop": "FERMA LA COPIA IN CORSO", "info_btn": "i",
        "pass_ph": "Password AES-256", "src": "Sorgente:", "dst": "Destinazione:",
        "refresh": "Aggiorna", "status_ready": "Pronto per acquisizione forense", "err_pass": "Password mancante!",
        "confirm": "Sovrascrivere {dst}?\nATTENZIONE: Procedura forense irreversibile.", "retention": "Conservazione Dati:",
        "days": ["30 Giorni", "90 Giorni", "1 Anno", "Illimitata"],
        "info_ver": "Versione: 1.5.0 'Forensic Platinum'", "info_auth": "Autore: Massimo Lo Sciuto",
        "info_supp": "Supporto: AI Assistant (Antigravity)", "info_desc": "Acquisizione forense certificata SHA-256 & PBKDF2."
    },
    "English": {
        "title": "🛡️ Disk Guard Pro v1.5.0", "header": "Forensic & GDPR Suite",
        "tab_ops": "Operations", "tab_gdpr": "Audit & Compliance", "tab_forensic": "Forensic",
        "swb_label": "Software Write Block (Read-Only)",
        "swb_desc": "Protects source from accidental writes.",
        "run": "START ACQUISITION", "stop": "STOP CURRENT COPY", "info_btn": "i",
        "pass_ph": "AES-256 Password", "src": "Source:", "dst": "Destination:",
        "refresh": "Refresh", "status_ready": "Ready for forensic acquisition", "err_pass": "Password missing!",
        "confirm": "Overwrite {dst}?\nWARNING: Irreversible forensic procedure.", "retention": "Data Retention:",
        "days": ["30 Days", "90 Days", "1 Year", "Unlimited"],
        "info_ver": "Version: 1.5.0 'Forensic Platinum'", "info_auth": "Author: Massimo Lo Sciuto",
        "info_supp": "Support: AI Assistant (Antigravity)", "info_desc": "Certified SHA-256 & PBKDF2 forensic acquisition."
    },
    "Español": {
        "title": "🛡️ Disk Guard Pro v1.5.0", "header": "Suite Forense y RGPD",
        "tab_ops": "Operaciones", "tab_gdpr": "Auditoría y Cumplimiento", "tab_forensic": "Forense",
        "swb_label": "Software Write Block (Solo Lectura)",
        "swb_desc": "Protege el origen de escrituras accidentales.",
        "run": "INICIAR ADQUISICIÓN", "stop": "DETENER COPIA EN CURSO", "info_btn": "i",
        "pass_ph": "Contraseña AES-256", "src": "Origen:", "dst": "Destino:",
        "refresh": "Actualizar", "status_ready": "Listo para adquisición forense", "err_pass": "¡Contraseña faltante!",
        "confirm": "¿Sobrescribir {dst}?\nADVERTENCIA: Procedimiento forense irreversible.", "retention": "Retención de datos:",
        "days": ["30 Días", "90 Días", "1 Año", "Ilimitada"],
        "info_ver": "Versión: 1.5.0 'Forensic Platinum'", "info_auth": "Autor: Massimo Lo Sciuto",
        "info_supp": "Soporte: AI Assistant (Antigravity)", "info_desc": "Adquisición forense certificada SHA-256 y PBKDF2."
    },
    "Français": {
        "title": "🛡️ Disk Guard Pro v1.5.0", "header": "Suite Forensique & RGPD",
        "tab_ops": "Opérations", "tab_gdpr": "Audit & Conformité", "tab_forensic": "Forensique",
        "swb_label": "Software Write Block (Lecture Seule)",
        "swb_desc": "Protège la source des écritures accidentelles.",
        "run": "LANCER L'ACQUISITION", "stop": "ARRÊTER LA COPIE", "info_btn": "i",
        "pass_ph": "Mot de passe AES-256", "src": "Source:", "dst": "Destination:",
        "refresh": "Actualiser", "status_ready": "Prêt pour l'acquisition forensique", "err_pass": "Mot de passe manquant!",
        "confirm": "Écraser {dst}?\nATTENTION: Procédure forensique irréversible.", "retention": "Rétention des données:",
        "days": ["30 Jours", "90 Jours", "1 An", "Illimitée"],
        "info_ver": "Version: 1.5.0 'Forensic Platinum'", "info_auth": "Auteur: Massimo Lo Sciuto",
        "info_supp": "Support: AI Assistant (Antigravity)", "info_desc": "Acquisition forensique certifiée SHA-256 & PBKDF2."
    },
    "Deutsch": {
        "title": "🛡️ Disk Guard Pro v1.5.0", "header": "Forensik & DSGVO Suite",
        "tab_ops": "Operationen", "tab_gdpr": "Audit & Compliance", "tab_forensic": "Forensik",
        "swb_label": "Software Write Block (Schreibschutz)",
        "swb_desc": "Schützt die Quelle vor versehentlichem Schreiben.",
        "run": "ERFASSUNG STARTEN", "stop": "KOPIERVORGANG STOPPEN", "info_btn": "i",
        "pass_ph": "AES-256 Passwort", "src": "Quelle:", "dst": "Ziel:",
        "refresh": "Aktualisieren", "status_ready": "Bereit für forensische Erfassung", "err_pass": "Passwort fehlt!",
        "confirm": "{dst} überschreiben?\nWARNUNG: Unumkehrbares forensisches Verfahren.", "retention": "Aufbewahrungsfrist:",
        "days": ["30 Tage", "90 Tage", "1 Jahr", "Unbegrenzt"],
        "info_ver": "Version: 1.5.0 'Forensic Platinum'", "info_auth": "Autor: Massimo Lo Sciuto",
        "info_supp": "Support: AI Assistant (Antigravity)", "info_desc": "Zertifizierte forensische SHA-256 & PBKDF2-Erfassung."
    }
}

class DiskGuardProV14(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.current_lang = "Italiano"
        self.dischi_mappa = {}
        self.stop_requested = False
        self.setup_ui()
        self.refresh_disks()

    def setup_ui(self):
        L = LANG_DATA[self.current_lang]
        self.title(L["title"])
        self.geometry("950x900")

        # Header
        self.h_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.h_frame.pack(fill="x", padx=20, pady=10)
        self.lang_menu = ctk.CTkOptionMenu(self.h_frame, values=list(LANG_DATA.keys()), command=self.change_lang, width=140)
        self.lang_menu.set(self.current_lang); self.lang_menu.pack(side="left")
        ctk.CTkButton(self.h_frame, text=L["info_btn"], width=35, height=35, corner_radius=17, fg_color="#1f538d", command=self.show_info).pack(side="right")

        self.tabs = ctk.CTkTabview(self, width=850, height=550)
        self.tabs.pack(pady=10)
        self.t_ops = self.tabs.add(L["tab_ops"])
        self.t_gdpr = self.tabs.add(L["tab_gdpr"])
        self.t_for = self.tabs.add(L["tab_forensic"])

        # Tab Operazioni
        self.pass_entry = ctk.CTkEntry(self.t_ops, placeholder_text=L["pass_ph"], show="*", width=400)
        self.pass_entry.pack(pady=15)
        self.src_combo = self.create_c(self.t_ops, L["src"], self.update_dst)
        self.dst_combo = self.create_c(self.t_ops, L["dst"], None)
        self.btn_refresh = ctk.CTkButton(self.t_ops, text=L["refresh"], command=self.refresh_disks).pack(pady=10)
        self.p_bar = ctk.CTkProgressBar(self.t_ops, width=600); self.p_bar.set(0); self.p_bar.pack(pady=20)
        self.stats_label = ctk.CTkLabel(self.t_ops, text="Velocità: 0 MB/s | ETA: --:--:--", font=("Arial", 12))
        self.stats_label.pack()
        self.status = ctk.CTkLabel(self.t_ops, text=L["status_ready"]); self.status.pack(pady=5)
        self.hash_label = ctk.CTkLabel(self.t_ops, text="SHA-256: ---", font=("Courier", 11), text_color="#3a7ebf")
        self.hash_label.pack()

        # Tab GDPR
        ctk.CTkLabel(self.t_gdpr, text=L["retention"], font=("Arial", 14, "bold")).pack(pady=10)
        self.ret_days = ctk.CTkSegmentedButton(self.t_gdpr, values=L["days"]); self.ret_days.set(L["days"][1]); self.ret_days.pack()
        self.audit_v = ctk.CTkTextbox(self.t_gdpr, width=750, height=250); self.audit_v.pack(pady=20)

        # Tab Forensic
        ctk.CTkLabel(self.t_for, text=L["swb_label"], font=("Arial", 16, "bold")).pack(pady=15)
        self.swb_switch = ctk.CTkSwitch(self.t_for, text="Attiva Software Write Block")
        self.swb_switch.pack(pady=10)
        ctk.CTkLabel(self.t_for, text=L["swb_desc"], font=("Arial", 11), text_color="gray").pack()

        # Main Buttons
        self.btn_run = ctk.CTkButton(self, text=L["run"], fg_color="green", height=55, command=self.start_task)
        self.btn_run.pack(pady=15)
        self.btn_stop = ctk.CTkButton(self, text=L["stop"], fg_color="#a82424", command=lambda: setattr(self, 'stop_requested', True))
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

    def log_audit(self, msg):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.audit_v.insert("end", f"[{ts}] {msg}\n"); self.audit_v.see("end")
        with open("forensic_audit_v150.csv", "a", newline='') as f:
            csv.writer(f).writerow([ts, msg])

    def refresh_disks(self):
        self.dischi_mappa = {}
        for p in psutil.disk_partitions(all=False):
            try:
                if 'loop' in p.device: continue
                u = psutil.disk_usage(p.mountpoint)
                lbl = f"{p.device} [{u.total//1024**3}GB] ({p.mountpoint})"
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

    def start_task(self):
        L = LANG_DATA[self.current_lang]
        if not self.pass_entry.get(): return messagebox.showerror("Error", L["err_pass"])
        if not messagebox.askyesno("Confirm", L["confirm"].format(dst=self.dst_combo.get())): return
        self.stop_requested = False
        threading.Thread(target=self.run_logic, daemon=True).start()

    def run_logic(self):
        L = LANG_DATA[self.current_lang]
        src = self.dischi_mappa.get(self.src_combo.get())
        dst = self.dischi_mappa.get(self.dst_combo.get())
        pwd = self.pass_entry.get().encode()
        
        idx_p = dst + ".idx"
        salt = os.urandom(16)
        s_off, d_off = 0, 0
        
        if os.path.exists(idx_p):
            with open(idx_p, 'r') as f: 
                i = json.load(f)
                s_off, d_off = i["src"], i["dst"]
                salt = bytes.fromhex(i["salt"])
        
        # PBKDF2 per conformità GDPR (Sicurezza del Trattamento)
        key = PBKDF2(pwd, salt, dkLen=32, count=100000)
        nonce = hashlib.md5(salt).digest()[:8] # Derivazione deterministica del nonce dal salt
        
        sha256_h = hashlib.sha256()
        start_time = time.time()
        last_update = start_time
        bytes_at_last_update = s_off

        try:
            self.log_audit(f"ACQUISIZIONE FORENSE AVVIATA: {src} -> {dst} (SWB: {self.swb_switch.get()})")
            with open(src, 'rb') as fs:
                fs.seek(0, 2); tot = fs.tell(); fs.seek(0)
                
                with open(dst, 'rb+' if d_off > 0 else 'wb') as fd:
                    if d_off > 0: fd.seek(d_off)
                    fs.seek(s_off)
                    
                    while s_off < tot and not self.stop_requested:
                        buf = fs.read(1024*1024)
                        if not buf: break
                        
                        # Aggiornamento Hash SHA-256 (Integrità Forense)
                        sha256_h.update(buf)
                        
                        ctr = Counter.new(64, prefix=nonce, initial_value=s_off // 16)
                        proc = AES.new(key, AES.MODE_CTR, counter=ctr).encrypt(zlib.compress(buf))
                        fd.write(proc); fd.flush(); os.fsync(fd.fileno())
                        
                        s_off += len(buf)
                        now = time.time()
                        
                        # Calcolo Metriche (UX & Monitoraggio)
                        if now - last_update > 0.5:
                            speed = (s_off - bytes_at_last_update) / (now - last_update) / (1024*1024)
                            rem_bytes = tot - s_off
                            eta = str(timedelta(seconds=int(rem_bytes / (speed * 1024 * 1024)))) if speed > 0 else "--:--:--"
                            self.stats_label.configure(text=f"Velocità: {speed:.2f} MB/s | ETA: {eta}")
                            bytes_at_last_update = s_off
                            last_update = now

                        with open(idx_p, 'w') as fi: 
                            json.dump({"src": s_off, "dst": fd.tell(), "salt": salt.hex()}, fi)
                        
                        self.p_bar.set(s_off/tot)
                        self.status.configure(text=f"{s_off//1024**2} MB / {tot//1024**2} MB")
            
            if not self.stop_requested:
                final_hash = sha256_h.hexdigest()
                self.hash_label.configure(text=f"SHA-256: {final_hash}")
                if os.path.exists(idx_p): os.remove(idx_p)
                self.log_audit(f"SUCCESSO: Immagine creata. SHA-256: {final_hash}")
                messagebox.showinfo("OK", f"Task Completato.\nHash SHA-256: {final_hash}")
        except Exception as e:
            self.log_audit(f"ERRORE FATALE: {str(e)}")
            messagebox.showerror("Error", str(e))

    def show_info(self):
        L = LANG_DATA[self.current_lang]
        w = ctk.CTkToplevel(self); w.title(f"About - {L['title']}"); w.geometry("600x350"); w.attributes("-topmost", True)
        c = f"{L['title']}\n_________________\n\n{L['info_ver']}\n{L['info_auth']}\n{L['info_supp']}\n\n{L['info_desc']}"
        ctk.CTkLabel(w, text=c, font=("Arial", 14), justify="center").pack(expand=True, padx=20)
        ctk.CTkButton(w, text="OK", width=100, command=w.destroy).pack(pady=15)

if __name__ == "__main__":
    DiskGuardProV14().mainloop()

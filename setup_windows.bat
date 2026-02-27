@echo off
echo --- Installazione Disk Guard Pro v1.4.0 ---
python -m venv venv
call venv\Scripts\activate
pip install customtkinter pycryptodome psutil paramiko
echo ------------------------------------------------
echo Installazione completata.
echo Per avviare: venv\Scripts\python.exe disk_guard_pro_v140.py
pause


#!/bin/bash
echo "--- Installazione Disk Guard Pro v1.5.0 Platinum ---"
sudo apt update && sudo apt install -y python3-tk python3-pip python3-venv

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo "------------------------------------------------"
echo "Installazione completata."
echo "Per avviare il programma usa: sudo ./venv/bin/python3 \"Disk Guard Pro.py\""

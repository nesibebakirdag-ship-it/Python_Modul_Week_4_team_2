#!/bin/bash

# 1️⃣ Proje root'a git
cd /c/Users/tevfi/OneDrive/Masaüstü/cmr || exit

# 2️⃣ FastAPI server'ı background'da başlat
echo "Starting FastAPI server..."
nohup python -m uvicorn API.LoginApi:app --reload > server.log 2>&1 &

# 3️⃣ Server'ın açılmasını biraz bekle
sleep 3

# 4️⃣ PyQt GUI scriptini çalıştır
echo "Starting PyQt application..."
python main.py

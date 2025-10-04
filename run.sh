#!/bin/bash

# 1️⃣ Proje root klasörüne git
cd "$(dirname "$0")/API" || exit

# 2️⃣ FastAPI server'ı arka planda başlat
# Windows için start kullanıyoruz
echo "Starting FastAPI server..."
start "" python -m uvicorn API.LoginApi:app --reload

# 3️⃣ Server'ın açılmasını biraz bekle
sleep 3

# 4️⃣ PyQt GUI scriptini çalıştır
# main.py dosyasının yolunu kendi projene göre düzenle
echo "Starting PyQt application..."
python main.py

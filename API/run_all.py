import subprocess

apis = [
    ("MentorApi", 8000),
    ("LoginApi", 8001),
    ("InterviewsApi", 8002)
]

processes = []

for module, port in apis:
    cmd = ["python", "-m", "uvicorn", f"{module}:app", "--reload", "--port", str(port)]
    p = subprocess.Popen(cmd)
    processes.append(p)

# Tüm süreçleri bekle
for p in processes:
    p.wait()

import gspread
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
cred_file = os.path.join(BASE_DIR, "vit8-credentials.json")
client = gspread.service_account(filename=cred_file)
sheet = client.open("Kullanicilar").get_worksheet(0)

mentorSheet = client.open("Mentor").get_worksheet(0)

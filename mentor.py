import sys
import pandas as pd
from PyQt6 import QtWidgets, uic, QtCore
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import gspread
from dotenv import load_dotenv
import os

load_dotenv()

# 🧠 Google Sheets API Servisini oluştur
def get_service():
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    creds = Credentials.from_service_account_file(os.getenv("CREDENTIALS_FILE"), scopes=scopes)
    service = build('sheets', 'v4', credentials=creds)
    return service

# 📥 Google Sheets'ten veriyi DataFrame olarak çek
def read_google_sheet():
    #client = gspread.service_account(filename=CREDENTIALS_FILE)
    #working = client.open("Mentor")
    #sayfabir = working.get_worksheet(0)
    #print(sayfabir.get_all_records())


    service = get_service()
    result = service.spreadsheets().values().get(
        spreadsheetId=os.getenv("SPREADSHEET_ID"),
        range=os.getenv("RANGE_NAME"),
    ).execute()

    values = result.get('values', [])
    if not values:
        return pd.DataFrame()
    else:
        return pd.DataFrame(values[1:], columns=values[0])  # ilk satır başlık



# 🧭 PyQt6 Arayüzü
class MyApp(QtWidgets.QMainWindow):
    
    def __init__(self,):
        super().__init__()
        uic.loadUi(r".\ui\mentor.ui", self)  # senin UI dosyanın adı

        #tableWidget ismi senin UI'daki tabloyla aynı olmalı!
        self.load_table_data()


        self.btn_search.clicked.connect(self.search_records)
        self.pushButton.clicked.connect(self.show_all_records)   # Tüm görüşmeler butonu

         # ComboBox seçim değiştiğinde filtre uygula
        self.comboBox.currentIndexChanged.connect(self.filter_by_combobox)

        self.pushButton_2.clicked.connect(self.close)  # Kapat butonu
    
    def close(self):
        QtWidgets.QApplication.instance().quit() 
    

    def load_table_data(self):
        df = read_google_sheet()
        if df.empty:
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Google Sheet'ten veri alınamadı.")
            return

        self.tableWidget.setRowCount(len(df))
        self.tableWidget.setColumnCount(len(df.columns))


        #self.tableWidget.setHorizontalHeaderLabels([str(col) for col in df.columns])
        #bu satir yuzunden df ilk satirini baslik olarak aliyor

        for row in range(len(df)):
            for col in range(len(df.columns)):
                val = str(df.iat[row, col]) if df.iat[row, col] is not None else ""
                self.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(val))
        self.df_all = df  # tüm veriyi sakla
        self.tableWidget.resizeColumnsToContents()

  # ComboBox'u doldur (6. sütun = index 5)
        self.comboBox.clear()
        unique_values = sorted(df.iloc[:, 5].dropna().unique())  
        self.comboBox.addItems(unique_values)



    def show_all_records(self):
        self.update_table(self.df_all)
   

    def search_records(self):
        #amac: eski kodda arama yaptigimizda liste guncelleniyordu ve guncellenen listesede sadece arama yaptigimiz isimler oluyordu ondan sonra baska ismi aradigimizda bulamiyorduk
        #guncelleme: isim aramayi her zaman ilk basta olusturdugumuz listeden yaptik.
        #bulunan liste: bulunan isimleri yeni bir listeye ekledik ve o listeyi tabloya aktardik
        #bunu yaparken de update_table adinda yeni bir fonksiyon olusturduk
        #yani kısaca arama yaparken hep orjinal listeyi kullanıyoruz ve bulunanları yeni listeye ekleyip tabloya aktarıyoruz
        #böylece arama yaptıktan sonra başka bir isim aradığımızda da bulabiliyoruz
       
        
        #  findData icerisinde arama sonucu bulunan veriler olacak
        findData = []
        
        #kac tane satir var listede. bunun nedenide for dongusu ile her satiri tek tek kontrol edebilmek icin
        row_count = len(self.df_all)  # satır sayısı

        # Arama metni
        search_text = self.lineEdit_search.text().lower()  # küçük harf ile arama

        for row in range(row_count):
            # 2. sütundaki değeri al (0 tabanlı indeksleme)
            val = str(self.df_all.iat[row, 2])  # 2. sütun
            # küçük harf ile karşılaştırma
            #arama metni val içinde geçiyorsa gir
            if search_text in val.lower():  # kısmi eşleşme
                # Eşleşen satırı tablo içinde seç
                self.tableWidget.selectRow(row)

                # Bulunan satırı findData listesine ekle
                findData.append([str(self.df_all.iat[row, col]) for col in range(self.df_all.shape[1])])
                print("Bulundu:", val)

        # findData liste olduğu için DataFrame'e çevirip update_table ile tabloya aktar
        self.update_table(pd.DataFrame(findData))

    
    def update_table(self,findData):
        # Tabloyu ilk baasta temizle ve yeni veriyi ekle
        #temizleme
        self.tableWidget.setRowCount(0)  # Tabloyu temizle
        #yeni veriyi ekleme
        self.tableWidget.setRowCount(len(findData))  # Yeni satır sayısını ayarla
        
        for row in range(len(findData)):
            for col in range(len(findData.columns)):
                val = str(findData.iat[row, col]) if findData.iat[row, col] is not None else ""
                self.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(val))

        # Sütun genişliklerini içeriğe göre ayarla
        self.tableWidget.resizeColumnsToContents()

    def filter_by_combobox(self):
        selected_value = self.comboBox.currentText()

        if not selected_value:
            self.update_table(self.df_all)
            return

        # 5. sütuna göre filtre uygula
        filtered_df = self.df_all[self.df_all.iloc[:, 5] == selected_value]
        self.update_table(filtered_df)




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())



# class MyWindow(QtWidgets.QMainWindow):
#     def _init_(self):
#         super(MyWindow, self)._init_()
#         uic.loadUi(r".\ui\admin.ui", self)  # .ui dosyasını yükler
#         self.pushButton.clicked.connect(self.butonTiklandi)

#     def butonTiklandi(self):
#         print("Butona tıklandı!")

# app = QtWidgets.QApplication(sys.argv)
# window = MyWindow()
# window.show()
# sys.exit(app.exec())  # PyQt6 tarzı
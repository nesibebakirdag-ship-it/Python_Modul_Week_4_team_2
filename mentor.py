import sys
from PyQt6 import QtWidgets, uic
import requests


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

    def send_request(self):
        url = "http://127.0.0.1:8000/getAllMentor"
        try:
            data = None
            resp = requests.get(url, timeout=8)
            data = resp.json()

            if resp.status_code == 200:
                return data
            else:
                print("Error:")

        except Exception as e:
                print("Error:")



    def load_table_data(self):
        
        data =  self.send_request()
      
        if not data:
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Google Sheet'ten veri alınamadı.")
            return
        self.df_all = data
        # satır ve sütun sayısı
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(data[0]))  # ilk elemandaki anahtar sayısı

        # Başlıklar
        self.tableWidget.setHorizontalHeaderLabels(list(data[0].keys()))

        # Tablonun doldurulması
        for row, row_data in enumerate(data):
            for col, key in enumerate(row_data):
                val = str(row_data[key]) if row_data[key] is not None else ""
                self.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(val))

        self.tableWidget.resizeColumnsToContents()

        # ComboBox doldurma (6. sütun = index 5)
        self.comboBox.clear()
        unique_values = sorted({row[list(row.keys())[5]] for row in data if row[list(row.keys())[5]] is not None})
        self.comboBox.addItems(unique_values)

    def show_all_records(self):
        self.update_table(self.df_all)
   
    def search_records(self):
        """
        Arama yaparken:
        - Her zaman orijinal veri listesi (self.df_all) kullanılır.
        - Bulunan sonuçlar yeni bir listeye eklenir.
        - update_table() ile tabloya aktarılır.
        """

        # Arama sonucu bulunan veriler
        findData = []

        # Arama metni
        search_text = self.lineEdit_search.text().lower()  # küçük harf ile arama

        for row_data in self.df_all:  # self.df_all artık JSON listesi
            # 3. sütundaki değer (0 tabanlı indeks: 2)
            keys = list(row_data.keys())
            val = str(row_data[keys[2]]) if keys[2] in row_data else ""

            if search_text in val.lower():  # kısmi eşleşme
                # Bulunan satırı findData listesine ekle
                findData.append(row_data)

        # findData artık JSON listesi, update_table fonksiyonunu JSON ile uyumlu hale getirmek gerekir
        self.update_table(findData)
    def update_table(self,findData):
            # Tabloyu ilk baasta temizle ve yeni veriyi ekle
            #temizleme
            self.tableWidget.setRowCount(0)  # Tabloyu temizle
            #yeni veriyi ekleme
            self.tableWidget.setRowCount(len(findData))  # Yeni satır sayısını ayarla
            
            for row, row_data in enumerate(findData):
                for col, key in enumerate(row_data):
                    val = str(row_data[key]) if row_data[key] is not None else ""
                    self.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(val))

            # Sütun genişliklerini içeriğe göre ayarla
            self.tableWidget.resizeColumnsToContents()

    def filter_by_combobox(self):
            selected_value = self.comboBox.currentText()

            if not selected_value:
                self.update_table(self.df_all)
                return

            # 5. sütuna göre filtre uygula
            # 6. sütun = index 5
            keys = list(self.df_all[0].keys())  # tüm satırlar aynı yapıda varsayılır
            column_key = keys[5]  # filtrelenecek sütun adı

            # Filtreleme
            filtered_data = [row for row in self.df_all if row.get(column_key) == selected_value]

            # Tabloyu güncelle
            self.update_table(filtered_data)




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
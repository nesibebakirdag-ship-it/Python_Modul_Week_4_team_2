import sys
import pandas as pd
from PyQt6 import QtWidgets, uic
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtGui import QTextDocument
from dotenv import load_dotenv
import os
from base_window import BaseWindow


load_dotenv()
# -------------------- Google Sheets Okuma --------------------
def get_service():
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    creds = Credentials.from_service_account_file(os.getenv("CREDENTIALS_FILE"), scopes=scopes)
    service = build('sheets', 'v4', credentials=creds)
    return service

def read_sheet(sheet_id, range_name=os.getenv("RANGE_NAME")):
    service = get_service()
    result = service.spreadsheets().values().get(
        spreadsheetId=sheet_id,
        range=range_name
    ).execute()
    values = result.get('values', [])
    if not values:
        return pd.DataFrame()
    headers = [h.strip() for h in values[0]]
    data = []
    for row in values[1:]:
        if len(row) < len(headers):
            row.extend([""] * (len(headers) - len(row)))
        elif len(row) > len(headers):
            row = row[:len(headers)]
        data.append(row)
    return pd.DataFrame(data, columns=headers)

# -------------------- PyQt6 Uygulaması --------------------
class Applications(BaseWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r".\ui\application_page.ui", self)
        self.resize(800, 600)
        self.vit1 = read_sheet(os.getenv("VIT1_SPREADSHEET_ID"))
        self.vit2 = read_sheet(os.getenv("VIT2_SPREADSHEET_ID"))

        # Başvurular verisi
        self.df = read_sheet(os.getenv("APP_SPREADSHEET_ID"))
        self.df.columns = [c.strip() for c in self.df.columns]
        self.filtered_df = self.df.copy()
        self.load_table_data(self.df)

        # Aktif filtre başlığı
        self.current_filter_title = "Tüm Başvurular"

        # ----------------- Buton Bağlantıları -----------------
        self.search_button.clicked.connect(self.search_records)
        self.all_application_button.clicked.connect(self.show_all_records)
        self.assigned_mentor_interviews_button.clicked.connect(self.show_mentor_assigned)
        self.unassigned_mentor_interviews_button.clicked.connect(self.show_mentor_unassigned)
        self.exit_button.clicked.connect(self.confirm_exit)
        self.preferences_button.clicked.connect(self.go_to_preferences)
        self.main_menu_button.clicked.connect(self.go_to_main_menu)
        self.dublicate_application_button.clicked.connect(self.show_duplicate_records)
        self.fltered_applications_button.clicked.connect(self.show_filtered_applications)
        self.prev_vit_check_button.clicked.connect(self.show_previous_vit)
        self.differen_registration_button.clicked.connect(self.show_unique_vit_records)
        self.print_buttton.clicked.connect(lambda: self.print_table(self.current_filter_title))

    # ----------------- Tabloyu Yükleme -----------------
    def load_table_data(self, df):
        self.tableWidget.setRowCount(len(df))
        self.tableWidget.setColumnCount(len(df.columns))
        self.tableWidget.setHorizontalHeaderLabels(df.columns)
        for row in range(len(df)):
            for col in range(len(df.columns)):
                item = QtWidgets.QTableWidgetItem(str(df.iat[row, col]))
                self.tableWidget.setItem(row, col, item)
        self.tableWidget.resizeColumnsToContents()

    # ----------------- Arama ve Filtreler -----------------
    def search_records(self):
        query = self.search_edit.text().strip()
        col_name = "Adınız Soyadınız"
        if query == "":
            self.filtered_df = self.df
            self.current_filter_title = "Arama: Tüm Kayıtlar"
        elif col_name in self.df.columns:
            self.filtered_df = self.df[self.df[col_name].str.lower().str.startswith(query.lower(), na=False)]
            self.current_filter_title = f"Arama: {query}"
        else:
            QtWidgets.QMessageBox.warning(self, "Error", f"Column '{col_name}' not found!")
            return
        self.load_table_data(self.filtered_df)

    def show_all_records(self):
        self.df.columns = [c.strip() for c in self.df.columns]
        if self.df.empty:
            QtWidgets.QMessageBox.warning(self, "Warning", "Google Sheet data could not be loaded.")
            return
        self.load_table_data(self.df)
        self.current_filter_title = "Tüm Başvurular"

    def show_mentor_assigned(self):
        col_name = "Mentor gorusmesi"
        if col_name in self.df.columns:
            filtered = self.df[self.df[col_name].str.strip() == "OK"]
            self.load_table_data(filtered)
            self.current_filter_title = "Mentor Görüşmesi Tanımlananlar"
        else:
            QtWidgets.QMessageBox.warning(self, "Error", f"Column '{col_name}' not found!")

    def show_mentor_unassigned(self):
        col_name = "Mentor gorusmesi"
        if col_name in self.df.columns:
            filtered = self.df[self.df[col_name].str.strip() == "ATANMADI"]
            self.load_table_data(filtered)
            self.current_filter_title = "Mentor Görüşmesi Tanımlanmayanlar"
        else:
            QtWidgets.QMessageBox.warning(self, "Error", f"Column '{col_name}' not found!")

    def show_duplicate_records(self):
        name_col = "Adınız Soyadınız"
        email_col = "Mail adresiniz"
        if name_col in self.df.columns and email_col in self.df.columns:
            duplicates = self.df[self.df.duplicated(subset=[name_col, email_col], keep=False)]
            if duplicates.empty:
                QtWidgets.QMessageBox.information(self, "Info", "No duplicate records found.")
            else:
                self.load_table_data(duplicates)
                self.current_filter_title = "Mükerrer Kayıtlar"
        else:
            QtWidgets.QMessageBox.warning(self, "Error", f"Columns '{name_col}' and/or '{email_col}' not found!")

    def show_filtered_applications(self):
        name_col = "Adınız Soyadınız"
        email_col = "Mail adresiniz"
        if name_col in self.df.columns and email_col in self.df.columns:
            filtered = self.df.drop_duplicates(subset=[name_col, email_col], keep='first')
            self.load_table_data(filtered)
            self.current_filter_title = "Filtrelenmiş Başvurular"
        else:
            QtWidgets.QMessageBox.warning(self, "Error", f"Columns '{name_col}' and/or '{email_col}' not found!")

    # ----------------- Önceki VIT -----------------
    def show_previous_vit(self):
        name_col = "Adınız Soyadınız"
        email_col = "Mail adresiniz"
        basvuru_col_candidates = [c for c in self.df.columns if 'basvuru' in c.lower() and 'donemi' in c.lower()]
        if not basvuru_col_candidates:
            QtWidgets.QMessageBox.warning(self, "Error", "Başvuru Donemi column not found!")
            return
        basvuru_col = basvuru_col_candidates[0]

        vit3_df = self.df[self.df[basvuru_col].str.strip() == "VIT3"]
        vit1_df = self.vit1
        vit2_df = self.vit2

        for df in [vit1_df, vit2_df]:
            if name_col not in df.columns or email_col not in df.columns:
                QtWidgets.QMessageBox.warning(self, "Error", f"Columns '{name_col}' or '{email_col}' not found in VIT sheet!")
                return

        common_vit1 = pd.merge(vit3_df, vit1_df, on=[name_col, email_col], how='inner')
        common_vit2 = pd.merge(vit3_df, vit2_df, on=[name_col, email_col], how='inner')
        combined_common = pd.concat([common_vit1, common_vit2]).drop_duplicates(subset=[name_col, email_col])

        if combined_common.empty:
            QtWidgets.QMessageBox.information(self, "Info", "No common candidates found in previous VITs.")
        else:
            self.load_table_data(combined_common)
            self.current_filter_title = "Önceki VIT Ortak Kayıtlar"

    # ----------------- Farklı Kayıt -----------------
    def show_unique_vit_records(self):
        name_col = "Adınız Soyadınız"
        email_col = "Mail adresiniz"
        basvuru_col_candidates = [c for c in self.df.columns if 'basvuru' in c.lower() and 'donemi' in c.lower()]
        if not basvuru_col_candidates:
            QtWidgets.QMessageBox.warning(self, "Error", "Başvuru Donemi column not found!")
            return
        basvuru_col = basvuru_col_candidates[0]

        vit3_df = self.df[self.df[basvuru_col].str.strip() == "VIT3"]
        vit1_df = self.vit1
        vit2_df = self.vit2

        merged_vit = pd.concat([vit1_df, vit2_df], ignore_index=True).drop_duplicates(subset=[name_col, email_col])
        unique_candidates = pd.merge(vit3_df, merged_vit, on=[name_col, email_col], how='left', indicator=True)
        unique_candidates = unique_candidates[unique_candidates['_merge'] == 'left_only'].drop(columns=['_merge'])

        if unique_candidates.empty:
            QtWidgets.QMessageBox.information(self, "Info", "No unique candidates found in VIT1 and VIT2.")
        else:
            self.load_table_data(unique_candidates)
            self.current_filter_title = "Farklı Kayıt"

   

    # ----------------- Yazdırma -----------------
    def print_table(self, title=""):
        html = f"<h2>{title}</h2><table border='1' cellspacing='0' cellpadding='2'>"
        html += "<tr>"
        for col in range(self.tableWidget.columnCount()):
            html += f"<th>{self.tableWidget.horizontalHeaderItem(col).text()}</th>"
        html += "</tr>"

        for row in range(self.tableWidget.rowCount()):
            html += "<tr>"
            for col in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, col)
                html += f"<td>{item.text() if item else ''}</td>"
            html += "</tr>"
        html += "</table>"

        doc = QTextDocument()
        doc.setHtml(html)
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            doc.print(printer)

# ----------------- Uygulama Başlat -----------------
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Applications()
    window.show()
    sys.exit(app.exec())

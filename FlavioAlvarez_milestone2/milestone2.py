# References video guide provided by professor. Code from milestone1 adapted to fit the requirements of milestone2.
import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt6 import uic, QtCore
from PyQt6.QtGui import QIcon, QPixmap
import psycopg2

qtCreatorFile = "milestone2.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class milestone2(QMainWindow):
    def __init__(self):
        super(milestone2, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStateList()
        self.ui.stateList.currentTextChanged.connect(self.stateChanged)
        self.ui.cityList.itemSelectionChanged.connect(self.cityChanged)
        self.ui.zipcodeList.itemSelectionChanged.connect(self.zipcodeChanged)

    def executeQuery(self,sql_str):
        try:
            conn = psycopg2.connect("dbname='yelpdb' user='postgres' host='localhost' password='XaviErni12'")
        except:
            print("Unable to connect to the database.")
        cur = conn.cursor()
        cur.execute(sql_str)
        conn.commit()
        result = cur.fetchall()
        conn.close()
        return result

    def loadStateList(self):
        self.ui.stateList.clear()
        sql_str = "SELECT DISTINCT state FROM business ORDER BY state;"
        try:
            result = self.executeQuery(sql_str)
            for row in result:
                self.ui.stateList.addItem(row[0])
        except:
            print("Query failed.")
        self.ui.stateList.setCurrentIndex(-1)
        self.ui.stateList.clearEditText()
        
    def stateChanged(self):
        self.ui.cityList.clear()

        state = self.ui.stateList.currentText()
        if (self.ui.stateList.currentIndex()>=0):
            sql_str = "SELECT DISTINCT city FROM business WHERE state='" + state +"' ORDER BY city;"
            try:
                result = self.executeQuery(sql_str)
                for row in result:
                    self.ui.cityList.addItem(row[0])
            except:
                print("Query failed.")
            
            for i in reversed(range(self.ui.businessTable.rowCount())):
                self.ui.businessTable.removeRow(i)
            sql_str = "SELECT name, city, state, postal_code FROM business WHERE state='" + state +"' ORDER BY name;"
            try:
                result = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(result[0]))
                self.ui.businessTable.setRowCount(len(result))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'City', 'State', 'Zipcode'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0, 250)
                self.ui.businessTable.setColumnWidth(1, 100)
                self.ui.businessTable.setColumnWidth(2, 50)
                self.ui.businessTable.setColumnWidth(3, 50)
                currentRowCount = 0
                for row in result:
                    for colCount in range(0, len(result[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))
                    currentRowCount += 1
            except:
                print("Query failed.")

    def cityChanged(self):
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems())>0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            sql_str = "SELECT distinct postal_code FROM business WHERE state='" + state +"' AND city ='" + city + "' ORDER BY postal_code;"
            try:
                result = self.executeQuery(sql_str)
                for row in result:
                    self.ui.zipcodeList.addItem(row[0])
            except:
                print("Query failed.")
            sql_str = "SELECT name, city, state, postal_code FROM business WHERE state='" + state +"' AND city ='" + city + "' ORDER BY name;"
            try:
                result = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(result[0]))
                self.ui.businessTable.setRowCount(len(result))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'City', 'State', 'Zipcode'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0, 250)
                self.ui.businessTable.setColumnWidth(1, 100)
                self.ui.businessTable.setColumnWidth(2, 50)
                self.ui.businessTable.setColumnWidth(3, 50)
                currentRowCount = 0
                for row in result:
                    for colCount in range(0, len(result[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))
                    currentRowCount += 1
            except:
                print("Query failed.")

    def zipcodeChanged(self):
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems())>0) and (len(self.ui.zipcodeList.selectedItems())>0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            zipcode = self.ui.zipcodeList.selectedItems()[0].text()
            sql_str = "SELECT name, city, state, postal_code FROM business WHERE state='" + state +"' AND city ='" + city + "' AND postal_code ='" + zipcode + "' ORDER BY name;"
            try:
                result = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(result[0]))
                self.ui.businessTable.setRowCount(len(result))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'City', 'State', 'Zipcode'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0, 250)
                self.ui.businessTable.setColumnWidth(1, 100)
                self.ui.businessTable.setColumnWidth(2, 50)
                self.ui.businessTable.setColumnWidth(3, 50)
                currentRowCount = 0
                for row in result:
                    for colCount in range(0, len(result[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))
                    currentRowCount += 1
            except:
                print("Query failed.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = milestone2()
    window.show()
    sys.exit(app.exec())
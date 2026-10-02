# References video guide provided by professor. Code from milestone1 adapted to fit the requirements of milestone2 and milestone3.s
# IMPORTANT NOTE: couldn't figure out how to connect to a US Census database in order to update zipcode details like in Appendix A, so I displayed total number of checkins for that zipcode intead
# Youtube demo: https://youtu.be/sEn6kGYaA74
import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt6 import uic, QtCore
from PyQt6.QtGui import QIcon, QPixmap
import psycopg2

qtCreatorFile = "milestone3.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class milestone3(QMainWindow):
    def __init__(self):
        super(milestone3, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStateList()
        self.ui.stateList.currentTextChanged.connect(self.stateChanged)
        self.ui.cityList.itemSelectionChanged.connect(self.cityChanged)
        self.ui.zipcodeList.itemSelectionChanged.connect(self.zipcodeChanged)
        self.ui.categoryList.currentTextChanged.connect(self.categoryChanged)


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
            sql_str = "SELECT name, address, city, stars, review_count, ROUND(review_rating,2), number_checkins FROM business WHERE state='" + state +"' ORDER BY name;"
            try:
                result = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(result[0]))
                self.ui.businessTable.setRowCount(len(result))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Stars', '#Review', 'Rating', '#Checkins']) # name, address, city, stars, review count, review rating, num checkins
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0, 200)
                self.ui.businessTable.setColumnWidth(1, 200)
                self.ui.businessTable.setColumnWidth(2, 100)
                self.ui.businessTable.setColumnWidth(3, 100)
                self.ui.businessTable.setColumnWidth(4, 100)
                self.ui.businessTable.setColumnWidth(5, 100)
                self.ui.businessTable.setColumnWidth(6, 100)
                currentRowCount = 0
                for row in result:
                    for colCount in range(0, len(result[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
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
            sql_str = "SELECT name, address, city, stars, review_count, ROUND(review_rating,2), number_checkins FROM business WHERE state='" + state +"' AND city ='" + city + "' ORDER BY name;"
            try:
                result = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(result[0]))
                self.ui.businessTable.setRowCount(len(result))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Stars', '#Review', 'Rating', '#Checkins']) # name, address, city, stars, review count, review rating, num checkins
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0, 200)
                self.ui.businessTable.setColumnWidth(1, 200)
                self.ui.businessTable.setColumnWidth(2, 100)
                self.ui.businessTable.setColumnWidth(3, 100)
                self.ui.businessTable.setColumnWidth(4, 100)
                self.ui.businessTable.setColumnWidth(5, 100)
                self.ui.businessTable.setColumnWidth(6, 100)
                currentRowCount = 0
                for row in result:
                    for colCount in range(0, len(result[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print("Query failed.")

    def zipcodeChanged(self):
        self.ui.numBusinessList.clear()
        self.ui.checkinsList.clear()
        
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems())>0) and (len(self.ui.zipcodeList.selectedItems())>0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            zipcode = self.ui.zipcodeList.selectedItems()[0].text()

            # update business table
            sql_str = "SELECT name, address, city, stars, review_count, ROUND(review_rating,2), number_checkins FROM business WHERE state='" + state +"' AND city ='" + city + "' AND postal_code ='" + zipcode + "' ORDER BY name;"
            try:
                result = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(result[0]))
                self.ui.businessTable.setRowCount(len(result))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Stars', '#Review', 'Rating', '#Checkins']) # name, address, city, stars, review count, review rating, num checkins
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0, 200)
                self.ui.businessTable.setColumnWidth(1, 200)
                self.ui.businessTable.setColumnWidth(2, 100)
                self.ui.businessTable.setColumnWidth(3, 100)
                self.ui.businessTable.setColumnWidth(4, 100)
                self.ui.businessTable.setColumnWidth(5, 100)
                self.ui.businessTable.setColumnWidth(6, 100)
                currentRowCount = 0
                for row in result:
                    for colCount in range(0, len(result[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print("Query failed.")
            
            #update category list
            sql_str = "SELECT DISTINCT Category.category FROM Category, Business WHERE Business.business_id = Category.business_id AND Business.postal_code ='" + zipcode + "';"
            try:
                result = self.executeQuery(sql_str)
                for row in result:
                    self.ui.categoryList.addItem(row[0])
            except:
                print("Query failed.")
            
            #update top category table
            sql_str = "SELECT COUNT(*), Category.category FROM Category, Business WHERE Business.business_id = Category.business_id AND Business.postal_code ='" + zipcode + "' GROUP BY Category.category ORDER BY COUNT(*) DESC";
            try:
                result = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.categoryTable.horizontalHeader().setStyleSheet(style)
                self.ui.categoryTable.setColumnCount(len(result[0]))
                self.ui.categoryTable.setRowCount(len(result))
                self.ui.categoryTable.setHorizontalHeaderLabels(['# of Businesses', 'Category'])
                self.ui.categoryTable.resizeColumnsToContents()
                self.ui.categoryTable.setColumnWidth(0, 150)
                self.ui.categoryTable.setColumnWidth(1, 200)
                currentRowCount = 0
                for row in result:
                    for colCount in range(0, len(result[0])):
                        self.ui.categoryTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print("Query failed.")

            #update number of businesses list
            sql_str = "SELECT COUNT(*) FROM Business WHERE postal_code ='" + zipcode + "';"
            print(sql_str)
            try:
                result = self.executeQuery(sql_str)
                for row in result:
                    self.ui.numBusinessList.addItem(str(row[0]))
            except:
                print("Query failed.")

            #update total checkins for zipcode
            sql_str = "SELECT SUM(number_checkins) FROM Business WHERE postal_code ='" + zipcode + "';"
            print(sql_str)
            try:
                result = self.executeQuery(sql_str)
                for row in result:
                    self.ui.checkinsList.addItem(str(row[0]))
            except:
                print("Query failed.")

            #update popular
            sql_str = "SELECT name, address, city, stars, review_count, ROUND(review_rating,2), number_checkins FROM business WHERE number_checkins > (SELECT AVG(number_checkins) FROM Business WHERE postal_code = '" + zipcode + "') AND state='" + state +"' AND city ='" + city + "' AND postal_code ='" + zipcode + "' ORDER BY name;"
            try:
                result = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.popularTable.horizontalHeader().setStyleSheet(style)
                self.ui.popularTable.setColumnCount(len(result[0]))
                self.ui.popularTable.setRowCount(len(result))
                self.ui.popularTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Stars', '#Review', 'Rating', '#Checkins']) # name, address, city, stars, review count, review rating, num checkins
                self.ui.popularTable.resizeColumnsToContents()
                self.ui.popularTable.setColumnWidth(0, 200)
                self.ui.popularTable.setColumnWidth(1, 200)
                self.ui.popularTable.setColumnWidth(2, 100)
                self.ui.popularTable.setColumnWidth(3, 100)
                self.ui.popularTable.setColumnWidth(4, 100)
                self.ui.popularTable.setColumnWidth(5, 100)
                self.ui.popularTable.setColumnWidth(6, 100)
                currentRowCount = 0
                for row in result:
                    for colCount in range(0, len(result[0])):
                        self.ui.popularTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print("Query failed.")

            #update successful
            sql_str = "SELECT name, address, city, stars, review_count, ROUND(review_rating,2), number_checkins FROM business WHERE review_rating >= 4.0 AND state='" + state +"' AND city ='" + city + "' AND postal_code ='" + zipcode + "' ORDER BY name;"
            try:
                result = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.successfulTable.horizontalHeader().setStyleSheet(style)
                self.ui.successfulTable.setColumnCount(len(result[0]))
                self.ui.successfulTable.setRowCount(len(result))
                self.ui.successfulTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Stars', '#Review', 'Rating', '#Checkins']) # name, address, city, stars, review count, review rating, num checkins
                self.ui.successfulTable.resizeColumnsToContents()
                self.ui.successfulTable.setColumnWidth(0, 200)
                self.ui.successfulTable.setColumnWidth(1, 200)
                self.ui.successfulTable.setColumnWidth(2, 100)
                self.ui.successfulTable.setColumnWidth(3, 100)
                self.ui.successfulTable.setColumnWidth(4, 100)
                self.ui.successfulTable.setColumnWidth(5, 100)
                self.ui.successfulTable.setColumnWidth(6, 100)
                currentRowCount = 0
                for row in result:
                    for colCount in range(0, len(result[0])):
                        self.ui.successfulTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print("Query failed.")

    def categoryChanged(self):
        if (self.ui.categoryList.currentIndex() >= 0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            zipcode = self.ui.zipcodeList.selectedItems()[0].text()
            category = self.ui.categoryList.currentText()
    
            sql_str = "SELECT B.name, B.address, B.city, B.stars, B.review_count, ROUND(B.review_rating,2), B.number_checkins FROM business as B, Category as C WHERE B.business_id = C.business_id AND B.state='" + state +"' AND B.city ='" + city + "' AND B.postal_code ='" + zipcode + "' AND C.category = '" + category +"' ORDER BY name;"
            try:
                result = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(result[0]))
                self.ui.businessTable.setRowCount(len(result))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Stars', '#Review', 'Rating', '#Checkins']) # name, address, city, stars, review count, review rating, num checkins
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0, 200)
                self.ui.businessTable.setColumnWidth(1, 200)
                self.ui.businessTable.setColumnWidth(2, 100)
                self.ui.businessTable.setColumnWidth(3, 100)
                self.ui.businessTable.setColumnWidth(4, 100)
                self.ui.businessTable.setColumnWidth(5, 100)
                self.ui.businessTable.setColumnWidth(6, 100)
                currentRowCount = 0
                for row in result:
                    for colCount in range(0, len(result[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print("Query failed.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = milestone3()
    window.show()
    sys.exit(app.exec())
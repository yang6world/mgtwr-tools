import sys

from PyQt5.QtWidgets import QApplication

from utils.xlsx_tools import generate_year_for_base_table
from views.app import MainWindow

if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # main_window = MainWindow()
    # main_window.show()
    # sys.exit(app.exec_())

    tabel =  generate_year_for_base_table(['2015', '2016', '2017', '2018', '2019', '2020'])
    print(tabel)
    tabel.to_excel('year.xlsx', index=False)

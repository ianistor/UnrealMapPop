import sys
import qdarkstyle
from PySide2 import QtWidgets

# create the application and the main window
app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()

# setup stylesheet
app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())
# or in new API
app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyside2'))


# run
window.show()
app.exec_()


import datetime
from functools import partial
from pathlib import Path

from sqlite3 import Connection
from PySide2 import QtWidgets, QtGui, QtCore
from weather.weather_ui import Ui_Dialog
from weather.models.all_day import AllDay
from weather.utils import load_all_csv


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, conn: Connection, csv_path: Path):
        super(MyWindow, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.conn = conn
        self.all_day_model = AllDay(conn=self.conn, parent=self)
        self.ui.all_day.setModel(self.all_day_model)
        self.ui.all_day.resizeColumnsToContents()

        self.ui.all_day.scrollTo(
            self.all_day_model.start_day_index,
            hint=QtWidgets.QAbstractItemView.PositionAtTop
        )

        self.ui.calendar.clicked.connect(self.date_changed)

        self.csv_path = csv_path
        self.ui.csv_path.setText(str(csv_path))
        self.ui.load_csv.clicked.connect(self.load_csv)

    def date_changed(self):
        date_from_window = datetime.date(
            *self.ui.calendar.selectedDate().getDate()
        )
        self.all_day_model.change_date(date_from_window)
        self.ui.all_day.resizeColumnsToContents()

    def resizeEvent(self, event: QtGui.QResizeEvent):
        super().resizeEvent(event)
        self.ui.all_day.setGeometry(QtCore.QRect(
            self.ui.all_day.x(),
            self.ui.all_day.y(),
            self.ui.all_day.width(),
            event.size().height(),
        ))

    def load_csv(self):
        cursor = self.conn.cursor()
        load_all_csv(cursor, self.csv_path)
        self.conn.commit()
        cursor.close()



###########################################################################
# Top30 is Copyright (C) 2016-2017 Kyle Robbertze <krobbertze@gmail.com>
#
# Top30 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# Top30 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Top30.  If not, see <http://www.gnu.org/licenses/>.
###########################################################################
"""
Main UI handlers
"""
import sys
from PyQt5 import QtCore, QtWidgets

from top30.top_30_creator import Top30Creator
from top30.clip_list import ClipListModel
from top30.main_window import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, chart_file, last_week):
        super(MainWindow, self).__init__()
        self.creator = Top30Creator(chart_file, last_week)
        self.main_window = Ui_MainWindow()
        self.main_window.setupUi(self)
        self.init_ui()

    def init_ui(self):
        """Initialises the UI"""
        self.main_window.btn_add_clip.clicked.connect(self.on_add_clip_clicked)
        self.main_window.btn_move_up.clicked.connect(self.on_move_up_clicked)
        self.main_window.btn_move_down.clicked.connect(self.on_move_down_clicked)
        self.main_window.btn_delete_clip.clicked.connect(self.on_delete_clip_clicked)
        self.main_window.btn_create.clicked.connect(self.on_create_clip_clicked)

        self.main_window.act_new.triggered.connect(self.on_new_clicked)
        self.main_window.act_exit.triggered.connect(QtWidgets.qApp.quit)
        self.main_window.act_create_clip.triggered.connect(self.on_create_clip_clicked)
        self.main_window.act_add_clip.triggered.connect(self.on_add_clip_clicked)
        self.main_window.act_delete_clip.triggered.connect(self.on_delete_clip_clicked)

        self.load_settings()
        self.init_table()

        self.move(200, 100)
        self.setWindowTitle("Top 30 Creator")
        self.show()

    def init_table(self):
        """Initialises the table implementation"""
        self.clip_model = ClipListModel()
        self.main_window.clip_view.setModel(self.clip_model)

    def on_new_clicked(self):
        """Event listener for the new menu item"""
        self.init_table()

    def on_add_clip_clicked(self):
        filenames, mime  = QtWidgets.QFileDialog.getOpenFileNames(self,
                "Add clip", "/home/kyle/projects/top30/songs",
                "Audio(*.mp3 *.ogg);;All Files(*)")
        for filename in filenames:
            self.add_clip(filename)
        self.main_window.clip_view.resizeColumnsToContents()

    def on_move_up_clicked(self):
        item = self.get_selected_clip()
        if not item == None and item.row() > 0:
            self.clip_model.moveRows(QtCore.QModelIndex(), item.row(),
                                     item.row(), QtCore.QModelIndex(),
                                     item.row() - 1)

    def on_move_down_clicked(self):
        item = self.get_selected_clip()
        if not item == None and item.row() < self.clip_model.rowCount() - 1:
            self.clip_model.moveRows(QtCore.QModelIndex(), item.row() + 1,
                                     item.row() + 1, QtCore.QModelIndex(),
                                     item.row())

    def on_delete_clip_clicked(self):
        """Event listener for the delete clip button"""
        item = self.get_selected_clip()
        if not item == None:
            self.clip_model.removeRow(item.row())

    def on_create_clip_clicked(self):
        """Event listener for the Create Clip button"""
        if self.clip_model.rowCount() == 0:
            QtWidgets.QMessageBox.warning(self, "No Clips",
                                          "Please add clips to use")
            return

        self.save_settings()
        rundown_name, file_type = self.save_clip()
        if not rundown_name:
            return

        item = self.clip_model.createIndex(-1, 1)
        item = item.sibling(item.row() + 1, item.column())
        while item.isValid():
            clip = item.data()
            clip_type = item.sibling(item.row(), item.column() - 1).data()
            if item.row() == 0:
                rundown = self.creator.get_start(clip)
            elif item.row() == self.clip_model.rowCount() - 1:
                rundown = self.creator.add_end(clip, rundown)
            elif clip_type == "Song":
                rundown = self.creator.add_song(clip, rundown)
            else:
                rundown = self.creator.add_voice(clip, rundown)
            item = item.sibling(item.row() + 1, item.column())
        self.creator.export(rundown_name, "mp3", rundown)
        QtWidgets.QMessageBox.information(self, "Complete",
                                          "Clip " + rundown_name + " created.")

    def get_selected_clip(self):
        """Returns the selected clip in the list"""
        row = self.main_window.clip_view.selectionModel().selectedRows()
        if len(row) == 0:
            return None
        return row[0]

    def add_clip(self, filename):
        """Adds a clip to the list"""
        try:
            time = self.creator.get_start_time(filename)/1000
            time_string = "%02d:%02.1f" % (time / 60, time % 60)
            row = ["Song", filename, time_string]
        except KeyError:
            row = ["Voice", filename, None]
        self.clip_model.appendRow(row)

    def load_settings(self):
        clip_length = str(self.creator.get_song_length()/1000)
        voice_begin_overlap = str(self.creator.get_voice_begin_overlap()/1000)
        voice_end_overlap = str(self.creator.get_voice_end_overlap()/1000)
        self.main_window.txt_song_length.setText(clip_length)
        self.main_window.txt_voice_start.setText(voice_begin_overlap)
        self.main_window.txt_voice_end.setText(voice_end_overlap)

    def save_settings(self):
        clip_length = float(self.main_window.txt_song_length.text()) * 1000
        self.creator.set_song_length(clip_length)

        voice_begin_overlap = float(self.main_window.txt_voice_start.text()) * 1000
        self.creator.set_voice_begin_overlap(voice_begin_overlap)

        voice_end_overlap = float(self.main_window.txt_voice_end.text()) * 1000
        self.creator.set_voice_end_overlap(voice_end_overlap)

    def save_clip(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(self, "Add clip", "/home/kyle",
                                                         "Audio (*.mp3 *.ogg)")
        return filename

class UserInterface:
    def run(self, chart, previous):
        app = QtWidgets.QApplication(sys.argv)
        ex = MainWindow(chart, previous)
        sys.exit(app.exec_())

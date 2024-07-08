import sys
from PyQt5.QtCore import Qt, QStringListModel, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QCompleter
from GUI.UI_Message import Ui_MainWindow
from util.QtFunc import upWindowsh


class LabelInputDialog(QMainWindow, Ui_MainWindow):
    confirmed = pyqtSignal(str)  # 定义一个自定义信号
    def __init__(self, parent=None):
        super(LabelInputDialog, self).__init__(parent)
        self.setupUi(self)
        self.history = self.load_history()
        self.setup_combo_box()


        self.text = None

        self.pushButton.clicked.connect(self.on_confirm)
        self.pushButton_2.clicked.connect(self.reject)

    def load_history(self):
        try:
            with open('GUI/history.txt', 'r', encoding='utf-8') as file:
                return [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            return []

    def setup_combo_box(self):
        self.comboBox.setEditable(True)
        self.history_model = QStringListModel(self)
        self.history_model.setStringList(self.history)
        self.comboBox.setModel(self.history_model)
        self.history_completer = QCompleter(self.history_model)
        self.history_completer.setCompletionMode(QCompleter.InlineCompletion)
        self.history_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.comboBox.setCompleter(self.history_completer)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.on_confirm()
            return
        elif event.key() == Qt.Key_Escape:
            self.reject()
            return
        super(LabelInputDialog, self).keyPressEvent(event)


    def on_confirm(self):
        text = self.comboBox.currentText()


        if text:  # 检查文本是否有效
            self.confirmed.emit(text)  # 发出信号，并传递文本
            if text not in self.history:
                self.history.append(text)

            self.save_history()
            self.close()  # 关闭对话框
        else:
            upWindowsh("标签不能为空")
    def save_history(self):
        try:
            with open('GUI/history.txt', 'w', encoding='utf-8') as file:
                for item in self.history:
                    file.write(f"{item}\n")
        except IOError as e:
            upWindowsh(f"保存历史记录失败：{e}")

    def reject(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = LabelInputDialog()
    dialog.show()
    sys.exit(app.exec_())




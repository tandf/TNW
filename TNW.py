import login
import msg
import re

import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore

class TNW():
    def __init__(self):
        self.loginWindow = TNWLogin()
        self.loginWindow.get_id_signal.connect(self.get_id)

    def get_id(self, Id):
        self.Id = Id
        self.mainWindow = TNWMain()

class TNWLogin(QWidget):
    get_id_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        label = QLabel('Enter ID to login.', self)
        label.setFixedSize(400, 100)
        label.move(0, 40)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setStyleSheet('*{font-size:18pt;}')

        self.idTextLine = QLineEdit('', self)
        self.idTextLine.setFixedSize(200, 40)
        self.idTextLine.move(100, 150)
        self.idTextLine.setAlignment(QtCore.Qt.AlignCenter)
        self.idTextLine.setFocus(True)
        self.idTextLine.setText('2016011470')
        self.idTextLine.setStyleSheet('*{font-size:18pt;}')
        regexp = QtCore.QRegExp('^\d{1,10}$')
        validator = QtGui.QRegExpValidator(regexp)
        self.idTextLine.setValidator(validator)
        self.idTextLine.returnPressed.connect(self.login)

        self.setFixedSize(400, 250)
        self.center()
        self.setWindowTitle('Login TNW')    
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def login(self):
        Id = self.idTextLine.text()
        if len(Id) == 10 and login.login(Id):
            self.get_id_signal.emit(str(Id))
            self.close()
        else:
            QMessageBox.about(self, 'Error', 'Please enter a right ID.')

class TNWMain(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.presentContact = []

    def initUI(self):
        self.addFriendBtn= QPushButton('Add friend')
        self.addFriendBtn.setFixedSize(140, 30)
        self.addFriendBtn.clicked.connect(self.add_friend_btn_clicked)

        self.addGroupBtn= QPushButton('Add group')
        self.addGroupBtn.setFixedSize(140, 30)
        self.addGroupBtn.clicked.connect(self.add_group_btn_clicked)

        self.msgArea = QScrollArea()
        self.msgArea.setWidgetResizable(True)
        self.msgAreaVbox = QVBoxLayout()
        self.msgAreaWidget = QWidget()
        self.msgAreaWidget.setLayout(self.msgAreaVbox)
        self.msgArea.setWidget(self.msgAreaWidget)

        self.textEdit = QTextEdit()
        self.textEdit.setFixedHeight(100)

        self.deleteBtn = QPushButton('Delete')
        self.deleteBtn.setFixedSize(60, 30)
        self.deleteBtn.clicked.connect(self.delete_btn_clicked)

        self.queryBtn = QPushButton('Query')
        self.queryBtn.setFixedSize(60, 30)
        self.queryBtn.clicked.connect(self.query_btn_clicked)

        self.sendFileBtn = QPushButton('Send file')
        self.sendFileBtn.setFixedSize(100, 30)
        self.sendFileBtn.clicked.connect(self.send_file_btn_clicked)

        self.sendBtn = QPushButton('Send <C-CR>')
        self.sendBtn.setFixedSize(100, 30)
        self.sendBtn.clicked.connect(self.send_btn_clicked)
        shortcut = QShortcut(QtGui.QKeySequence("Ctrl+Return"), self)
        shortcut.activated.connect(self.send_btn_clicked) 

        self.disable_btn()

        self.conversationLabel = QLabel()
        self.conversationLabel.setText('')
        self.conversationLabel.setWordWrap(True)

        self.vboxrHbox = QHBoxLayout()
        self.vboxrHbox.addWidget(self.deleteBtn)
        self.vboxrHbox.addWidget(self.queryBtn)
        self.vboxrHbox.addStretch()
        self.vboxrHbox.addWidget(self.sendFileBtn)
        self.vboxrHbox.addWidget(self.sendBtn)

        self.contactArea = QScrollArea()
        self.contactArea.setWidgetResizable(True)
        self.contactAreaVbox = QVBoxLayout()
        self.contactAreaVbox.addStretch()
        self.contactAreaWidget = QWidget()
        self.contactAreaWidget.setLayout(self.contactAreaVbox)
        self.contactArea.setWidget(self.contactAreaWidget)

        self.vboxl = QVBoxLayout()
        self.vboxl.addWidget(self.contactArea)
        self.vboxl.addWidget(self.addFriendBtn)
        self.vboxl.addWidget(self.addGroupBtn)

        self.vboxr = QVBoxLayout()
        self.vboxr.addWidget(self.conversationLabel)
        self.vboxr.addWidget(self.msgArea)
        self.vboxr.addWidget(self.textEdit)
        self.vboxr.addLayout(self.vboxrHbox)

        self.hbox = QHBoxLayout()
        self.hbox.addLayout(self.vboxl, 0)
        self.hbox.addLayout(self.vboxr, 1)

        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.hbox)
        self.setCentralWidget(self.centralWidget)

        self.resize(600, 400)
        self.setMinimumSize(500, 300)
        self.center()
        self.setWindowTitle('TNW is Not WeChat')    

        for i in range(10):
            self.show_msg('information  haha', 'text, text, text, text, text, text, text, text, text, text, text, text, text, text, text, text, text')

        self.show_msg('information  haha', 'text, text, text, text, text, a long long long wordddddddddddddd', 'right')

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def disable_btn(self):
        self.deleteBtn.setEnabled(False)
        self.queryBtn.setEnabled(False)
        self.sendFileBtn.setEnabled(False)
        self.sendBtn.setEnabled(False)

    def enable_btn(self):
        self.deleteBtn.setEnabled(True)
        self.queryBtn.setEnabled(True)
        self.sendFileBtn.setEnabled(True)
        self.sendBtn.setEnabled(True)

    def read_contact_file(self):
        # TODO rt
        return 0

    def show_msg(self, info, text, align='left'):
        msgWidget = QWidget()
        msgHbox = QHBoxLayout()
        msgVboxR = QVBoxLayout()
        msgWidget.setLayout(msgHbox)
        msgInfoLabel = QLabel()
        msgInfoLabel.setText(info)
        msgTextLabel = QLabel()
        msgTextLabel.setText(text)
        msgTextLabel.setWordWrap(True)
        if align == 'right':
            msgHbox.addStretch(2)
            msgHbox.addLayout(msgVboxR, 5)
            msgInfoLabel.setAlignment(QtCore.Qt.AlignRight)
            msgTextLabel.setAlignment(QtCore.Qt.AlignRight)
        else:
            msgHbox.addLayout(msgVboxR, 5)
            msgHbox.addStretch(2)

        msgVboxR.addWidget(msgInfoLabel)
        msgVboxR.addWidget(msgTextLabel)
        self.msgAreaVbox.addWidget(msgWidget)

    def clear_msg_area(self):
        for i in reversed(range(self.msgAreaVbox.count())): 
            self.msgAreaVbox.itemAt(i).widget().setParent(None)

    def add_contact(self, contact):
        # TODO check exist
        # TODO write to file
        contactBtn = ContactBtn(contact)
        contactBtn.clicked.connect(self.contact_btn_clicked)
        count = self.contactAreaVbox.count()
        self.contactAreaVbox.insertWidget(count - 1, contactBtn)

    def add_friend_btn_clicked(self):
        Id, okPressed = QInputDialog.getText(self, "Add friend","Friend id:", QLineEdit.Normal, "")
        if okPressed and Id != '':
            queryResult = login.query(Id)
            regex = re.compile('(\d{1,3}\.?){4}')
            if queryResult == 'n' or regex.match(queryResult):
                self.add_contact([Id])
            else:
                QMessageBox.about(self, "Error", "No such user!")

    def add_group_btn_clicked(self):
        return 0

    def contact_btn_clicked(self):
        self.enable_btn()
        self.presentContact = self.sender().contact
        self.conversationLabel.setText('chat with: ' + \
                ' & '.join(self.presentContact))
        if len(self.presentContact) > 1:
            self.queryBtn.hide()
        else:
            self.queryBtn.show()

    def delete_btn_clicked(self):
        # TODO delete according to contact
        return 0

    def query_btn_clicked(self):
        result = login.query(self.presentContact[0])
        regex = re.compile('(\d{1,3}\.?){4}')
        if result == 'n':
            text = 'Friend offline'
        elif regex.match(result):
            text = 'Friend online'
        else:
            text = 'No such User!'
        QMessageBox.about(self, 'Query result', text)

    def send_btn_clicked(self):
        text = self.textEdit.toPlainText()
        self.textEdit.setText('')
        if text:
            print(text)

    def send_file_btn_clicked(self):
        return 0

class ContactBtn(QPushButton):
    def __init__(self, contact):
        super().__init__()
        self.contact = contact
        self.initUI()

    def initUI(self):
        self.setFixedSize(120, 50)
        if len(self.contact) > 1:
            self.setText('Group: \n' + self.contact[0] + ' ...')
        else:
            self.setText(self.contact[0])

if __name__ == '__main__':

    app = QApplication(sys.argv)
    tnw = TNW()
    sys.exit(app.exec_())

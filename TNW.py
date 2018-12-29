import re
import time
import sys
import json
import hashlib
import os
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore

import login
import msg

class TNW():
    def __init__(self):
        self.loginWindow = TNWLogin()
        self.loginWindow.get_id_signal.connect(self.get_id)

    def get_id(self, Id):
        self.mainWindow = TNWMain(Id)

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
            QMessageBox.about(self, 'Error',\
                    'Please enter a right ID.')

class TNWMain(QMainWindow):

    def __init__(self, Id):
        super().__init__()
        self.Id = Id
        self.presentContact = []
        self.initUI()
        self.read_contact_file()
        idDir = 'data/' + str(self.Id) + '/'
        if not os.path.exists(idDir):
                os.makedirs(idDir)

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
        self.msgAreaVbox.addStretch()
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

        self.disable_contact()

        self.conversationLabel = QLabel()
        self.conversationLabel.setText('')
        self.conversationLabel.setWordWrap(True)

        self.vboxrHbox1 = QHBoxLayout()
        self.vboxrHbox1.addWidget(self.deleteBtn)
        self.vboxrHbox1.addWidget(self.conversationLabel)

        self.vboxrHbox2 = QHBoxLayout()
        self.vboxrHbox2.addWidget(self.queryBtn)
        self.vboxrHbox2.addStretch()
        self.vboxrHbox2.addWidget(self.sendFileBtn)
        self.vboxrHbox2.addWidget(self.sendBtn)

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
        self.vboxr.addLayout(self.vboxrHbox1)
        self.vboxr.addWidget(self.msgArea)
        self.vboxr.addWidget(self.textEdit)
        self.vboxr.addLayout(self.vboxrHbox2)

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

        self.receivingMsg(7070)
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def receivingMsg(self, port):
        self.server = msg.ServerThread(port, self)
        self.server.incomingMsg.connect(self.deal_msg)
        self.server.start()
        print('receivingMsg')

    def disable_contact(self):
        self.deleteBtn.setEnabled(False)
        self.queryBtn.setEnabled(False)
        self.sendFileBtn.setEnabled(False)
        self.sendBtn.setEnabled(False)
        self.textEdit.setEnabled(False)

    def enable_contact(self):
        self.deleteBtn.setEnabled(True)
        self.queryBtn.setEnabled(True)
        self.sendFileBtn.setEnabled(True)
        self.sendBtn.setEnabled(True)
        self.textEdit.setEnabled(True)

    def write_contact_info(self):
        contactList = [self.contactAreaVbox.itemAt(i).widget().contact
            for i in range(self.contactAreaVbox.count() - 1)]
        with open('data/' + str(self.Id) + '/contact', 'w') as contactF:
            contactF.write(json.dumps(contactList) + ' ')

    def read_contact_file(self):
        contactFPath = 'data/' + str(self.Id) + '/contact'
        if os.path.isfile(contactFPath):
            with open(contactFPath, 'r') as contactF:
                contactList = json.load(contactF)
                for contact in contactList:
                    self.add_contact(contact)

    def read_msg_file(self):
        self.clear_msg_area()
        contact = sorted(set(self.presentContact + [self.Id]))
        hash_object = hashlib.md5(''.join(contact).encode('utf8'))
        filePath ='data/' + str(self.Id) + '/' + hash_object.hexdigest()
        if os.path.isfile(filePath):
            with open(filePath, 'r') as msgF:
                line = msgF.readline()[:-1]
                while line:
                    data = json.loads(line)
                    self.show_msg(data)
                    line = msgF.readline()[:-1]

    def deal_msg(self, data):
        contact = sorted(set([data['source']] + data['target']))

        # write file
        hash_object = hashlib.md5(''.join(contact).encode('utf8'))
        with open('data/' + str(self.Id) + '/' + hash_object.hexdigest(), 'a+')\
                as msgF:
            msgF.write(json.dumps(data) + '\n')

        # Check active chat.
        if contact ==  sorted(set(self.presentContact + [self.Id])):
            self.show_msg(data)
        else:
             contactBtn = self.add_contact(sorted(set(contact) -\
                     set([self.Id])), False)
             contactBtn.setStyleSheet('*{background-color:#ABC;}')

    def show_msg(self, data, align='left'):
        if data['type'] == 'TEXT':
            timeArray = time.localtime(data['time'] / 1000)
            info = data['source'] + ' ' + \
                    time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            text = data['data']

        msgWidget = QWidget()
        msgHbox = QHBoxLayout()
        msgVbox = QVBoxLayout()
        msgWidget.setLayout(msgHbox)

        msgInfoLabel = QLabel()
        msgInfoLabel.setText(info)
        msgInfoLabel.setWordWrap(True)
        msgVbox.addWidget(msgInfoLabel)

        msgTextLabel = QLabel()
        msgTextLabel.setText(text)
        msgTextLabel.setWordWrap(True)
        msgVbox.addWidget(msgTextLabel)

        if data['source'] == self.Id:
            msgHbox.addStretch(2)
            msgHbox.addLayout(msgVbox, 5)
            msgInfoLabel.setAlignment(QtCore.Qt.AlignRight)
            msgTextLabel.setAlignment(QtCore.Qt.AlignRight)
        else:
            msgHbox.addLayout(msgVbox, 5)
            msgHbox.addStretch(2)

        msgInfoLabel.setStyleSheet('*{background-color:yellow;}')
        msgTextLabel.setStyleSheet('*{background-color:yellow;}')
        count = self.msgAreaVbox.count()
        self.msgAreaVbox.insertWidget(count - 1, msgWidget)

    def clear_msg_area(self):
        for i in reversed(range(self.msgAreaVbox.count() - 1)):
            self.msgAreaVbox.itemAt(i).widget().setParent(None)

    def add_contact(self, contact, activate=True):
        searchContact = self.search_contact_btn(contact) 
        if searchContact == -1:
            contactBtn = ContactBtn(contact)
            contactBtn.clicked.connect(self.contact_btn_clicked)
            count = self.contactAreaVbox.count()
            self.contactAreaVbox.insertWidget(count - 1, contactBtn)
            if activate:
                contactBtn.clicked.emit()
            return contactBtn
        elif activate:
            self.contactAreaVbox.itemAt(searchContact).\
                    widget().clicked.emit()
        return self.contactAreaVbox.itemAt(searchContact).widget()

    def search_contact_btn(self, contact):
        for i in range(self.contactAreaVbox.count() - 1):
            if self.contactAreaVbox.itemAt(i).widget().contact \
                    == contact:
                return i
        return -1

    def add_friend_btn_clicked(self):
        Id, okPressed = QInputDialog.getInt(self,\
                "Add friend","Friend id:", QLineEdit.Normal)
        Id = str(Id)
        if okPressed:
            if Id == self.Id:
                QMessageBox.about(self, "Error", "You can't add youself!")
            elif login.checkValid(Id):
                self.add_contact([Id])
            else:
                QMessageBox.about(self, "Error", "No such user!")

    def add_group_btn_clicked(self):
        dialog = TNWAddGroupWidget(self.Id, self)
        contact = dialog.getContact()
        if len(contact):
            self.add_contact(sorted(contact))

    def contact_btn_clicked(self):
        self.enable_contact()
        self.presentContact = self.sender().contact
        self.sender().setStyleSheet('*{background-color:white}')
        self.read_msg_file()
        self.conversationLabel.setText('chat with: ' + \
                ' & '.join(self.presentContact))
        if len(self.presentContact) > 1:
            self.queryBtn.hide()
        else:
            self.queryBtn.show()

    def delete_btn_clicked(self):
        searchContact = self.search_contact_btn(self.presentContact)
        if searchContact != -1:
            self.contactAreaVbox.itemAt(searchContact).widget().\
                    setParent(None)
            self.disable_contact()
            self.conversationLabel.setText('')
            self.clear_msg_area()

            contact = sorted(set(self.presentContact + [self.Id]))
            hash_object = hashlib.md5(''.join(contact).encode('utf8'))
            with open('data/' + str(self.Id) + '/' + hash_object.hexdigest(),\
                    'w') as msgF:
                msgF.write('')
            self.presentContact = []

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
            print(msg.send_text(self.Id, self.presentContact, text))

    def send_file_btn_clicked(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Select file",\
                "","All Files (*)", options=options)
        if fileName:
            print(fileName)

    def closeEvent(self, event):
        print('login out')
        login.logout(self.Id)
        self.write_contact_info();
        event.accept()

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

class TNWAddGroupWidget(QDialog):

    def __init__(self, Id, parent = None):
        super().__init__(parent)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.Id = Id
        self.contact = set([])
        self.initUI()

    def initUI(self):
        self.label = QLabel('', self)
        self.label.setText('Group member:')
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet('*{font-size:18pt;}')
        self.label.setWordWrap(True)
        self.label.setFixedWidth(340)
        self.labelScroll = QScrollArea(self)
        self.labelScroll.setFixedSize(360, 100)
        self.labelScroll.move(20, 40)
        self.labelScroll.setWidget(self.label)

        self.idTextLine = QLineEdit(self.Id, self)
        self.idTextLine.setFixedSize(200, 40)
        self.idTextLine.move(100, 150)
        self.idTextLine.setAlignment(QtCore.Qt.AlignCenter)
        self.idTextLine.setFocus(True)
        self.idTextLine.setText('')
        self.idTextLine.setStyleSheet('*{font-size:18pt;}')
        regexp = QtCore.QRegExp('^\d{1,10}$')
        validator = QtGui.QRegExpValidator(regexp)
        self.idTextLine.setValidator(validator)

        self.addBtn = QPushButton('Add id', self)
        self.addBtn.setFixedSize(100, 30)
        self.addBtn.move(25, 200)
        self.addBtn.clicked.connect(self.addId)
        self.startGroupBtn = QPushButton('Start Group', self)
        self.startGroupBtn.setFixedSize(100, 30)
        self.startGroupBtn.move(150, 200)
        self.startGroupBtn.clicked.connect(self.startGroup)
        self.cancelBtn = QPushButton('Cancel', self)
        self.cancelBtn.setFixedSize(100, 30)
        self.cancelBtn.move(275, 200)
        self.cancelBtn.clicked.connect(self.cancel)

        self.setFixedSize(400, 250)
        self.center()
        self.setWindowTitle('Start a group chat')    
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def addId(self):
        Id = self.idTextLine.text()
        if Id == self.Id:
            QMessageBox.about(self, 'Error',\
                    'You are inlcuded already!')
            self.idTextLine.setText('')
        elif login.checkValid(Id):
            self.contact.add(Id)
            self.idTextLine.setText('')
            self.label.setText('Group member:\n' +\
                    ' '.join(sorted(self.contact)))
            self.label.adjustSize()
        else:
            QMessageBox.about(self, 'Error', 'Invalid Id!')

    def cancel(self):
        self.contact = set([])
        self.close()

    def startGroup(self):
        if len(self.contact) > 1:
            self.close()
        else:
            QMessageBox.about(self, 'Error', 'Groups need more than 2\
                    users(including yourself)!')

    def getContact(self):
        self.exec_()
        return list(self.contact)

# TODO send msg
# TODO send file

if __name__ == '__main__':

    app = QApplication(sys.argv)
    tnw = TNW()
    sys.exit(app.exec_())

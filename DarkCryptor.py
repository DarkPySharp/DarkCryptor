#!/home/darkpydeu/Python/venv/bin/python3
"""
<-*- coding: utf-8 -*->
Powered by -> {-*> DarkPyDeu <*-}
# доделать функцию перезаписи файла при шифровки и расшифровки.
"""
from PyQt5 import QtCore, QtGui, QtWidgets
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, Blowfish
from Crypto import Random
from struct import pack
from random import shuffle
import pyAesCrypt as Cry
import os

file = ""
directory = ""
name = None
privateKey = ""
publicKey = ""
choiceSettings = None
bufferSize = 512 * 1024
AppName = "DarkCryptor"
infoEnc = {
    "AES": "AES - Способен зашифровать любой файл ключом до 1024 бит ( но ключ надо запонить | записать куда-либо )",
    "BlowFish": "BlowFish - Способен зашифровать любой файл ключом от 4 бит до 50 бит ( но ключ надо запонить | записать куда-либо )",
    "RSA": "RSA - Способен зашифровать любой файл ключом от 1024 бит ( ключ храниться в файлах public.key & private.key )"
}

class Ui_Main(object):
    def setupUi(self, Main):
        Main.setObjectName("Main")
        Main.resize(647, 130)
        Main.setMinimumSize(QtCore.QSize(647, 130))
        Main.setMaximumSize(QtCore.QSize(647, 130))
        Main.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.lineEdit = QtWidgets.QLineEdit(Main)
        self.lineEdit.setGeometry(QtCore.QRect(8, 9, 540, 35))
        self.lineEdit.setStyleSheet("color: rgb(255, 85, 0); background-color: rgb(39, 39, 39);")
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(Main)
        self.pushButton.setGeometry(QtCore.QRect(550, 9, 88, 35))
        self.pushButton.setStyleSheet("color: rgb(255, 85, 0); background-color: rgb(39, 39, 39);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Main)
        self.pushButton_2.setGeometry(QtCore.QRect(507, 91, 132, 35))
        self.pushButton_2.setStyleSheet("color: rgb(255, 85, 0); background-color: rgb(39, 39, 39);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.groupBox = QtWidgets.QGroupBox(Main)
        self.groupBox.setGeometry(QtCore.QRect(8, 50, 631, 41))
        self.groupBox.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_3.setGeometry(QtCore.QRect(520, 1, 110, 34))
        self.pushButton_3.setStyleSheet("color: rgb(255, 85, 0); background-color: rgb(39, 39, 39);")
        self.pushButton_3.setObjectName("pushButton_3")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_3.setGeometry(QtCore.QRect(417, 1, 101, 34))
        self.lineEdit_3.setStyleSheet("color: rgb(255, 85, 0); background-color: rgb(39, 39, 39);")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.pushButton_6 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_6.setGeometry(QtCore.QRect(0, 0, 110, 34))
        self.pushButton_6.setStyleSheet("color: rgb(255, 85, 0); background-color: rgb(39, 39, 39);")
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_7.setGeometry(QtCore.QRect(111, 0, 110, 34))
        self.pushButton_7.setStyleSheet("color: rgb(255, 85, 0); background-color: rgb(39, 39, 39);")
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_4 = QtWidgets.QPushButton(Main)
        self.pushButton_4.setGeometry(QtCore.QRect(417, 91, 88, 35))
        self.pushButton_4.setStyleSheet("color: rgb(255, 85, 0); background-color: rgb(39, 39, 39);")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(Main)
        self.pushButton_5.setGeometry(QtCore.QRect(327, 91, 88, 35))
        self.pushButton_5.setStyleSheet("color: rgb(255, 85, 0);\n"
"background-color: rgb(39, 39, 39);")
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.setEnabled(False)
        self.retranslateUi(Main)
        QtCore.QMetaObject.connectSlotsByName(Main)

    def retranslateUi(self, Main):
        _translate = QtCore.QCoreApplication.translate
        Main.setWindowTitle(_translate("Main", "DarkCryptorRSA"))
        self.lineEdit.setPlaceholderText(_translate("Main", "Имя файла"))
        self.pushButton.setText(_translate("Main", "Выбрать"))
        self.pushButton_2.setText(_translate("Main", "Шифровать"))
        self.pushButton_3.setText(_translate("Main", "Сгенерировать"))
        self.lineEdit_3.setPlaceholderText(_translate("Main", "Кол-во битов"))
        self.pushButton_6.setText(_translate("Main", "Публичный"))
        self.pushButton_7.setText(_translate("Main", "Приватный"))
        self.pushButton_4.setText(_translate("Main", "Настройки"))
        self.pushButton_5.setText(_translate("Main", "Имя"))

    def runCreate(self):
        self.Threading = ThreadClass()
        ms_info(AppName, "Производиться создание ключа, пожалуйста ожидайте", detail="Иногда проверяйте файл")
        self.Threading.start()

class Ui_Name(object):
    def setupUi(self, Name):
        Name.setObjectName("Name")
        Name.resize(200, 90)
        Name.setMinimumSize(QtCore.QSize(200, 90))
        Name.setMaximumSize(QtCore.QSize(200, 90))
        Name.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.lineEdit = QtWidgets.QLineEdit(Name)
        self.lineEdit.setGeometry(QtCore.QRect(0, 10, 201, 32))
        self.lineEdit.setStyleSheet("color: rgb(255, 85, 0); background-color: rgb(39, 39, 39);")
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(Name)
        self.pushButton.setGeometry(QtCore.QRect(55, 50, 88, 34))
        self.pushButton.setStyleSheet("color: rgb(255, 85, 0); background-color: rgb(39, 39, 39);")
        self.pushButton.setObjectName("pushButton")
        self.retranslateUi(Name)
        QtCore.QMetaObject.connectSlotsByName(Name)

    def retranslateUi(self, Name):
        _translate = QtCore.QCoreApplication.translate
        Name.setWindowTitle(_translate("Name", "Редактор имени"))
        self.lineEdit.setPlaceholderText(_translate("Name", "Введите имя с расширением"))
        self.pushButton.setText(_translate("Name", "Сохранить"))

class Ui_StartMenu(object):
    def setupUi(self, StartMenu):
        StartMenu.setObjectName("StartMenu")
        StartMenu.resize(200, 135)
        StartMenu.setMinimumSize(QtCore.QSize(200, 135))
        StartMenu.setMaximumSize(QtCore.QSize(200, 135))
        StartMenu.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.frame = QtWidgets.QFrame(StartMenu)
        self.frame.setGeometry(QtCore.QRect(0, 0, 200, 135))
        self.frame.setStyleSheet("background-color: black; border-radius: 15px")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.BlowFish = QtWidgets.QPushButton(StartMenu)
        self.BlowFish.setGeometry(QtCore.QRect(10, 50, 145, 35))
        self.BlowFish.setStyleSheet("background-color: rgb(51, 51, 51);\n"
"color: rgb(255, 62, 0);")
        self.BlowFish.setObjectName("BlowFish")
        self.AES = QtWidgets.QPushButton(StartMenu)
        self.AES.setGeometry(QtCore.QRect(10, 10, 145, 35))
        self.AES.setStyleSheet("background-color: rgb(51, 51, 51);\n"
"color: rgb(255, 62, 0);")
        self.AES.setObjectName("AES")
        self.RSA = QtWidgets.QPushButton(StartMenu)
        self.RSA.setGeometry(QtCore.QRect(10, 90, 145, 35))
        self.RSA.setStyleSheet("background-color: rgb(51, 51, 51);\n"
"color: rgb(255, 62, 0);")
        self.RSA.setObjectName("RSA")
        self.AESinfo = QtWidgets.QPushButton(StartMenu)
        self.AESinfo.setGeometry(QtCore.QRect(155, 10, 35, 35))
        self.AESinfo.setStyleSheet("background-color: rgb(51, 51, 51);\n"
"color: rgb(255, 62, 0);")
        self.AESinfo.setObjectName("AESinfo")
        self.BlowFishInfo = QtWidgets.QPushButton(StartMenu)
        self.BlowFishInfo.setGeometry(QtCore.QRect(155, 50, 35, 35))
        self.BlowFishInfo.setStyleSheet("background-color: rgb(51, 51, 51);\n"
"color: rgb(255, 62, 0);")
        self.BlowFishInfo.setObjectName("BlowFishInfo")
        self.RSAinfo = QtWidgets.QPushButton(StartMenu)
        self.RSAinfo.setGeometry(QtCore.QRect(155, 90, 35, 35))
        self.RSAinfo.setStyleSheet("background-color: rgb(51, 51, 51);\n"
"color: rgb(255, 62, 0);")
        self.RSAinfo.setObjectName("RSAinfo")
        self.retranslateUi(StartMenu)
        QtCore.QMetaObject.connectSlotsByName(StartMenu)

    def retranslateUi(self, StartMenu):
        _translate = QtCore.QCoreApplication.translate
        StartMenu.setWindowTitle(_translate("StartMenu", "DarkCryptor Start"))
        StartMenu.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        StartMenu.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.BlowFish.setText(_translate("StartMenu", "BlowFish"))
        self.AES.setText(_translate("StartMenu", "AES"))
        self.RSA.setText(_translate("StartMenu", "RSA"))
        self.AESinfo.setText(_translate("StartMenu", "i"))
        self.BlowFishInfo.setText(_translate("StartMenu", "i"))
        self.RSAinfo.setText(_translate("StartMenu", "i"))

class Ui_Settings(object):
    def setupUi(self, Settings):
        Settings.setObjectName("Settings")
        Settings.resize(190, 255)
        Settings.setMinimumSize(QtCore.QSize(190, 255))
        Settings.setMaximumSize(QtCore.QSize(190, 255))
        Settings.setStyleSheet("background-color: black")
        self.verticalLayoutWidget = QtWidgets.QWidget(Settings)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 10, 191, 206))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.radioButton = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioButton.setStyleSheet("color: rgb(255, 62, 0);")
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.verticalLayout.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioButton_2.setStyleSheet("color: rgb(255, 62, 0);")
        self.radioButton_2.setObjectName("radioButton_2")
        self.verticalLayout.addWidget(self.radioButton_2)
        self.checkBox = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBox.setStyleSheet("color: rgb(255, 62, 0);")
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout.addWidget(self.checkBox)
        self.checkBox_2 = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBox_2.setStyleSheet("color: rgb(255, 62, 0);")
        self.checkBox_2.setObjectName("checkBox_2")
        self.verticalLayout.addWidget(self.checkBox_2)
        self.checkBox_3 = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBox_3.setStyleSheet("color: rgb(255, 62, 0);")
        self.checkBox_3.setObjectName("checkBox_3")
        self.verticalLayout.addWidget(self.checkBox_3)
        self.checkBox_4 = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBox_4.setStyleSheet("color: rgb(255, 62, 0);")
        self.checkBox_4.setObjectName("checkBox_4")
        self.verticalLayout.addWidget(self.checkBox_4)
        self.ChWrite = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.ChWrite.setStyleSheet("color: rgb(255, 62, 0);")
        self.ChWrite.setObjectName("ChWrite")
        self.ChWrite.setEnabled(False)
        self.verticalLayout.addWidget(self.ChWrite)
        self.pushButton = QtWidgets.QPushButton(Settings)
        self.pushButton.setGeometry(QtCore.QRect(5, 220, 180, 31))
        self.pushButton.setStyleSheet("background-color: rgb(51, 51, 51);color: rgb(255, 62, 0);")
        self.pushButton.setObjectName("pushButton")
        self.retranslateUi(Settings)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        _translate = QtCore.QCoreApplication.translate
        Settings.setWindowTitle(_translate("Settings", "Settings"))
        self.radioButton.setText(_translate("Settings", "Шифровать"))
        self.radioButton_2.setText(_translate("Settings", "Расшифровать"))
        self.checkBox.setText(_translate("Settings", "Директории"))
        self.checkBox_2.setText(_translate("Settings", "Сохранить пароль"))
        self.checkBox_3.setText(_translate("Settings", "Пользовательское имя"))
        self.checkBox_4.setText(_translate("Settings", "Исходный файл"))
        self.ChWrite.setText(_translate("Settings", "Перезапись файла"))
        self.pushButton.setText(_translate("Settings", "Сохранить"))

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(647, 190)
        Dialog.setMinimumSize(QtCore.QSize(647, 190))
        Dialog.setMaximumSize(QtCore.QSize(647, 190))
        Dialog.setWindowIcon(QtGui.QIcon("/home/darkpydeu/Изображения/Lock.ico"))
        Dialog.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(8, 9, 540, 35))
        self.lineEdit.setStyleSheet("color: rgb(255, 85, 0); background-color: rgb(39, 39, 39);")
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(550, 9, 88, 35))
        self.pushButton.setStyleSheet("color: rgb(255, 85, 0); background-color: rgb(39, 39, 39);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(507, 150, 132, 35))
        self.pushButton_2.setStyleSheet("color: rgb(255, 85, 0); background-color: rgb(39, 39, 39);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(8, 50, 631, 91))
        self.groupBox.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_3.setGeometry(QtCore.QRect(515, 50, 110, 34))
        self.pushButton_3.setStyleSheet("color: rgb(255, 85, 0); background-color: rgb(39, 39, 39);")
        self.pushButton_3.setObjectName("pushButton_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_2.setGeometry(QtCore.QRect(0, 10, 631, 35))
        self.lineEdit_2.setStyleSheet("color: rgb(255, 85, 0); background-color: rgb(39, 39, 39);")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_3.setGeometry(QtCore.QRect(412, 50, 101, 34))
        self.lineEdit_3.setStyleSheet("color: rgb(255, 85, 0); background-color: rgb(39, 39, 39);")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setToolTip("Длина пароля в символах\nБайт = 1 символ")
        self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        self.pushButton_4.setGeometry(QtCore.QRect(417, 150, 88, 35))
        self.pushButton_4.setStyleSheet("color: rgb(255, 85, 0); background-color: rgb(39, 39, 39);")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(Dialog)
        self.pushButton_5.setGeometry(QtCore.QRect(327, 150, 88, 35))
        self.pushButton_5.setStyleSheet("color: rgb(255, 85, 0); background-color: rgb(39, 39, 39);")
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.setEnabled(False)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "DarkCryptorAES"))
        self.lineEdit.setPlaceholderText(_translate("Dialog", "Имя файла"))
        self.pushButton.setText(_translate("Dialog", "Выбрать"))
        self.pushButton_2.setText(_translate("Dialog", "Шифровать"))
        self.pushButton_3.setText(_translate("Dialog", "Сгенерировать"))
        self.lineEdit_2.setPlaceholderText(_translate("Dialog", "Пароль"))
        self.lineEdit_3.setPlaceholderText(_translate("Dialog", "Кол-во битов"))
        self.pushButton_4.setText(_translate("Dialog", "Настройки"))
        self.pushButton_5.setText(_translate("Dialog", "Имя"))

class ThreadClass(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent=parent)
    def run(self):
        create_key()

def create_key():
    bits = mn.lineEdit_3.text()
    keys = RSA.generate(int(bits))
    keys_dir = "rsa"
    if not os.path.exists(keys_dir):
        os.mkdir(keys_dir)
    with open(f"{keys_dir}/public.rsa", "wb") as pub, open(f"{keys_dir}/private.rsa", "wb") as priv:
        pub.write(keys.publickey().exportKey('PEM'))
        priv.write(keys.export_key('PEM'))

def getpassword():
    try:
        kolvo = int(ui.lineEdit_3.text())
        oneBytes= ["q","w","e","r","t","y","u","i","o","p","Z","X","C","V","B","a","s","d","f","g","h","j","k","l","N","M","z","x","c","v","b","n","m","1",
           "2","3","Q","W","E","R","T","Y","U","I","O","P","4","5","A","S","D","F","G","H","J","K","L","6",'7',"8","9","0","(",")",'"',"'","-","_","=","+",
           "!","@","#","$","%","^","&","*","№",";",":","?",".",",","`","~"]
        bytesText = ""
        for i in range(0, kolvo):
            shuffle(oneBytes)
            bytesText += oneBytes[0]
        ui.lineEdit_2.setText(bytesText)
    except:
        ms_info(AppName, "Введите число байтов в пароле", information="байт = 1 символ")

def settings_save(choice: bool):
    if choice: # AES | BlowFish
        if st.checkBox.isChecked():
            ui.lineEdit.setPlaceholderText("Директория")
        else:
           ui.lineEdit.setPlaceholderText("Имя файла")
        if st.radioButton.isChecked():
            ui.pushButton_2.setText("Шифровать")
        elif st.radioButton_2.isChecked():
            ui.pushButton_2.setText("Расшифровать")
        if st.checkBox_3.isChecked():
            ui.pushButton_5.setEnabled(True)
        else:
           ui.pushButton_5.setEnabled(False)
    elif not choice: # RSA
        if st.checkBox.isChecked():
            mn.lineEdit.setPlaceholderText("Директория")
        else:
            mn.lineEdit.setPlaceholderText("Имя файла")
        if st.radioButton.isChecked():
            mn.pushButton_2.setText("Шифровать")
        elif st.radioButton_2.isChecked():
            mn.pushButton_2.setText("Расшифровать")
        if st.checkBox_3.isChecked():
            mn.pushButton_5.setEnabled(True)
        else:
            mn.pushButton_5.setEnabled(False)
        SettingsDialog.close()
    SettingsDialog.close()

def encrypt_blow(dirCrypt=False):
    global name
    try:
        bs = Blowfish.block_size
        password = ui.lineEdit_2.text()
        if not len(password) <= 3:
            key = bytes(password.encode())
            iv = Random.new().read(bs)
            cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
            with open(file, "r") as f:
                readFileText = f.read()
            if st.checkBox_2.isChecked():
                savepass = open("CCSavePass.txt", "w")
                if name != "" and name != None:
                    savepass.write(f"\n {name} ::: {password}")
                else:
                    savepass.write(f"\n {file}.DC ::: {password}")
                savepass.close()
            plaintext = bytes(readFileText.encode())
            plen = bs - divmod(len(plaintext), bs)[1]
            padding = [plen] * plen
            padding = pack('b' * plen, *padding)
            msg = iv + cipher.encrypt(plaintext + padding)
            if name != '' and name != None:
                fullPath = os.path.join(directory, name)
            else:
                fullPath = os.path.join(directory, str(file) + ".DC")
            with open(fullPath, "wb") as fil:
                fil.write(msg)
            if not dirCrypt:
                ui.lineEdit.clear()
                ui.lineEdit_2.clear()
                nm.lineEdit.clear()
                name = ""
            if not st.checkBox_4.isChecked():
                os.remove(str(file))
            ms_info(AppName, "Done!")
    except Exception as exp:
        if not dirCrypt:
            ms_error(AppName, str(exp))

def decrypt_blow(dirCrypt=False):
    global name
    try:
        bs = Blowfish.block_size
        password = ui.lineEdit_2.text()
        with open(file, "rb") as f:
            text = f.read()
        ciphertext = text
        key = bytes(password.encode())
        iv = ciphertext[:bs]
        ciphertext = ciphertext[bs:]
        cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
        msg = cipher.decrypt(ciphertext)
        last_byte = msg[-1]
        msg = msg[:- (last_byte if type(last_byte) is int else ord(last_byte))]
        if name != '' and name != None:
            fullPath = os.path.join(directory, str(name))
        else:
            fullPath = os.path.join(directory, str(os.path.splitext(str(file))[0]))
        with open(fullPath, "w") as fil:
            fil.write(msg.decode())
        if not st.checkBox_4.isChecked():
            os.remove(str(file))
        if not dirCrypt:
            ui.lineEdit.clear()
            ui.lineEdit_2.clear()
            nm.lineEdit.clear()
            name = ""
            ms_info(AppName, "Done!")
    except Exception as exp:
        if not dirCrypt:
            ms_error(AppName, str(exp))

def encryptUi(dirCrypt=False):
    global name
    try:
        password = ui.lineEdit_2.text()
        if name != '' and name != None:
            fullPath = os.path.join(directory, name)
        else:
            fullPath = os.path.join(directory, str(file) + ".DC")
        Cry.encryptFile(str(file), fullPath, password, bufferSize)
        if st.checkBox_2.isChecked():
            savepass = open("CCSavePass.txt", "w")
            if name != "" and name != None:
                savepass.write(f"\n {name} ::: {password}")
            else:
                savepass.write(f"\n {file}.DC ::: {password}")
            savepass.close()
        if not st.checkBox_4.isChecked():
            os.remove(str(file))
        if not dirCrypt:
            ms_info(AppName, "Done!")
            ui.lineEdit.clear()
            ui.lineEdit_2.clear()
            nm.lineEdit.clear()
            name = ""
    except Exception as exp:
        if not dirCrypt:
            ms_error(AppName, str(exp))

def decryptUi(dirCrypt=False):
    global name
    try:
        passworded = ui.lineEdit_2.text()
        if name != '' and name != None:
            fullPath = os.path.join(directory, str(name))
            Cry.decryptFile(str(file), fullPath, passworded, bufferSize)
        else:
            fullPath = os.path.join(directory, str(os.path.splitext(str(file))[0]))
            Cry.decryptFile(str(file), fullPath, passworded, bufferSize)
        if not st.checkBox_4.isChecked():
            os.remove(str(file))
        if not dirCrypt:
            ms_info(AppName, "Done!")
            nm.lineEdit.clear()
            ui.lineEdit.clear()
            ui.lineEdit_2.clear()
            name = ""
    except Exception as exp:
        if not dirCrypt:
            ms_error(AppName, str(exp))

def encrypt(dirCrypt=False):
    global name
    try:
        with open(file, "rb") as fil:
            crypt = fil.read()
            rsa_public_key = RSA.importKey(publicKey)
            rsa_public_key = PKCS1_OAEP.new(rsa_public_key)
            encrypted_file = rsa_public_key.encrypt(crypt)
            if name != '' and name != None:
                encrypted_file_name = os.path.join(directory, str(name))
            else:
                encrypted_file_name = os.path.join(directory, f"{file}.DC")
            with open(encrypted_file_name, "wb") as encryFile:
                encryFile.write(encrypted_file)
            if st.checkBox_2.isChecked():
                savepass = open("CCSavePass.txt", "w")
                if name != "" and name != None:
                    savepass.write(f"\n {name} ::: политика не одобраяет")
                else:
                    savepass.write(f"\n {file}.CC ::: политика не одобраяет")
                savepass.close()
            if not st.checkBox_4.isChecked():
                os.remove(str(file))
        if not dirCrypt:
            ms_info(AppName, "Done!")
            mn.lineEdit.clear()
            nm.lineEdit.clear()
            name = ""
    except Exception as exp:
        if not dirCrypt:
            ms_error(AppName, str(exp))

def decrypt(dirCrypt=False):
    global name
    try:
        with open(file, "rb") as fil:
            crypted = fil.read()
            rsa_private_key = RSA.importKey(privateKey)
            rsa_private_key = PKCS1_OAEP.new(rsa_private_key)
            decrypted_text = rsa_private_key.decrypt(crypted)
            if name != '' and name != None:
                decrypted_file_name = os.path.join(directory, str(name))
            else:
                decrypted_file_name = os.path.join(directory, str(os.path.splitext(str(file))[0]))
            with open(decrypted_file_name, "w") as decrypted_file:
                decrypted_file.write(decrypted_text.decode("utf-8"))
            if not st.checkBox_4.isChecked():
                os.remove(str(file))
        if not dirCrypt:
            ms_info(AppName, "Done!")
            mn.lineEdit.clear()
            nm.lineEdit.clear()
            name = ""
    except Exception as exp:
        if not dirCrypt:
            ms_error(AppName, str(exp))

def decrypt_dir():
    global file, name
    try:
        filesindir = os.listdir(directory)
        for filesindirs in filesindir:
            path = os.path.join(filesindirs)
            file = os.path.join(str(directory), path)
            decrypt(True)
        mn.lineEdit.clear()
        nm.lineEdit.clear()
        name = ""
        ms_info(AppName, "Done!")
    except Exception as exp:
        ms_error(AppName, str(exp))

def encrypt_dir():
    global file, name
    try:
        filesindir = os.listdir(directory)
        for filesindirs in filesindir:
            path = os.path.join(filesindirs)
            file = os.path.join(str(directory), path)
            encrypt(True)
        mn.lineEdit.clear()
        nm.lineEdit.clear()
        name = ""
        ms_info(AppName, "Done!")
    except Exception as exp:
        ms_error(AppName, str(exp))

def decrypt_dirUi():
    global file, name
    try:
        filesindir = os.listdir(directory)
        for filesindirs in filesindir:
            path = os.path.join(filesindirs)
            file = os.path.join(str(directory), path)
            decryptUi(True)
        nm.lineEdit.clear()
        ui.lineEdit.clear()
        ui.lineEdit_2.clear()
        name = ""
        ms_info(AppName, "Done!")
    except Exception as exp:
        ms_error(AppName, str(exp))

def encrypt_dirUi():
    global file, name
    try:
        filesindir = os.listdir(directory)
        for filesindirs in filesindir:
            path = os.path.join(filesindirs)
            file = os.path.join(str(directory), path)
            encryptUi(True)
        nm.lineEdit.clear()
        ui.lineEdit.clear()
        ui.lineEdit_2.clear()
        name = ""
        ms_info(AppName, "Done!")
    except Exception as exp:
        ms_error(AppName, str(exp))

def decrypt_dir_blow():
    global file, name
    try:
        filesindir = os.listdir(directory)
        for filesindirs in filesindir:
            path = os.path.join(filesindirs)
            file = os.path.join(str(directory), path)
            decrypt_blow(True)
        mn.lineEdit.clear()
        nm.lineEdit.clear()
        name = ""
        ms_info(AppName, "Done!")
    except Exception as exp:
        ms_error(AppName, str(exp))

def encrypt_dir_blow():
    global file, name
    try:
        filesindir = os.listdir(directory)
        for filesindirs in filesindir:
            path = os.path.join(filesindirs)
            file = os.path.join(str(directory), path)
            encrypt_blow(True)
        mn.lineEdit.clear()
        nm.lineEdit.clear()
        name = ""
        ms_info(AppName, "Done!")
    except Exception as exp:
        ms_error(AppName, str(exp))

def btn_crypt(choice: bool):
    if choice: # AES | BlowFish
        if choiceSettings == 0:
            if st.checkBox.isChecked():
                if st.radioButton.isChecked():
                    encrypt_dirUi()
                elif st.radioButton_2.isChecked():
                    decrypt_dirUi()
            else:
                if st.radioButton.isChecked():
                    encryptUi()
                elif st.radioButton_2.isChecked():
                    decryptUi()
        elif choiceSettings == 2:
            if st.checkBox.isChecked():
                if st.radioButton.isChecked():
                    encrypt_dir_blow()
                elif st.radioButton_2.isChecked():
                    decrypt_dir_blow()
            else:
                if st.radioButton.isChecked():
                    encrypt_blow()
                elif st.radioButton_2.isChecked():
                    decrypt_blow()
    elif not choice: # RSA
        if st.checkBox.isChecked():
            if st.radioButton.isChecked():
                encrypt_dir()
            elif st.radioButton_2.isChecked():
                decrypt_dir()
        else:
            if st.radioButton.isChecked():
                encrypt()
            elif st.radioButton_2.isChecked():
                decrypt()

def ms_info(title, text, information=None, detail=None):
    ms = QtWidgets.QMessageBox()
    ms.setIcon(QtWidgets.QMessageBox.Information)
    ms.setText(text)
    ms.setWindowTitle(title)
    if information != None:
        ms.setInformativeText(information)
    if detail != None:
        ms.setDetailedText(detail)
    ms.exec_()

def ms_error(title, text, information=None, detail=None):
    ms = QtWidgets.QMessageBox()
    ms.setIcon(QtWidgets.QMessageBox.Critical)
    ms.setText(text)
    ms.setWindowTitle(title)
    if information != None:
        ms.setInformativeText(information)
    if detail != None:
        ms.setDetailedText(detail)
    ms.exec_()

def ms_warning(title, text, information=None, detail=None):
    ms = QtWidgets.QMessageBox()
    ms.setIcon(QtWidgets.QMessageBox.Warning)
    ms.setText(text)
    ms.setWindowTitle(title)
    if information != None:
        ms.setInformativeText(information)
    if detail != None:
        ms.setDetailedText(detail)
    ms.exec_()

def qtOpen(choice=True):
    if choice:
        a = QtWidgets.QFileDialog.getOpenFileName()[0]
    else:
        a = QtWidgets.QFileDialog.getExistingDirectory()
    return a

def takefile(choice: bool):
    global file, directory
    try:
        file = qtOpen()
        directory = os.path.dirname(file)
        if choice: # RSA
            mn.lineEdit.setText(file)
        elif not choice: # Cipher
            ui.lineEdit.setText(file)
    except:
        ms_warning(AppName, "Файл не выбран")

def takedir(choice: bool):
    global directory
    try:
        directory = qtOpen(False)
        if choice: # RSA
            mn.lineEdit.setText(directory)
        elif not choice: # Cipher
            ui.lineEdit.setText(directory)
    except:
        ms_warning(AppName, "Файл не выбран")

def saveName():
    global name
    name = nm.lineEdit.text()
    NameDialog.close()

def openWind(openW: int):
    global choiceSettings
    if openW == 1: # RSA
        MainDialog.show()
        choiceSettings = 1
    elif openW == 0: # AES
        CCDialog.show()
        choiceSettings = 0
    elif openW == 2: # BlowFish
        CCDialog.setWindowTitle("DarkCryptorBlowFish")
        CCDialog.show()
        Start.close()
        choiceSettings = 2
    Start.close()

def take_public():
    global publicKey
    try:
        pub = qtOpen()
        with open(pub, "rb") as publ:
            publicKey = publ.read()
        if not "PUBLIC" in publicKey.decode("utf-8"):
            ms_info(AppName, "Выбран не тот файл!")
            publicKey = ""
    except:
        ms_warning(AppName, "Файл не выбран")

def take_private():
    global privateKey
    try:
        priv = qtOpen()
        with open(priv, "rb") as priva:
            privateKey = priva.read()
        if not "PRIVATE" in privateKey.decode("utf-8"):
            ms_info(AppName, "Выбран не тот файл")
            privateKey = ""
    except:
        ms_warning(AppName, "Файл не выбран")

def takebtn(choice: bool):
    if choice:
        if st.checkBox.isChecked():
            takedir(True)
        else:
            takefile(True)
    elif not choice:
        if st.checkBox.isChecked():
            takedir(False)
        else:
            takefile(False)

def rename():
    if st.checkBox_3.isChecked():
        NameDialog.show()
    else:
        ms_info(AppName, "Чтобы работало изменения имени файла включите его в настройках")

def choice_settings_save():
    if choiceSettings == 1:
        settings_save(False)
    elif choiceSettings == 0 or 2:
        settings_save(True)

def showInfo(button: str):
    ms_info(button, "Откройте \"show details...\"", detail=infoEnc[button])

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    CCDialog = QtWidgets.QDialog()
    MainDialog = QtWidgets.QDialog()
    NameDialog = QtWidgets.QDialog()
    SettingsDialog = QtWidgets.QDialog()
    Start = QtWidgets.QDialog()
    ui = Ui_Dialog()
    st = Ui_Settings()
    mn = Ui_Main()
    nm = Ui_Name()
    start = Ui_StartMenu()
    start.setupUi(Start)
    st.setupUi(SettingsDialog)
    nm.setupUi(NameDialog)
    mn.setupUi(MainDialog)
    ui.setupUi(CCDialog)
    Start.show()

    mn.pushButton_7.clicked.connect(take_private)
    mn.pushButton_6.clicked.connect(take_public)
    mn.pushButton.clicked.connect(lambda: takebtn(True))
    mn.pushButton_5.clicked.connect(lambda: NameDialog.show())
    mn.pushButton_2.clicked.connect(lambda: btn_crypt(False))
    mn.pushButton_4.clicked.connect(lambda: SettingsDialog.show())
    mn.pushButton_3.clicked.connect(mn.runCreate)
    nm.pushButton.clicked.connect(saveName)
    start.RSA.clicked.connect(lambda: openWind(1))
    start.AES.clicked.connect(lambda: openWind(0))
    start.BlowFish.clicked.connect(lambda: openWind(2))
    start.AESinfo.clicked.connect(lambda: showInfo("AES"))
    start.BlowFishInfo.clicked.connect(lambda: showInfo("BlowFish"))
    start.RSAinfo.clicked.connect(lambda: showInfo("RSA"))
    st.pushButton.clicked.connect(choice_settings_save)
    ui.pushButton.clicked.connect(lambda: takebtn(False))
    ui.pushButton_3.clicked.connect(getpassword)
    ui.pushButton_5.clicked.connect(lambda: NameDialog.show())
    ui.pushButton_2.clicked.connect(lambda: btn_crypt(True))
    ui.pushButton_4.clicked.connect(lambda: SettingsDialog.show())

    app.exec_()
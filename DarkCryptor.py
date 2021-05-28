#!/home/darkpydeu/Python/venv/bin/python3
"""
<-*- coding: utf-8 -*->
Powered by -> {-*> DarkPyDeu <*-}
# DarkCryptor 1.0.2
"""
from PyQt5 import QtCore, QtGui, QtWidgets
from cryptography.fernet import Fernet
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, Blowfish
from Crypto.Util import Padding
from Crypto import Random
from Modules.CustomAES import encryptFile, decryptFile, encryptStream
from PIL import Image, ImageDraw
from random import randint
from random import shuffle
from io import BytesIO
from re import findall
import os

keys = ""
file = ""
directory = ""
privateKey = ""
publicKey = ""
name = None
choiceSettings = None
bufferSize = 512 * 1024
AppName = "DarkCryptor"
infoEnc = {
    "AES": "AES - Способен зашифровать любой файл ключом до 1024 бит ( но ключ надо запонить | записать куда-либо )",
    "BlowFish": "BlowFish - Способен зашифровать любой файл ключом от 4 бит до 50 бит ( но ключ надо запонить | записать куда-либо )",
    "RSA": "RSA - Способен зашифровать любой файл ключом от 1024 бит ( ключ храниться в файлах public.key & private.key )",
    "Steganography": """Steganography -  Записывает зашифрованый текст ( ключ будет в отдельном файле ) в изображение и 
    записывает ключевые точки в текстовый файл, который будет зашифрован AES алгоритмом."""
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
        ms_box(AppName, "Производиться создание ключа, пожалуйста ожидайте", "info",detail="Иногда проверяйте файл")
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

class Ui_StartMenu(object):
    def setupUi(self, StartMenu):
        StartMenu.setObjectName("StartMenu")
        StartMenu.resize(200, 175)
        StartMenu.setMinimumSize(QtCore.QSize(200, 175))
        StartMenu.setMaximumSize(QtCore.QSize(200, 175))
        StartMenu.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.frame = QtWidgets.QFrame(StartMenu)
        self.frame.setGeometry(QtCore.QRect(0, 0, 200, 175))
        self.frame.setStyleSheet("background-color: black; border-radius: 15px")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.BlowFish = QtWidgets.QPushButton(StartMenu)
        self.BlowFish.setGeometry(QtCore.QRect(10, 50, 145, 35))
        self.BlowFish.setStyleSheet("background-color: rgb(51, 51, 51);color: rgb(255, 62, 0);")
        self.BlowFish.setObjectName("BlowFish")
        self.AES = QtWidgets.QPushButton(StartMenu)
        self.AES.setGeometry(QtCore.QRect(10, 10, 145, 35))
        self.AES.setStyleSheet("background-color: rgb(51, 51, 51);color: rgb(255, 62, 0);")
        self.AES.setObjectName("AES")
        self.RSA = QtWidgets.QPushButton(StartMenu)
        self.RSA.setGeometry(QtCore.QRect(10, 90, 145, 35))
        self.RSA.setStyleSheet("background-color: rgb(51, 51, 51);color: rgb(255, 62, 0);")
        self.RSA.setObjectName("RSA")
        self.AESinfo = QtWidgets.QPushButton(StartMenu)
        self.AESinfo.setGeometry(QtCore.QRect(155, 10, 35, 35))
        self.AESinfo.setStyleSheet("background-color: rgb(51, 51, 51);color: rgb(255, 62, 0);")
        self.AESinfo.setObjectName("AESinfo")
        self.BlowFishInfo = QtWidgets.QPushButton(StartMenu)
        self.BlowFishInfo.setGeometry(QtCore.QRect(155, 50, 35, 35))
        self.BlowFishInfo.setStyleSheet("background-color: rgb(51, 51, 51);color: rgb(255, 62, 0);")
        self.BlowFishInfo.setObjectName("BlowFishInfo")
        self.RSAinfo = QtWidgets.QPushButton(StartMenu)
        self.RSAinfo.setGeometry(QtCore.QRect(155, 90, 35, 35))
        self.RSAinfo.setStyleSheet("background-color: rgb(51, 51, 51);color: rgb(255, 62, 0);")
        self.RSAinfo.setObjectName("RSAinfo")
        self.Steganography = QtWidgets.QPushButton(StartMenu)
        self.Steganography.setGeometry(QtCore.QRect(10, 130, 145, 35))
        self.Steganography.setStyleSheet("background-color: rgb(51, 51, 51);color: rgb(255, 62, 0);")
        self.Steganography.setObjectName("Steganography")
        self.SteganoInfo = QtWidgets.QPushButton(StartMenu)
        self.SteganoInfo.setGeometry(QtCore.QRect(155, 130, 35, 35))
        self.SteganoInfo.setStyleSheet("background-color: rgb(51, 51, 51);color: rgb(255, 62, 0);")
        self.SteganoInfo.setObjectName("SteganoInfo")
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
        self.Steganography.setText(_translate("StartMenu", "Steganography"))
        self.SteganoInfo.setText(_translate("StartMenu", "i"))

class Ui_Stegano(object):
    def setupUi(self, Stegano):
        Stegano.setObjectName("Stegano")
        Stegano.resize(1101, 625)
        Stegano.setMinimumSize(QtCore.QSize(1101, 625))
        Stegano.setMaximumSize(QtCore.QSize(1101, 625))
        Stegano.setStyleSheet("background-color: black;")
        self.PlainTextDecrypted = QtWidgets.QPlainTextEdit(Stegano)
        self.PlainTextDecrypted.setGeometry(QtCore.QRect(5, 5, 561, 616))
        self.PlainTextDecrypted.setStyleSheet("background-color: rgb(51, 51, 51);color: rgb(255, 62, 0);")
        self.PlainTextDecrypted.setObjectName("PlainTextDecrypted")
        self.ImageLine = QtWidgets.QLineEdit(Stegano)
        self.ImageLine.setGeometry(QtCore.QRect(570, 5, 440, 35))
        self.ImageLine.setStyleSheet("background-color: rgb(51, 51, 51);color: rgb(255, 62, 0);")
        self.ImageLine.setReadOnly(True)
        self.ImageLine.setObjectName("ImageLine")
        self.TakeImage = QtWidgets.QPushButton(Stegano)
        self.TakeImage.setGeometry(QtCore.QRect(1012, 5, 88, 35))
        self.TakeImage.setStyleSheet("background-color: rgb(51, 51, 51);color: rgb(255, 62, 0);")
        self.TakeImage.setObjectName("TakeImage")
        self.PasswordLine = QtWidgets.QLineEdit(Stegano)
        self.PasswordLine.setGeometry(QtCore.QRect(570, 42, 529, 35))
        self.PasswordLine.setStyleSheet("background-color: rgb(51, 51, 51);color: rgb(255, 62, 0);")
        self.PasswordLine.setObjectName("PasswordLine")
        self.PlainTextToEncrypt = QtWidgets.QPlainTextEdit(Stegano)
        self.PlainTextToEncrypt.setGeometry(QtCore.QRect(570, 80, 526, 501))
        self.PlainTextToEncrypt.setStyleSheet("background-color: rgb(51, 51, 51);color: rgb(255, 62, 0);")
        self.PlainTextToEncrypt.setObjectName("PlainTextToEncrypt")
        self.S = QtWidgets.QPushButton(Stegano)
        self.S.setGeometry(QtCore.QRect(570, 585, 100, 35))
        self.S.setStyleSheet("background-color: rgb(51, 51, 51);color: rgb(255, 62, 0);")
        self.S.setObjectName("S")
        self.pushButton_3 = QtWidgets.QPushButton(Stegano)
        self.pushButton_3.setGeometry(QtCore.QRect(987, 585, 111, 35))
        self.pushButton_3.setStyleSheet("background-color: rgb(51, 51, 51);color: rgb(255, 62, 0);")
        self.pushButton_3.setObjectName("pushButton_3")
        self.ImageLine_2 = QtWidgets.QLineEdit(Stegano)
        self.ImageLine_2.setGeometry(QtCore.QRect(570, 80, 440, 35))
        self.ImageLine_2.setStyleSheet("background-color: rgb(51, 51, 51);color: rgb(255, 62, 0);")
        self.ImageLine_2.setReadOnly(True)
        self.ImageLine_2.setObjectName("ImageLine_2")
        self.ImageLine_2.hide()
        self.TakeImage_2 = QtWidgets.QPushButton(Stegano)
        self.TakeImage_2.setGeometry(QtCore.QRect(1012, 80, 88, 35))
        self.TakeImage_2.setStyleSheet("background-color: rgb(51, 51, 51);color: rgb(255, 62, 0);")
        self.TakeImage_2.setObjectName("TakeImage_2")
        self.TakeImage_2.hide()
        self.PasswordLineNE = QtWidgets.QLineEdit(Stegano)
        self.PasswordLineNE.setGeometry(QtCore.QRect(570, 120, 440, 35))
        self.PasswordLineNE.setStyleSheet("background-color: rgb(51, 51, 51);color: rgb(255, 62, 0);")
        self.PasswordLineNE.setReadOnly(True)
        self.PasswordLineNE.setObjectName("PasswordLineNE")
        self.PasswordLineNE.hide()
        self.TakePasswordNE = QtWidgets.QPushButton(Stegano)
        self.TakePasswordNE.setGeometry(QtCore.QRect(1012, 120, 88, 35))
        self.TakePasswordNE.setStyleSheet("background-color: rgb(51, 51, 51);color: rgb(255, 62, 0);")
        self.TakePasswordNE.setObjectName("TakePasswordNE")
        self.TakePasswordNE.hide()
        self.retranslateUi(Stegano)
        QtCore.QMetaObject.connectSlotsByName(Stegano)

    def retranslateUi(self, Stegano):
        _translate = QtCore.QCoreApplication.translate
        Stegano.setWindowTitle(_translate("Stegano", "Stegano"))
        self.ImageLine.setPlaceholderText(_translate("Stegano", "Изображение"))
        self.TakeImage.setText(_translate("Stegano", "Open"))
        self.PasswordLine.setPlaceholderText(_translate("Stegano", "Пароль"))
        self.PlainTextToEncrypt.setPlaceholderText(_translate("Stegano", "Текст для шифрования"))
        self.PlainTextDecrypted.setPlaceholderText(_translate("Stegano", "Расшифрованый текст"))
        self.PlainTextDecrypted.setReadOnly(True)
        self.S.setText(_translate("Stegano", "Настройки"))
        self.pushButton_3.setText(_translate("Stegano", "Шифровать"))
        self.ImageLine_2.setPlaceholderText(_translate("Stegano", "Файловый пароль"))
        self.TakeImage_2.setText(_translate("Stegano", "Open"))
        self.PasswordLineNE.setPlaceholderText(_translate("Stegano", "Файловый пароль ( читабельный )"))
        self.TakePasswordNE.setText(_translate("Stegano", "Open"))

class Ui_StegSett(object):
    def setupUi(self, StegSett):
        StegSett.setObjectName("StegSett")
        StegSett.resize(170, 95)
        StegSett.setMinimumSize(QtCore.QSize(170, 95))
        StegSett.setMaximumSize(QtCore.QSize(170, 95))
        StegSett.setStyleSheet("background-color: black;")
        self.EncryptButn = QtWidgets.QRadioButton(StegSett)
        self.EncryptButn.setGeometry(QtCore.QRect(0, 5, 171, 24))
        self.EncryptButn.setStyleSheet("color: rgb(255, 62, 0);")
        self.EncryptButn.setObjectName("EncryptButn")
        self.DecryptButn = QtWidgets.QRadioButton(StegSett)
        self.DecryptButn.setGeometry(QtCore.QRect(0, 30, 171, 24))
        self.DecryptButn.setStyleSheet("color: rgb(255, 62, 0);")
        self.DecryptButn.setObjectName("DecryptButn")
        self.pushButton = QtWidgets.QPushButton(StegSett)
        self.pushButton.setGeometry(QtCore.QRect(5, 60, 161, 31))
        self.pushButton.setStyleSheet("background-color: rgb(51, 51, 51);color: rgb(255, 62, 0);")
        self.pushButton.setObjectName("pushButton")
        self.retranslateUi(StegSett)
        QtCore.QMetaObject.connectSlotsByName(StegSett)

    def retranslateUi(self, StegSett):
        _translate = QtCore.QCoreApplication.translate
        StegSett.setWindowTitle(_translate("StegSett", "Settings"))
        self.EncryptButn.setText(_translate("StegSett", "Шифровать"))
        self.EncryptButn.setChecked(True)
        self.DecryptButn.setText(_translate("StegSett", "Расшифровать"))
        self.pushButton.setText(_translate("StegSett", "Сохранить"))

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
        ms_box(AppName, "Введите число байтов в пароле", "info", information="байт = 1 символ")

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
            cipher = Blowfish.new(key, Blowfish.MODE_EAX, iv)
            with open(file, "r") as f:
                readFileText = f.read()
            if st.checkBox_2.isChecked():
                savepass = open("CCSavePass.txt", "w")
                if name != "" and name != None:
                    savepass.write(f"\n {name} ::: {password}")
                else:
                    savepass.write(f"\n {file}.DC ::: {password}")
                savepass.close()
            plaintext = Padding.pad(bytes(readFileText.encode()), 1000, "iso7816")
            msg = iv + cipher.encrypt(plaintext)
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
            ms_box(AppName, "Done!", "info")
    except Exception as exp:
        if not dirCrypt:
            ms_box(AppName, str(exp), "err")

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
        cipher = Blowfish.new(key, Blowfish.MODE_EAX, iv)
        msg = Padding.unpad(cipher.decrypt(ciphertext), 1000, "iso7816")
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
            ms_box(AppName, "Done!", "info")
    except Exception as exp:
        if not dirCrypt:
            ms_box(AppName, str(exp), "err")

def encrypt_image():
    global keys
    try:
        Key = Fernet.generate_key()
        imageName = steg.ImageLine.text()
        img = Image.open(imageName)
        password = steg.PasswordLine.text()
        draw = ImageDraw.Draw(img)
        width = img.size[0]
        height = img.size[1]
        pix = img.load()
        fullPath = os.path.join(directory, "keys.txt")
        passwordFile = open(os.path.join(directory, "passwordImage.txt"), "wb")
        f = open(fullPath, 'wb')
        fIn = steg.PlainTextToEncrypt.toPlainText()
        cipher = Fernet(Key)
        fOut = cipher.encrypt(bytes(fIn.encode()))

        for elem in ([ord(elem) for elem in fOut.decode()]):
            key = (randint(1, width - 10), randint(1, height - 10))
            g, b = pix[key][1:3]
            draw.point(key, (elem, g, b))
            keys += str(key) + '\n'

        keys = BytesIO(bytes(keys.encode("utf-8")))

        encryptStream(keys, f, password, bufferSize)
        passwordFile.write(Key)
        passwordFile.close()
        img.save(f"{imageName}.png", "PNG")
        f.close()
        steg.ImageLine.clear()
        steg.PlainTextToEncrypt.clear()
        steg.PasswordLine.clear()
        ms_box("DarkCryptor", "Done", "info", detail=f"Картинка сохранена в директории \"{imageName}.png\".\nКлючи сохранены в файл \"{fullPath}\"")
    except Exception as exp:
        ms_box("DarkCryptor", str(exp), "err")

def decrypt_image():
    try:
        a = []
        keys = []
        imageName = steg.ImageLine.text()
        img = Image.open(imageName)
        password = steg.PasswordLine.text()
        passwordFile = steg.PasswordLineNE.text()
        pix = img.load()
        file = steg.ImageLine_2.text()
        decFile = "11ppp1pp1p1pp.txt"
        decryptFile(file, decFile, password, bufferSize)
        with open(passwordFile, "rb") as fPass:
            Key = fPass.read()
            cipher = Fernet(Key)
        with open(decFile, "r") as fOut:
            y = str([line.strip() for line in fOut])
            os.remove(decFile)
        for i in range(len(findall(r'\((\d+)\,', y))):
            keys.append((int(findall(r'\((\d+)\,', y)[i]), int(findall(r'\,\s(\d+)\)', y)[i])))
        for key in keys:
            a.append(pix[tuple(key)][0])
        complitedText = ''.join([chr(elem) for elem in a])
        outText = cipher.decrypt(bytes(complitedText.encode()))
        steg.PlainTextDecrypted.setPlainText(outText.decode())
        steg.PasswordLine.clear()
        steg.ImageLine.clear()
        steg.ImageLine_2.clear()
        steg.PasswordLineNE.clear()
    except Exception as exp:
        ms_box("DarkCryptor", str(exp), "err")

def encryptUi(dirCrypt=False):
    global name
    try:
        password = ui.lineEdit_2.text()
        if name != '' and name != None:
            fullPath = os.path.join(directory, name)
        else:
            fullPath = os.path.join(directory, str(file) + ".DC")
        encryptFile(str(file), fullPath, password, bufferSize)
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
            ui.lineEdit.clear()
            ui.lineEdit_2.clear()
            nm.lineEdit.clear()
            name = ""
            ms_box(AppName, "Done!", "info")
    except Exception as exp:
        if not dirCrypt:
            ms_box(AppName, str(exp), "err")

def decryptUi(dirCrypt=False):
    global name
    try:
        passworded = ui.lineEdit_2.text()
        if name != '' and name != None:
            fullPath = os.path.join(directory, str(name))
        else:
            fullPath = os.path.join(directory, str(os.path.splitext(str(file))[0]))
        decryptFile(str(file), fullPath, passworded, bufferSize)
        if not st.checkBox_4.isChecked():
            os.remove(str(file))
        if not dirCrypt:
            nm.lineEdit.clear()
            ui.lineEdit.clear()
            ui.lineEdit_2.clear()
            name = ""
            ms_box(AppName, "Done!", "info")
    except Exception as exp:
        if not dirCrypt:
            ms_box(AppName, str(exp), "err")

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
            mn.lineEdit.clear()
            nm.lineEdit.clear()
            name = ""
            ms_box(AppName, "Done!", "info")
    except Exception as exp:
        if not dirCrypt:
            ms_box(AppName, str(exp), "err")

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
            mn.lineEdit.clear()
            nm.lineEdit.clear()
            name = ""
            ms_box(AppName, "Done!", "info")
    except Exception as exp:
        if not dirCrypt:
            ms_box(AppName, str(exp), "err")

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
        ms_box(AppName, "Done!", "info")
    except Exception as exp:
        ms_box(AppName, str(exp), "err")

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
        ms_box(AppName, "Done!", "info")
    except Exception as exp:
        ms_box(AppName, str(exp), "err")

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
        ms_box(AppName, "Done!", "info")
    except Exception as exp:
        ms_box(AppName, str(exp), "err")

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
        ms_box(AppName, "Done!", "info")
    except Exception as exp:
        ms_box(AppName, str(exp), "err")

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
        ms_box(AppName, "Done!", "info")
    except Exception as exp:
        ms_box(AppName, str(exp), "err")

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
        ms_box(AppName, "Done!", "info")
    except Exception as exp:
        ms_box(AppName, str(exp), "err")

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

def ms_box(title, text, icon, information=None, detail=None):
    ms = QtWidgets.QMessageBox()
    if icon == "err":
        ms.setIcon(QtWidgets.QMessageBox.Critical)
    elif icon == "info":
        ms.setIcon(QtWidgets.QMessageBox.Information)
    elif icon == "war":
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

def takefile(choice=0):
    global file, directory
    try:
        file = qtOpen()
        directory = os.path.dirname(file)
        if choice == 0: # RSA
            mn.lineEdit.setText(file)
        elif choice == 1: # Cipher
            ui.lineEdit.setText(file)
        elif choice == 2: # stegano Image line
            steg.ImageLine.setText(file)
        elif choice == 3:
            steg.ImageLine_2.setText(file)
        elif choice == 4: # файловый пароль не читабельный
            steg.PasswordLineNE.setText(file)
    except:
        ms_box(AppName, "Файл не выбран", "war")

def takedir(choice: bool):
    global directory
    try:
        directory = qtOpen(False)
        if choice: # RSA
            mn.lineEdit.setText(directory)
        elif not choice: # Cipher
            ui.lineEdit.setText(directory)
    except:
        ms_box(AppName, "Файл не выбран", "war")

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
    elif openW == 3:
        SteganoDialog.show()
        Start.close()
    Start.close()

def take_public():
    global publicKey
    try:
        pub = qtOpen()
        with open(pub, "rb") as publ:
            publicKey = publ.read()
        if not "PUBLIC" in publicKey.decode("utf-8"):
            ms_box(AppName, "Выбран не тот файл!", "war")
            publicKey = ""
    except:
        ms_box(AppName, "Файл не выбран", "war")

def take_private():
    global privateKey
    try:
        priv = qtOpen()
        with open(priv, "rb") as priva:
            privateKey = priva.read()
        if not "PRIVATE" in privateKey.decode("utf-8"):
            ms_box(AppName, "Выбран не тот файл", "war")
            privateKey = ""
    except:
        ms_box(AppName, "Файл не выбран", "war")

def takebtn(choice: int):
    if choice:
        if st.checkBox.isChecked():
            takedir(True)
        else:
            takefile(0)
    elif not choice:
        if st.checkBox.isChecked():
            takedir(False)
        else:
            takefile(1)

def rename():
    if st.checkBox_3.isChecked():
        NameDialog.show()
    else:
        ms_box(AppName, "Чтобы работало изменения имени файла включите его в настройках", "info")

def choice_settings_save():
    if choiceSettings == 1:
        settings_save(False)
    elif choiceSettings == 0 or 2:
        settings_save(True)

def showInfo(button: str):
    ms_box(button, "Откройте \"show details...\"", "info",detail=infoEnc[button])

def settings_Save_Steg():
    if stegS.EncryptButn.isChecked():
        steg.PlainTextToEncrypt.show()
        steg.ImageLine_2.hide()
        steg.TakeImage_2.hide()
        steg.PlainTextDecrypted.clear()
        steg.PasswordLineNE.hide()
        steg.TakePasswordNE.hide()
        steg.pushButton_3.setText("Шифровать")
    elif stegS.DecryptButn.isChecked():
        steg.PlainTextToEncrypt.hide()
        steg.TakeImage_2.show()
        steg.ImageLine_2.show()
        steg.PasswordLineNE.show()
        steg.TakePasswordNE.show()
        steg.pushButton_3.setText("Расшифровать")
    StegSettDial.close()

def CryptButton_steg(button: str):
    if button.lower() == "шифровать":
        encrypt_image()
    elif button.lower() == "расшифровать":
        decrypt_image()

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    CCDialog = QtWidgets.QDialog()
    MainDialog = QtWidgets.QDialog()
    NameDialog = QtWidgets.QDialog()
    SettingsDialog = QtWidgets.QDialog()
    Start = QtWidgets.QDialog()
    SteganoDialog = QtWidgets.QDialog()
    StegSettDial = QtWidgets.QDialog()
    ui = Ui_Dialog()
    st = Ui_Settings()
    mn = Ui_Main()
    nm = Ui_Name()
    start = Ui_StartMenu()
    steg = Ui_Stegano()
    stegS = Ui_StegSett()
    start.setupUi(Start)
    st.setupUi(SettingsDialog)
    nm.setupUi(NameDialog)
    mn.setupUi(MainDialog)
    ui.setupUi(CCDialog)
    steg.setupUi(SteganoDialog)
    stegS.setupUi(StegSettDial)
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
    start.SteganoInfo.clicked.connect(lambda: showInfo("Steganography"))
    start.Steganography.clicked.connect(lambda: openWind(3))
    st.pushButton.clicked.connect(choice_settings_save)
    ui.pushButton.clicked.connect(lambda: takebtn(False))
    ui.pushButton_3.clicked.connect(getpassword)
    ui.pushButton_5.clicked.connect(lambda: NameDialog.show())
    ui.pushButton_2.clicked.connect(lambda: btn_crypt(True))
    ui.pushButton_4.clicked.connect(lambda: SettingsDialog.show())
    steg.TakeImage.clicked.connect(lambda: takefile(2))
    steg.TakeImage_2.clicked.connect(lambda: takefile(3))
    steg.pushButton_3.clicked.connect(lambda: CryptButton_steg(steg.pushButton_3.text()))
    steg.S.clicked.connect(lambda: StegSettDial.show())
    steg.TakePasswordNE.clicked.connect(lambda: takefile(4))
    stegS.pushButton.clicked.connect(settings_Save_Steg)

    app.exec_()
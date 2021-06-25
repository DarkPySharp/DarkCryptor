#!/home/darkpydeu/Python/venv/bin/python3
"""
<-*- coding: utf-8 -*->
Powered by -> {-*> DarkPyDeu <*-}
# DarkCryptor 2.0.0
#
"""
from PyQt5 import QtCore, QtGui, QtWidgets
from cryptography.fernet import Fernet
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, Blowfish, DES3
from Crypto.Util import Padding
from Crypto import Random
from Modules.CustomAES import encryptFile, decryptFile, encryptStream
from PIL import Image, ImageDraw
from random import randint
from random import choice
from io import BytesIO
from re import findall
from string import ascii_letters, digits, hexdigits, punctuation
import os

keys = ""
file = ""
directory = ""
privateKey = ""
publicKey = ""
name = ""
choiceSettings = None
bufferSize = 512 * 1024
progress = 0
ROOT = os.getcwd()
APP_NAME = "DarkCryptor"
ICON = "Modules/Pictures/DarkC_Ico.png"
infoEnc = {
    "AES": "AES - Способен зашифровать любой файл ключом до 1024 бит ( но ключ надо запонить | записать куда-либо ) ключ генерируется, который делится на 4",
    "BlowFish": "BlowFish - Способен зашифровать любой файл ключом от 4 бит до 50 бит ( но ключ надо запонить | записать куда-либо ) ключ генерируется, который делится на 4",
    "RSA": """RSA - Способен зашифровать любой файл ключом от 1024 бит { длина ключа зависит от размера шифруемого файла }
    ( ключ храниться в файлах public.key & private.key )""",
    "Steganography": """Steganography -  Записывает зашифрованый текст ( ключ будет в отдельном файле ) в изображение и 
    записывает ключевые точки в текстовый файл, который будет зашифрован AES алгоритмом. { фотография не должна быть в формате png }""",
    "3DES": "3DES - шифрует только англиский текст"
}

class Ui_Main(object):
    def __init__(self):
        global CSS
        with open("DarkCryptor/DarkC.css", "r") as CSS_READ:
            CSS = CSS_READ.read()

    def setupUi(self, Main):
        Main.setObjectName("Main")
        Main.resize(1012, 717)
        Main.setMinimumSize(QtCore.QSize(1012, 717))
        Main.setMaximumSize(QtCore.QSize(1012, 717))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Modules/Pictures/DarkC_Ico.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Main.setWindowIcon(icon)
        Main.setStyleSheet(CSS)
        self.verticalLayout = QtWidgets.QVBoxLayout(Main)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Header = QtWidgets.QFrame(Main)
        self.Header.setMaximumSize(QtCore.QSize(16777215, 37))
        self.Header.setStyleSheet("")
        self.Header.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Header.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Header.setObjectName("Header")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.Header)
        self.horizontalLayout.setContentsMargins(0, 0, 5, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.Header)
        self.label.setMaximumSize(QtCore.QSize(35, 16777215))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("Modules/Pictures/DarkC_Ico.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.HeaderText = QtWidgets.QLabel(self.Header)
        font = QtGui.QFont()
        font.setFamily("Cantarell")
        font.setBold(True)
        font.setWeight(75)
        self.HeaderText.setFont(font)
        self.HeaderText.setAlignment(QtCore.Qt.AlignCenter)
        self.HeaderText.setObjectName("HeaderText")
        self.horizontalLayout.addWidget(self.HeaderText)
        self.closeButton = QtWidgets.QPushButton(self.Header)
        self.closeButton.setMaximumSize(QtCore.QSize(35, 27))
        self.closeButton.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.closeButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Modules/Pictures/Close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.closeButton.setIcon(icon1)
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        self.verticalLayout.addWidget(self.Header)
        self.Body = QtWidgets.QFrame(Main)
        self.Body.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.Body.setStyleSheet(CSS)
        self.Body.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Body.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Body.setObjectName("Body")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.Body)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Menu = QtWidgets.QFrame(self.Body)
        self.Menu.setMinimumSize(QtCore.QSize(60, 680))
        self.Menu.setMaximumSize(QtCore.QSize(60, 680))
        self.Menu.setStyleSheet("")
        self.Menu.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Menu.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Menu.setObjectName("Menu")
        self.OpenMenu = QtWidgets.QPushButton(self.Menu)
        self.OpenMenu.setGeometry(QtCore.QRect(5, 5, 50, 50))
        self.OpenMenu.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("Modules/Pictures/menu.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.OpenMenu.setIcon(icon2)
        self.OpenMenu.setIconSize(QtCore.QSize(26, 26))
        self.OpenMenu.setObjectName("OpenMenu")
        self.AES = QtWidgets.QPushButton(self.Menu)
        self.AES.setGeometry(QtCore.QRect(5, 115, 50, 50))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.AES.setFont(font)
        self.AES.setIconSize(QtCore.QSize(26, 26))
        self.AES.setObjectName("AES")
        self.RSA = QtWidgets.QPushButton(self.Menu)
        self.RSA.setGeometry(QtCore.QRect(5, 170, 50, 50))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.RSA.setFont(font)
        self.RSA.setIconSize(QtCore.QSize(26, 26))
        self.RSA.setObjectName("RSA")
        self.ThreeDes = QtWidgets.QPushButton(self.Menu)
        self.ThreeDes.setGeometry(QtCore.QRect(5, 225, 50, 50))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.ThreeDes.setFont(font)
        self.ThreeDes.setIconSize(QtCore.QSize(26, 26))
        self.ThreeDes.setObjectName("ThreeDes")
        self.BlowFish = QtWidgets.QPushButton(self.Menu)
        self.BlowFish.setGeometry(QtCore.QRect(5, 280, 50, 50))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.BlowFish.setFont(font)
        self.BlowFish.setIconSize(QtCore.QSize(26, 26))
        self.BlowFish.setObjectName("BlowFish")
        self.Steganography = QtWidgets.QPushButton(self.Menu)
        self.Steganography.setGeometry(QtCore.QRect(5, 335, 50, 50))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Steganography.setFont(font)
        self.Steganography.setIconSize(QtCore.QSize(26, 26))
        self.Steganography.setObjectName("Steganography")
        self.SettingsButt = QtWidgets.QPushButton(self.Menu)
        self.SettingsButt.setGeometry(QtCore.QRect(5, 624, 50, 50))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.SettingsButt.setFont(font)
        self.SettingsButt.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("Modules/Pictures/settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SettingsButt.setIcon(icon3)
        self.SettingsButt.setIconSize(QtCore.QSize(36, 36))
        self.SettingsButt.setObjectName("SettingsButt")
        self.Home = QtWidgets.QPushButton(self.Menu)
        self.Home.setGeometry(QtCore.QRect(5, 60, 50, 50))
        font = QtGui.QFont()
        font.setWeight(50)
        self.Home.setFont(font)
        self.Home.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("Modules/Pictures/home.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Home.setIcon(icon4)
        self.Home.setIconSize(QtCore.QSize(28, 28))
        self.Home.setObjectName("Home")
        self.infoAES = QtWidgets.QPushButton(self.Menu)
        self.infoAES.setGeometry(QtCore.QRect(60, 115, 50, 50))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.infoAES.setFont(font)
        self.infoAES.setIconSize(QtCore.QSize(26, 26))
        self.infoAES.setObjectName("infoAES")
        self.infoRSA = QtWidgets.QPushButton(self.Menu)
        self.infoRSA.setGeometry(QtCore.QRect(60, 170, 50, 50))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.infoRSA.setFont(font)
        self.infoRSA.setIconSize(QtCore.QSize(26, 26))
        self.infoRSA.setObjectName("infoRSA")
        self.info3DES = QtWidgets.QPushButton(self.Menu)
        self.info3DES.setGeometry(QtCore.QRect(60, 225, 50, 50))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.info3DES.setFont(font)
        self.info3DES.setIconSize(QtCore.QSize(26, 26))
        self.info3DES.setObjectName("info3DES")
        self.infoBLFISH = QtWidgets.QPushButton(self.Menu)
        self.infoBLFISH.setGeometry(QtCore.QRect(60, 280, 50, 50))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.infoBLFISH.setFont(font)
        self.infoBLFISH.setIconSize(QtCore.QSize(26, 26))
        self.infoBLFISH.setObjectName("infoBLFISH")
        self.infoSteg = QtWidgets.QPushButton(self.Menu)
        self.infoSteg.setGeometry(QtCore.QRect(60, 335, 50, 50))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.infoSteg.setFont(font)
        self.infoSteg.setIconSize(QtCore.QSize(26, 26))
        self.infoSteg.setObjectName("infoSteg")
        self.horizontalLayout_2.addWidget(self.Menu)
        self.MainFrame = QtWidgets.QFrame(self.Body)
        self.MainFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.MainFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.MainFrame.setObjectName("MainFrame")
        self.stackedWidget = QtWidgets.QStackedWidget(self.MainFrame)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 981, 681))
        self.stackedWidget.setObjectName("stackedWidget")
        self.SteganoWidget = QtWidgets.QWidget()
        self.SteganoWidget.setObjectName("SteganoWidget")
        self.TagLabelSteg = QtWidgets.QLabel(self.SteganoWidget)
        self.TagLabelSteg.setGeometry(QtCore.QRect(0, 0, 895, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.TagLabelSteg.setFont(font)
        self.TagLabelSteg.setAlignment(QtCore.Qt.AlignCenter)
        self.TagLabelSteg.setObjectName("TagLabelSteg")
        self.CryptButtonSteg = QtWidgets.QPushButton(self.SteganoWidget)
        self.CryptButtonSteg.setObjectName(u"CryptButtonSteg")
        self.CryptButtonSteg.setGeometry(QtCore.QRect(761, 645, 131, 30))
        self.FileLineSteg = QtWidgets.QLineEdit(self.SteganoWidget)
        self.FileLineSteg.setGeometry(QtCore.QRect(460, 35, 331, 30))
        self.FileLineSteg.setReadOnly(True)
        self.FileLineSteg.setObjectName("FileLineSteg")
        self.PasswordLineSteg = QtWidgets.QLineEdit(self.SteganoWidget)
        self.PasswordLineSteg.setGeometry(QtCore.QRect(460, 67, 433, 30))
        self.PasswordLineSteg.setObjectName("PasswordLineSteg")
        self.PasswordFileNR = QtWidgets.QLineEdit(self.SteganoWidget)
        self.PasswordFileNR.setGeometry(QtCore.QRect(460, 99, 331, 30))
        self.PasswordFileNR.setReadOnly(True)
        self.PasswordFileNR.setObjectName("PasswordFileNR")
        self.PasswordFileR = QtWidgets.QLineEdit(self.SteganoWidget)
        self.PasswordFileR.setGeometry(QtCore.QRect(460, 131, 331, 30))
        self.PasswordFileR.setReadOnly(True)
        self.PasswordFileR.setObjectName("PasswordFileR")
        self.TakeImageBtn = QtWidgets.QPushButton(self.SteganoWidget)
        self.TakeImageBtn.setGeometry(QtCore.QRect(793, 35, 100, 30))
        self.TakeImageBtn.setObjectName("TakeImageBtn")
        self.TakeFileNR = QtWidgets.QPushButton(self.SteganoWidget)
        self.TakeFileNR.setGeometry(QtCore.QRect(793, 99, 100, 30))
        self.TakeFileNR.setObjectName("TakeFileNR")
        self.TakeFileR = QtWidgets.QPushButton(self.SteganoWidget)
        self.TakeFileR.setGeometry(QtCore.QRect(793, 131, 100, 30))
        self.TakeFileR.setObjectName("TakeFileR")
        self.plainTextForEncrypt = QtWidgets.QPlainTextEdit(self.SteganoWidget)
        self.plainTextForEncrypt.setGeometry(QtCore.QRect(460, 99, 433, 544))
        self.plainTextForEncrypt.setObjectName("plainTextForEncrypt")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.SteganoWidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(4, 35, 451, 640))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.AnonTag_3 = QtWidgets.QGroupBox(self.SteganoWidget)
        self.AnonTag_3.setGeometry(QtCore.QRect(890, 0, 55, 669))
        self.AnonTag_3.setTitle("")
        self.AnonTag_3.setObjectName("AnonTag_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.AnonTag_3)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.A_Tag_3 = QtWidgets.QLabel(self.AnonTag_3)
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.A_Tag_3.setFont(font)
        self.A_Tag_3.setAlignment(QtCore.Qt.AlignCenter)
        self.A_Tag_3.setObjectName("A_Tag_3")
        self.verticalLayout_4.addWidget(self.A_Tag_3)
        self.N_Tag_3 = QtWidgets.QLabel(self.AnonTag_3)
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.N_Tag_3.setFont(font)
        self.N_Tag_3.setAlignment(QtCore.Qt.AlignCenter)
        self.N_Tag_3.setObjectName("N_Tag_3")
        self.verticalLayout_4.addWidget(self.N_Tag_3)
        self.O_Tag_3 = QtWidgets.QLabel(self.AnonTag_3)
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.O_Tag_3.setFont(font)
        self.O_Tag_3.setAlignment(QtCore.Qt.AlignCenter)
        self.O_Tag_3.setObjectName("O_Tag_3")
        self.verticalLayout_4.addWidget(self.O_Tag_3)
        self.N_Tag2_3 = QtWidgets.QLabel(self.AnonTag_3)
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.N_Tag2_3.setFont(font)
        self.N_Tag2_3.setAlignment(QtCore.Qt.AlignCenter)
        self.N_Tag2_3.setObjectName("N_Tag2_3")
        self.verticalLayout_4.addWidget(self.N_Tag2_3)
        self.Y_Tag_3 = QtWidgets.QLabel(self.AnonTag_3)
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.Y_Tag_3.setFont(font)
        self.Y_Tag_3.setAlignment(QtCore.Qt.AlignCenter)
        self.Y_Tag_3.setObjectName("Y_Tag_3")
        self.verticalLayout_4.addWidget(self.Y_Tag_3)
        self.M_Tag_3 = QtWidgets.QLabel(self.AnonTag_3)
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.M_Tag_3.setFont(font)
        self.M_Tag_3.setAlignment(QtCore.Qt.AlignCenter)
        self.M_Tag_3.setObjectName("M_Tag_3")
        self.verticalLayout_4.addWidget(self.M_Tag_3)
        self.O_Tag2_3 = QtWidgets.QLabel(self.AnonTag_3)
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.O_Tag2_3.setFont(font)
        self.O_Tag2_3.setAlignment(QtCore.Qt.AlignCenter)
        self.O_Tag2_3.setObjectName("O_Tag2_3")
        self.verticalLayout_4.addWidget(self.O_Tag2_3)
        self.U_Tag_3 = QtWidgets.QLabel(self.AnonTag_3)
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.U_Tag_3.setFont(font)
        self.U_Tag_3.setAlignment(QtCore.Qt.AlignCenter)
        self.U_Tag_3.setObjectName("U_Tag_3")
        self.verticalLayout_4.addWidget(self.U_Tag_3)
        self.S_Tag_3 = QtWidgets.QLabel(self.AnonTag_3)
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.S_Tag_3.setFont(font)
        self.S_Tag_3.setAlignment(QtCore.Qt.AlignCenter)
        self.S_Tag_3.setObjectName("S_Tag_3")
        self.verticalLayout_4.addWidget(self.S_Tag_3)
        self.stackedWidget.addWidget(self.SteganoWidget)
        self.CipherWidget = QtWidgets.QWidget()
        self.CipherWidget.setObjectName("CipherWidget")
        self.TagLabel = QtWidgets.QLabel(self.CipherWidget)
        self.TagLabel.setGeometry(QtCore.QRect(0, 0, 895, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.TagLabel.setFont(font)
        self.TagLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.TagLabel.setObjectName("TagLabel")
        self.FileLine = QtWidgets.QLineEdit(self.CipherWidget)
        self.FileLine.setGeometry(QtCore.QRect(10, 50, 785, 30))
        self.FileLine.setReadOnly(True)
        self.FileLine.setObjectName("FileLine")
        self.TakeFile = QtWidgets.QPushButton(self.CipherWidget)
        self.TakeFile.setGeometry(QtCore.QRect(800, 50, 90, 30))
        self.TakeFile.setObjectName("TakeFile")
        self.PassworLine = QtWidgets.QLineEdit(self.CipherWidget)
        self.PassworLine.setGeometry(QtCore.QRect(10, 85, 785, 30))
        self.PassworLine.setObjectName("PassworLine")
        self.GeneratePassword = QtWidgets.QPushButton(self.CipherWidget)
        self.GeneratePassword.setGeometry(QtCore.QRect(800, 85, 90, 30))
        self.GeneratePassword.setObjectName("GeneratePassword")
        self.CustomNameLine = QtWidgets.QLineEdit(self.CipherWidget)
        self.CustomNameLine.setGeometry(QtCore.QRect(10, 120, 331, 30))
        self.CustomNameLine.setObjectName("CustomNameLine")
        self.LengthLine = QtWidgets.QLineEdit(self.CipherWidget)
        self.LengthLine.setGeometry(QtCore.QRect(800, 120, 90, 30))
        self.LengthLine.setAlignment(QtCore.Qt.AlignCenter)
        self.LengthLine.setObjectName("LengthLine")
        self.CryptButton = QtWidgets.QPushButton(self.CipherWidget)
        self.CryptButton.setGeometry(QtCore.QRect(530, 120, 111, 30))
        self.CryptButton.setObjectName("CryptButton")
        self.InfoPlain = QtWidgets.QPlainTextEdit(self.CipherWidget)
        self.InfoPlain.setGeometry(QtCore.QRect(10, 155, 881, 518))
        self.InfoPlain.setReadOnly(True)
        self.InfoPlain.setObjectName("InfoPlain")
        self.AnonTag_2 = QtWidgets.QGroupBox(self.CipherWidget)
        self.AnonTag_2.setGeometry(QtCore.QRect(890, 0, 55, 669))
        self.AnonTag_2.setTitle("")
        self.AnonTag_2.setObjectName("AnonTag_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.AnonTag_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.A_Tag_2 = QtWidgets.QLabel(self.AnonTag_2)
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.A_Tag_2.setFont(font)
        self.A_Tag_2.setAlignment(QtCore.Qt.AlignCenter)
        self.A_Tag_2.setObjectName("A_Tag_2")
        self.verticalLayout_3.addWidget(self.A_Tag_2)
        self.N_Tag_2 = QtWidgets.QLabel(self.AnonTag_2)
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.N_Tag_2.setFont(font)
        self.N_Tag_2.setAlignment(QtCore.Qt.AlignCenter)
        self.N_Tag_2.setObjectName("N_Tag_2")
        self.verticalLayout_3.addWidget(self.N_Tag_2)
        self.O_Tag_2 = QtWidgets.QLabel(self.AnonTag_2)
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.O_Tag_2.setFont(font)
        self.O_Tag_2.setAlignment(QtCore.Qt.AlignCenter)
        self.O_Tag_2.setObjectName("O_Tag_2")
        self.verticalLayout_3.addWidget(self.O_Tag_2)
        self.N_Tag2_2 = QtWidgets.QLabel(self.AnonTag_2)
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.N_Tag2_2.setFont(font)
        self.N_Tag2_2.setAlignment(QtCore.Qt.AlignCenter)
        self.N_Tag2_2.setObjectName("N_Tag2_2")
        self.verticalLayout_3.addWidget(self.N_Tag2_2)
        self.Y_Tag_2 = QtWidgets.QLabel(self.AnonTag_2)
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.Y_Tag_2.setFont(font)
        self.Y_Tag_2.setAlignment(QtCore.Qt.AlignCenter)
        self.Y_Tag_2.setObjectName("Y_Tag_2")
        self.verticalLayout_3.addWidget(self.Y_Tag_2)
        self.M_Tag_2 = QtWidgets.QLabel(self.AnonTag_2)
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.M_Tag_2.setFont(font)
        self.M_Tag_2.setAlignment(QtCore.Qt.AlignCenter)
        self.M_Tag_2.setObjectName("M_Tag_2")
        self.verticalLayout_3.addWidget(self.M_Tag_2)
        self.O_Tag2_2 = QtWidgets.QLabel(self.AnonTag_2)
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.O_Tag2_2.setFont(font)
        self.O_Tag2_2.setAlignment(QtCore.Qt.AlignCenter)
        self.O_Tag2_2.setObjectName("O_Tag2_2")
        self.verticalLayout_3.addWidget(self.O_Tag2_2)
        self.U_Tag_2 = QtWidgets.QLabel(self.AnonTag_2)
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.U_Tag_2.setFont(font)
        self.U_Tag_2.setAlignment(QtCore.Qt.AlignCenter)
        self.U_Tag_2.setObjectName("U_Tag_2")
        self.verticalLayout_3.addWidget(self.U_Tag_2)
        self.S_Tag_2 = QtWidgets.QLabel(self.AnonTag_2)
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.S_Tag_2.setFont(font)
        self.S_Tag_2.setAlignment(QtCore.Qt.AlignCenter)
        self.S_Tag_2.setObjectName("S_Tag_2")
        self.verticalLayout_3.addWidget(self.S_Tag_2)
        self.stackedWidget.addWidget(self.CipherWidget)
        self.HomeWidget = QtWidgets.QWidget()
        self.HomeWidget.setObjectName("HomeWidget")
        self.DarkCryptorLabel = QtWidgets.QLabel(self.HomeWidget)
        self.DarkCryptorLabel.setGeometry(QtCore.QRect(0, 240, 895, 80))
        font = QtGui.QFont()
        font.setPointSize(50)
        font.setBold(True)
        font.setWeight(75)
        self.DarkCryptorLabel.setFont(font)
        self.DarkCryptorLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.DarkCryptorLabel.setObjectName("DarkCryptorLabel")
        self.WelcomeLabel = QtWidgets.QLabel(self.HomeWidget)
        self.WelcomeLabel.setGeometry(QtCore.QRect(0, 315, 895, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.WelcomeLabel.setFont(font)
        self.WelcomeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.WelcomeLabel.setObjectName("WelcomeLabel")
        self.stackedWidget.addWidget(self.HomeWidget)
        self.RSA_Widget = QtWidgets.QWidget()
        self.RSA_Widget.setObjectName("RSA_Widget")
        self.TakeFileRSA = QtWidgets.QPushButton(self.RSA_Widget)
        self.TakeFileRSA.setGeometry(QtCore.QRect(800, 50, 90, 30))
        self.TakeFileRSA.setObjectName("TakeFileRSA")
        self.TagLabelRSA = QtWidgets.QLabel(self.RSA_Widget)
        self.TagLabelRSA.setGeometry(QtCore.QRect(0, 0, 895, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.TagLabelRSA.setFont(font)
        self.TagLabelRSA.setAlignment(QtCore.Qt.AlignCenter)
        self.TagLabelRSA.setObjectName("TagLabelRSA")
        self.FileLineRSA = QtWidgets.QLineEdit(self.RSA_Widget)
        self.FileLineRSA.setGeometry(QtCore.QRect(10, 50, 785, 30))
        self.FileLineRSA.setReadOnly(True)
        self.FileLineRSA.setObjectName("FileLineRSA")
        self.TakePublic = QtWidgets.QPushButton(self.RSA_Widget)
        self.TakePublic.setGeometry(QtCore.QRect(10, 85, 100, 30))
        self.TakePublic.setObjectName("TakePublic")
        self.TakePrivate = QtWidgets.QPushButton(self.RSA_Widget)
        self.TakePrivate.setGeometry(QtCore.QRect(113, 85, 100, 30))
        self.TakePrivate.setObjectName("TakePrivate")
        self.PassGenerateRSA = QtWidgets.QPushButton(self.RSA_Widget)
        self.PassGenerateRSA.setGeometry(QtCore.QRect(800, 85, 90, 30))
        self.PassGenerateRSA.setObjectName("PassGenerateRSA")
        self.PassLenRSA = QtWidgets.QLineEdit(self.RSA_Widget)
        self.PassLenRSA.setGeometry(QtCore.QRect(704, 85, 90, 30))
        self.PassLenRSA.setObjectName("PassLenRSA")
        self.CryptButtonRSA = QtWidgets.QPushButton(self.RSA_Widget)
        self.CryptButtonRSA.setGeometry(QtCore.QRect(704, 120, 186, 30))
        self.CryptButtonRSA.setObjectName("CryptButtonRSA")
        self.CustomNameLineRSA = QtWidgets.QLineEdit(self.RSA_Widget)
        self.CustomNameLineRSA.setObjectName(u"CustomNameLineRSA")
        self.CustomNameLineRSA.setGeometry(QtCore.QRect(10, 120, 201, 30))
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.RSA_Widget)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(10, 154, 880, 520))
        self.plainTextEdit_2.setReadOnly(True)
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.AnonTag = QtWidgets.QGroupBox(self.RSA_Widget)
        self.AnonTag.setGeometry(QtCore.QRect(890, 0, 55, 669))
        self.AnonTag.setTitle("")
        self.AnonTag.setObjectName("AnonTag")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.AnonTag)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.A_Tag = QtWidgets.QLabel(self.AnonTag)
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.A_Tag.setFont(font)
        self.A_Tag.setAlignment(QtCore.Qt.AlignCenter)
        self.A_Tag.setObjectName("A_Tag")
        self.verticalLayout_2.addWidget(self.A_Tag)
        self.N_Tag = QtWidgets.QLabel(self.AnonTag)
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.N_Tag.setFont(font)
        self.N_Tag.setAlignment(QtCore.Qt.AlignCenter)
        self.N_Tag.setObjectName("N_Tag")
        self.verticalLayout_2.addWidget(self.N_Tag)
        self.O_Tag = QtWidgets.QLabel(self.AnonTag)
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.O_Tag.setFont(font)
        self.O_Tag.setAlignment(QtCore.Qt.AlignCenter)
        self.O_Tag.setObjectName("O_Tag")
        self.verticalLayout_2.addWidget(self.O_Tag)
        self.N_Tag2 = QtWidgets.QLabel(self.AnonTag)
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.N_Tag2.setFont(font)
        self.N_Tag2.setAlignment(QtCore.Qt.AlignCenter)
        self.N_Tag2.setObjectName("N_Tag2")
        self.verticalLayout_2.addWidget(self.N_Tag2)
        self.Y_Tag = QtWidgets.QLabel(self.AnonTag)
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.Y_Tag.setFont(font)
        self.Y_Tag.setAlignment(QtCore.Qt.AlignCenter)
        self.Y_Tag.setObjectName("Y_Tag")
        self.verticalLayout_2.addWidget(self.Y_Tag)
        self.M_Tag = QtWidgets.QLabel(self.AnonTag)
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.M_Tag.setFont(font)
        self.M_Tag.setAlignment(QtCore.Qt.AlignCenter)
        self.M_Tag.setObjectName("M_Tag")
        self.verticalLayout_2.addWidget(self.M_Tag)
        self.O_Tag2 = QtWidgets.QLabel(self.AnonTag)
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.O_Tag2.setFont(font)
        self.O_Tag2.setAlignment(QtCore.Qt.AlignCenter)
        self.O_Tag2.setObjectName("O_Tag2")
        self.verticalLayout_2.addWidget(self.O_Tag2)
        self.U_Tag = QtWidgets.QLabel(self.AnonTag)
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.U_Tag.setFont(font)
        self.U_Tag.setAlignment(QtCore.Qt.AlignCenter)
        self.U_Tag.setObjectName("U_Tag")
        self.verticalLayout_2.addWidget(self.U_Tag)
        self.S_Tag = QtWidgets.QLabel(self.AnonTag)
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.S_Tag.setFont(font)
        self.S_Tag.setAlignment(QtCore.Qt.AlignCenter)
        self.S_Tag.setObjectName("S_Tag")
        self.verticalLayout_2.addWidget(self.S_Tag)
        self.stackedWidget.addWidget(self.RSA_Widget)
        self.stackedWidget.addWidget(self.RSA_Widget)
        self.Settings_Widget = QtWidgets.QWidget()
        self.Settings_Widget.setObjectName("Settings_Widget")
        self.TagLabelRSA_2 = QtWidgets.QLabel(self.Settings_Widget)
        self.TagLabelRSA_2.setGeometry(QtCore.QRect(0, 2, 895, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.TagLabelRSA_2.setFont(font)
        self.TagLabelRSA_2.setAlignment(QtCore.Qt.AlignCenter)
        self.TagLabelRSA_2.setObjectName("TagLabelRSA_2")
        self.EncryptRadio = QtWidgets.QRadioButton(self.Settings_Widget)
        self.EncryptRadio.setGeometry(QtCore.QRect(10, 40, 161, 24))
        self.EncryptRadio.setObjectName("EncryptRadio")
        self.DecryptRadio = QtWidgets.QRadioButton(self.Settings_Widget)
        self.DecryptRadio.setGeometry(QtCore.QRect(10, 60, 171, 24))
        self.DecryptRadio.setObjectName("DecryptRadio")
        self.SaveFileMode = QtWidgets.QCheckBox(self.Settings_Widget)
        self.SaveFileMode.setGeometry(QtCore.QRect(10, 90, 96, 24))
        self.SaveFileMode.setObjectName("SaveFileMode")
        self.Re_writeMode = QtWidgets.QCheckBox(self.Settings_Widget)
        self.Re_writeMode.setGeometry(QtCore.QRect(10, 110, 121, 24))
        self.Re_writeMode.setObjectName("Re_writeMode")
        self.DirectoryCheck = QtWidgets.QCheckBox(self.Settings_Widget)
        self.DirectoryCheck.setObjectName(u"DirectoryCheck")
        self.DirectoryCheck.setGeometry(QtCore.QRect(10, 130, 131, 21))
        self.stackedWidget.addWidget(self.Settings_Widget)
        self.horizontalLayout_2.addWidget(self.MainFrame)
        self.verticalLayout.addWidget(self.Body)
        self.horizontalLayout_2.addWidget(self.MainFrame)
        self.verticalLayout.addWidget(self.Body)
        self.retranslateUi(Main)
        self.stackedWidget.setCurrentIndex(2) # Home - 2; cipher - 1; RSA - 3; steg - 0
        QtCore.QMetaObject.connectSlotsByName(Main)

    def retranslateUi(self, Main):
        _translate = QtCore.QCoreApplication.translate
        Main.setWindowTitle("DarkCryptor")
        Main.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        Main.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.HeaderText.setText("DackCryptor")
        self.AES.setText("AES")
        self.RSA.setText("RSA")
        self.ThreeDes.setText("3DES")
        self.BlowFish.setText("BF")
        self.Steganography.setText("Steg")
        self.infoAES.setText("i")
        self.infoRSA.setText("i")
        self.info3DES.setText("i")
        self.infoBLFISH.setText("i")
        self.infoSteg.setText("i")
        self.TagLabelSteg.setText("|Steganography|")
        self.FileLineSteg.setPlaceholderText("Image")
        self.PasswordLineSteg.setPlaceholderText("Password")
        self.PasswordFileNR.setPlaceholderText("Password in file non-read")
        self.PasswordFileR.setPlaceholderText("Password file read")
        self.TakeImageBtn.setText("Take")
        self.TakeFileNR.setText("Take")
        self.TakeFileR.setText("Take")
        self.plainTextForEncrypt.setPlaceholderText("Text for encryption")
        self.plainTextEdit.setPlaceholderText("Decrypted text")
        self.A_Tag_3.setText("A")
        self.N_Tag_3.setText("N")
        self.O_Tag_3.setText("O")
        self.N_Tag2_3.setText("N")
        self.Y_Tag_3.setText("Y")
        self.M_Tag_3.setText("M")
        self.O_Tag2_3.setText("O")
        self.U_Tag_3.setText("U")
        self.S_Tag_3.setText("S")
        self.TagLabel.setText("|AES|")
        self.TakeFile.setText("Take")
        self.PassworLine.setPlaceholderText("Password")
        self.GeneratePassword.setText("Generate")
        self.CustomNameLine.setPlaceholderText("Custom name { Test.txt }")
        self.LengthLine.setPlaceholderText("length")
        self.InfoPlain.setPlaceholderText("Information")
        self.A_Tag_2.setText("A")
        self.N_Tag_2.setText("N")
        self.O_Tag_2.setText("O")
        self.N_Tag2_2.setText("N")
        self.Y_Tag_2.setText("Y")
        self.M_Tag_2.setText("M")
        self.O_Tag2_2.setText("O")
        self.U_Tag_2.setText("U")
        self.S_Tag_2.setText("S")
        self.DarkCryptorLabel.setText("DarkCryptor")
        self.WelcomeLabel.setText("Welcome")
        self.TakeFileRSA.setText("Take")
        self.TagLabelRSA.setText("|RSA|")
        self.TakePublic.setText("Public")
        self.TakePrivate.setText("Private")
        self.PassGenerateRSA.setText("Generate")
        self.PassLenRSA.setPlaceholderText("length")
        self.plainTextEdit_2.setPlaceholderText("Information")
        self.A_Tag.setText("A")
        self.N_Tag.setText("N")
        self.O_Tag.setText("O")
        self.N_Tag2.setText("N")
        self.Y_Tag.setText("Y")
        self.M_Tag.setText("M")
        self.O_Tag2.setText("O")
        self.U_Tag.setText("U")
        self.S_Tag.setText("S")
        self.TagLabelRSA_2.setText("|SETTINGS|")
        self.EncryptRadio.setText("Encrypt mode")
        self.EncryptRadio.setChecked(True)
        self.DecryptRadio.setText("Decrypt mode")
        self.SaveFileMode.setText("Save file")
        self.Re_writeMode.setText("Re-write file")
        self.DirectoryCheck.setText("Directory")
        self.CustomNameLineRSA.setPlaceholderText("Custom file name { Test.txt }")
        self.CryptButtonSteg.setText("ENCRYPT")
    # AES 10
    def AES_APP(self):
        global choiceSettings
        mn.TagLabel.setText("|AES|")
        if mn.EncryptRadio.isChecked():
            mn.CryptButton.setText("ENCRYPT")
        else:
            mn.CryptButton.setText("DECRYPT")
        if mn.DirectoryCheck.isChecked():
            mn.FileLine.setPlaceholderText("Directory")
        else:
            mn.FileLine.setPlaceholderText("File")
        mn.stackedWidget.setCurrentIndex(1)
        choiceSettings = 10
    # 3DES 11
    def ThreeDES_APP(self):
        global choiceSettings
        mn.TagLabel.setText("|3DES|")
        if mn.EncryptRadio.isChecked():
            mn.CryptButton.setText("ENCRYPT")
        else:
            mn.CryptButton.setText("DECRYPT")
        if mn.DirectoryCheck.isChecked():
            mn.FileLine.setPlaceholderText("Directory")
        else:
            mn.FileLine.setPlaceholderText("File")
        mn.stackedWidget.setCurrentIndex(1)
        choiceSettings = 11
    # blowfish 12
    def BlowFish_APP(self):
        global choiceSettings
        mn.TagLabel.setText("|BlowFish|")
        if mn.EncryptRadio.isChecked():
            mn.CryptButton.setText("ENCRYPT")
        else:
            mn.CryptButton.setText("DECRYPT")
        if mn.DirectoryCheck.isChecked():
            mn.FileLine.setPlaceholderText("Directory")
        else:
            mn.FileLine.setPlaceholderText("File")
        mn.stackedWidget.setCurrentIndex(1)
        choiceSettings = 12

    def Home_APP(self):
        global choiceSettings
        mn.stackedWidget.setCurrentIndex(2)
        choiceSettings = 2
    # RSA 3
    def RSA_APP(self):
        global choiceSettings
        if mn.EncryptRadio.isChecked():
            mn.CryptButtonRSA.setText("ENCRYPT")
        else:
            mn.CryptButtonRSA.setText("DECRYPT")
        if mn.DirectoryCheck.isChecked():
            mn.FileLineRSA.setPlaceholderText("Directory")
        else:
            mn.FileLineRSA.setPlaceholderText("File")
        mn.stackedWidget.setCurrentIndex(3)
        choiceSettings = 3

    def Stegano_APP(self):
        global choiceSettings
        mn.stackedWidget.setCurrentIndex(0)
        if mn.EncryptRadio.isChecked():
            mn.CryptButtonSteg.setText("ENCRYPT")
            mn.plainTextForEncrypt.show()
        else:
            mn.CryptButtonSteg.setText("DECRYPT")
            mn.plainTextForEncrypt.hide()
        choiceSettings = 0

    def runCrate(self):
        self.Threading = ThreadClass()
        self.Threading.start()

    def ShowAllMenu(self):
        wight = self.Menu.width()
        self.Anime = QtCore.QPropertyAnimation(self.Menu, b"maximumWidth")
        self.Anime.setDuration(250)
        self.Anime.setStartValue(wight)
        self.Anime.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        if wight == 60:
            self.Anime.setEndValue(115)
        elif wight == 115:
            self.Anime.setEndValue(60)
        self.Anime.start()

class ThreadClass(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent=parent)
    def run(self):
        act.create_key()

class Encryption_func:
    def encrypt_3DES(self, dirCrypt=False):
        try:
            if len(list(mn.PassworLine.text())) >= 16 and len(list(mn.PassworLine.text())) <= 24:
                name = mn.CustomNameLine.text()
                bs = DES3.block_size
                password = bytes(mn.PassworLine.text().encode())
                iv = Random.new().read(bs)
                cipher = DES3.new(password, DES3.MODE_EAX, iv)
                with open(file, "r") as f:
                    readFileText = f.read()
                plaintext = Padding.pad(bytes(readFileText.encode()), 1000, "iso7816")
                print(plaintext)
                msg = iv + cipher.encrypt(plaintext)
                if name != "":
                    fullPath = os.path.join(directory, name)
                else:
                    fullPath = os.path.join(directory, str(file) + ".DC")
                with open(fullPath, "wb") as fil:
                    fil.write(msg)
                if not mn.SaveFileMode.isChecked():
                    os.remove(str(file))
                if not dirCrypt:
                    mn.PassworLine.clear()
                    mn.FileLine.clear()
                    mn.CustomNameLine.clear()
                    name = ""
                    mn.InfoPlain.setPlainText(f"File saved in |{fullPath}| with password |{password.decode()}|")
                    act.ms_box(APP_NAME, "Done!", "info")
            else:
                act.ms_box(APP_NAME, "password length is too small", "err")
        except Exception as err:
            act.ms_box(APP_NAME, str(err), "err")

    def decrypt_3DES(self, dirCrypt=False):
        try:
            name = mn.CustomNameLine.text()
            bs = DES3.block_size
            password = mn.PassworLine.text()
            with open(file, "rb") as f:
                text = f.read()
            ciphertext = text
            key = bytes(password.encode())
            iv = ciphertext[:bs]
            ciphertext = ciphertext[bs:]
            cipher = DES3.new(key, Blowfish.MODE_EAX, iv)
            msg = Padding.unpad(cipher.decrypt(ciphertext), 1000, "iso7816")
            if name != "":
                fullPath = os.path.join(directory, str(name))
            else:
                fullPath = os.path.join(directory, str(os.path.splitext(str(file))[0]))
            with open(fullPath, "w") as fil:
                fil.write(msg.decode())
            if not mn.SaveFileMode.isChecked():
                os.remove(str(file))
            if not dirCrypt:
                mn.PassworLine.clear()
                mn.FileLine.clear()
                mn.CustomNameLine.clear()
                name = ""
                mn.InfoPlain.setPlainText(f"File saved in |{fullPath}|")
                act.ms_box(APP_NAME, "Done!", "info")
        except Exception as exp:
            if not dirCrypt:
                act.ms_box(APP_NAME, str(exp), "err")

    def encrypt_blow(self, dirCrypt=False):
        try:
            name = mn.CustomNameLine.text()
            bs = Blowfish.block_size
            password = mn.PassworLine.text()
            if not len(password) <= 3:
                key = bytes(password.encode())
                iv = Random.new().read(bs)
                cipher = Blowfish.new(key, Blowfish.MODE_EAX, iv)
                with open(file, "r") as f:
                    readFileText = f.read()
                plaintext = Padding.pad(bytes(readFileText.encode()), 1000, "iso7816")
                msg = iv + cipher.encrypt(plaintext)
                if name != "":
                    fullPath = os.path.join(directory, name)
                else:
                    fullPath = os.path.join(directory, str(file) + ".DC")
                with open(fullPath, "wb") as fil:
                    fil.write(msg)
                if not mn.SaveFileMode.isChecked():
                    os.remove(str(file))
                if not dirCrypt:
                    mn.PassworLine.clear()
                    mn.FileLine.clear()
                    mn.CustomNameLine.clear()
                    name = ""
                    mn.InfoPlain.setPlainText(f"File saved in |{fullPath}| with password |{password}|")
                    act.ms_box(APP_NAME, "Done!", "info")
        except Exception as exp:
            if not dirCrypt:
                act.ms_box(APP_NAME, str(exp), "err")

    def decrypt_blow(self, dirCrypt=False):
        try:
            name = mn.CustomNameLine.text()
            bs = Blowfish.block_size
            password = mn.PassworLine.text()
            with open(file, "rb") as f:
                text = f.read()
            ciphertext = text
            key = bytes(password.encode())
            iv = ciphertext[:bs]
            ciphertext = ciphertext[bs:]
            cipher = Blowfish.new(key, Blowfish.MODE_EAX, iv)
            msg = Padding.unpad(cipher.decrypt(ciphertext), 1000, "iso7816")
            if name != "":
                fullPath = os.path.join(directory, str(name))
            else:
                fullPath = os.path.join(directory, str(os.path.splitext(str(file))[0]))
            with open(fullPath, "w") as fil:
                fil.write(msg.decode())
            if not mn.SaveFileMode.isChecked():
                os.remove(str(file))
            if not dirCrypt:
                mn.PassworLine.clear()
                mn.FileLine.clear()
                mn.CustomNameLine.clear()
                name = ""
                mn.InfoPlain.setPlainText(f"File saved in |{fullPath}|")
                act.ms_box(APP_NAME, "Done!", "info")
        except Exception as exp:
            if not dirCrypt:
                act.ms_box(APP_NAME, str(exp), "err")

    def encrypt_image(self):
        global keys
        try:
            Key = Fernet.generate_key()
            imageName = mn.FileLineSteg.text()
            img = Image.open(imageName)
            password = mn.PasswordLineSteg.text()
            draw = ImageDraw.Draw(img)
            width = img.size[0]
            height = img.size[1]
            pix = img.load()
            fullPath = os.path.join(directory, "keys.txt")
            passwordFile = open(os.path.join(directory, "passwordImage.txt"), "wb")
            f = open(fullPath, 'wb')
            fIn = mn.plainTextForEncrypt.toPlainText()
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
            imageName = ""
            mn.FileLineSteg.clear()
            mn.plainTextForEncrypt.clear()
            mn.PasswordLineSteg.clear()
            act.ms_box("DarkCryptor", "Done", "info",
                   detail=f"Картинка сохранена в директории \"{imageName}.png\".\nКлючи сохранены в файл \"{fullPath}\"")
        except TypeError:
            act.ms_box(APP_NAME, "Проверь формат файла", "err", detail="неподдерживаемый формат - png")
        except Exception as exp:
            act.ms_box(APP_NAME, str(exp), "err")

    def decrypt_image(self):
        try:
            a = []
            keys = []
            imageName = mn.FileLineSteg.text()
            img = Image.open(imageName)
            password = mn.PasswordLineSteg.text()
            passwordFile = mn.PasswordFileR.text()
            pix = img.load()
            file = mn.PasswordFileNR.text()
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
            mn.plainTextEdit.setPlainText(outText.decode())
            mn.PasswordLineSteg.clear()
            mn.PasswordFileR.clear()
            mn.PasswordFileNR.clear()
            mn.FileLineSteg.clear()
            imageName = ""
            act.ms_box(APP_NAME, "Done", "info")
        except Exception as exp:
            act.ms_box("DarkCryptor", str(exp), "err")

    def encryptUi(self, dirCrypt=False):
        try:
            password = mn.PassworLine.text()
            name = mn.CustomNameLine.text()
            if name != "":
                fullPath = os.path.join(directory, name)
            else:
                fullPath = os.path.join(directory, str(file) + ".DC")
            encryptFile(str(file), fullPath, password, bufferSize)
            if not mn.SaveFileMode.isChecked():
                os.remove(str(file))
            if not dirCrypt:
                name = ""
                mn.PassworLine.clear()
                mn.FileLine.clear()
                mn.CustomNameLine.clear()
                mn.InfoPlain.setPlainText(f"File saved in |{fullPath}| with password |{password}|")
                act.ms_box(APP_NAME, "Done!", "info")
        except Exception as exp:
            if not dirCrypt:
                act.ms_box(APP_NAME, str(exp), "err")

    def decryptUi(self, dirCrypt=False):
        try:
            name = mn.CustomNameLine.text()
            passworded = mn.PassworLine.text()
            if name != "":
                fullPath = os.path.join(directory, str(name))
            else:
                fullPath = os.path.join(directory, str(os.path.splitext(str(file))[0]))
            decryptFile(str(file), fullPath, passworded, bufferSize)
            if not mn.SaveFileMode.isChecked():
                os.remove(str(file))
            if not dirCrypt:
                name = ""
                mn.PassworLine.clear()
                mn.FileLine.clear()
                mn.CustomNameLine.clear()
                mn.InfoPlain.setPlainText(f"File saved in |{fullPath}|")
                act.ms_box(APP_NAME, "Done!", "info")
        except Exception as exp:
            if not dirCrypt:
                act.ms_box(APP_NAME, str(exp), "err")

    def encrypt(self, dirCrypt=False):
        try:
            name = mn.CustomNameLineRSA.text()
            with open(file, "rb") as fil:
                crypt = fil.read()
                rsa_public_key = RSA.importKey(publicKey)
                cipher = PKCS1_OAEP.new(rsa_public_key)
                encrypted_file = cipher.encrypt(crypt)
                if name != "":
                    encrypted_file_name = os.path.join(directory, str(name))
                else:
                    encrypted_file_name = os.path.join(directory, f"{file}.DC")
                with open(encrypted_file_name, "wb") as encryFile:
                    encryFile.write(encrypted_file)
                if not mn.SaveFileMode.isChecked():
                    os.remove(str(file))
            if not dirCrypt:
                mn.FileLineRSA.clear()
                mn.CustomNameLineRSA.clear()
                mn.InfoPlain.setPlainText(
                    f"File saved in |{encrypted_file_name}| with password in file bits |{rsa_public_key.size_in_bits()}|")
                act.ms_box(APP_NAME, "Done!", "info")
                name = ""
        except Exception as exp:
            if not dirCrypt:
                info = None
                if str(exp) == "Plaintext is too long.":
                    exp = "Ключ мал для данного файла"
                    info = f"Попробуйте сгенерировать ключ {rsa_public_key.size_in_bits() + 1024}"
                act.ms_box(APP_NAME, str(exp), "err", info)

    def decrypt(self, dirCrypt=False):
        try:
            name = mn.CustomNameLineRSA.text()
            with open(file, "rb") as fil:
                crypted = fil.read()
                rsa_private_key = RSA.importKey(privateKey)
                rsa_private_key = PKCS1_OAEP.new(rsa_private_key)
                decrypted_text = rsa_private_key.decrypt(crypted)
                if name != "":
                    decrypted_file_name = os.path.join(directory, str(name))
                else:
                    decrypted_file_name = os.path.join(directory, str(os.path.splitext(str(file))[0]))
                with open(decrypted_file_name, "w") as decrypted_file:
                    decrypted_file.write(decrypted_text.decode("utf-8"))
                if not mn.SaveFileMode.isChecked():
                    os.remove(str(file))
            if not dirCrypt:
                name = ""
                mn.FileLineRSA.clear()
                mn.CustomNameLineRSA.clear()
                mn.InfoPlain.setPlainText(f"File saved in |{decrypted_file_name}|")
                act.ms_box(APP_NAME, "Done!", "info")
        except Exception as exp:
            if not dirCrypt:
                act.ms_box(APP_NAME, str(exp), "err")

    def decrypt_dir(self):
        global file, directory
        try:
            filesindir = os.walk(directory)
            for address, dirs, filename in filesindir:
                for fil in filename:
                    directory = address
                    file = os.path.join(directory, fil)
                    if choiceSettings == 10:
                        self.decryptUi(True)
                    elif choiceSettings == 3:
                        self.decrypt(True)
                    elif choiceSettings == 12:
                        self.decrypt_blow(True)
                    elif choiceSettings == 11:
                        self.decrypt_3DES(True)
            mn.FileLineRSA.clear()
            mn.CustomNameLineRSA.clear()
            mn.FileLine.clear()
            mn.CustomNameLine.clear()
            mn.PassworLine.clear()
            directory = ""
            act.ms_box(APP_NAME, "Done!", "info")
        except Exception as exp:
            act.ms_box(APP_NAME, str(exp), "err")

    def encrypt_dir(self):
        global file, directory, progress
        try:
            filesindir = os.walk(directory)
            for address, dirs, filename in filesindir:
                for fil in filename:
                    directory = address
                    file = os.path.join(directory, fil)
                    if choiceSettings == 10:
                        self.encryptUi(True)
                    elif choiceSettings == 3:
                        self.encrypt(True)
                    elif choiceSettings == 12:
                        self.encrypt_blow(True)
                    elif choiceSettings == 11:
                        self.encrypt_3DES(True)
            mn.FileLineRSA.clear()
            mn.CustomNameLineRSA.clear()
            mn.FileLine.clear()
            mn.CustomNameLine.clear()
            mn.PassworLine.clear()
            directory = ""
            progress = 0
            act.ms_box(APP_NAME, "Done!", "info")
        except Exception as exp:
            act.ms_box(APP_NAME, str(exp), "err")

    def btn_crypt(self, choice: bool):
        if not mn.DirectoryCheck.isChecked():
            if choice:  # AES | BlowFish | 3DES
                if choiceSettings == 10:
                    if mn.EncryptRadio.isChecked():
                        self.encryptUi()
                    elif mn.DecryptRadio.isChecked():
                        self.decryptUi()
                elif choiceSettings == 11:
                    if mn.EncryptRadio.isChecked():
                        self.encrypt_3DES()
                    elif mn.DecryptRadio.isChecked():
                        self.decrypt_3DES()
                elif choiceSettings == 12:
                    if mn.EncryptRadio.isChecked():
                        self.encrypt_blow()
                    elif mn.DecryptRadio.isChecked():
                        self.decrypt_blow()
                elif choiceSettings == 0:
                    if mn.EncryptRadio.isChecked():
                        self.encrypt_image()
                    elif mn.DecryptRadio.isChecked():
                        self.decrypt_image()
            elif not choice:  # RSA
                if mn.EncryptRadio.isChecked():
                    self.encrypt()
                elif mn.DecryptRadio.isChecked():
                    self.decrypt()
        else:
            if mn.EncryptRadio.isChecked():
                self.encrypt_dir()
            elif mn.DecryptRadio.isChecked():
                self.decrypt_dir()

class Actions:
    def create_key(self):
        try:
            bits = mn.PassLenRSA.text()
            _keys = RSA.generate(int(bits))
            keys_dir = os.path.join(ROOT, "rsa")
            if not os.path.exists(keys_dir):
                os.mkdir(keys_dir)
            with open(f"{keys_dir}/public.rsa", "wb") as pub, open(f"{keys_dir}/private.rsa", "wb") as private:
                pub.write(_keys.publickey().exportKey('PEM'))
                private.write(_keys.export_key('PEM'))
            mn.PassLenRSA.clear()
            self.ms_box(APP_NAME, "Done crate!", "info")
        except:
            self.ms_box(APP_NAME, "Не веденно количество бит", "err")

    def get_password(self):
        try:
            bytesText = ""
            kolvo = int(mn.LengthLine.text())
            for i in range(kolvo//4):
                bytesText += choice(ascii_letters)
                bytesText += choice(digits)
                bytesText += choice(hexdigits)
                bytesText += choice(punctuation)
            mn.PassworLine.setText(bytesText)
            mn.LengthLine.clear()
        except:
            self.ms_box(APP_NAME, "Введите число битов в пароле", "info", information="бит = 1 символ ( Цифры )")

    def ms_box(self, title, text, icon, information=None, detail=None):
        ms = QtWidgets.QMessageBox()
        if icon == "err":
            ms.setIcon(QtWidgets.QMessageBox.Critical)
        elif icon == "info":
            ms.setIcon(QtWidgets.QMessageBox.Information)
        elif icon == "war":
            ms.setIcon(QtWidgets.QMessageBox.Warning)
        ms.setText(text)
        ms.setWindowTitle(title)
        if information is not None:
            ms.setInformativeText(information)
        if detail is not None:
            ms.setDetailedText(detail)
        ms.exec_()

    def qtOpen(self, choice=True):
        if choice:
            a = QtWidgets.QFileDialog.getOpenFileName()[0]
        else:
            a = QtWidgets.QFileDialog.getExistingDirectory()
        return a

    def takeFile(self, choice=0):
        global file, directory
        try:
            file = self.qtOpen()
            directory = os.path.dirname(file)
            if choice == 0: # RSA
                mn.FileLineRSA.setText(file)
            elif choice == 1: # Cipher
                mn.FileLine.setText(file)
            elif choice == 2: # stegano Image line
                mn.FileLineSteg.setText(file)
            elif choice == 3: # файловый пароль читабельный
                mn.PasswordFileR.setText(file)
            elif choice == 4: # файловый пароль не читабельный
                mn.PasswordFileNR.setText(file)
        except:
            self.ms_box(APP_NAME, "Файл не выбран", "war")

    def takeDir(self, choice: bool):
        global directory
        try:
            directory = self.qtOpen(False)
            if choice: # RSA
                mn.FileLineRSA.setText(directory)
            elif not choice: # Cipher
                mn.FileLine.setText(directory)
        except:
            self.ms_box(APP_NAME, "Файл не выбран", "war")

    def take_public(self):
        global publicKey
        try:
            pub = self.qtOpen()
            with open(pub, "rb") as publ:
                publicKey = publ.read()
            if not "PUBLIC" in publicKey.decode("utf-8"):
                self.ms_box(APP_NAME, "Выбран не тот файл!", "war")
                publicKey = ""
        except:
            self.ms_box(APP_NAME, "Файл не выбран", "war")

    def take_private(self):
        global privateKey
        try:
            priv = self.qtOpen()
            with open(priv, "rb") as priva:
                privateKey = priva.read()
            if not "PRIVATE" in privateKey.decode("utf-8"):
                self.ms_box(APP_NAME, "Выбран не тот файл", "war")
                privateKey = ""
        except:
            self.ms_box(APP_NAME, "Файл не выбран", "war")

    def takeBtn(self, choice: bool):
        if choice:
            if mn.DirectoryCheck.isChecked():
                self.takeDir(True)
            else:
                self.takeFile(0)
        elif not choice:
            if mn.DirectoryCheck.isChecked():
                self.takeDir(False)
            else:
                self.takeFile(1)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    MainDialog = QtWidgets.QDialog()
    mn = Ui_Main()
    cr = Encryption_func()
    act = Actions()
    mn.setupUi(MainDialog)
    MainDialog.show()
    mn.closeButton.clicked.connect(lambda: MainDialog.close())
    mn.AES.clicked.connect(mn.AES_APP)
    mn.OpenMenu.clicked.connect(mn.ShowAllMenu)
    mn.Home.clicked.connect(mn.Home_APP)
    mn.ThreeDes.clicked.connect(mn.ThreeDES_APP)
    mn.BlowFish.clicked.connect(mn.BlowFish_APP)
    mn.RSA.clicked.connect(mn.RSA_APP)
    mn.Steganography.clicked.connect(mn.Stegano_APP)
    mn.SettingsButt.clicked.connect(lambda: mn.stackedWidget.setCurrentIndex(4))
    mn.TakePrivate.clicked.connect(act.take_private)
    mn.TakePublic.clicked.connect(act.take_public)
    mn.TakeFileRSA.clicked.connect(lambda: act.takeBtn(True))
    mn.CryptButtonRSA.clicked.connect(lambda: cr.btn_crypt(False))
    mn.PassGenerateRSA.clicked.connect(mn.runCrate)
    mn.infoAES.clicked.connect(lambda: act.ms_box("AES", "Откройте \"show details...\"", "info", detail=infoEnc["AES"]))
    mn.infoBLFISH.clicked.connect(lambda: act.ms_box("BlowFish", "Откройте \"show details...\"", "info", detail=infoEnc["BlowFish"]))
    mn.infoRSA.clicked.connect(lambda: act.ms_box("RSA", "Откройте \"show details...\"", "info", detail=infoEnc["RSA"]))
    mn.infoSteg.clicked.connect(lambda: act.ms_box("Steganography", "Откройте \"show details...\"", "info", detail=infoEnc["Steganography"]))
    mn.info3DES.clicked.connect(lambda: act.ms_box("3DES", "Откройте \"show details...\"", "info", detail=infoEnc["3DES"]))
    mn.TakeFile.clicked.connect(lambda: act.takeBtn(False))
    mn.GeneratePassword.clicked.connect(act.get_password)
    mn.CryptButton.clicked.connect(lambda: cr.btn_crypt(True))
    mn.TakeFileR.clicked.connect(lambda: act.takeFile(3))
    mn.TakeFileNR.clicked.connect(lambda: act.takeFile(4))
    mn.TakeImageBtn.clicked.connect(lambda: act.takeFile(2))
    mn.CryptButtonSteg.clicked.connect(lambda: cr.btn_crypt(True))

    app.exec_()

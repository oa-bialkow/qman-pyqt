# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'qman-pyqt.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLayout, QListWidget,
    QListWidgetItem, QMainWindow, QMenu, QMenuBar,
    QPushButton, QScrollArea, QSizePolicy, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1148, 751)
        font = QFont()
        font.setFamilies([u"Noto Mono for Powerline"])
        MainWindow.setFont(font)
        self.actionAdd_queue = QAction(MainWindow)
        self.actionAdd_queue.setObjectName(u"actionAdd_queue")
        self.actionRemove_queue = QAction(MainWindow)
        self.actionRemove_queue.setObjectName(u"actionRemove_queue")
        self.actionSet_queue = QAction(MainWindow)
        self.actionSet_queue.setObjectName(u"actionSet_queue")
        self.actionChange_name = QAction(MainWindow)
        self.actionChange_name.setObjectName(u"actionChange_name")
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.qscroll = QScrollArea(self.centralwidget)
        self.qscroll.setObjectName(u"qscroll")
        self.qscroll.setEnabled(True)
        font1 = QFont()
        font1.setFamilies([u"Monaco"])
        font1.setBold(False)
        font1.setItalic(False)
        self.qscroll.setFont(font1)
        self.qscroll.setWidgetResizable(True)
        self.qlist = QWidget()
        self.qlist.setObjectName(u"qlist")
        self.qlist.setGeometry(QRect(0, 0, 381, 698))
        self.verticalLayout_4 = QVBoxLayout(self.qlist)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.qobjs = QListWidget(self.qlist)
        self.qobjs.setObjectName(u"qobjs")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.qobjs.sizePolicy().hasHeightForWidth())
        self.qobjs.setSizePolicy(sizePolicy1)
        font2 = QFont()
        font2.setFamilies([u"Monaco"])
        font2.setPointSize(18)
        font2.setBold(False)
        font2.setItalic(False)
        self.qobjs.setFont(font2)

        self.verticalLayout_4.addWidget(self.qobjs)

        self.qscroll.setWidget(self.qlist)

        self.horizontalLayout_2.addWidget(self.qscroll)

        self.qview = QWidget(self.centralwidget)
        self.qview.setObjectName(u"qview")
        sizePolicy.setHeightForWidth(self.qview.sizePolicy().hasHeightForWidth())
        self.qview.setSizePolicy(sizePolicy)
        self.qview.setFont(font1)
        self.verticalLayout = QVBoxLayout(self.qview)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.qscroll2 = QScrollArea(self.qview)
        self.qscroll2.setObjectName(u"qscroll2")
        self.qscroll2.setFont(font2)
        self.qscroll2.setWidgetResizable(True)
        self.queue = QWidget()
        self.queue.setObjectName(u"queue")
        self.queue.setGeometry(QRect(0, 0, 380, 613))
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.queue.sizePolicy().hasHeightForWidth())
        self.queue.setSizePolicy(sizePolicy2)
        self.verticalLayout_5 = QVBoxLayout(self.queue)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setSizeConstraint(QLayout.SetFixedSize)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.qscroll2.setWidget(self.queue)

        self.verticalLayout.addWidget(self.qscroll2)

        self.add_row = QPushButton(self.qview)
        self.add_row.setObjectName(u"add_row")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.add_row.sizePolicy().hasHeightForWidth())
        self.add_row.setSizePolicy(sizePolicy3)
        self.add_row.setFont(font2)

        self.verticalLayout.addWidget(self.add_row)

        self.setq = QPushButton(self.qview)
        self.setq.setObjectName(u"setq")
        sizePolicy3.setHeightForWidth(self.setq.sizePolicy().hasHeightForWidth())
        self.setq.setSizePolicy(sizePolicy3)
        font3 = QFont()
        font3.setFamilies([u"Monaco"])
        font3.setPointSize(30)
        font3.setBold(False)
        font3.setItalic(False)
        self.setq.setFont(font3)

        self.verticalLayout.addWidget(self.setq)


        self.horizontalLayout_2.addWidget(self.qview)

        self.obj = QWidget(self.centralwidget)
        self.obj.setObjectName(u"obj")
        self.obj.setFont(font1)
        self.verticalLayout_3 = QVBoxLayout(self.obj)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.alladin = QWidget(self.obj)
        self.alladin.setObjectName(u"alladin")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.alladin.sizePolicy().hasHeightForWidth())
        self.alladin.setSizePolicy(sizePolicy4)
        self.alladin.setFont(font1)

        self.verticalLayout_3.addWidget(self.alladin)

        self.details = QListWidget(self.obj)
        self.details.setObjectName(u"details")
        self.details.setFont(font1)

        self.verticalLayout_3.addWidget(self.details)


        self.horizontalLayout_2.addWidget(self.obj)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1148, 24))
        self.menuMenu = QMenu(self.menubar)
        self.menuMenu.setObjectName(u"menuMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuMenu.menuAction())
        self.menuMenu.addAction(self.actionAdd_queue)
        self.menuMenu.addAction(self.actionRemove_queue)
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionChange_name)
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionSet_queue)
        self.menuMenu.addSeparator()

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionAdd_queue.setText(QCoreApplication.translate("MainWindow", u"Add queue", None))
        self.actionRemove_queue.setText(QCoreApplication.translate("MainWindow", u"Remove queue", None))
        self.actionSet_queue.setText(QCoreApplication.translate("MainWindow", u"Set queue", None))
        self.actionChange_name.setText(QCoreApplication.translate("MainWindow", u"Change name", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.add_row.setText(QCoreApplication.translate("MainWindow", u"ADD ROW", None))
        self.setq.setText(QCoreApplication.translate("MainWindow", u"SET QUEUE", None))
        self.menuMenu.setTitle(QCoreApplication.translate("MainWindow", u"Menu", None))
    # retranslateUi


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
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QGridLayout, QHBoxLayout,
    QHeaderView, QLayout, QLineEdit, QListWidget,
    QListWidgetItem, QMainWindow, QMenu, QMenuBar,
    QPushButton, QScrollArea, QSizePolicy, QStatusBar,
    QTableView, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1166, 813)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamilies([u"Roboto Flex"])
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
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.qlist = QVBoxLayout()
        self.qlist.setSpacing(0)
        self.qlist.setObjectName(u"qlist")
        self.qlist.setContentsMargins(2, 2, -1, -1)
        self.qobjs_filter = QLineEdit(self.centralwidget)
        self.qobjs_filter.setObjectName(u"qobjs_filter")
        font1 = QFont()
        font1.setFamilies([u"Roboto Flex"])
        font1.setPointSize(14)
        self.qobjs_filter.setFont(font1)

        self.qlist.addWidget(self.qobjs_filter)

        self.qobjs = QListWidget(self.centralwidget)
        self.qobjs.setObjectName(u"qobjs")
        sizePolicy1.setHeightForWidth(self.qobjs.sizePolicy().hasHeightForWidth())
        self.qobjs.setSizePolicy(sizePolicy1)
        font2 = QFont()
        font2.setFamilies([u"Roboto Flex"])
        font2.setPointSize(14)
        font2.setBold(False)
        font2.setItalic(False)
        self.qobjs.setFont(font2)

        self.qlist.addWidget(self.qobjs)


        self.horizontalLayout.addLayout(self.qlist)

        self.qview = QWidget(self.centralwidget)
        self.qview.setObjectName(u"qview")
        sizePolicy1.setHeightForWidth(self.qview.sizePolicy().hasHeightForWidth())
        self.qview.setSizePolicy(sizePolicy1)
        font3 = QFont()
        font3.setFamilies([u"Roboto Flex"])
        font3.setBold(False)
        font3.setItalic(False)
        self.qview.setFont(font3)
        self.verticalLayout = QVBoxLayout(self.qview)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.qscroll2 = QScrollArea(self.qview)
        self.qscroll2.setObjectName(u"qscroll2")
        self.qscroll2.setMinimumSize(QSize(0, 0))
        font4 = QFont()
        font4.setFamilies([u"Roboto Flex"])
        font4.setPointSize(14)
        font4.setBold(True)
        font4.setItalic(False)
        self.qscroll2.setFont(font4)
        self.qscroll2.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.qscroll2.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.qscroll2.setWidgetResizable(True)
        self.qscroll2.setAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.queue = QWidget()
        self.queue.setObjectName(u"queue")
        self.queue.setGeometry(QRect(0, 0, 386, 680))
        sizePolicy1.setHeightForWidth(self.queue.sizePolicy().hasHeightForWidth())
        self.queue.setSizePolicy(sizePolicy1)
        font5 = QFont()
        font5.setFamilies([u"Monaco"])
        font5.setPointSize(11)
        font5.setBold(False)
        font5.setItalic(False)
        self.queue.setFont(font5)
        self.verticalLayout_5 = QVBoxLayout(self.queue)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setSizeConstraint(QLayout.SetFixedSize)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.qscroll2.setWidget(self.queue)

        self.verticalLayout.addWidget(self.qscroll2)

        self.add_row = QPushButton(self.qview)
        self.add_row.setObjectName(u"add_row")
        sizePolicy.setHeightForWidth(self.add_row.sizePolicy().hasHeightForWidth())
        self.add_row.setSizePolicy(sizePolicy)
        font6 = QFont()
        font6.setFamilies([u"Roboto Flex"])
        font6.setPointSize(13)
        font6.setBold(False)
        font6.setItalic(False)
        self.add_row.setFont(font6)

        self.verticalLayout.addWidget(self.add_row)

        self.setq = QPushButton(self.qview)
        self.setq.setObjectName(u"setq")
        sizePolicy.setHeightForWidth(self.setq.sizePolicy().hasHeightForWidth())
        self.setq.setSizePolicy(sizePolicy)
        font7 = QFont()
        font7.setFamilies([u"Roboto Flex"])
        font7.setPointSize(34)
        font7.setBold(False)
        font7.setItalic(False)
        self.setq.setFont(font7)

        self.verticalLayout.addWidget(self.setq)


        self.horizontalLayout.addWidget(self.qview)

        self.obj = QWidget(self.centralwidget)
        self.obj.setObjectName(u"obj")
        sizePolicy2 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.obj.sizePolicy().hasHeightForWidth())
        self.obj.setSizePolicy(sizePolicy2)
        self.obj.setFont(font3)
        self.gridLayout_4 = QGridLayout(self.obj)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.aladin = QWidget(self.obj)
        self.aladin.setObjectName(u"aladin")
        sizePolicy1.setHeightForWidth(self.aladin.sizePolicy().hasHeightForWidth())
        self.aladin.setSizePolicy(sizePolicy1)
        self.aladin.setBaseSize(QSize(0, 0))
        font8 = QFont()
        font8.setFamilies([u"Roboto Flex"])
        font8.setPointSize(11)
        font8.setBold(False)
        font8.setItalic(False)
        self.aladin.setFont(font8)
        self.gridLayout_2 = QGridLayout(self.aladin)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.aladin_view = QWebEngineView(self.aladin)
        self.aladin_view.setObjectName(u"aladin_view")
        sizePolicy1.setHeightForWidth(self.aladin_view.sizePolicy().hasHeightForWidth())
        self.aladin_view.setSizePolicy(sizePolicy1)
        self.aladin_view.setFont(font8)
        self.aladin_view.setUrl(QUrl(u"about:blank"))

        self.gridLayout_2.addWidget(self.aladin_view, 0, 0, 1, 2)

        self.resolve = QPushButton(self.aladin)
        self.resolve.setObjectName(u"resolve")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.resolve.sizePolicy().hasHeightForWidth())
        self.resolve.setSizePolicy(sizePolicy3)
        self.resolve.setMaximumSize(QSize(16777215, 39))
        font9 = QFont()
        font9.setFamilies([u"Roboto Flex"])
        font9.setPointSize(12)
        font9.setBold(False)
        font9.setItalic(False)
        self.resolve.setFont(font9)

        self.gridLayout_2.addWidget(self.resolve, 1, 1, 1, 1)

        self.details_table = QTableView(self.aladin)
        self.details_table.setObjectName(u"details_table")
        sizePolicy1.setHeightForWidth(self.details_table.sizePolicy().hasHeightForWidth())
        self.details_table.setSizePolicy(sizePolicy1)
        self.details_table.setMinimumSize(QSize(0, 0))
        self.details_table.setMaximumSize(QSize(16777215, 180))
        self.details_table.setFont(font2)
        self.details_table.horizontalHeader().setVisible(False)

        self.gridLayout_2.addWidget(self.details_table, 3, 0, 1, 2)

        self.obj_name = QLineEdit(self.aladin)
        self.obj_name.setObjectName(u"obj_name")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.obj_name.sizePolicy().hasHeightForWidth())
        self.obj_name.setSizePolicy(sizePolicy4)
        self.obj_name.setMinimumSize(QSize(0, 0))
        self.obj_name.setMaximumSize(QSize(16777215, 20))
        self.obj_name.setFont(font2)

        self.gridLayout_2.addWidget(self.obj_name, 1, 0, 1, 1)


        self.gridLayout_4.addWidget(self.aladin, 0, 0, 1, 1)

        self.skyplot = QWidget(self.obj)
        self.skyplot.setObjectName(u"skyplot")
        sizePolicy1.setHeightForWidth(self.skyplot.sizePolicy().hasHeightForWidth())
        self.skyplot.setSizePolicy(sizePolicy1)
        self.skyplot.setMinimumSize(QSize(0, 0))
        self.skyplot.setMaximumSize(QSize(16777215, 300))
        self.skyplot.setFont(font2)

        self.gridLayout_4.addWidget(self.skyplot, 2, 0, 1, 2)


        self.horizontalLayout.addWidget(self.obj)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1166, 24))
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
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"qman", None))
        self.actionAdd_queue.setText(QCoreApplication.translate("MainWindow", u"Add queue", None))
        self.actionRemove_queue.setText(QCoreApplication.translate("MainWindow", u"Remove queue", None))
        self.actionSet_queue.setText(QCoreApplication.translate("MainWindow", u"Set queue", None))
        self.actionChange_name.setText(QCoreApplication.translate("MainWindow", u"Change name", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.qobjs_filter.setInputMask("")
        self.qobjs_filter.setText("")
        self.qobjs_filter.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search...", None))
        self.add_row.setText(QCoreApplication.translate("MainWindow", u"ADD ROW", None))
        self.setq.setText(QCoreApplication.translate("MainWindow", u"SET QUEUE", None))
        self.resolve.setText(QCoreApplication.translate("MainWindow", u"Resolve", None))
        self.menuMenu.setTitle(QCoreApplication.translate("MainWindow", u"Menu", None))
    # retranslateUi


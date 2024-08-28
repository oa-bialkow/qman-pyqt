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
        MainWindow.resize(1107, 862)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamilies([u"Noto Mono"])
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
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
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
        self.qobjs_filter.setFont(font)

        self.qlist.addWidget(self.qobjs_filter)

        self.qobjs = QListWidget(self.centralwidget)
        self.qobjs.setObjectName(u"qobjs")
        sizePolicy.setHeightForWidth(self.qobjs.sizePolicy().hasHeightForWidth())
        self.qobjs.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setFamilies([u"Noto Mono"])
        font1.setPointSize(11)
        font1.setBold(False)
        font1.setItalic(False)
        self.qobjs.setFont(font1)

        self.qlist.addWidget(self.qobjs)


        self.horizontalLayout.addLayout(self.qlist)

        self.qview = QWidget(self.centralwidget)
        self.qview.setObjectName(u"qview")
        sizePolicy.setHeightForWidth(self.qview.sizePolicy().hasHeightForWidth())
        self.qview.setSizePolicy(sizePolicy)
        font2 = QFont()
        font2.setFamilies([u"Noto Mono"])
        font2.setBold(False)
        font2.setItalic(False)
        self.qview.setFont(font2)
        self.verticalLayout = QVBoxLayout(self.qview)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.qscroll2 = QScrollArea(self.qview)
        self.qscroll2.setObjectName(u"qscroll2")
        self.qscroll2.setMinimumSize(QSize(0, 0))
        self.qscroll2.setFont(font1)
        self.qscroll2.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.qscroll2.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.qscroll2.setWidgetResizable(True)
        self.qscroll2.setAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.queue = QWidget()
        self.queue.setObjectName(u"queue")
        self.queue.setGeometry(QRect(0, 0, 367, 733))
        sizePolicy.setHeightForWidth(self.queue.sizePolicy().hasHeightForWidth())
        self.queue.setSizePolicy(sizePolicy)
        font3 = QFont()
        font3.setFamilies([u"Monaco"])
        font3.setPointSize(11)
        font3.setBold(False)
        font3.setItalic(False)
        self.queue.setFont(font3)
        self.verticalLayout_5 = QVBoxLayout(self.queue)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setSizeConstraint(QLayout.SetFixedSize)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.qscroll2.setWidget(self.queue)

        self.verticalLayout.addWidget(self.qscroll2)

        self.add_row = QPushButton(self.qview)
        self.add_row.setObjectName(u"add_row")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.add_row.sizePolicy().hasHeightForWidth())
        self.add_row.setSizePolicy(sizePolicy1)
        self.add_row.setFont(font1)

        self.verticalLayout.addWidget(self.add_row)

        self.setq = QPushButton(self.qview)
        self.setq.setObjectName(u"setq")
        sizePolicy1.setHeightForWidth(self.setq.sizePolicy().hasHeightForWidth())
        self.setq.setSizePolicy(sizePolicy1)
        font4 = QFont()
        font4.setFamilies([u"Noto Mono"])
        font4.setPointSize(30)
        font4.setBold(False)
        font4.setItalic(False)
        self.setq.setFont(font4)

        self.verticalLayout.addWidget(self.setq)


        self.horizontalLayout.addWidget(self.qview)

        self.obj = QWidget(self.centralwidget)
        self.obj.setObjectName(u"obj")
        sizePolicy2 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.obj.sizePolicy().hasHeightForWidth())
        self.obj.setSizePolicy(sizePolicy2)
        self.obj.setFont(font2)
        self.gridLayout_4 = QGridLayout(self.obj)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.aladin = QWidget(self.obj)
        self.aladin.setObjectName(u"aladin")
        sizePolicy.setHeightForWidth(self.aladin.sizePolicy().hasHeightForWidth())
        self.aladin.setSizePolicy(sizePolicy)
        self.aladin.setFont(font1)
        self.gridLayout_2 = QGridLayout(self.aladin)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.aladin_view = QWebEngineView(self.aladin)
        self.aladin_view.setObjectName(u"aladin_view")
        self.aladin_view.setUrl(QUrl(u"about:blank"))

        self.gridLayout_2.addWidget(self.aladin_view, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.aladin, 0, 0, 1, 1)

        self.details = QWidget(self.obj)
        self.details.setObjectName(u"details")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.details.sizePolicy().hasHeightForWidth())
        self.details.setSizePolicy(sizePolicy3)
        self.details.setMaximumSize(QSize(16777215, 163))
        self.details.setFont(font2)
        self.gridLayout = QGridLayout(self.details)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.obj_layout = QHBoxLayout()
        self.obj_layout.setSpacing(0)
        self.obj_layout.setObjectName(u"obj_layout")
        self.obj_layout.setContentsMargins(0, -1, -1, -1)
        self.obj_name = QLineEdit(self.details)
        self.obj_name.setObjectName(u"obj_name")
        sizePolicy3.setHeightForWidth(self.obj_name.sizePolicy().hasHeightForWidth())
        self.obj_name.setSizePolicy(sizePolicy3)
        self.obj_name.setFont(font1)

        self.obj_layout.addWidget(self.obj_name)

        self.resolve = QPushButton(self.details)
        self.resolve.setObjectName(u"resolve")
        self.resolve.setFont(font1)

        self.obj_layout.addWidget(self.resolve)


        self.gridLayout.addLayout(self.obj_layout, 0, 0, 1, 1)

        self.details_table = QTableView(self.details)
        self.details_table.setObjectName(u"details_table")
        sizePolicy1.setHeightForWidth(self.details_table.sizePolicy().hasHeightForWidth())
        self.details_table.setSizePolicy(sizePolicy1)
        self.details_table.setFont(font1)
        self.details_table.horizontalHeader().setVisible(False)

        self.gridLayout.addWidget(self.details_table, 1, 0, 1, 1)


        self.gridLayout_4.addWidget(self.details, 1, 0, 1, 2)

        self.skyplot = QWidget(self.obj)
        self.skyplot.setObjectName(u"skyplot")
        sizePolicy.setHeightForWidth(self.skyplot.sizePolicy().hasHeightForWidth())
        self.skyplot.setSizePolicy(sizePolicy)
        self.skyplot.setMinimumSize(QSize(298, 298))
        self.skyplot.setMaximumSize(QSize(1400, 1400))

        self.gridLayout_4.addWidget(self.skyplot, 2, 0, 1, 2)


        self.horizontalLayout.addWidget(self.obj)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1107, 24))
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


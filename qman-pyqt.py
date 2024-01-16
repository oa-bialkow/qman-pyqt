#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 12:05:04 2024
This is the program for Andor CCDOBS quene management. It is written in Python 3.11 and
uses PyQt5 for the GUI. It is based on the PyQt5 designer file ui_bltman.ui.

authors: 
    K. Kotysz:      k.kotysz(at)gmail.com
    P. Mikolajczyk: przeminio(at)gmail.com
"""

import sys
from typing import Sequence
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QDoubleSpinBox, QComboBox, QSpinBox, QHBoxLayout, QWidget, QInputDialog, QPushButton
from PySide6.QtCore import SIGNAL, Qt
from ui_qman_pyqt import Ui_MainWindow
import pandas as pd
import numpy as np
from datetime import datetime as dt
import logging
# from astropy.coordinates import Angle, SkyCoord, EarthLocation, AltAz, ICRS, name_resolve
# from astropy.time import Time
# from astropy import units as u
# import ephem
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
# os.environ['QT_MAC_WANTS_LAYER'] = '1'    # to work on MacOS

class QueueObject:
    def __init__(self, name, n_exp, img_type, filter_type, exp_t, readout_time):
        self.name = name
        self.n_exp = n_exp
        self.img_type = img_type
        self.filter_type = filter_type
        self.exp_t = exp_t
        self.readout_time = readout_time
    
    def countQTime(self):
        n_px = 1252*1152
        total_exp_t = [a*b for a,b in zip(self.n_exp,self.exp_t)]
        total_readout_time = [a*b*1e-6*n_px for a,b in zip(self.n_exp,self.readout_time)]
        return np.sum(total_exp_t) + np.sum(total_readout_time)
    
class qrow_widget(QWidget):
    def __init__(self, qrow, qrows):
        super().__init__()
        self.qrows = qrows
        self.nexp = QSpinBox()    
        self.nexp.setValue(qrow['Number'])
        self.nexp.setMinimum(1)
        self.nexp.setMaximum(9999)
        self.imptyp = QComboBox()
        self.imptyp.addItems(['Bias', 'Dark', 'Image'])
        self.imptyp.setCurrentText(qrow['Type'])
        self.filter = QComboBox()
        self.filter.addItems(['U', 'B', 'V', 'R', 'I', 'Han', 'Haw', 'None'])
        self.filter.setCurrentText(qrow['Filter'])
        self.exptime = QDoubleSpinBox()
        self.exptime.setMinimum(0.0)
        self.exptime.setMaximum(9999.0)
        self.exptime.setDecimals(2)
        self.exptime.setSingleStep(0.01)
        self.exptime.setValue(qrow['Exposure'])
        self.rot = QComboBox()
        self.rot.addItems(['1', '2', '16'])
        self.rot.setCurrentText(qrow['ROT'])
        self.delrow = QPushButton('Delete')
        self.delrow.clicked.connect(self.deleterow)
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(0)
        layout.setStretch(0, 1)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.nexp)
        layout.addWidget(self.imptyp)
        layout.addWidget(self.filter)
        layout.addWidget(self.exptime)
        layout.addWidget(self.rot)
        layout.addWidget(self.delrow)
        self.setLayout(layout)

    def deleterow(self):
        self.deleteLater()
        self.qrows.remove(self)
        logging.info(f'Row deleted!')
    
class QmanMain(QMainWindow):
    def __init__(self, cargs):
        super(QmanMain, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ccdobs = cargs[1]
        self.qobjs = self.get_qlist()
        self.qrows = []

        # Fill QListWidget with objects
        for obj in sorted(self.qobjs['Object'].unique(), key=str.lower):
            self.ui.qobjs.addItem(obj)
        # Connect QListWidget click to function
        self.ui.qobjs.connect(self.ui.qobjs, SIGNAL("itemClicked(QListWidgetItem *)"), self.on_qlist_item_clicked)
        # Set first object as current at startup
        self.ui.qobjs.setCurrentItem(self.ui.qobjs.item(0))
        self.on_qlist_item_clicked(self.ui.qobjs.item(0))
        # Connect SetQueue button to function
        self.ui.setq.clicked.connect(self.set_queue)
        self.ui.actionSet_queue.triggered.connect(self.set_queue)
        self.ui.setq.setShortcut('Ctrl+S')
        # Connect Add Queue button to function
        self.ui.actionAdd_queue.triggered.connect(self.add_queue)
        # Connect Add Row button to function
        self.ui.add_row.clicked.connect(self.add_row)
        # Connect Remove Queue button to function
        self.ui.actionRemove_queue.triggered.connect(self.remove_queue)
        self.ui.statusbar.showMessage(f'{dt.now().strftime("%H:%M:%S")} Ready!')
        logging.info(f'Ready!')

    def set_queue(self):
        self.qobjs = self.get_qlist()
        # Set current queue as 0_CURRENT_QUEUE
        self.qobjs = self.qobjs[self.qobjs['Object'] != '0_CURRENT_QUEUE'] # remove all 0_CURRENT_QUEUEs from list
        self.qobjs = pd.concat([self.get_current_queue('0_CURRENT_QUEUE'), self.qobjs]) # add current queue to list
        self.save_queue()
        self.ui.statusbar.showMessage(f'{dt.now().strftime("%H:%M:%S")} Queue set!')
        logging.info(f'Queue set!')

    def save_queue(self):
        # Save all queues to file
        self.current_queue = self.qobjs[self.qobjs['Object'] == '0_CURRENT_QUEUE']
        with open('ccdobs.lst', 'w') as f:
            for n, row in self.current_queue.iterrows():
                row['Filter'] = 'Ha narrow' if row['Filter'] == 'Han' else row['Filter']
                row['Filter'] = 'Ha wide' if row['Filter'] == 'Haw' else row['Filter']
                f.write(f"{row['Number']:^5d}{row['Type']:<7s}{row['Filter']:<11s}{row['Exposure']:<7.1f}{row['ROT']:<2s}\n")
            f.write('\n')

            all_queues = self.qobjs[self.qobjs['Object'] != '0_CURRENT_QUEUE']
            for obj in all_queues['Object'].unique():
                obj_queue = all_queues[all_queues['Object'] == obj]
                f.write(f"% {obj}\n")
                for n, row in obj_queue.iterrows():
                    row['Filter'] = 'Ha narrow' if row['Filter'] == 'Han' else row['Filter']
                    row['Filter'] = 'Ha wide' if row['Filter'] == 'Haw' else row['Filter']
                    f.write(f"{row['Number']:^5d}{row['Type']:<7s}{row['Filter']:<11s}{row['Exposure']:<7.1f}{row['ROT']:<2s}\n")
                f.write('\n')
    
    def get_current_queue(self, text):
        curr_q = pd.DataFrame()
        for wid in self.qrows:
            obj = { 'Object':   [text], 
                    'Number':   [wid.nexp.value()], 
                    'Type':     [wid.imptyp.currentText()], 
                    'Filter':   [wid.filter.currentText()], 
                    'Exposure': [wid.exptime.value()],
                    'ROT':      [wid.rot.currentText()]
                    }
            curr_q = pd.concat([curr_q, pd.DataFrame(obj)])
        return curr_q

    def remove_queue(self):
        # show dialog with name input
        self.qobjs = self.get_qlist()
        name = self.ui.qobjs.currentItem().text()
        self.qobjs = self.qobjs[self.qobjs['Object'] != name]
        self.save_queue()
        self.ui.qobjs.takeItem(self.ui.qobjs.currentRow())
        self.ui.qobjs.setCurrentItem(self.ui.qobjs.item(0))
        self.on_qlist_item_clicked(self.ui.qobjs.item(0))
        self.ui.statusbar.showMessage(f'{dt.now().strftime("%H:%M:%S")} Queue for {name} removed!')
        logging.info(f'Queue for {name} removed!')

    def add_queue(self):
        # show dialog with name input
        self.qobjs = self.get_qlist()
        text, ok = QInputDialog.getText(self, 'Add queue', 'Object name:')
        if ok:
            self.ui.qobjs.addItem(text)
            toadd = self.get_current_queue(text)
            self.qobjs = pd.concat([toadd, self.qobjs])
            self.save_queue()
        self.ui.qobjs.sortItems()
        self.ui.qobjs.setCurrentItem(self.ui.qobjs.findItems(text, Qt.MatchExactly)[0])
        self.on_qlist_item_clicked(self.ui.qobjs.currentItem())
        self.ui.statusbar.showMessage(f'{dt.now().strftime("%H:%M:%S")} Queue for {text} added!')
        logging.info(f'Queue for {text} added!')

    def add_row(self):
        empty_row = {'Object': 'Foo', 'Number': 1, 'Type': 'Image', 'Filter': 'None', 'Exposure': 0.0, 'ROT': '16'}
        new_qrow = qrow_widget(empty_row, self.qrows)
        self.qrows.append(new_qrow)
        self.ui.queue.layout().addWidget(new_qrow)
        self.ui.statusbar.showMessage(f'{dt.now().strftime("%H:%M:%S")} Row added!')
        logging.info(f'Row added!')

    def on_qlist_item_clicked(self, item):
        clicked_queue = self.qobjs[self.qobjs['Object'] == item.text()]
        for wid in self.qrows:
            wid.deleteLater()
        self.qrows = []
        for n, row in clicked_queue.iterrows():
            new_qrow = qrow_widget(row, self.qrows)
            self.qrows.append(new_qrow)
            self.ui.queue.layout().addWidget(new_qrow)
        self.ui.statusbar.showMessage(f'{dt.now().strftime("%H:%M:%S")} Queue for {item.text()} loaded!')
        logging.info(f'Queue for {item.text()} loaded!')

    def get_qlist(self):
        data = {'Object': [], 'Number': [], 'Type': [], 'Filter': [], 'Exposure': [], 'ROT': []}
        with open(self.ccdobs, 'r') as file:
            current_object_name = '0_CURRENT_QUEUE'
            for line in file:
                line = line.replace('Ha narrow', 'Han') if 'Ha narrow' in line else line
                line = line.replace('Ha wide', 'Haw') if 'Ha wide' in line else line
                line = line.strip()
                if line.startswith('%'):
                    current_object_name = line[1:].strip()
                else:
                    parts = line.split()
                    if parts:
                        data['Object'].append(current_object_name)
                        data['Number'].append(int(parts[0]))
                        data['Type'].append(parts[1])
                        data['Filter'].append(parts[2])
                        data['Exposure'].append(float(parts[3]))
                        data['ROT'].append(str(parts[4]))

        return pd.DataFrame(data)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\n Usage: qman-pyqt.py <ccdobs.lst>")
        print(" Version of 12.01.2024 by K. Kotysz: k.kotysz(at)gmail.com")
        print("                          P. Mikolajczyk: przeminio(at)gmail.com")
        sys.exit(1)
    else:
        app = QApplication(sys.argv)
        window = QmanMain(sys.argv)
        window.show()
        sys.exit(app.exec())

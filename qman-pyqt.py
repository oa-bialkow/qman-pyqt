#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 12:05:04 2024
This is the program for Andor CCDOBS queue management. It is written in Python 3.11 and
uses PySide6 (PyQt6) for the GUI. It is based on the PyQt6 designer file qman-pyqt.ui. 
Every change in ui file must be converted to Python file with command:
    pyside6-uic qman-pyqt.ui -o ui_qman_pyqt.py

authors: 
    K. Kotysz:      k.kotysz(at)gmail.com
    P. Mikolajczyk: przeminio(at)gmail.com
"""

import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QInputDialog
from widgets import qrow_widget, CurrentQueue, update_table, ObjectInfo, SkyView
from PySide6.QtCore import SIGNAL, Qt
from ui_qman_pyqt import Ui_MainWindow
import pandas as pd
import numpy as np
import json
from datetime import datetime as dt
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', filemode='w', filename='qman.log')
# os.environ['QT_MAC_WANTS_LAYER'] = '1'    # to work on MacOS

class QmanMain(QMainWindow):
    def __init__(self, cargs):
        super(QmanMain, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ccdobs = cargs[1]
        self.qobjs = self.get_qlist()
        self.qrows = []
        logging.info(f'QMAN started!')
        logging.info(f'CCDOBS file: {self.ccdobs}')
        # SkyView instance
        self.skyview = SkyView(self.ui)

        # Read objpos.dat file
        self.objpos = pd.read_csv(cargs[2], sep='\s+', header=None,
                                  names=['Object', 'RAd', 'RAm', 'RAs', 
                                         'DECd', 'DECm', 'DECs', 'Epoch', 
                                         'Pier side', 'Guiding star', 'Guider position'],
                                  comment='#', skipinitialspace=True)
        # Fill QListWidget with objects
        for obj in sorted(self.qobjs['Object'].unique(), key=str.lower):
            self.ui.qobjs.addItem(obj)
        # Connect QListWidget click to function
        self.ui.qobjs.connect(self.ui.qobjs, SIGNAL("itemClicked(QListWidgetItem *)"), self.on_qlist_item_clicked)
        # Set first object as current at startup
        self.ui.qobjs.setCurrentItem(self.ui.qobjs.item(0))
        self.on_qlist_item_clicked(self.ui.qobjs.item(0))
        # self.ui.qview.setMinimumWidth(qrow_widget.sizeHint().width())
        self.ui.qview.setMinimumWidth(380)
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
        # Connect Change Name button to function
        self.ui.actionChange_name.triggered.connect(self.change_name)
        # Connect Resolve button to function
        self.ui.resolve.clicked.connect(self.get_obj_data)
        # Connect Filter inpout to function on text change
        self.ui.qobjs_filter.textChanged.connect(self.filter_qobjs)


        self.ui.statusbar.showMessage(f'{dt.now().strftime("%H:%M:%S")} Ready!')
        logging.info(f'Ready!')

    def set_queue(self):
        self.qobjs = self.get_qlist()
        curr_q = CurrentQueue(self.qrows, '0_CURRENT_QUEUE')
        # Set current queue as 0_CURRENT_QUEUE
        self.qobjs = self.qobjs[self.qobjs['Object'] != '0_CURRENT_QUEUE'] # remove all 0_CURRENT_QUEUEs from list
        self.qobjs = pd.concat([curr_q.queue, self.qobjs]) # add current queue to list
        self.save_queue()
        rtcoor_path = '/dev/shm/rtcoor.data' if os.path.exists('/dev/shm') else 'rtcoor.data'
        with open(rtcoor_path, 'w') as f:
            ra = self.my_obj.ra
            json.dump({'ra': np.round(self.my_obj.ra, 5), 
                       'dec': np.round(self.my_obj.dec, 5),
                       'dec_sex': self.table_data['DEC'].values[0].split()[0],
                       'ha': np.round(self.my_obj.ha, 5),
                       'ha_sex': self.table_data['HA'].values[0].split()[0],
                       'alt': np.round(self.my_obj.alt, 1), 
                       'az': np.round(self.my_obj.az, 1), 
                       'objname': self.my_obj.objname},
                       f)
        self.ui.statusbar.showMessage(f'{dt.now().strftime("%H:%M:%S")} Queue set!')
        logging.info(f'Queue set!')

    def save_queue(self):
        # Save all queues to file
        self.current_queue = self.qobjs[self.qobjs['Object'] == '0_CURRENT_QUEUE']
        with open(self.ccdobs, 'w') as f:
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
            toadd = CurrentQueue(self.qrows, text).queue
            self.qobjs = pd.concat([toadd, self.qobjs])
            self.save_queue()
            self.ui.qobjs.sortItems()
            self.ui.qobjs.setCurrentItem(self.ui.qobjs.findItems(text, Qt.MatchExactly)[0])
            self.on_qlist_item_clicked(self.ui.qobjs.currentItem())
            self.ui.statusbar.showMessage(f'{dt.now().strftime("%H:%M:%S")} Queue for {text} added!')
            logging.info(f'Queue for {text} added!')
    
    def change_name(self):
        # show dialog with name input
        text, ok = QInputDialog.getText(self, 'Change name', 'Object name:')
        if ok:
            old_name = self.ui.qobjs.currentItem().text()
            self.ui.qobjs.currentItem().setText(text)
            self.ui.qobjs.setCurrentItem(self.ui.qobjs.findItems(text, Qt.MatchExactly)[0])
            self.qobjs = self.qobjs.replace(old_name, text)
            self.on_qlist_item_clicked(self.ui.qobjs.currentItem())
            self.save_queue()
            self.ui.qobjs.sortItems()
            self.ui.statusbar.showMessage(f'{dt.now().strftime("%H:%M:%S")} Name changed to {text}!')
            logging.info(f'Name changed to {text}!')
    
    @update_table
    def add_row(self):
        # Add row to queue
        empty_row = {'Object': 'Foo', 'Number': 1, 'Type': 'Image', 'Filter': 'None', 'Exposure': 1.0, 'ROT': '16'}
        new_qrow = qrow_widget(empty_row, self.qrows, self)
        self.qrows.append(new_qrow)
        self.ui.queue.layout().addWidget(new_qrow)
        qtime = CurrentQueue(self.qrows, 'dummy').countQueue()
        self.table_data['Queue time'] = str(qtime)
        self.ui.statusbar.showMessage(f'{dt.now().strftime("%H:%M:%S")} Row added!')
        logging.info(f'Row added!')
        return self
    
    def on_qlist_item_clicked(self, item):
        clicked_queue = self.qobjs[self.qobjs['Object'] == item.text()]
        self.ui.obj_name.setText(item.text())
        for wid in self.qrows:
            wid.deleteLater()
        self.qrows = []
        for n, row in clicked_queue.iterrows():
            new_qrow = qrow_widget(row, self.qrows, self)
            self.qrows.append(new_qrow)
            self.ui.queue.layout().addWidget(new_qrow)
        self.get_obj_data()
        self.ui.statusbar.showMessage(f'{dt.now().strftime("%H:%M:%S")} Queue for {item.text()} loaded!')
        logging.info(f'Queue for {item.text()} loaded!')

    def get_qlist(self):
        # Read CCD queue from file
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
    
    
    @update_table
    def get_obj_data(self):
        objname = self.ui.obj_name.text()
        qtime = CurrentQueue(self.qrows, objname).countQueue()
        # Initialize table as pandas DataFrame from dictionary
        data = {'Object': [objname], 'RA': [''], 'DEC': [''], 'HA': [''], 'Alt': [''], 'Queue time': [str(qtime)]}
        self.table_data = pd.DataFrame.from_dict(data)
        # Get object data from astropy
        self.my_obj = ObjectInfo(objname, self.objpos)
        obj_alt, obj_az, obj_ha, ra, dec, found = self.my_obj.get_info()
        self.table_data['RA'] = f'{ra} (J2000)' if found else f'{ra} (J2000)*'
        self.table_data['DEC'] = f'{dec} (J2000)' if found else f'{dec} (J2000)*'
        self.table_data['HA'] = f'{obj_ha}'
        self.table_data['Alt'] = f'{obj_alt}'
        # if objname != '0_CURRENT_QUEUE' and objname not in self.objpos['Object'].values:
        # elif objname != '0_CURRENT_QUEUE':
        return self

    def filter_qobjs(self):
        filt_obj = self.ui.qobjs_filter.text()
        all_obj = self.qobjs['Object'].unique()
        filtered = filter(lambda x: filt_obj.lower() in x.lower(), all_obj)
        self.ui.qobjs.clear()
        for obj in sorted(filtered, key=str.lower):
            self.ui.qobjs.addItem(obj)



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\n Usage: qman-pyqt.py <ccdobs.lst> <objpos.dat>")
        print(" Version of 12.01.2024 by K. Kotysz: k.kotysz(at)gmail.com")
        print("                          P. Mikolajczyk: przeminio(at)gmail.com")
        sys.exit(1)
    else:
        app = QApplication(sys.argv)
        window = QmanMain(sys.argv)
        window.show()
        sys.exit(app.exec())

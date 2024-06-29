from PySide6.QtWidgets import QDoubleSpinBox, QComboBox, QSpinBox, QHBoxLayout, QWidget, QPushButton, QHeaderView, QSizePolicy
from PySide6.QtCore import Qt
from PySide6 import QtCore, QtGui
import logging
import time
import pandas as pd
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, Angle
from astropy import units as u
from astropy.coordinates import name_resolve
from datetime import datetime as dt
import ephem
from astropy.time import Time
import numpy as np
from baladin import Aladin
import os

'''
Function to normalize object names - remove spaces, underscores, dashes, brackets, commas, and equal signs and convert to lowercase
This is used to compare the object name in the queue with the object name in the objpos.dat file
The function returns a tuple with two options to handle different naming conventions
'''
def normalize_objname(name):
    opt1 = name.replace(' ', '').split('_')[0].split('-')[0].split('(')[0].split('[')[0].split(',')[0].split('=')[0].lower()
    opt2 = name.replace('_', '').split('_')[0].split('-')[0].split('(')[0].split('[')[0].split(',')[0].split('=')[0].lower()
    return (opt1, opt2)

class ObjectInfo:
    def __init__(self, objname, objpos):
        self.objname = objname
        self.objpos = objpos
        self.myobs = ephem.Observer()
        self.myobs.lon = 16.656667
        self.myobs.lat = 51.476111
        self.myobs.elevation = 130
        self.myobs.date = str(Time(dt.utcnow(), scale='ut1', location=(self.myobs.lon * u.deg, self.myobs.lat * u.deg)))  # Time in UT
        self.ra = None
        self.dec = None
        self.alt = None
        self.az = None
        self.ha = None

    def get_info(self):
        norm_obj_name = normalize_objname(self.objname) # Normalize the object name (tuple with two options)
        norm_objpos = self.objpos['Object'].apply(normalize_objname).values # Normalize the object names in objpos.dat (list of tuples)
        flattened_list = [item for sublist in norm_objpos for item in sublist] # Flatten the list of tuples
        if any(obj in flattened_list for obj in norm_obj_name) and self.objname != '0_CURRENT_QUEUE': # Check if any of the normalized object names is in the list of normalized object names
            mask = [obj in flattened_list for obj in norm_obj_name] # Create a mask to find the matching object name
            matched_name = np.array(norm_obj_name)[mask][0] # Extract the matched object name
            matching_row_index = self.objpos.index[self.objpos['Object'].apply(normalize_objname).apply(lambda x: matched_name in x)].tolist() # Find the row index where the tuple contains the desired string
            obj = self.objpos.iloc[matching_row_index] # Extract the matching row
            ra = f"{int(obj['RAd'].values[0]):2d}:{int(obj['RAm'].values[0]):02d}:{int(obj['RAs'].values[0]):02d} (J{obj['Epoch'].values[0]})"
            dec = f"{obj['DECd'].values[0].zfill(2)}:{int(obj['DECm'].values[0]):02d}:{int(obj['DECs'].values[0]):02d} (J{obj['Epoch'].values[0]})"
            self.c = SkyCoord(ra=ra.split()[0], dec=dec.split()[0], frame='icrs', unit=(u.hourangle, u.deg))
            found = True
            logging.info(f'{self.objname} found in objpos.dat!')
        else:
            try:
                self.c = SkyCoord.from_name(self.objname)
                logging.info(f'{self.objname} resolved!')
                found = False
            except name_resolve.NameResolveError:
                self.c = SkyCoord.from_name('M1')
                logging.info(f'{self.objname} not found!')
                return ('--', '--', '--', '--', '--', False)

        obs_location = EarthLocation(lat=self.myobs.lat*u.deg, lon=self.myobs.lon*u.deg, height=self.myobs.elevation*u.m)
        obs_time = Time(dt.utcnow(), scale='ut1', location=obs_location)
        obs_altaz = AltAz(location=obs_location, obstime=obs_time, pressure=1010.0 * u.hPa, temperature=10.0 * u.deg_C,
            relative_humidity=20, obswl=0.6 * u.micron)
        obj_altaz = self.c.transform_to(obs_altaz)
        # obj_alt = obj_altaz.alt.to_string(u.deg, sep=':', precision=0)
        obj_alt = f'{obj_altaz.alt.degree:.2f}°'
        obj_az = obj_altaz.az.to_string(u.deg, sep=':', precision=0)
        sidereal_time = obs_time.sidereal_time('apparent', obs_location.lon)
        if sidereal_time - self.c.ra < 0:
            obj_hms = 360*u.deg + sidereal_time - self.c.ra
        else:
            obj_hms = sidereal_time - self.c.ra
        obj_ha = f'{obj_hms.hms[0]:02.0f}:{obj_hms.hms[1]:02.0f}:{obj_hms.hms[2]:02.0f}'
        ra = self.c.ra.to_string(u.hour, sep=':', precision=0)
        dec = self.c.dec.to_string(u.deg, sep=':', precision=0, pad=True, alwayssign=True)
        self.ra = self.c.ra.value
        self.dec = self.c.dec.value
        self.ha = obj_hms.degree
        self.alt = obj_altaz.alt.degree
        self.az = obj_altaz.az.degree
        return (obj_alt, obj_az, obj_ha, ra, dec, found)

def update_table(func):
    def wrapper_update_table(*args, **kwargs):
        obj = func(*args, **kwargs)
        obj.ui.details_table.setModel(TableModel(obj.table_data))
        obj.ui.details_table.resizeColumnsToContents()
        obj.ui.details_table.resizeRowsToContents()
        header = obj.ui.details_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        obj.skyview.create_aladin_view(obj.my_obj.c.ra.deg, obj.my_obj.c.dec.deg)
    return wrapper_update_table

class CurrentQueue:
    def __init__(self, qrows, text):
        self.queue = pd.DataFrame()
        for wid in qrows:
            obj = { 'Object':   [text], 
                    'Number':   [wid.nexp.value()], 
                    'Type':     [wid.imptyp.currentText()], 
                    'Filter':   [wid.filter.currentText()], 
                    'Exposure': [wid.exptime.value()],
                    'ROT':      [wid.rot.currentText()]
                    }
            self.queue = pd.concat([self.queue, pd.DataFrame(obj)])

    def countQueue(self):
        n_px = 1252*1152
        total_exp_t = self.queue['Number']*self.queue['Exposure']
        total_readout_time = self.queue['Number']*self.queue['ROT'].apply(int)*1e-6*n_px
        q_time  = total_exp_t.sum() + total_readout_time.sum()
        time_obj = time.gmtime(q_time)
        resultant_time = time.strftime("%Hh %Mm %Ss",time_obj)
        return f'{resultant_time} ({q_time:.1f} s)' # convert to hms
    
class qrow_widget(QWidget):
    def __init__(self, qrow, qrows, obj):
        super().__init__()
        self.obj = obj
        self.nexp = QSpinBox()    
        self.nexp.setValue(qrow['Number'])
        self.nexp.setMinimum(1)
        self.nexp.setMaximum(999)
        self.nexp.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.nexp.valueChanged.connect(lambda: self.on_value_changed())

        self.imptyp = QComboBox()
        self.imptyp.addItems(['Bias', 'Dark', 'Image'])
        self.imptyp.setCurrentText(qrow['Type'])
        self.imptyp.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.filter = QComboBox()
        self.filter.addItems(['U', 'B', 'V', 'R', 'I', 'Han', 'Haw', 'None'])
        self.filter.setCurrentText(qrow['Filter'])
        self.filter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.exptime = QDoubleSpinBox()
        self.exptime.setMinimum(0.0)
        self.exptime.setMaximum(9999.0)
        self.exptime.setDecimals(1)
        self.exptime.setSingleStep(1)
        self.exptime.setValue(qrow['Exposure'])
        self.exptime.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.exptime.valueChanged.connect(lambda: self.on_value_changed())

        self.rot = QComboBox()
        self.rot.addItems(['1', '2', '16'])
        self.rot.setCurrentText(qrow['ROT'])
        self.rot.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.rot.currentTextChanged.connect(lambda: self.on_value_changed())

        self.delrow = QPushButton('')
        self.delrow.clicked.connect(self.deleterow)
        delicon = QtGui.QIcon('assets/delete-64.png')
        self.delrow.setIcon(delicon)
        self.delrow.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QHBoxLayout()
        # layout.setAlignment(Qt.AlignTop)
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

    @update_table
    def on_value_changed(self):
        qtime = CurrentQueue(self.obj.qrows, 'dummy').countQueue()
        self.obj.table_data['Queue time'] = str(qtime)
        logging.info(f'Queue time updated!')
        return self.obj

    @update_table
    def deleterow(self):
        self.deleteLater()
        self.obj.qrows.remove(self)
        qtime = CurrentQueue(self.obj.qrows, 'dummy').countQueue()
        self.obj.table_data['Queue time'] = str(qtime)
        logging.info(f'Row deleted!')
        return self.obj

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data.T

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])
            else:
                return str(self._data.index[section])

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            row = index.row()
            column = index.column()
            value = self._data.iloc[row][column]
            return str(value)
        elif role == QtCore.Qt.TextAlignmentRole:
            return Qt.AlignCenter

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._data.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._data.columns.values)
    
class SkyView:

    def __init__(self, ui):
        self.aladin_path = os.path.join('assets', 'index.html')
        self.ui = ui

    def create_aladin_view(self, ra, dec):
        a = Aladin(target=f'{ra} {dec}', width=self.ui.aladin_view.width()*0.94, height=self.ui.aladin_view.height()*0.9, fov=12*u.arcmin.to(u.deg))
        a.b1 = a.b1.replace(', cooFrame: "ICRSd"', ', cooFrame: "ICRSd", fullScreen: true') # make it fullscreen
        a.create()
        a.save(self.aladin_path)
        self.ui.aladin_view.setHtml(open(self.aladin_path).read())
        # self.aladin.loadFinished.connect(lambda: self.aladin_page_loaded())
    

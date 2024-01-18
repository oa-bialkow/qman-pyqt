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

class ObjectInfo:
    def __init__(self, objname):
        self.objname = objname
        self.myobs = ephem.Observer()
        self.myobs.lon = 16.656667
        self.myobs.lat = 51.476111
        self.myobs.elevation = 130
        self.myobs.date = str(Time(dt.utcnow(), scale='ut1', location=(self.myobs.lon * u.deg, self.myobs.lat * u.deg)))  # Time in UT
        
    def get_info(self):
        try:
            self.c = SkyCoord.from_name(self.objname)
            logging.info(f'{self.objname} resolved!')
        except name_resolve.NameResolveError:
            self.c = SkyCoord.from_name('M1')
            logging.info(f'{self.objname} not found!')
            return ('', '', '', '')
        obs_location = EarthLocation(lat=self.myobs.lat*u.deg, lon=self.myobs.lon*u.deg, height=self.myobs.elevation*u.m)
        obs_time = dt.utcnow()
        obs_altaz = AltAz(location=obs_location, obstime=obs_time, pressure=1010.0 * u.hPa, temperature=10.0 * u.deg_C,
            relative_humidity=20, obswl=0.6 * u.micron)
        obj_altaz = self.c.transform_to(obs_altaz)
        # obj_alt = obj_altaz.alt.to_string(u.deg, sep=':', precision=0)
        obj_alt = f'{obj_altaz.alt.degree:.2f}°'
        # obj_az = obj_altaz.az.to_string(u.deg, sep=':', precision=0)
        obj_radian = Angle(((self.myobs.sidereal_time() - self.c.ra.to(u.rad).value) % (2*np.pi))*u.rad)
        obj_hms = obj_radian.hms
        obj_ha = f'{obj_hms.h:02.0f}h {obj_hms.m:02.0f}m {obj_hms.s:02.0f}s'
        ra = self.c.ra.to_string(u.hour, sep=':', precision=0)
        dec = self.c.dec.to_string(u.deg, sep=':', precision=0)
        return (obj_alt, obj_ha, ra, dec)

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
    

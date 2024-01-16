from PySide6.QtWidgets import QDoubleSpinBox, QComboBox, QSpinBox, QHBoxLayout, QWidget, QPushButton, QLabel, QSizePolicy
from PySide6.QtCore import Qt
from PySide6 import QtCore, QtGui
import logging
import numpy as np


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
        self.nexp.setMaximum(999)
        self.nexp.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

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
        self.exptime.setDecimals(2)
        self.exptime.setSingleStep(0.01)
        self.exptime.setValue(qrow['Exposure'])
        self.exptime.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.rot = QComboBox()
        self.rot.addItems(['1', '2', '16'])
        self.rot.setCurrentText(qrow['ROT'])
        self.rot.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

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

    def deleterow(self):
        self.deleteLater()
        self.qrows.remove(self)
        logging.info(f'Row deleted!')

class details_widget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.ra = QLabel()
        self.ra.setText('RA: ')
        self.ra_value = QLabel()
        self.ra_value.setText('999.999')
        self.dec = QLabel()
        self.dec.setText('DEC')
        self.dec_value = QLabel()
        self.dec_value.setText('999.999')
        layout = QHBoxLayout()
        layout.addWidget(self.ra)
        self.setLayout(layout) 

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])
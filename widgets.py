from PySide6.QtWidgets import QDoubleSpinBox, QComboBox, QSpinBox, QHBoxLayout, QWidget, QPushButton, QHeaderView, QSizePolicy
from PySide6.QtCore import Qt
from PySide6 import QtCore, QtGui
import logging
import time
import pandas as pd

def update_table(func):
    def wrapper_update_table(*args, **kwargs):
        obj = func(*args, **kwargs)
        obj.ui.details_table.setModel(TableModel(obj.table_data))
        obj.ui.details_table.resizeColumnsToContents()
        obj.ui.details_table.resizeRowsToContents()
        header = obj.ui.details_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
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
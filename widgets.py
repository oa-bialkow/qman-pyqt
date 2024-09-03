from PySide6.QtWidgets import QDoubleSpinBox, QComboBox, QSpinBox, QHBoxLayout, QWidget, QPushButton, QHeaderView, QSizePolicy, QWidget, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, QRunnable, Slot, QThreadPool
from PySide6 import QtCore, QtGui
from dataclasses import dataclass
import logging
import time
import pandas as pd
from datetime import datetime as dt
import numpy as np
import os
import configparser
import ephem
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, get_body, solar_system_ephemeris
from astropy import units as u
from astropy.coordinates import name_resolve, Angle
from astropy.time import Time
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backend_bases import MouseButton
from astroplan.plots import plot_sky, plot_finder_image
from astroplan import FixedTarget, Observer
from baladin import Aladin



'''
Function to normalize object names - remove spaces, underscores, dashes, brackets, commas, and equal signs and convert to lowercase
This is used to compare the object name in the queue with the object name in the objpos.dat file
The function returns a tuple with two options to handle different naming conventions
'''
def normalize_objname(name):
    opt1 = name.replace(' ', '').split('_')[0].split('-')[0].split('(')[0].split('[')[0].split(',')[0].split('=')[0].lower()
    opt2 = name.replace('_', '').split('_')[0].split('-')[0].split('(')[0].split('[')[0].split(',')[0].split('=')[0].lower()
    opt3 = name.rsplit('_', 1)[0].replace('_', '').split('-')[0].split('(')[0].split('[')[0].split(',')[0].split('=')[0].lower()
    opt4 = name.split()[0].replace('_', '')[0].lower()
    return set((opt1, opt2, opt3, opt4, name))

config = configparser.ConfigParser()
config.read('observatory.ini')
chosen_obs = 'BIALKOW'
if chosen_obs not in config.sections():
    chosen_obs = 'DEFAULT'



class SkyPlot(QWidget):
    def __init__(self, parent=None, my_obj=None, ui=None):
        super().__init__(parent)
        
        # Create a Figure object and a FigureCanvas
        self.figure = Figure(figsize=(3, 3))
        self.figure.tight_layout()
        self.figure.patch.set_facecolor('#323232')
        self.ax = self.figure.add_subplot(111, projection='polar')
        self.ax.tick_params(axis='x', colors='white') 
        self.plots = []
        self.temp_obj = (0, -90)
        self.canvas = FigureCanvas(self.figure)
        cid = self.canvas.mpl_connect('button_press_event', self.on_click)

        self.my_obj = my_obj
        self.ui = ui
        self.location = EarthLocation.from_geodetic(lon=self.my_obj.myobs.lon, lat=self.my_obj.myobs.lat, height=self.my_obj.myobs.elevation)
        self.observer = Observer(location=self.location, name="Observatory", timezone="UTC")

        # Example plot
        self.plot()

    def plot(self):

        # Astroplan sky chart
        time = Time.now()
        sun_style = {'color': 'yellow', 'marker': 'o', 'linestyle': 'None', "alpha": 0.75, 's': 100, 'edgecolors': 'darkgoldenrod'}
        moon_style = {'color': 'grey', 'marker': 'o', 'linestyle': 'None', "alpha": 0.75, 's': 100, 'edgecolors': 'black'}
        obj_style = {'color': 'lightgreen', 'marker': '*', 'linestyle': 'None', "alpha": 0.75, 's': 160, 'edgecolors': 'darkgreen'} 

        with solar_system_ephemeris.set('builtin'):
            sun_ep = get_body('sun', time, self.location)
            moon_ep = get_body('moon', time, self.location)
        sun = FixedTarget(coord=sun_ep, name="Sun")
        moon = FixedTarget(coord=moon_ep, name="Moon")
        sun_altaz = sun_ep.transform_to(AltAz(obstime=time, location=self.location))
        moon_altaz = moon_ep.transform_to(AltAz(obstime=time, location=self.location))
        if sun_altaz.alt.deg > 0 or sun_altaz.alt.deg < -18:
            self.plots.append(plot_sky(sun, self.observer, time, ax=self.ax, style_kwargs=sun_style))
        else:
            self.plots.append(self.ax.scatter(sun_altaz.az.rad, 90-sun_altaz.alt.deg, color='yellow', marker='o', s=100, alpha=0.75, edgecolors='darkgoldenrod'))
        if moon_altaz.alt.deg > 0 or moon_altaz.alt.deg < -18:
            self.plots.append(plot_sky(moon, self.observer, time, ax=self.ax, style_kwargs=moon_style))
        else:
            self.plots.append(self.ax.scatter(moon_altaz.az.rad, 90-moon_altaz.alt.deg, color='grey', marker='o', s=100, alpha=0.75, edgecolors='black'))
        self.plots.append(self.ax.scatter(self.temp_obj[0], self.temp_obj[1], color='lightcoral', marker='x', s=100, alpha=0.75))

        if self.my_obj.ra is not None:
            current_object = SkyCoord(ra=self.my_obj.ra*u.deg, dec=self.my_obj.dec*u.deg)
            obj = FixedTarget(coord=current_object, name="OBJ")
            plot_sky(obj, self.observer, time, ax=self.ax, style_kwargs=obj_style)

        self.ax.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2]) 
        self.ax.set_xticklabels(['N', 'E', 'S', 'W']) 
        self.ax.set_yticks([0, 10, 30, 55, 90, 96, 102, 108]) # polar plot has 0 at the top, 90 at the bottm. Ticks set here are for altitude from 90 at the top to -12 at the bottom
        self.ax.set_yticklabels([' ']*len(self.ax.get_yticks())) # remove labels
        self.ax.set_theta_direction(-1)
        self.ax.set_theta_zero_location('N')
        fill_theta = np.linspace(0, 2*np.pi, 100)
        [self.ax.fill_between(fill_theta, 90+i, 90+i+6, color=c, alpha=0.5) for i, c in zip([0, 6, 12], ['lightgrey', 'darkgrey', 'black'])]
        self.ax.fill_between(fill_theta, 55, 90, color='xkcd:bright red', alpha=0.1)
        self.ax.fill_between(fill_theta, 0, 55, color='xkcd:apple green', alpha=0.1)
        self.canvas.draw()  # Refresh canvas

    def replot(self):
        # self.figure.clear()
        self.ax.clear()
        self.plot()

    def on_click(self, event):
        if event.button is MouseButton.LEFT:
            if event.inaxes == self.ax:
                # logging.info(f'[RAW]: Az: {event.xdata} Alt: {event.ydata}')
                theta_ = event.xdata*u.rad if event.xdata > 0 else event.xdata*u.rad + 2*np.pi*u.rad # Make sure it's positive
                theta_ = theta_.to(u.deg) # Convert to degrees
                r_click = (90 - event.ydata)*u.deg
                # logging.info(f'Az: {theta_} Alt: {r_click}')
                self.temp_obj = (event.xdata, event.ydata)
                self.ui.statusbar.showMessage(f'Selected point: Az: {theta_:.2f}° Alt: {r_click:.2f}°')
                self.replot()

class FinderChart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure(figsize=(3.5, 3.5))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.figure.tight_layout()

    def get_limits(self, hdu):
        self.hfov = 20 / 2. / 60. # half of the full field of view in degrees
        limit = lambda scale: self.hfov/scale # arcmin to pixels
        x_px, y_px = hdu.shape
        x_px_scale = np.abs(hdu.header['CDELT1']) # in arcmin
        y_px_scale = np.abs(hdu.header['CDELT2']) # in arcmin
        return limit(x_px_scale), limit(y_px_scale)

    def plot(self, ra, dec, name):
        self.ax.clear()
        if ra is not None:
            current_object = SkyCoord(ra=ra*u.deg, dec=dec*u.deg)
            obj = FixedTarget(coord=current_object, name=name)
            ax, hdu = plot_finder_image(obj, ax=self.ax)
            limit_x, limit_y = self.get_limits(hdu)
            self.ax.set_xlim(hdu.shape[1]/2 - limit_x, hdu.shape[1]/2 + limit_x) # center the image in x (pixels)
            self.ax.set_ylim(hdu.shape[0]/2 - limit_y, hdu.shape[0]/2 + limit_y) # center the image in y (pixels)
            self.ax.tick_params(axis='x', which='both', direction='in', labelsize=8, pad=0)
            self.ax.tick_params(axis='y', which='both', direction='in', labelsize=8, pad=20)
            self.ax.tick_params(axis='both', which='major', length=7)  # Major ticks longer
            self.ax.tick_params(axis='both', which='minor', length=4)  # Minor ticks shorter
            n_ticks = 5
            xtl = Angle(np.linspace((ra/360*24 - self.hfov)*u.hourangle, (ra/360*24 + self.hfov)*u.hourangle, n_ticks), unit=u.hourangle)
            ytl = Angle(np.linspace((dec - self.hfov)*u.deg, (dec + self.hfov)*u.deg, n_ticks), unit=u.deg)
            # xtl = [f"{x.to(u.hourangle):latex}" for x in xtl]
            xtl = [f"${{{int(x.hms.h)}}}^\mathrm{{{'h'}}}{{{int(x.hms.m)}}}^\mathrm{{{'m'}}}$" for x in xtl]
            ytl = [f"${{{int(y.dms.d)}}}^\circ{{{int(np.abs(y.dms.m))}}}'$" for y in ytl]
            # ytl = [f"{y.to(u.deg):latex}" for y in ytl]
            self.ax.set_xticks(np.linspace(0, hdu.shape[1], n_ticks))
            self.ax.set_yticks(np.linspace(0, hdu.shape[0], n_ticks))
            self.ax.set_xticklabels(xtl, rotation=0, ha='center')
            self.ax.set_yticklabels(ytl, rotation=0, ha='center', va='bottom')
            self.ax.title.set_visible(False)
            self.ax.xaxis.label.set_visible(False)
            self.ax.yaxis.label.set_visible(False)
            self.ax.spines['top'].set_visible(False)
            self.ax.spines['right'].set_visible(False)
            self.ax.spines['bottom'].set_visible(False)
            self.ax.spines['left'].set_visible(False)

            self.canvas.draw() 


@dataclass
class ObjectInfo:
    objname: str
    objpos: any
    debug: bool = False
    normed_objname: str = None
    myobs: any = ephem.Observer()
    ra: any = None
    dec: any = None
    alt: any = None
    az: any = None
    ha: any = None

    def __post_init__(self):
        self.objpos = self.objpos
        self.myobs.lon = config.getfloat(chosen_obs, 'longitude')
        self.myobs.lat = config.getfloat(chosen_obs, 'latitude')
        self.myobs.elevation = config.getfloat(chosen_obs, 'elevation')
        self.myobs.date = str(Time(dt.utcnow(), scale='ut1', location=(self.myobs.lon * u.deg, self.myobs.lat * u.deg)))  # Time in UT

    def check_objpos(self):
        norm_obj_name = normalize_objname(self.objname)
        norm_objpos = self.objpos['Object'].apply(normalize_objname).values
        flattened_list = [item for sublist in norm_objpos for item in sublist]
        logging.debug(f'Normalized object names: {norm_obj_name}')
        mask = []
        for obj in norm_obj_name:
            if len(obj) > 1:
                mask.append(obj in flattened_list)
            else:
                mask.append(False)
        if any(obj in flattened_list for obj in norm_obj_name) and self.objname != '0_CURRENT_QUEUE' and mask.count(True) > 0:
            # mask = [obj in flattened_list for obj in norm_obj_name if len(obj) > 1]
            logging.debug(f'Mask: {mask}')
            if mask.count(True) > 1:
                len_mask = np.array([len(obj) for obj in norm_obj_name])
                logging.debug(f'Length mask: {len_mask}')
                for i in range(len(mask)):
                    if mask[i] and len_mask[i] > 1:
                        mask[i] = mask[i] and len_mask[i] == max(len_mask[mask])
                    else:
                        mask[i] = False
                        
            matched_name = np.array(list(norm_obj_name))[mask][0]
            matching_row_index = self.objpos.index[self.objpos['Object'].apply(normalize_objname).apply(lambda x: matched_name in x)].tolist()
            obj = self.objpos.iloc[matching_row_index]
            ra = f"{int(obj['RAd'].values[0]):2d}:{int(obj['RAm'].values[0]):02d}:{int(obj['RAs'].values[0]):02d} (J{obj['Epoch'].values[0]})"
            dec = f"{obj['DECd'].values[0].zfill(2)}:{int(obj['DECm'].values[0]):02d}:{int(obj['DECs'].values[0]):02d} (J{obj['Epoch'].values[0]})"
            self.c = SkyCoord(ra=ra.split()[0], dec=dec.split()[0], frame='icrs', unit=(u.hourangle, u.deg))
            self.found = True
            self.resolved = False
            self.normed_objname = obj['Object'].values[0]
            logging.info(f'{self.objname} found in objpos.dat!')
        else:
            self.found = False
            try:
                self.c = SkyCoord.from_name(self.objname)
                self.resolved = True
                logging.info(f'{self.objname} resolved!')
                found = False
            except name_resolve.NameResolveError:
                self.resolved = False
                self.c = SkyCoord.from_name('M1')
                logging.info(f'{self.objname} not found!')

    def get_info(self):
        if not self.resolved and not self.found:
            return ('--', '--', '--', '--', '--')

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
        return (obj_alt, obj_az, obj_ha, ra, dec)

def update_table(func):
    def wrapper_update_table(*args, **kwargs):
        obj = func(*args, **kwargs)
        obj.ui.details_table.setModel(TableModel(obj.table_data))
        obj.ui.details_table.resizeColumnsToContents()
        header = obj.ui.details_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        # obj.skyview.create_aladin_view(obj.my_obj.c.ra.deg, obj.my_obj.c.dec.deg)
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
    

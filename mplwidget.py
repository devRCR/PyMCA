# Imports
from PyQt5 import QtWidgets
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvas as Canvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


# Ensure using PyQt5 backend
#matplotlib.use('QT5Agg')
#matplotlib.rcParams.update({'font.size': 8})

# Matplotlib canvas class to create figure
class MplCanvas(Canvas):
    def __init__(self):
        self.fig = Figure(tight_layout=True,figsize=(5,5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        #self.ax.grid()
        self.ax.set_ylabel('Energy (kV)')
        self.ax.set_xlabel('Channel')
        self.ax.set_xlim(0,4095)
        self.ax.set_ylim(auto=True)
        self.ax.set_title('Spectrometer')

        Canvas.__init__(self, self.fig)
        Canvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        Canvas.updateGeometry(self)

# Matplotlib widget
class MplWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)                # Inherit from QWidget
        self.canvas = MplCanvas()                               # Create canvas object
        self.toolbar = NavigationToolbar(self.canvas, self)     # MatplotLib Toolbar
        self.vbl = QtWidgets.QVBoxLayout()                      # Set box for plotting
        self.vbl.addWidget(self.canvas)
        self.vbl.addWidget(self.toolbar)
        self.setLayout(self.vbl)

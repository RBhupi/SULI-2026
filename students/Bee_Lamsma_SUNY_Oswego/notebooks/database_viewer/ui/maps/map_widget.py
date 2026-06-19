from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MapWidget(FigureCanvas):

    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)

        super().__init__(self.fig)

    def clear(self):
        self.ax.clear()

    def plot_points(self, lats, lons, values=None):

        self.ax.clear()

        self.ax.scatter(lons, lats, c=values or "red", s=20)

        self.draw()
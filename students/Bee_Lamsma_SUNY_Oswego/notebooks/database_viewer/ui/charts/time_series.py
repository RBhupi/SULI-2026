from PyQt5.QtWidgets import QWidget, QVBoxLayout

from ui.widgets.plot_widget import PlotWidget


class TimeSeriesChart(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.plot = PlotWidget()

        layout.addWidget(self.plot)

        self.setLayout(layout)

    def plot_series(self, x, y, label="Series"):

        self.plot.ax.clear()
        self.plot.ax.plot(x, y, label=label)

        self.plot.ax.legend()
        self.plot.draw()
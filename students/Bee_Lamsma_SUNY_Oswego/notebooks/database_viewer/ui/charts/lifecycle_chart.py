from PyQt5.QtWidgets import QWidget, QVBoxLayout

from ui.widgets.plot_widget import PlotWidget


class LifecycleChart(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.plot = PlotWidget()

        layout.addWidget(self.plot)

        self.setLayout(layout)

    def plot_lifecycle(self, time, dbz, area, flash):

        self.plot.ax.clear()

        self.plot.ax.plot(time, dbz, label="DBZ", color="red")
        self.plot.ax.plot(time, area, label="Area", color="blue")
        self.plot.ax.plot(time, flash, label="Lightning", color="yellow")

        self.plot.ax.legend()
        self.plot.draw()
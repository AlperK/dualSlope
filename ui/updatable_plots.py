import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class UpdatablePlot:
    def __init__(self, canvas) -> None:
        self.fig_agg = None
        self.figure = None
        self.canvas = canvas

        self.x = None
        self.y = None
        self.axes = None
        self.scatter = None
        self.background = None

    def plot(self, x, y):
        self.x = x
        self.y = y
        self.figure_controller()
        # self.figure_drawer()

    def figure_controller(self):
        if self.figure is None:
            self.figure = plt.figure(figsize=(4, 2.5))
            self.axes = self.figure.add_subplot(111)
            self.axes.set_xlim([-1, 5])
            self.axes.set_ylim([-1, 3])
            self.scatter = self.axes.scatter(self.x, self.y,
                                             linewidth=2,
                                             marker='o',
                                             color='blue')
            self.figure.tight_layout()
            # self.axes.draw_artist(self.scatter)
            self.background = self.figure.canvas.copy_from_bbox(self.axes.bbox)
            print('background')
        else:
            pass
            # self.axes.draw_artist(self.scatter)

            # self.axes.relim()
            # self.axes.autoscale_view()

    def figure_drawer(self):
        if self.fig_agg is not None:
            self.fig_agg.get_tk_widget().forget()
        self.fig_agg = FigureCanvasTkAgg(self.figure, self.canvas.TKCanvas)
        self.fig_agg.get_tk_widget().pack(side='top', fill='both', expand=1)

        self.fig_agg.restore_region(self.background)
        self.scatter.set_offsets(np.c_[self.x, self.y])
        self.axes.draw_artist(self.scatter)
        # self.fig_agg.draw()
        self.figure.canvas.flush_events()
        # self.fig_agg.blit(self.axes.bbox)
        self.figure.canvas.blit(self.axes.bbox)

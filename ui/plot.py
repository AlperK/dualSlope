import PySimpleGUI as Sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


canvas = Sg.Canvas(size=(0, 0), key='__CANVAS__')


def create_figure(x, y):

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(2, 2))
    ax = axes[0]
    ax.scatter(x, y, marker='o', linewidth=4, color='blue')
    ax.set_xlabel('X1')
    ax.set_xlim([0, 5])
    ax.set_ylabel('Y1')
    ax.set_ylim([0, 5])

    ax = axes[1]
    ax.scatter(x, y, marker='o', linewidth=4, color='red')
    ax.set_xlabel('X1')
    ax.set_xlim([0, 5])
    ax.set_ylabel('Y1')
    ax.set_ylim([0, 5])

    fig.tight_layout()
    # plt.figure()
    # plt.scatter(x=x, y=y, color='blue', alpha=0.7, marker='o')
    # plt.xlim([0, 5])
    # plt.ylim([0, 5])

    # print(plt.dpi)
    return fig


def draw_figure(canvas: Sg.Canvas, x, y):
    figure = create_figure(x, y)
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack()
    return figure_canvas_agg

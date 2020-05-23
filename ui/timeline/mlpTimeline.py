from PyQt5.QtWidgets import QSizePolicy, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib import pyplot as plt
import mplcursors
import numpy as np
import matplotlib.dates as mdates
labels = {}
class MlpTimelineCanvas(FigureCanvasQTAgg):
    '''
    Класс холста Qt для помещения рисунка Matplotlib
    '''
    def __init__(self, fig):
        FigureCanvasQTAgg.__init__(self, fig)
        self.setMinimumSize(200,200)
        self.labels = {}

def prepare_canvas(layout = None):
    '''
    Функция для инициализации рисунка Matplotlib и его размещения в виджете Qt
    '''
    # Подготовка рисунка и осей
    fig, axes = plot_single_empty_graph()
    # Получение экземпляра класса холста с размещенным рисунком
    canvas = MlpTimelineCanvas(fig)
    # Добавление виджета холста с рисунком в размещение
    layout.addWidget(canvas)
    return canvas

def plot_single_empty_graph():
    '''
    Функция для подготовки рисунка с пустыми осями и предварительного их оформления, без задания данных
    '''
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(10, 7), dpi=85, facecolor='white', frameon=True, edgecolor='black', linewidth=1)
    fig.subplots_adjust(wspace=0.4, hspace=0.6, left=0.15, right=0.85, top=0.9, bottom=0.1)
    axes.grid(True, c='lightgrey', alpha=0.5)
    axes.set_xlabel('Дата статьи', fontsize=8)
    axes.set_ylabel('Частота', fontsize=8)
    return fig, axes



def plot_draw_lines(data, canvas):
     ax = canvas.figure.get_children()[1]
     ax.cla()
     global labels
     labels = {}
     lines = {}
     for key, item in data.items():
         color = '#%02x%02x%02x' % (item[0][0], item[0][1], item[0][2])
         x = mdates.date2num(item[1])
         y = np.array(item[2])
         coeffs = np.polyfit(x, y, 5)
         poly_eqn = np.poly1d(coeffs)
         y_hat = poly_eqn(x)-0.01
         xx = np.linspace(x.min(), x.max(), len(x))


         lines[key] = item[3]
         ax.plot(item[1], y_hat, c=color, label=key+'_line')
         ax.fill_between(item[1], y_hat , color=color, alpha=0.2)
         pl = ax.plot(item[1], y, 'ro', c=color, label=key)
     labels = lines
     mplcursors.cursor(ax).connect("add", get_plot_label)
     canvas.draw()

def get_plot_label(sel):
    if sel.target.index == int(sel.target.index) and sel.artist.get_label() in labels:
        text = labels[sel.artist.get_label()][sel.target.index]
        sel.annotation.set_text(text)
    else:
        sel.annotation.set_text('')
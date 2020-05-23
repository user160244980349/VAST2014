from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib import pyplot as plt
import mplcursors
import numpy as np
from ui.emails.chordDiagram import chordDiagram, hex2rgb

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
    return fig, axes



def plot_draw_lines(data, canvas):
     ax = canvas.figure.get_children()[1]
     ax.cla()
     names, colors, flux = tuple(data)
     # nodePos = chordDiagram(flux, ax, colors=[hex2rgb(x) for x in ['#666666', '#66ff66', '#ff6666', '#6666ff']])
     nodePos = chordDiagram(flux, ax, [hex2rgb('#%02x%02x%02x' % (color[0], color[1], color[2]) ) for color in colors])
     ax.axis('off')
     prop = dict(fontsize=16 * 0.8, ha='center', va='center')
     for i in range(len(names)):
         ax.text(nodePos[i][0], nodePos[i][1], names[i].split('@')[0], rotation=90+nodePos[i][2], **prop) #nodePos[i][2]
     #mplcursors.cursor(ax).connect("add", get_plot_label)
     canvas.draw()


import tkinter as tk
from tkinter import ttk, font
from tkinter.filedialog import asksaveasfilename
from datetime import timedelta, datetime


# -------------------------------------------------------------------------------
from tkinter import scrolledtext
# -------------------------------------------------------------------------------
def text_message(root, text: str, title='information',
                 width=40, height=10, background='white'):
    """Independent window containing a scrolling text box ."""

    _WIN = tk.Toplevel(root)
    _WIN.title(title)

    _TXT = scrolledtext.ScrolledText(
        _WIN,
        wrap=tk.WORD,
        width=width,
        height=height,
        background=background)
    _TXT.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    _TXT.insert(tk.END, text)
    _TXT.config(state=tk.DISABLED)

    _BTN = ttk.Button(_WIN, text='Ok', command=lambda: _WIN.destroy())
    _BTN.pack()


def about_window(root, text: str, title='About',
                 width=40, height=10, background='lightgrey'):
    """Independent window containing a small text box."""
    _WIN = tk.Toplevel(root, background=background)
    _WIN.title(title)
    _WIN.resizable(height=False, width=False)
    _TXT = tk.Text(_WIN, background=background, width=width, height=height)
    _TXT.insert(tk.END, text)
    _TXT.grid(row=0, column=0, sticky='nswe')
    _BTN = ttk.Button(_WIN, text='Ok', command=lambda: _WIN.destroy())
    _BTN.grid(row=1, column=0)


# -------------------------------------------------------------------------------
from tkhtmlview import HTMLText, RenderHTML
# -------------------------------------------------------------------------------
def user_manual(root, html_file: str, title='User instructions'):
    """Independent window containing an html content."""
    _WIN = tk.Toplevel(root)
    _WIN.title(title)
    _HTML = HTMLText(_WIN, html=RenderHTML(html_file), padx=10, pady=10)
    # _HTML.grid(row = 0, column = 0, sticky = N+S+W+E, padx=5, pady=5)
    _HTML.pack(padx=5, pady=5, fill='both', expand=True)
    _HTML.grid_columnconfigure(0, weight=1)
    _HTML.grid_rowconfigure(0, weight=1)
    _BTN = ttk.Button(_WIN, text='Close', command=lambda: _WIN.destroy())
    # _BTN.grid(row=1, column=0)
    _BTN.pack()


# -------------------------------------------------------------------------------
def display_list(root, datalist: list, title: str='Data List'):
    _WIN = tk.Toplevel(root)
    _WIN.title(title)
    _WIN.geometry("1000x800")

    _SCROLLBAR = ttk.Scrollbar(_WIN, orient=tk.VERTICAL)
    _LIST = tk.Listbox(
        _WIN,
        width=5,
        selectmode=tk.SINGLE,
        yscrollcommand=_SCROLLBAR.set
    )

    for data in datalist:
        _LIST.insert(tk.END, data)

    _LIST.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

    _SCROLLBAR.config(command=_LIST.yview)
    _SCROLLBAR.grid(row=0, column=1, sticky='ns')

    # give a minimum width to the scrollbar
    style = ttk.Style()
    style.configure('Vertical.TScrollbar', arrowsize=40)


    _BTN = ttk.Button(_WIN, text='close', command=lambda: _WIN.destroy())
    _BTN.grid(row=1, column=0, stick='s')

    _WIN.rowconfigure(0, weight=1)
    _WIN.columnconfigure(0,weight=1)
    _WIN.rowconfigure(1, weight=0)


# -------------------------------------------------------------------------------
import matplotlib
matplotlib.use('TkAgg')
# import matplotlib.pyplot as plt

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
import matplotlib.dates as mdates
# -------------------------------------------------------------------------------
plot_settings = {
    'width': 2000,
    'height': 1000,
    'labelsize': 20,
    'ylim': (0,200),
}

def format_x_axis(axes, data):
    """First function to help formatting the x-axis"""
    min_date = min(data)
    max_date = max(data)
    data_range = max_date - min_date

    if data_range < timedelta(days=1):
        axes.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    else:
        axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))


def display_source_plot(root, datasets: dict, title='Graphs', settings=plot_settings):
    """Independent window containing graph from MatPlotLib."""
    _WIN = tk.Toplevel(root)
    _WIN.title('Graph of the source measures.')

    # create the figure
    figure = Figure(figsize=(6,4), dpi=100)

    # create FigureCanvasTkAgg object
    canvas = FigureCanvasTkAgg(figure, _WIN)

    # create the toolbar
    NavigationToolbar2Tk(canvas, _WIN)

    # create axes
    axes = figure.add_subplot()

    # create the graph
    # key = list(datasets.keys())[0]  # to get a single element
    line = {}
    for key in datasets.keys():
        datX = [x[0] for x in datasets[key]]
        datY = [x[1] for x in datasets[key]]
        line[key], = axes.plot(datX, datY, label=key)

    axes.set_ylim(*settings['ylim'])
    axes.tick_params(axis='both', labelsize=settings['labelsize'])
    axes.legend(handles=[line[key] for key in datasets.keys()],
                prop={'size': settings['labelsize']})
    axes.set_title(title, fontweight='bold',
                   fontsize=int(settings['labelsize']*1.8))

    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    canvas_widget.configure(width=settings['width'], height=settings['height'])

# -------------------------------------------------------------------------------
import pandas as pd
# -------------------------------------------------------------------------------
def display_table(root, table: pd.DataFrame, title='Graphs', settings=plot_settings):
    """Independent window containing graph from MatPlotLib."""
    _WIN = tk.Toplevel(root)
    _WIN.title(title)

    # create the figure
    figure = Figure(figsize=(6,4), dpi=100)

    # create FigureCanvasTkAgg object
    canvas = FigureCanvasTkAgg(figure, _WIN)

    # create the toolbar
    NavigationToolbar2Tk(canvas, _WIN)

    # create axes
    axes = figure.add_subplot()
    
    for colTitle in table.columns:
        axes.plot(table[colTitle], label=colTitle)
    
    axes.set_ylim(*settings['ylim'])
    axes.tick_params(axis='both', labelsize=settings['labelsize'])
    axes.legend(prop={'size': settings['labelsize']})
    axes.set_title(title, 
                   fontsize=int(settings['labelsize']*1.8),
                    fontweight='bold' )

    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    canvas_widget.configure(width=settings['width'], height=settings['height'])


# -------------------------------------------------------------------------------
def plot_compare(root, datasets:dict, table: pd.DataFrame, title='Graphs', settings=plot_settings):
    """Compare in a graph the sources measures with their synchronized version."""
    _WIN = tk.Toplevel(root)
    _WIN.title(title)

    # create the figure
    figure = Figure(figsize=(6,4), dpi=100)

    # create FigureCanvasTkAgg object
    canvas = FigureCanvasTkAgg(figure, _WIN)

    # create the toolbar
    NavigationToolbar2Tk(canvas, _WIN)

    # create axes
    axes = figure.add_subplot()
    
    line = {}
    for key in datasets.keys():
        datX = [x[0] for x in datasets[key]]
        datY = [x[1] for x in datasets[key]]
        line[key], = axes.plot(datX, datY, label=key)
    
    for colTitle in table.columns:
        axes.plot(table[colTitle], label=f'{colTitle} synchronized')
    
    # axes.plot(table['LBA10CT001'], label='synchronized')

    axes.set_ylim(*settings['ylim'])
    axes.tick_params(axis='both', labelsize=settings['labelsize'])
    axes.legend(prop={'size': settings['labelsize']})
    axes.set_title(title, 
                   fontsize=int(settings['labelsize']*1.8),
                    fontweight='bold' )

    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    canvas_widget.configure(width=settings['width'], height=settings['height'])    


if __name__ == '__main__':

    """Open a window with buttons to test each dialogs"""

    root = tk.Tk()
    root.title('Testing my dialogs windows')

    normal_width, normal_height = 1024, 768
    screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
    percentage_width = screen_width / normal_width
    percentage_height = screen_height / normal_height
    scale_factor = ((percentage_height + percentage_width) / 2)

    fontsize=int(10 * scale_factor)
    minimumu_size = 8
    maximum_size = 18
    if fontsize < minimumu_size:
        fontsize = minimumu_size
    elif fontsize > maximum_size:
        fontsize = maximum_size
    
    # changing the size of the default font
    default_font = font.nametofont('TkDefaultFont')
    default_font.configure(size=fontsize)
    root.option_add('*Font', default_font)

    style = ttk.Style()
    style.configure('Vertical.TScrollbar', arrowsize=80)

    frame = tk.Frame(root, padx=20, pady=20, background='lightblue')
    frame.pack(fill=tk.BOTH, expand=True)

    frame2 = tk.Frame(root, padx=20, pady=20, background='lightblue')
    button = tk.Button(frame2, text='Close', command=root.destroy, width=10)
    button.pack(side='bottom', expand=False)
    frame2.pack(fill=tk.BOTH, expand=True)

    # test_window = Callable[[],[]]    # eventually not useful
    title = 'window'

    BUTTON_WIDTH = 20  # buttons to launch demo

    # -------------------------------------------------------------------------------------
    title = 'Open text message'
    # -------------------------------------------------------------------------------------
    txtmsg = "Je suis le prince d'Aquitaine à la tour abolie,\n"
    txtmsg += 'Ma seule étoile est morte et porte le soleil noir '
    txtmsg += 'de la mélancolie.'

    def open_text_message():
        open_text_message_btn.configure(background='grey', foreground='white')
        text_message(frame, text=txtmsg, background='lightgrey',
                     width=70, height=4)
    open_text_message_btn = tk.Button(frame, text=title,
                                      command=open_text_message,
                                      width=BUTTON_WIDTH)
    open_text_message_btn.pack(pady=10)
    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    title = 'About Window'
    # -------------------------------------------------------------------------------------
    def open_about_window():
        open_about_button.configure(background='grey', foreground='white')
        about_window(frame, text='About Window', title='About', width=15, height=3, background='lightgrey')
    open_about_button = tk.Button(frame, text=title, command=open_about_window, width=BUTTON_WIDTH)
    open_about_button.pack(pady=10)
    # -------------------------------------------------------------------------------------
    
    # -------------------------------------------------------------------------------------
    title = 'User Manual'
    # -------------------------------------------------------------------------------------
    def open_user_manual():
        open_user_manual_btn.configure(background='grey', foreground='white')
        user_manual(frame, html_file='./lib/html/help.html', title='User Manual')
    open_user_manual_btn = tk.Button(frame, text=title, command=open_user_manual, width=BUTTON_WIDTH)
    open_user_manual_btn.pack(pady=10)
    # -------------------------------------------------------------------------------------
    
    # -------------------------------------------------------------------------------------
    title = 'Display list'
    # -------------------------------------------------------------------------------------
    mylist = ['table', 'chair', 'sofa', 'bed', 'light']
    mylist = 6*mylist

    def open_display_list():
        display_list(frame, mylist, title)
    
    display_list_btn = tk.Button(frame, text=title, command=open_display_list, width=BUTTON_WIDTH)
    display_list_btn.pack(pady=10)
    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    title = 'plot source'
    # -------------------------------------------------------------------------------------
    from setsManagement import read_measures

    def open_plot_source():
        sets = read_measures('./dat/data.csv')
        open_plot_source_btn.configure(background='grey', foreground='white')
        plot_source(frame, datasets=sets, title='Source measures.')
    open_plot_source_btn = tk.Button(frame, text=title, command=open_plot_source, width=BUTTON_WIDTH)
    open_plot_source_btn.pack(pady=10)
    # -------------------------------------------------------------------------------------
    
    # -------------------------------------------------------------------------------------
    title = 'plot table'
    # -------------------------------------------------------------------------------------
    from setsManagement import read_measures, synchronized_sets

    def open_plot_table():
        table = synchronized_sets(read_measures('./dat/data.csv'))
        open_plot_table_btn.configure(background='grey', foreground='white')
        plot_table(frame, table=table, title='Synchronized table.')
    open_plot_table_btn = tk.Button(frame, text=title, command=open_plot_table, width=BUTTON_WIDTH)
    open_plot_table_btn.pack(pady=10)
    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    title = 'plot compare'
    # -------------------------------------------------------------------------------------
    def open_plot_compare():
        sets = read_measures('./dat/data.csv')
        table = synchronized_sets(sets)
        open_plot_compare_btn.configure(background='grey', foreground='white')
        plot_compare(frame, datasets=sets, table=table, title='Compare source with synchronized version.')
    open_plot_compare_btn = tk.Button(frame, text=title, command=open_plot_compare, width=BUTTON_WIDTH)
    open_plot_compare_btn.pack(pady=10)
    # -------------------------------------------------------------------------------------

    root.mainloop()

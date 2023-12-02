from tkinter import Tk, ttk, font, Toplevel, TOP, BOTH
from entryWithModel import EntryWithModel
from entryTimescale import EntryTimeScale
from my_dialogs import display_list

from math import *
from random import uniform

from datetime import datetime, timedelta

import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# -------------------------------------------------------------------------------
plot_settings = {
    'width': 2000,
    'height': 1000,
    'labelsize': 20,
    'ylim': (0,200),
}

class EntryGenerator(ttk.Frame):

    def __init__(self, container, name, accuracy=3,
                 duration='1h', step='1min', **kwargs):

        super().__init__(container, **kwargs)

        # -------------------------------------------------
        frame1 = ttk.Frame(container, padding=5)
        frame1.grid(row=0, column=0, sticky='nsew')
        self.main_lbl = ttk.LabelFrame(frame1, text=name)
        self.main_lbl.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        frame11 = ttk.Frame(self.main_lbl)
        frame11.grid(row=0, column=0, sticky='nesw')

        self.timescale = EntryTimeScale(frame11, duration=duration, step=step)
        self.timescale.grid(row=0, column=0, sticky='nsew')
        # -------------------------------------------------
        frame12 = ttk.Frame(self.main_lbl)
        frame12.grid(row=1, column=0, sticky='news')

        self.gen_lbl = ttk.LabelFrame(frame12, text='Generate the set', padding=5)
        self.gen_lbl.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        frame21 = ttk.Frame(self.gen_lbl)
        frame21.grid(row=0, column=0, sticky='nsew')

        self.func_lbl = ttk.LabelFrame(frame21, text='func.', padding=(20,5))
        self.func_lbl.grid(row=0, column=0, padx=20, pady=10)
        self.func_entry = EntryWithModel(self.func_lbl, model='X*X', width=15)
        self.func_entry.grid()

        self.min_lbl = ttk.LabelFrame(frame21, text='min.', padding=(20,5))
        self.min_lbl.grid(row=0, column=1, padx=20, pady=10)
        self.min_entry = EntryWithModel(self.min_lbl, model='00.0', width=4)
        self.min_entry.grid()

        self.max_lbl = ttk.LabelFrame(frame21, text='max.', padding=(20,5))
        self.max_lbl.grid(row=0, column=2, padx=20, pady=10)
        self.max_entry = EntryWithModel(self.max_lbl, model='00.0', width=4)
        self.max_entry.grid()

        self.rand_lbl = ttk.LabelFrame(frame21, text='rand.', padding=(20,5))
        self.rand_lbl.grid(row=0, column=3, padx=20, pady=10)
        self.rand_entry = EntryWithModel(self.rand_lbl, model='0.0%', width=5,
                                         min=0, max=100)
        self.rand_entry.grid()

        # -------------------------------------------------
        frame22 = ttk.Frame(self.gen_lbl)
        frame22.grid(row=0, column=1, sticky='nswe')

        self.gen_btn = ttk.Button(frame22, text='gen.', padding=(20,5),
                                  command=self.generate_set)
        self.gen_btn.grid(row=0, column=0, padx=20, pady=10, sticky='ews')
        self.list_btn = ttk.Button(frame22, text='list', padding=(20,5),
                                   command=self.list_data, state='disabled')
        self.list_btn.grid(row=1, column=0, padx=20, pady=10, sticky='ews')
        self.plot_btn = ttk.Button(frame22, text='plot', padding=(20,5),
                                   command=self.plot_set, state='disabled')
        self.plot_btn.grid(row=0, column=1, padx=20, pady=10, sticky='ews')
        self.reset_btn = ttk.Button(frame22, text='new', padding=(20,5),
                                    command=self.reset_set, state='disabled')
        self.reset_btn.grid(row=1, column=1, padx=20, pady=10, sticky='ews')
        # -------------------------------------------------

        self.ACC = accuracy
        self.event_handler = None
        self.NAME = name
        self.X_values = []
        self.Y_values = []
        self.DATE_FORMAT = self.timescale.start_entry.DATE_FORMAT

    @property
    def name(self):
        return self.NAME

    @property
    def values(self):
        return [[x, y] for x, y in zip(self.X_values, self.Y_values)]

    @property
    def date_format(self):
        return self.DATE_FORMAT

    @property
    def csv(self):
        _RESULT = ''
        for x,y in zip(self.X_values, self.Y_values):
            STR = datetime.strftime(x, self.timescale.date_format)
            STR += ', '
            STR += str(round(y, self.ACC))
            STR += '\n'
            _RESULT += STR
        return _RESULT

    @property
    def llist(self):
        """A list of list, indeed a list of couples."""
        return [[datetime.strftime(x, format=self.timescale.date_format),
                round(y, self.ACC)]
                for x, y in zip(self.X_values, self.Y_values)]

    @property
    def list(self):
        _RESULT = []
        for x,y in zip(self.X_values, self.Y_values):
            _STR = datetime.strftime(x, format=self.timescale.date_format)
            _STR += '  '
            _STR += '{:15.3f}'.format(y)
            _RESULT.append(_STR)
        return _RESULT

    def set_event_handler(self, handler):
        """allow to externally defined the event handler."""
        self.event_handler = handler

    def publish_set_generated_event(self):
        self.timescale.configure(state='disabled')
        self.gen_btn.configure(state='disabled')
        self.list_btn.configure(state='normal')
        self.plot_btn.configure(state='normal')
        self.reset_btn.configure(state='normal')
        self.func_entry.configure(state='disabled')
        self.min_entry.configure(state='disabled')
        self.max_entry.configure(state='disabled')
        self.rand_entry.configure(state='disabled')
        if self.event_handler is not None:
            self.event_generate('<<set generated>>', when='tail')
            self.event_handler('set generated event')

    def publish_reset_event(self):
        self.timescale.configure(state='normal')
        self.gen_btn.configure(state='normal')
        self.list_btn.configure(state='disabled')
        self.plot_btn.configure(state='disabled')
        self.reset_btn.configure(state='disabled')
        self.func_entry.configure(state='normal')
        self.min_entry.configure(state='normal')
        self.max_entry.configure(state='normal')
        self.rand_entry.configure(state='normal')
        if self.event_handler is not None:
            self.event_generate('<<reset>>', when='tail')
            self.event_handler('reset event')

    def generate_set(self):
        _MIN = float(self.min_entry.get())
        _MAX = float(self.max_entry.get())
        _RAND = self.rand_entry.get()
        if _RAND[-1:] == "%":
            _COEF_RAND = float(_RAND[:-1])/100
        else:
            _COEF_RAND = float(_RAND)/100
        if _COEF_RAND < 0 or _COEF_RAND > 1:
            # entry error
            self.rand_entry.configure(background='red', foreground='yellow')
            self.rand_entry.ENTRY_ERROR = True
            return
        _RANGE = _MAX - _MIN
        _FUNC = self.func_entry.get()
        _PT_NBS = self.timescale.ticks_number

        try:
            x_val = range(_PT_NBS)
            y_val = []
            y_min = 0
            y_max = 0
            y = y_min
            # generate points
            for x in x_val:
                y = eval(_FUNC.replace('X', str(x)))
                # update y_min & y_max
                if y < y_min:
                    y_min = y
                if y > y_max:
                    y_max = y
                y_val.append(y)
            # normalize            
            _range = y_max - y_min
            if _range <= 0:
                # entry error
                self.min_entry.configure(background='red', foreground='yellow')
                self.max_entry.configure(background='red', foreground='yellow')
                self.min_entry.ENTRY_ERROR = True

            _COEF = _RANGE / _range
            self.Y_values = [_MIN + _COEF * y + 
                             uniform(_MIN, _COEF_RAND*_MAX) for y in y_val]
            self.X_values = self.timescale.ticks_list
            self.publish_set_generated_event()

        except Exception as e:
            raise Exception(f'error: {str(e)}')

    def list_data(self, title='Data list'):
        display_list(self, datalist=self.list, title='data list')

    def plot_set(self, title='Plot of the generated set.',
                 settings=plot_settings):
        if len(self.Y_values) == 0:
            return
        _WIN = Toplevel(root)
        _WIN.title(title)
        figure = Figure(figsize=(6,4), dpi=100)
        canvas = FigureCanvasTkAgg(figure, _WIN)
        NavigationToolbar2Tk(canvas, _WIN)
        axes = figure.add_subplot()
        line, = axes.plot(self.X_values, self.Y_values)

        if self.timescale.duration < timedelta(days=1):
            axes.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        else:
            axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

        # axes.set_ylim()
        axes.tick_params(axis='both', labelsize=settings['labelsize'])
        axes.set_title(f'Graph of {self.name}',
                        fontsize=int(settings['labelsize']*1.8),
                        fontweight='bold')
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=TOP, fill=BOTH, expand=True)
        canvas_widget.configure(width=settings['width'], height=settings['height'])

    def reset_set(self):
        self.X_values = []
        self.Y_values = []
        self.publish_reset_event()


if __name__ == '__main__':

    root = Tk()
    root.title('Test entry of a generator.')
    root.geometry('2300x800')
    # root.attributes('-topmost', 1)  # keep window on top, while checking the code

    # controlling the size of the default font
    default_font = font.nametofont('TkDefaultFont')
    default_font.configure(size=12)
    root.option_add('*Font', default_font)

    style = ttk.Style()
    style.configure('light.TFrame', background='cornsilk')
    style.configure('light.TLabel', background='cornsilk')
    style.configure('red.TFrame', background='red')
    style.configure('yellow.TFrame', background='yellow')
    style.configure('black.TEntry', fieldbackground='gray99', foreground='black')
    style.configure('blue.TEntry', fieldbackground='khaki', foreground='blue')
    style.configure('gray.TEntry', fieldbackground='gray99', foreground='gray60')
    style.configure('red.TEntry', fieldbackground='yellow', foreground='red')

    frame = ttk.Frame(root)
    frame.grid(row=0, column=0, padx=40, pady=20, sticky='nsew')
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    entryGenerator = EntryGenerator(frame, name='set 01')
    entryGenerator.grid(row=0,column=0, sticky='nesw')

    # proposal of entries ---------------------------------
    entryGenerator.timescale.start_entry.enter('2022-02-01 09:00:00')
    entryGenerator.timescale.end_entry.enter('2022-02-01 11:00:00')
    entryGenerator.timescale.step_entry.enter('1min')
    # ------------------------------------------------------

    frame_btn = ttk.Frame(root)
    frame_btn.grid(row=1, column=0, sticky='nsew')
    frame_btn.rowconfigure(0, weight=1)
    frame_btn.columnconfigure(0, weight=1)

    """
    def open_list():
        display_list(root, datalist=entryGenerator.list, title='data list')

    button_list = tk.Button(frame_btn, text='list data', state='disabled',
                            command=open_list)
    button_list.grid(row=0, column=0, padx=20, pady=20)
    """

    button_close = ttk.Button(frame_btn, text='close', command=lambda: root.destroy())
    button_close.grid(row=0, column=0, padx=20, pady=20)

    frame_status = ttk.Frame(root, style='light.TFrame')
    frame_status.grid(row=2, column=0, padx=20, pady=20, sticky='sew')
    status_lbl= ttk.Label(frame_status, text='status: ', padding=10, anchor='w', style='light.TLabel')
    status_lbl.grid(sticky='nsew')

    def status_update(event):
        if event == 'set generated event':
            status_lbl.configure(text='status: set generated')
        elif event == 'reset event':
            status_lbl.configure(text='status: ')

    entryGenerator.set_event_handler(status_update)

    root.resizable(height=True, width=False)
    root.rowconfigure(0, weight=0)
    root.rowconfigure(1, weight=1)
    root.rowconfigure(2, weight=0)

    root.mainloop()

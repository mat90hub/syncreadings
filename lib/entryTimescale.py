from tkinter import Tk, ttk, font, NORMAL, DISABLED
from datetime import datetime, timedelta
from entryDatetime import EntryDatetime
from entryTimedelta import EntryTimedelta, strptimedelta, strftimedelta


class EntryTimeScale(ttk.Frame):
    
    def __init__(self, container, duration="1h", step="1min", **kwargs):

        self.STYLE_ENTRY = kwargs.pop('style_entry','TEntry')
        self.STYLE_LABEL = kwargs.pop('style_label', 'TLabelFrame')
        super().__init__(container, **kwargs)
        self.start_lbl = ttk.LabelFrame(container,text="start", padding=(10,1,10,1))
        self.start_lbl.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.start_entry = EntryDatetime(self.start_lbl, style=self.STYLE_ENTRY)
        self.start_entry.grid()
        self.start_entry.IS_EMPTY = True

        self.end_lbl = ttk.LabelFrame(container, text="end", padding=(10,1,10,1))
        self.end_lbl.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.end_entry = EntryDatetime(self.end_lbl, style=self.STYLE_ENTRY)
        self.end_entry.grid()
        self.end_entry.IS_EMPTY = True
        
        self.DURATION = strptimedelta(duration)
        self.STEP = strptimedelta(step)
        
        self.step_lbl = ttk.LabelFrame(container, text="step", padding=(10,1,10,1))
        self.step_lbl.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        self.step_entry = EntryTimedelta(self.step_lbl, model=step, style=self.STYLE_ENTRY)
        self.step_entry.grid()

        container.rowconfigure(0, weight=0)
        container.columnconfigure(0, weight=0)
        container.columnconfigure(1, weight=0)
        container.columnconfigure(2, weight=0)

        if 'state' in kwargs:
            self.STATE = kwargs.pop('state', 'normal')
            self.start_entry.configure(state=self.STATE)
            self.end_entry.configure(state=self.STATE)
            self.step_entry.configure(state=self.STATE)
        else:
            self.STATE = NORMAL
        
        if 'style' in kwargs:
            self.STYLE = kwargs.pop('style', 'TEntry')
            self.start_entry.configure(style=self.STYLE)
            self.end_entry.configure(style=self.STYLE)
            self.step_entry.configure(style=self.STYLE)
        else:
            self.STYLE = 'TEntry'
        
        # define style for small labels on the Labelframe and padding for TEntry
        self.style = ttk.Style(self)
        self.style.configure('TLabelframe.Label', font=('Helvetica', 10, 'bold', 'italic'), foreground='gray60')
        self.style.configure('TEntry', padding=(50,1,50,1))

        self.start_entry.bind('<Leave>', self.on_leave)
        
    @property
    def start(self) -> datetime:
        return self.start_entry.datetime
    
    @property
    def end(self) -> datetime:
        return self.end_entry.datetime
    
    @property
    def date_format(self) -> str:
        return self.start_entry.DATE_FORMAT
         # >> check that start and end have the same format?

    @property
    def step(self) -> timedelta:
        self.STEP = self.step_entry.timedelta
        return self.STEP

    @property
    def duration(self) -> timedelta:
        self.DURATION = self.end - self.start
        return self.DURATION

    @property
    def ticks_number(self) -> int:
        return int(self.DURATION.total_seconds() / self.step.total_seconds())

    @property
    def ticks_list(self) -> list:
        """Generate the time scale from the values"""
        try:
            START = self.start
            STEP = self.step
            NB = self.ticks_number
            TIME_PT = [START + n * STEP for n in range(NB)]
            return TIME_PT
        except Exception as e:
            raise Exception(f"error: {str(e)}")

    def on_leave(self, event):
        '''prefill the end entry with the start'''
        print(event)
        if not self.start_entry.isEmpty and self.end_entry.isEmpty:
            _START = self.start_entry.datetime
            _END = _START + self.DURATION
            _END_STR = datetime.strftime(_END, self.end_entry.format)
            self.end_entry.enter(_END_STR)
            self.step_entry.enter(strftimedelta(self.STEP))

    def configure(self, **kwargs):
        if 'state' in kwargs:
            self.STATE = kwargs.pop('state', 'normal')
            self.start_entry.configure(state=self.STATE)
            self.end_entry.configure(state=self.STATE)
            self.step_entry.configure(state=self.STATE)

        if 'style' in kwargs:
            self.STYLE = kwargs.pop('style', 'TEntry')
            self.start_entry.configure(style=self.STYLE)
            self.end_entry.configure(style=self.STYLE)
            self.step_entry.configure(style=self.STYLE)
        
        super().configure

    def cget(self, property: str):
        if property == 'state':
            if str(self.start_entry['state']) == 'disabled' and \
               str(self.end_entry['state']) == 'disabled' and \
               str(self.step_entry['state']) == 'disabled':
                return DISABLED
            else:
                return NORMAL
        else:
            super().cget(property)

if __name__ == "__main__":
    root = Tk()
    root.title("Test entry of a time scale.")
    root.geometry('2500x800')
    root.attributes('-topmost', 1)  # keep window on top, while checking the code

    # content of root shall expand
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=0)
    root.rowconfigure(1, weight=0)
    root.rowconfigure(2, weight=0)

    # controlling the size of the default font
    default_font = font.nametofont('TkDefaultFont')
    default_font.configure(size=18)
    root.option_add('*Font', default_font)

    style = ttk.Style()
    style.configure('red.TFrame', background='red')
    style.configure('yellow.TFrame', background='yellow')
    style.configure('black.TEntry', fieldbackground='gray99', foreground='black', padding=(50,1,50,1))
    style.configure('blue.TEntry', fieldbackground='khaki', foreground='blue', padding=(50,1,50,1))
    style.configure('gray.TEntry', fieldbackground='gray99', foreground='gray60', padding=(50,1,50,1))
    style.configure('red.TEntry', fieldbackground='yellow', foreground='red', padding=(50,1,50,1))
    
    # change the size and color of the Label of the Labelframe
    # smallFont = font.Font(family='Helvetica', name='smallFont', size=9, weight='bold', slant='italic')
    # style.configure('TLabelframe.Label', font=smallFont, foreground='gray60')

    # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-map.html 

    frame = ttk.Frame(root)
    frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    # frame.configure(style='red.TFrame')
    frame.grid_columnconfigure(0, weight=0)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_rowconfigure(0, weight=0)
    frame.grid_rowconfigure(1, weight=0)
    frame.grid_rowconfigure(2, weight=1)

    entryTimescale = EntryTimeScale(frame, style_entry='blue.TEntry')
    entryTimescale.grid(row=0,column=0, rowspan=2, sticky='ew')
    
    # Enter a date ---------------------------------
    entryTimescale.start_entry.enter("2022-02-01 09:00:00")
    entryTimescale.end_entry.enter("2022-02-01 11:00:00")
    entryTimescale.step_entry.enter("1min")
    # ----------------------------------------------

    frame_res = ttk.Frame(root)
    frame_res.grid(row=1, column=0, sticky="nsew", padx=20, pady=5)
    # frame.configure(style='red.TFrame')
    frame_res.grid_columnconfigure(0, weight=0)
    frame_res.grid_columnconfigure(1, weight=1)
    frame_res.grid_rowconfigure(0, weight=1)
    
    # ttk.Label(frame, text='result:', justify='left', anchor="w").grid(row=1, column=0, padx=(20,10), day=20)
    ttk.Label(frame_res, text='result:').grid(row=0, column=0, sticky='e', padx=(20,10), pady=20)
    result = ttk.Label(frame_res, anchor='w', justify='left')
    result.grid(row=0 ,column=1, sticky="ew", padx=(10,20), pady=20)

    # ----------------------------------------------
    frame_btn = ttk.Frame(root)
    frame_btn.grid(row=2, column=0, sticky="nesw", padx=20, pady=20)
    frame_btn.grid_columnconfigure(0, weight=1)
    frame_btn.grid_columnconfigure(1, weight=1)
    frame_btn.grid_columnconfigure(2, weight=1)
    frame_btn.grid_columnconfigure(3, weight=1)
    frame_btn.grid_rowconfigure(0, weight=1)

    button_nb = ttk.Button(frame_btn, text='ticks number', padding=10,
                           command=lambda: result.configure(text=entryTimescale.ticks_number))
    button_nb.grid(row=0, column=0, padx=20, pady=50)

    button_lst = ttk.Button(frame_btn, text='ticks list', padding=10,
                            command=lambda: result.configure(text=entryTimescale.ticks_list))
    button_lst.grid(row=0, column=1, padx=20, pady=50)

    def switch_disabled():
        STATE = entryTimescale.cget("state")
        if STATE == "normal":
            entryTimescale.configure(state="disabled")
            button_disabled.configure(text="enable")
        else:
            entryTimescale.configure(state="normal")
            button_disabled.configure(text="disable")

    button_disabled=ttk.Button(frame_btn, text="disabled", padding=10, command=switch_disabled)
    button_disabled.grid(row=0, column=2, padx=20, pady=50)

    button_close = ttk.Button(frame_btn, text='close', padding=10, command=lambda: root.destroy())
    button_close.grid(row=0, column=3, padx=20, pady=50)

    # root.resizable(False, False)
    root.mainloop()


# https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-Entry.html
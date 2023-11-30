from tkinter import Tk, ttk, font, StringVar, END

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

class EntryWithModel(ttk.Entry):
    """Entry widget with a model."""
    def __init__(self, container, **kwargs):
        self.MODEL = kwargs.pop('model', ' sin(x) ')
        self.STYLE = kwargs.pop('style', 'TEntry')
        self.STYLE_MODEL = kwargs.pop('style_model', 'TEntry')
        self.STYLE_ERROR = kwargs.pop('style_error', 'TEntry')
        self.MIN = kwargs.pop('min', 0)
        self.MAX = kwargs.pop('max', 100)
        # if no width give, choose a sufficient width to show content
        if 'width' not in kwargs and self.MODEL is not None:
            self.WIDTH = len(self.MODEL) + 2        
        # initialize the remaining parameters
        super().__init__(container, **kwargs)
        
        # other initializations
        self.IS_EMPTY = True
        self.ENTRY_ERROR = False
        super().insert(0, self.MODEL)        
        super().configure(style=self.STYLE_MODEL)

        self.bind('<KeyRelease>', self.on_keyrelease)
        self.bind('<Leave>', self.on_leave)
        self.bind('<Enter>', self.on_enter)
        
    @property
    def isEmpty(self):
        return self.IS_EMPTY   

    @property
    def style_in_use(self):
        if self.isEmpty:
            return self.STYLE_MODEL
        elif self.ENTRY_ERROR:
            return self.STYLE_ERROR
        else:
            return self.STYLE

    def configure(self, **kwargs):
        """Extension of configure to new cases."""
        if 'model' in kwargs:
            self.MODEL = kwargs.pop('model')
            if self.IS_EMPTY:            
                self.delete(0, END)
                self.insert(END, self.MODEL)
        if 'width' not in kwargs:
            self.WIDTH = len(self.MODEL) + 2
        else:
            self.WIDTH = kwargs.pop('width')

        if 'style_error' in kwargs:
            self.STYLE_ERROR = kwargs.pop('style_error')            
        if 'style_model' in kwargs:
            self.STYLE_MODEL = kwargs.pop('style_model')
            if self.IS_EMPTY:
                super().configure(style=self.STYLE_MODEL)
        super().configure(**kwargs)

    def cget(self, property_name: str):
        match property_name:
            case 'model':
                return self.MODEL        
            case 'style_model':
                return self.STYLE_MODEL
            case 'style_error':
                return self.STYLE_ERROR
            case 'min':
                return self.MIN
            case 'max':
                return self.MAX
            case _:
                return super().cget(property_name)

    def enter(self, value):
        """simulate a user entry."""
        if len(value) > 0:
            self.delete(0, END)
            self.insert(0, value)
            self.configure(style=self.STYLE)
            self.IS_EMPTY = False
            self.on_leave(None)

    def clear(self):
        self.delete(0, END)
        self.ENTRY_ERROR = False
        self.configure(style=self.STYLE_MODEL)
        self.insert(0, self.MODEL)
        self.IS_EMPTY = True         
    
    def on_enter(self, event=None):
        """when the user enter in the entry widget."""
        _VAL = self.get()
        if self.IS_EMPTY and len(_VAL) > 0:
            self.delete(0, END)
            super().configure(style=self.STYLE)

    def on_keyrelease(self, event):
        if len(self.get()) > 0:
            self.IS_EMPTY = False
        else:
            self.IS_EMPTY = True
            self.ENTRY_ERROR = False
    
    def on_leave(self, event=None):
        """when the user leases the entry widget."""
        _VAL = self.get()
        if self.IS_EMPTY and len(_VAL) == 0:
            self.insert(0, self.MODEL)
            self.configure(style=self.STYLE_MODEL)
        elif isfloat(_VAL):
            if self.MIN != None and self.MAX != None:                        
                _VAL = float(_VAL)
                if _VAL < self.MIN or _VAL > self.MAX:
                    self.raise_entry_error()
        return 'break'

    def raise_entry_error(self):
        self.ENTRY_ERROR = True
        self.configure(style=self.STYLE_ERROR)

if __name__ == '__main__':
     
    root = Tk()
    root.title('Test entry with model.')
    root.geometry('1800x600')
    root.attributes('-topmost', 1)  # keep window on top, while checking the code

    # content of root shall expand
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=0)

    # controlling the size of the default font
    default_font = font.nametofont('TkDefaultFont')
    default_font.configure(size=18)
    root.option_add('*Font', default_font)

    style = ttk.Style()
    style.configure('red.TFrame', background='red')
    style.configure('yellow.TFrame', background='yellow')
    style.configure('black.TEntry', fieldbackground='gray99', foreground='black')
    style.configure('blue.TEntry', fieldbackground='khaki', foreground='blue')
    style.configure('gray.TEntry', fieldbackground='gray99', foreground='gray60')
    style.configure('red.TEntry', fieldbackground='yellow', foreground='red')
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    frame = ttk.Frame(root)
    frame.grid(row=0, column=0, sticky='nsew')
    # frame.configure(style='red.TFrame')
    frame.grid_columnconfigure(0, weight=0)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_rowconfigure(0, weight=0)
    frame.grid_rowconfigure(1, weight=0)
    frame.grid_rowconfigure(2, weight=1)

    entryWithModel = EntryWithModel(frame, style_model='gray.TEntry', style_error='red.TEntry')
    entryWithModel.grid(row=0, column=0, columnspan=2, pady=20, padx=20, sticky='ew')
    
    variable = StringVar(root, 'default result')
    entry = ttk.Entry(frame, style='blue.TEntry', textvariable=variable)
    entry.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky='ew')

    res_lbl = ttk.Label(frame, text="result:", anchor="e", justify="left", width=6)
    res_lbl.grid(row=2, column=0, sticky='w', pady=20, padx=(20,5))
    result = ttk.Label(frame, anchor="e", justify="left")
    result.grid(row=2, column=1, sticky='ew', padx=(5,20), pady=20)
    
    # rules for expansion in frame

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    frame_btn = ttk.Frame(root, height=4)
    frame_btn.grid(row=1, column=0, sticky='nesw')
    # frame_btn.configure(style='yellow.TFrame')
    frame_btn.grid_columnconfigure(0, weight=1)
    frame_btn.grid_columnconfigure(1, weight=1)
    frame_btn.grid_columnconfigure(2, weight=1)
    frame_btn.grid_rowconfigure(0, weight=1)

    # Button frame:
    # rapid and rough check of configure for new and old properties
    button_mdl = ttk.Button(frame_btn, text='model',
                            command=lambda: {entryWithModel.configure(model=' arctan(x) ')
                                            if (entryWithModel.cget('model')==' sin(x) ')
                                            else entryWithModel.configure(model=' sin(x) ')})
    button_mdl.grid(row=0, column=0, padx=40, pady=20, ipadx=10, sticky='s')

    button_bg = ttk.Button(frame_btn, text='color',
                           command=lambda: entryWithModel.configure(style='gray.TEntry')
                                           if entryWithModel['style'] == 'red.TEntry'
                                           else entryWithModel.configure(style='red.TEntry'))
    
    button_bg.grid(row=0, column=1, padx=40, pady=20, sticky='se')
    button_close = ttk.Button(frame_btn, text='close', command=lambda: root.destroy())
    button_close.grid(row=0, column=2, padx=40, pady=20, sticky='se')
    
    root.mainloop()


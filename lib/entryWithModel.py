import tkinter as tk
from tkinter import ttk, font
from ttkthemes import ThemedTk

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

class EntryWithModel(ttk.Entry):
    """Entry widget with a model."""
    def __init__(self, master, **kwargs):
        
        # recover all particular new parameters
        # from kwargs (avoid mixing)
        if 'model' in kwargs:
            self.MODEL = kwargs.pop('model')
        else:
            self.MODEL = " sin(x)"

        if 'style' in kwargs:
            self.STYLE = kwargs.pop('style')
        
        if 'style_model' in kwargs:
            self.STYLE_MODEL = kwargs.pop('style_model')
        else:
            self.STYLE_MODEL=''
        
        if 'style_error' in kwargs:
            self.STYLE_ERROR = kwargs.pop('style_error')
        else:
            self.STYLE_ERROR=''
        
        if 'min' in kwargs:
            self.MIN = kwargs.pop('min')        
        else:
            self.MIN = 0

        if 'max' in kwargs:
            self.MAX = kwargs.pop('max')
        else:
            self.MAX = 100

        # the standard parameters, that may be absent
        if 'width' not in kwargs and self.MODEL is not None:
            self.WIDTH = len(self.MODEL) + 2
        
        # initialize the remaining parameters
        super().__init__(master, **kwargs)
        
        # other initializations
        self.IS_EMPTY = True
        self.ENTRY_ERROR = False
        super().insert(0, self.MODEL)
        super().configure(style=self.STYLE_MODEL)

        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)
        self.bind("<Return>", self.on_focus_out)
        self.bind("<Tab>", self.on_focus_out)
        self.bind("<Shift-Tab>", self.on_focus_out)
        self.bind("<Leave>", self.on_focus_out)
        
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
        if 'width' not in kwargs:
            self.WIDTH = len(self.MODEL) + 2
        else:
            self.WIDTH = kwargs.pop('width')
        if self.IS_EMPTY:
            super().configure(style=self.STYLE_MODEL)
            self.delete(0, tk.END)
            self.insert(0, self.MODEL)
        if 'style_error' in kwargs:
            self.STYLE_ERROR = kwargs.pop('style_error')
        if 'style_model' in kwargs:
            self.STYLE_MODEL = kwargs.pop('style_model')
            super().configure(style=self.STYLE_MODEL)
        super().configure(**kwargs)

    def cget(self, property_name: str):
        match property_name:
            case "model":
                return self.MODEL        
            case "style_model":
                return self.STYLE_MODEL
            case "style_error":
                return self.STYLE_ERROR
            case "min":
                return self.MIN
            case "max":
                return self.MAX
            case _:
                return super().cget(property_name)
            
    def enter(self, value):
        """simulate a user entry."""
        self.delete(0, tk.END)
        self.insert(0, value)
        self.configure(style=self.STYLE)
        self.on_focus_out(None)

    def clear(self):
        self.delete(0, tk.END)
        self.ENTRY_ERROR = False
        self.configure(style=self.STYLE_MODEL)
        self.insert(0, self.MODEL)
        self.IS_EMPTY = True

    def on_focus_in(self, event=None):
        if self.get() == self.MODEL:
            self.delete(0, tk.END)
            self.ENTRY_ERROR = False
            self.configure(style=self.STYLE)

    def on_focus_out(self, event):
        VAL = self.get()
        if VAL == self.MODEL:
            self.IS_EMPTY = True
            self.configure(style=self.STYLE_MODEL)            
        elif isfloat(VAL) and self.MIN != None and self.MAX != None:                        
            VAL = float(VAL)
            if VAL < self.MIN or VAL > self.MAX:
                self.raise_entry_error()
            else:
                self.ENTRY_ERROR = False
                self.configure(style=self.STYLE)
        else:
            self.configure(style=self.STYLE)
    
    def raise_entry_error(self):
        self.ENTRY_ERROR = True
        self.configure(self=self.STYLE_ERROR)

if __name__ == '__main__':
     
    # root = ThemedTk(theme='keramic')
    root = ThemedTk(theme='arc')
    root.title('Test entry with model.')
    root.geometry('1200x400')
    root.attributes('-topmost', 1)  # keep window on top, while checking the code

    # controlling the size of the default font
    default_font = font.nametofont('TkDefaultFont')
    default_font.configure(size=12)
    root.option_add('*Font', default_font)

    style = ttk.Style()
    style.configure('red.TFrame', background='red')
    style.configure('yellow.TFrame', background='yellow')
    style.configure('grey.TEntry', foreground='grey')
    style.configure('red.TEntry', foreground='yellow', background='red')

    frame = ttk.Frame(root)
    frame.grid(row=0, column=0, sticky='nsew')
    # frame.configure(style='red.TFrame')

    frame_btn = ttk.Frame(root, height=4)
    frame_btn.grid(row=1, column=0, sticky='nesw')
    # frame_btn.configure(style='yellow.TFrame')

    # content of root shall expand
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=0)

    # content of frame
    entryWithModel = EntryWithModel(frame, 
                                    style_model='grey.TEntry',
                                    style_error='red.TEntry')
    entryWithModel.grid(row=0, column=0, columnspan=2, pady=20, padx=20, sticky='ew')
    
    res_lbl = ttk.Label(frame, text="result:", anchor="e", justify="left", width=6)
    res_lbl.grid(row=1, column=0, sticky='w', pady=20, padx=(20,5))
    result = ttk.Label(frame, anchor="e", justify="left")
    result.grid(row=1, column=1, sticky='ew', padx=(5,20), pady=20)
    
    # rules for expansion in frame
    frame.grid_columnconfigure(0, weight=0)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_rowconfigure(0, weight=0)
    frame.grid_rowconfigure(1, weight=1)
    
    # Button frame:
    # rapid and rough check of configure for new and old properties
    button_mdl = ttk.Button(frame_btn, text='model',
                            command=lambda: {entryWithModel.configure(model=" arctan(x) ")
                                            if (entryWithModel.cget("model")==" sin(x)")
                                            else entryWithModel.configure(model=" sin(x)")})
    button_mdl.grid(row=0, column=0, padx=40, pady=20, ipadx=10, sticky='s')

    button_bg = ttk.Button(frame_btn, text='color',
                           command=lambda: entryWithModel.configure(style='grey.TEntry')
                                           if entryWithModel.style_in_use == 'red.TEntry'
                                           else entryWithModel.configure(style='red.TEntry'))
    button_bg.grid(row=0, column=1, padx=40, pady=20, sticky='se')

    
    button_close = ttk.Button(frame_btn, text='close', command=lambda: root.destroy())
    button_close.grid(row=0, column=2, padx=40, pady=20, sticky='se')
    
    # rules for expansion in frame
    frame_btn.grid_columnconfigure(0, weight=1)
    frame_btn.grid_columnconfigure(1, weight=1)
    frame_btn.grid_columnconfigure(2, weight=1)
    frame_btn.grid_rowconfigure(0, weight=1)
    
    
    root.mainloop()


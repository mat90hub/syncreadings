import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

class EntryWithModel(tk.Entry):
    """Entry widget with a model."""
    def __init__(self, master, **kwargs):
        
        # recover all particular new parameters
        # from kwargs (avoid mixing)
        if 'model' in kwargs:
            self.MODEL_TEXT = kwargs.pop('model')
        else:
            self.MODEL_TEXT = " sin(x)"
        
        if 'model_color' in kwargs:
            self.MODEL_COLOR = kwargs.pop('model_color')
        else:
            self.MODEL_COLOR="grey"
        
        if 'err_bg_col' in kwargs:
            self.ERR_BG_COLOR = kwargs.pop('err_bg_col')
        else:
            self.ERR_BG_COLOR='red'
        
        if 'err_fg_col' in kwargs:
            self.ERR_FG_COLOR = kwargs.pop('err_fg_col')
        else:
            self.ERR_FG_COLOR='yellow'
        
        if 'min' in kwargs:
            self.MIN = kwargs.pop('min')        
        else:
            self.MIN = 0

        if 'max' in kwargs:
            self.MAX = kwargs.pop('max')
        else:
            self.MAX = 100

        # the standard parameters, that may be absent
        if 'width' not in kwargs and self.MODEL_TEXT is not None:
            self.WIDTH = len(self.MODEL_TEXT) + 2
        
        # initialize the remaining parameters
        super().__init__(master, **kwargs)
        
        # other initializations
        self.IS_EMPTY = True
        self.FG_COLOR = self.cget("foreground")
        self.BG_COLOR = self.cget("background")
        self.ENTRY_ERR = False
        
        super().insert(0, self.MODEL_TEXT)
        super().configure(foreground=self.MODEL_COLOR)

        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)
        self.bind("<Return>", self.on_focus_out)
        self.bind("<Tab>", self.on_focus_out)
        self.bind("<Shift-Tab>", self.on_focus_out)
        self.bind("<Leave>", self.on_focus_out)
        
    @property
    def isEmpty(self):
        return self.IS_EMPTY   

    def configure(self, **kwargs):
        """Extension of configure to new cases."""
        if 'model' in kwargs:
            self.MODEL_TEXT = kwargs.pop('model')
            if 'width' not in kwargs:
                self.WIDTH = len(self.MODEL_TEXT) + 2
                super().configure(width=self.WIDTH)
            else:
                self.WIDTH = kwargs.pop('width')
            if self.IS_EMPTY:
                super().configure(foreground=self.MODEL_COLOR, 
                                  background=self.BG_COLOR)
                self.delete(0,tk.END)
                self.insert(0, self.MODEL_TEXT)
        if 'model_color' in kwargs:
            self.MODEL_COLOR = kwargs.pop('model_color')
            if self.IS_EMPTY:
                self.clear()
        super().configure(**kwargs)

    def cget(self, property_name: str):
        match property_name:
            case "model":
                return self.MODEL_TEXT
            case "model_color":
                return self.MODEL_COLOR
            case "error_fg_color":
                return self.ERR_FG_COLOR
            case "error_bg_color":
                return self.ERR_BG_COLOR
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
        self.configure(foreground=self.FG_COLOR,
                       background=self.BG_COLOR)
        self.on_focus_out(None)

    def clear(self):
        self.delete(0, tk.END)
        self.ENTRY_ERR = False
        self.configure(foreground=self.MODEL_COLOR,
                       background=self.BG_COLOR)
        self.insert(0, self.MODEL_TEXT)
        self.IS_EMPTY = True

    def on_focus_in(self, event=None):
        if self.get() == self.MODEL_TEXT:
            self.delete(0, tk.END)
        self.ENTRY_ERR = False
        self.configure(foreground=self.FG_COLOR, 
                       background=self.BG_COLOR)

    def on_focus_out(self, event):
        VAL = self.get()
        if VAL == None:
            self.insert(0, self.MODEL_TEXT)
            self.configure(foreground=self.MODEL_COLOR, 
                           background=self.BG_COLOR)

        elif isfloat(VAL) and self.MIN != None and self.MAX != None:                        
            VAL = float(VAL)
            if VAL < self.MIN or VAL > self.MAX:
                self.raise_entry_error()
            else:
                self.ENTRY_ERR = False
                self.configure(foreground=self.FG_COLOR, 
                               background=self.BG_COLOR)
        else:
            self.configure(foreground=self.FG_COLOR, 
                           background=self.BG_COLOR)
    
    def raise_entry_error(self):
        self.ENTRY_ERR = True
        self.configure(foreground=self.ERR_FG_COLOR, 
                       background=self.ERR_BG_COLOR)

if __name__ == "__main__":
     
    # root = ThemedTk(theme='keramic')
    root = ThemedTk(theme='arc')
    root.title("Test entry with model.")
    root.geometry("1200x400")

    style = ttk.Style()
    style.configure('red.TFrame', background='red')

    frame = ttk.Frame(root, height = 80, width=1200)
    frame.grid(row=0, column=0, sticky='nsew')
    frame.configure(style='red.TFrame')
    
    # for the root window to be totally filled
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # idem for the frame
    frame.grid_columnconfigure(0, minsize=30, pad=5, weight=1)
    frame.grid_columnconfigure(1, minsize=30, pad=5, weight=1)
    frame.grid_columnconfigure(2, minsize=30, pad=5, weight=1)
    frame.grid_rowconfigure(0, minsize=30, pad=10, weight=0)
    frame.grid_rowconfigure(1, minsize=30, pad=10, weight=0)
    frame.grid_rowconfigure(2, minsize=30, pad=10, weight=1)

    entryWithModel = EntryWithModel(frame)
    entryWithModel.grid(row=0, column=0, columnspan=3, pady=20, padx=20, sticky='ew')
    
    res_lbl = ttk.Label(frame, text="result:", width=6, anchor="w", justify="right")
    res_lbl.grid(row=1, column=0, sticky='e', pady=20)
    result = ttk.Label(frame, width=44, anchor="w", justify="left")
    result.grid(row=1, column=1, columnspan=2, sticky='ew', padx=20, pady=20)

    # rapid and rough check of configure for new and old properties
    button_mdl = ttk.Button(frame, text='ch mdl',
                            command=lambda: {entryWithModel.configure(model=" arctan(x) ")
                                            if (entryWithModel.cget("model")==" sin(x)")
                                            else entryWithModel.configure(model=" sin(x)")})
    button_mdl.grid(row=3, column=0, padx=40, pady=20)

    button_bg = ttk.Button(frame, text='chge bg',
                           command=lambda: {entryWithModel.configure(background="white", foreground="black") 
                                            if (entryWithModel.cget("background") == "blue")
                                            else entryWithModel.configure(background="blue", foreground="white")})
    button_bg.grid(row=3, column=1, padx=40, pady=20, sticky='e')

    
    button_close = ttk.Button(frame, text='close', command=lambda: root.destroy())
    button_close.grid(row=3, column=2, padx=40, pady=20, sticky='e')
    
    root.mainloop()


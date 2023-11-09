import tkinter as tk

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

class EntryWithModel(tk.Entry):
    """Entry widget with a model."""
    def __init__(self, master,    
                 model=" sin(x) ",
                 model_color="grey",
                 min = None,
                 max = None,
                 err_bg_col="red",
                 err_fg_col="yellow",
                 **kwargs):
        super().__init__(master, **kwargs)
        self.MODEL_TEXT = model
        self.MODEL_COLOR = model_color
        self.IS_EMPTY = True
        
        self.FG_COLOR = self.cget("foreground")
        self.BG_COLOR = self.cget("background")
        self.ERR_BG_COLOR = err_bg_col
        self.ERR_FG_COLOR = err_fg_col

        self.MIN = min
        self.MAX = max
        self.ENTRY_ERR = False

        if 'width' not in kwargs:
            self.WIDTH = len(self.MODEL_TEXT) + 2
            self.configure(width=self.WIDTH)
        
        self.configure(foreground=self.MODEL_COLOR)
        self.insert(0, self.MODEL_TEXT)               
        
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
            case _:
                return super().cget(property_name)
            
    def enter(self, value):
        """simulate a user entry"""
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
    
    root = tk.Tk()
    root.title("Test entry with model.")
    frame = tk.Frame(root,width=15, height=6)
    frame.pack(expand=True)

    entryWithModel = EntryWithModel(frame)
    entryWithModel.pack()

    frame2 = tk.Frame(root, width = 15)
    frame2.pack(expand=True, fill=tk.BOTH)
    
    tk.Label(frame2, text="result:", width=6, anchor="w", justify="right").pack(side=tk.LEFT, padx=20, pady=20)
    result = tk.Label(frame2, width=44, anchor="w", justify="left")
    result.pack(side=tk.LEFT, padx=20, pady=30)

    frame_btn = tk.Frame(root)
    frame_btn.pack(side=tk.BOTTOM, expand=True)

    # rapid and rough check of configure for new and old properties
    button_bg = tk.Button(frame_btn, text='change background', 
                          command=lambda: {entryWithModel.configure(background="white", foreground="black") 
                                           if (entryWithModel.cget("background") == "blue") 
                                           else entryWithModel.configure(background="blue", foreground="white")})
    button_bg.pack(side=tk.LEFT, padx=20, pady=20)

    button_mdl = tk.Button(frame_btn, text='change model',
                           command=lambda: {entryWithModel.configure(model="arctan(x)")
                                            if (entryWithModel.cget("model")=="sin(x)")
                                            else entryWithModel.configure(model="sin(x)")})
    button_mdl.pack(padx=20, pady=20)

    button_close = tk.Button(frame2, text='close', 
                             command=lambda: root.destroy())
    button_close.pack(side=tk.RIGHT)
    root.mainloop()


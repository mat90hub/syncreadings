import tkinter as tk
from datetime import datetime
from entryWithModel import EntryWithModel
import string

class EntryDatetime(EntryWithModel):
    """
    Class for an entry dedicated to datetime.
    It will auto-correct entry and propose a model.
    With date property, it recovers a datetime.
    """
    def __init__(self, container,
                 model="YYYY-MM-DD HH:MM:SS",
                 format="%Y-%m-%d %H:%M:%S",              
                 err_bg_col="red",
                 err_fg_col="yellow",
                 **kwargs):
        super().__init__(container, **kwargs)
        self.MODEL_TEXT = model
        self.DATE_FORMAT = format
        self.ENTRY_ERROR = False
        self.STATE = "normal"

        self.ERR_BG_COL = err_bg_col
        self.ERR_FG_COL = err_fg_col

        if 'width' not in kwargs:
            self.WIDTH = len(self.MODEL_TEXT) + 2
        else:
            self.WIDTH = kwargs['width']
        self.configure(foreground=self.MODEL_COLOR,
                       width=self.WIDTH)
        self.delete(0,tk.END)
        self.insert(0, self.MODEL_TEXT)

        # Bind a click event to clear the model text
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)
        self.bind("<KeyPress>", self.key_press_handler)
        self.bind("<Return>", self.final_validation)
        self.bind("<Tab>", self.final_validation)
        self.bind("<Shift-Tab>", self.final_validation)
        self.bind("<Leave>", self.leave_widget)
        self.bind("<Left>", self.move_cursor_left)
        self.bind("<Right>", self.move_cursor_right)

        self.autocompletion_chars = {
            4: "-", 7:"-", 10: " ", 13: ":", 16: ":", 19: ""
        }
        # check if format contain microseconds and keep only milliseconds
        if self.DATE_FORMAT[-1] == 'f':
            self.autocompletion_chars[19] = "."
            self.autocompletion_chars[23] = ""
    
    @property
    def format(self):
        return self.DATE_FORMAT

    @property
    def datetime(self):
        if self.IS_EMPTY:
            return None
        else:
            return datetime.strptime(self.get(), self.DATE_FORMAT)
        
    @property
    def entryError(self):
        return self.ENTRY_ERROR
    
    def model_match_format(self) -> bool:
        """Check if the model text matches the format."""
        match self.DATE_FORMAT:
            case "%Y-%m-%d %H:%M:%S":
                if self.MODEL_TEXT == "YYYY-MM-DD HH:MM:SS":
                    return True
                else:
                    return False
            case "%Y-%m-%d %H:%M:%S.%f":
                if self.MODEL_TEXT == "YYYY-MM-DD HH:MM:SS.000":
                    return True
                else:
                    return False
            case "%H:%M:%S":
                if self.MODEL_TEXT == "HH:MM:SS":
                    return True
                else:
                    return False
            case "%H:%M:%S.%f":
                if self.MODEL_TEXT == "HH:MM:SS.000":
                    return True
                else:
                    return False
    
    def update_format_with_model(self):
        """change the format in function of the text model."""
        match self.MODEL_TEXT:
            case "YYYY-MM-DD HH:MM:SS":
                self.DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
            case "YYYY-MM-DD HH:MM:SS.000":
                self.DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
            case "HH:MM:SS":
                self.DATE_FORMAT = "%H:%M:%S"
            case "HH:MM:SS.000":
                self.DATE_FORMAT = "%H:%M:%S.%f"
            case _:
                raise Exception("Model not forecast?")
    
    def update_model_with_format(self):
        """change the model in function of the format."""
        match self.DATE_FORMAT:
            case "%Y-%m-%d %H:%M:%S":
                self.MODEL_TEXT = "YYYY-MM-DD HH:MM:SS"
            case "%Y-%m-%d %H:%M:%S.%f":
                self.MODEL_TEXT = "YYYY-MM-DD HH:MM:SS.000"
            case "%H:%M:%S":
                self.MODEL_TEXT = "HH:MM:SS"
            case "%H:%M:%S.%f":
                self.MODEL_TEXT = "HH:MM:SS.000"
            case _:
                raise Exception("date-time format not forecast!")

    def configure(self, **kwargs):
        """Extension of configure to new cases."""
        if 'model' in kwargs:
            _MODEL = kwargs.pop('model')
            _FORMER_FORMAT = self.DATE_FORMAT
            super().configure(model=_MODEL)
            self.update_format_with_model()
            if not self.IS_EMPTY and _FORMER_FORMAT != self.DATE_FORMAT:
                _CONTENT_STR = self.get()
                if _FORMER_FORMAT[-1] == "f":
                    # we need to shorten the content
                    _CONTENT_STR = _CONTENT_STR[:len(self.MODEL_TEXT)]
                else:
                    _CONTENT_STR += '.000'
                self.delete(0,tk.END)
                self.insert(0, _CONTENT_STR)

        elif 'format' in kwargs:
            _FORMAT = kwargs.pop('format')
            _FORMER_FORMAT = self.DATE_FORMAT
            self.DATE_FORMAT = _FORMAT
            self.update_model_with_format()        
            if not self.IS_EMPTY and _FORMER_FORMAT != self.DATE_FORMAT:
                _CONTENT_STR = self.get()
                if _FORMER_FORMAT[-1] == "f":
                    # we need to shorten the content
                    _CONTENT_STR = _CONTENT_STR[:len(self.MODEL_TEXT)]
                else:
                    _CONTENT_STR += '.000'
                self.delete(0,tk.END)
                self.insert(0, _CONTENT_STR)

        if 'err_bg_col' in kwargs:
            self.ERR_BG_COL = kwargs.pop('err_bg_col')
        if 'err_fg_col' in kwargs:
            self.ERR_FG_COL = kwargs.pop('err_fg_col')
        
        super().configure(**kwargs)

    def cget(self, property: str):
        match property:
            case "format":
                return self.DATE_FORMAT
            case "err_bg_col":
                return self.ERR_BG_COL
            case "err_fg_col":
                return self.ERR_FG_COL
            case _:
                return super().cget(property)

    def clear(self):
        super().clear()
        self.ENTRY_ERROR = False
    
    def on_focus_in(self, event):
        if self.IS_EMPTY:
            self.delete(0, tk.END)
            self.configure(foreground=self.FG_COL,
                           background=self.BG_COL)

    def on_focus_out(self, event):
        if not self.get():
            self.insert(0, self.MODEL_TEXT)
            self.configure(foreground=self.MODEL_COLOR,
                           background=self.BG_COL)
            self.IS_EMPTY = True
        else:
            self.IS_EMPTY = False
            self.final_validation(event)

    def key_press_handler(self, event):
        cursor_position = self.index(tk.INSERT)
        if (self.cget("background") == self.ERR_BG_COL):
            self.configure(background=self.BG_COL,
                           foreground=self.FG_COL)
        # check for auto-completion
        if event.keysym == "BackSpace":
            self.delete(cursor_position)
        elif event.keysym == "Delete":
            self.delete(cursor_position, cursor_position + 1)
        elif cursor_position in self.autocompletion_chars:
            char_to_insert = self.autocompletion_chars[cursor_position]
            self.insert(cursor_position, char_to_insert)
            self.icursor(cursor_position + 1)
            return "break"  # Prevent the default character insertion
        elif event.char not in string.digits:
            return "break"

    def move_cursor_left(self, event):
        if (self.cget("background") == self.ERR_BG_COL):
            self.configure(background=self.BG_COL,
                           foreground=self.FG_COL)
        cursor_position = self.index(tk.INSERT)
        if cursor_position > 0:
            self.icursor(cursor_position - 1)

    def move_cursor_right(self, event):
        if (self.cget("background") == self.ERR_BG_COL):
            self.configure(background=self.BG_COL,
                           foreground=self.FG_COL)
        cursor_position = self.index(tk.INSERT)
        if cursor_position < len(self.get()):
            self.icursor(cursor_position + 1)

    def final_validation(self, event):
        '''Check the datetime is valid.'''        
        try:
            _CONTENT_STR = self.get()
            if len(_CONTENT_STR) > 0:
                self.IS_EMPTY = False
            else:
                self.IS_EMPTY = True
                return
            
            if self.DATE_FORMAT[-1] == "f":
                _POS = _CONTENT_STR.find('.')
                _FORMAT =self.DATE_FORMAT[:-3]
                # we don't check what is below the seconds.
                if _POS > 0:
                    _CONTENT_STR = _CONTENT_STR[:_POS]
            else:
                _FORMAT = self.DATE_FORMAT
            _CONTENT_DT = datetime.strptime(_CONTENT_STR, _FORMAT)
            if (_CONTENT_STR != datetime.strftime(_CONTENT_DT, _FORMAT)):
                raise Exception("Incorrect date entered.")
            else:
                self.ENTRY_ERR = False
                self.configure(foreground=self.FG_COLOR,
                               background=self.BG_COLOR)
            return "break"
                  
        except Exception as e:
            print(e)
            self.raise_entry_error()

    def leave_widget(self, event):
        _CONTENT_STR = self.get()
        if _CONTENT_STR == "" or _CONTENT_STR == self.MODEL_TEXT:
            self.IS_EMPTY = True
            return "break"
        else:
            self.IS_EMPTY = False
            self.final_validation(event)
    

if __name__ == "__main__":

    root = tk.Tk()
    root.title("Check Simple Datetime Entry.")

    frame = tk.Frame(root, height=5)
    frame.pack(side=tk.TOP, expand=True)

    datetime_entry = EntryDatetime(frame)
    datetime_entry.pack(side=tk.TOP, padx=50, pady=50)

    # enter a default datetime ---------------------
    datetime_entry.delete(0, tk.END)
    datetime_entry.insert(0, "2010-10-01 09:34:23")
    # datetime_entry.insert(1, "2010-14-32 45:34:23")   # wrong date!
    datetime_entry.configure(foreground="black")
    datetime_entry.IS_EMPTY = False
    # ----------------------------------------------

    frame.configure(width=len(datetime_entry.format) + 52)

    frame2 = tk.Frame(root, height = 5, width=frame.cget("width"))
    frame2.pack(fill=tk.BOTH, expand=True)

    tk.Label(frame2, text="result:", width=6, anchor="w", justify="right").pack(side=tk.LEFT, padx=20, pady=20)
    result = tk.Label(frame2, width=44, anchor="w", justify="left")
    result.pack(side=tk.LEFT, padx=20, pady=30)

    frame_btn = tk.Frame(root)
    frame_btn.pack()

    button_date=tk.Button(frame_btn,text='date', command=lambda: result.configure(text=datetime_entry.datetime))
    button_date.pack(side=tk.LEFT, padx=20, pady=20)
    button_fmt=tk.Button(frame_btn,text='format', command=lambda: result.configure(text=datetime_entry.format))
    button_fmt.pack(side=tk.LEFT, padx=20, pady=20)

    # to prove we retrieve a real datetime object
    button_s=tk.Button(frame_btn,text='seconds in 21st century', 
                       command=lambda: result.configure(text=str((datetime_entry.datetime-datetime(2000,1,1)).total_seconds())))
    button_s.pack(side=tk.LEFT, padx=20, pady=20)

    days_of_the_week=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    button_weekday=tk.Button(frame_btn,text='day of week', 
                             command=lambda: result.configure(text=days_of_the_week[datetime_entry.datetime.weekday()]))
    button_weekday.pack(side=tk.LEFT, padx=20, pady=20)
    
    frame_btn2 = tk.Frame(root)
    frame_btn2.pack()

    # to check configure
    button_conf=tk.Button(frame_btn2,text='change background', 
                          command=lambda: {datetime_entry.configure(background="white", foreground="black") 
                                           if (datetime_entry.cget("background") == "blue") 
                                           else datetime_entry.configure(background="blue", foreground="white")})
    button_conf.pack(side=tk.LEFT, padx=20, pady=20)

    def switch_disabled():
        _STATE = datetime_entry.cget("state")
        if _STATE == "normal":
            datetime_entry.configure(state="disabled")
            button_disabled.configure(text="enable")
        else:
            datetime_entry.configure(state="normal")
            button_disabled.configure(text="disable")

    button_disabled=tk.Button(frame_btn2, text="disabled",
                              command=switch_disabled)
    button_disabled.pack(side=tk.LEFT, padx=20, pady=20)

    def change_format():        
        if (datetime_entry.cget("format") == "%Y-%m-%d %H:%M:%S"):            
            datetime_entry.configure(model="YYYY-MM-DD HH:MM:SS.000",format="%Y-%m-%d %H:%M:%S.%f")
            # datetime_entry.refresh(datetime.strftime(datetime_entry.datetime, datetime_entry.format))
        else:
            datetime_entry.configure(model="YYYY-MM-DD HH:MM:SS", format="%Y-%m-%d %H:%M:%S")
            # datetime_entry.refresh(datetime.strftime(datetime_entry.datetime, datetime_entry.format))
        result.configure(text=datetime_entry.format)


    button_date=tk.Button(frame_btn2,text='change format', command=change_format)
    button_date.pack(side=tk.LEFT, padx=20, pady=20)

    button_close=tk.Button(frame_btn2, text='close', command=lambda: root.destroy())
    button_close.pack(side=tk.RIGHT, padx=20, pady=20)

    root.mainloop()

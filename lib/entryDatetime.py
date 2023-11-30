from tkinter import Tk, ttk, font, DISABLED, NORMAL, END, INSERT
from datetime import datetime
from entryWithModel import EntryWithModel
import string

class EntryDatetime(EntryWithModel):
    """
    Class for an entry dedicated to datetime.
    It will auto-correct entry and propose a model.
    With date property, it recovers a datetime.
    """
    def __init__(self, container, **kwargs):
        
        super().__init__(container, **kwargs)
        
        self.MODEL = kwargs.pop('model', 'YYYY-MM-DD HH:MM:SS')
        self.DATE_FORMAT = kwargs.pop('format','%Y-%m-%d %H:%M:%S')        
        if 'width' not in kwargs:
            self.WIDTH = len(self.MODEL) + 2
        else:
            self.WIDTH = kwargs['width']
        self.configure(style=self.STYLE_MODEL, width=self.WIDTH)
        self.delete(0, END)
        self.insert(0, self.MODEL)

        # Bind a click event to clear the model text
        # self.bind('<FocusIn>', self.on_focus_in)
        # self.bind('<FocusOut>', self.on_focus_out)
        self.bind('<KeyPress>', self.key_press_handler)
        self.bind('<Return>', self.final_validation)
        # self.bind('<Tab>', self.final_validation)
        # self.bind('<Shift-Tab>', self.final_validation)
        self.bind('<Leave>', self.on_leave)
        self.bind('<Left>', self.move_cursor_left)
        self.bind('<Right>', self.move_cursor_right)

        self.autocompletion_chars = {
            4: '-', 7:'-', 10: ' ', 13: ':', 16: ':', 19: ''
        }
        # check if format contain microseconds and keep only milliseconds
        if self.DATE_FORMAT[-1] == 'f':
            self.autocompletion_chars[19] = '.'
            self.autocompletion_chars[23] = ''
    
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
            case '%Y-%m-%d %H:%M:%S':
                if self.MODEL == 'YYYY-MM-DD HH:MM:SS':
                    return True
                else:
                    return False
            case '%Y-%m-%d %H:%M:%S.%f':
                if self.MODEL == 'YYYY-MM-DD HH:MM:SS.000':
                    return True
                else:
                    return False
            case '%H:%M:%S':
                if self.MODEL == 'HH:MM:SS':
                    return True
                else:
                    return False
            case '%H:%M:%S.%f':
                if self.MODEL == 'HH:MM:SS.000':
                    return True
                else:
                    return False
    
    def update_format_with_model(self):
        """change the format in function of the text model."""
        match self.MODEL:
            case 'YYYY-MM-DD HH:MM:SS':
                self.DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
            case 'YYYY-MM-DD HH:MM:SS.000':
                self.DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
            case 'HH:MM:SS':
                self.DATE_FORMAT = '%H:%M:%S'
            case 'HH:MM:SS.000':
                self.DATE_FORMAT = '%H:%M:%S.%f'
            case _:
                raise Exception('Model not forecast?')
    
    def update_model_with_format(self):
        """change the model in function of the format."""
        match self.DATE_FORMAT:
            case '%Y-%m-%d %H:%M:%S':
                self.MODEL = 'YYYY-MM-DD HH:MM:SS'
            case '%Y-%m-%d %H:%M:%S.%f':
                self.MODEL = 'YYYY-MM-DD HH:MM:SS.000'
            case '%H:%M:%S':
                self.MODEL = 'HH:MM:SS'
            case '%H:%M:%S.%f':
                self.MODEL = 'HH:MM:SS.000'
            case _:
                raise Exception('date-time format not forecast!')

    def configure(self, **kwargs):
        """Extension of configure to new cases."""
        if 'model' in kwargs:
            _FORMER_FORMAT = self.DATE_FORMAT
            self.MODEL = kwargs.pop('model')            
            super().configure(model=self.MODEL)
            self.update_format_with_model()
            if not self.IS_EMPTY and _FORMER_FORMAT != self.DATE_FORMAT:
                _CONTENT_STR = self.get()
                if _FORMER_FORMAT[-1] == 'f':
                    # we need to shorten the content
                    _CONTENT_STR = _CONTENT_STR[:len(self.MODEL)]
                else:
                    _CONTENT_STR += '.000'
                self.delete(0, END)
                self.insert(0, _CONTENT_STR)
        
        elif 'format' in kwargs:
            _FORMER_FORMAT = self.DATE_FORMAT
            self.DATE_FORMAT = kwargs.pop('format')                        
            self.update_model_with_format()        
            if not self.IS_EMPTY and _FORMER_FORMAT != self.DATE_FORMAT:
                _CONTENT_STR = self.get()
                if _FORMER_FORMAT[-1] == 'f':
                    # we need to shorten the content
                    _CONTENT_STR = _CONTENT_STR[:len(self.MODEL)]
                else:
                    _CONTENT_STR += '.000'
                self.delete(0, END)
                self.insert(0, _CONTENT_STR)
        else:
            super().configure(**kwargs)

    def cget(self, property: str):
        match property:
            case 'format':
                return self.DATE_FORMAT
            case _:
                return super().cget(property)

    def clear(self):
        super().clear()
        self.ENTRY_ERROR = False
    
    def on_focus_in(self, event):
        if self.IS_EMPTY:
            self.delete(0, END)
            self.configure(style=self.STYLE)

    def on_focus_out(self, event):
        if not self.get():
            self.insert(0, self.MODEL)
            self.configure(style=self.STYLE_MODEL)
            self.IS_EMPTY = True
        else:
            self.IS_EMPTY = False
            self.final_validation(event)

    def key_press_handler(self, event):
        cursor_position = self.index(INSERT)
        if self.ENTRY_ERROR:
            self.configure(style=self.STYLE_ERROR)
        # check for auto-completion
        if event.keysym == 'BackSpace':
            self.delete(cursor_position)
        elif event.keysym == 'Delete':
            self.delete(cursor_position, cursor_position + 1)
        elif cursor_position in self.autocompletion_chars:
            char_to_insert = self.autocompletion_chars[cursor_position]
            self.insert(cursor_position, char_to_insert)
            self.icursor(cursor_position + 1)
            return 'break'  # Prevent the default character insertion
        elif event.char not in string.digits:
            return 'break'

    def move_cursor_left(self, event):
        if self.ENTRY_ERROR:
            self.configure(style=self.STYLE_ERROR)
        cursor_position = self.index(INSERT)
        if cursor_position > 0:
            self.icursor(cursor_position - 1)

    def move_cursor_right(self, event):
        if self.ENTRY_ERROR:
            self.configure(style=self.STYLE_ERROR)    
        cursor_position = self.index(INSERT)
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
            
            if self.DATE_FORMAT[-1] == 'f':
                _POS = _CONTENT_STR.find('.')
                _FORMAT =self.DATE_FORMAT[:-3]
                # we don't check what is below the seconds.
                if _POS > 0:
                    _CONTENT_STR = _CONTENT_STR[:_POS]
            else:
                _FORMAT = self.DATE_FORMAT
            _CONTENT_DT = datetime.strptime(_CONTENT_STR, _FORMAT)
            if (_CONTENT_STR != datetime.strftime(_CONTENT_DT, _FORMAT)):
                raise Exception('Incorrect date entered.')
            else:
                self.ENTRY_ERR = False
                self.configure(style=self.STYLE)
            return 'break'
                  
        except Exception as e:
            print(e)
            self.ENTRY_ERR = True
            self.configure(style=self.STYLE_MODEL)
            self.raise_entry_error()

    def on_leave(self, event=None):
        super().on_leave(event)        
        if not self.IS_EMPTY:
            self.final_validation(event)
    

if __name__ == '__main__':

    root = Tk()
    root.title('Check Simple Datetime Entry.')
    root.geometry('2000x650')
    root.attributes('-topmost', 1)

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
    style.configure('grey.TEntry', foreground='grey', fieldbackground='gray99')
    style.configure('red.TEntry', foreground='yellow', fieldbackground='red')
    style.configure('black.TEntry', foreground='black', fieldbackground='gray99')
    style.configure('blue.TEntry', foreground='blue', fieldbackground='gray85')
    

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    frame = ttk.Frame(root, style='yellow.TFrame')
    frame.grid(row=0, column=0, sticky='nsew')
    # frame.configure(style='red.TFrame')

    # rules for expansion in frame
    frame.grid_columnconfigure(0, weight=0)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_rowconfigure(0, weight=0)
    frame.grid_rowconfigure(1, weight=1)

    datetime_entry = EntryDatetime(frame, style='black.TEntry')
    datetime_entry.grid(sticky='n', padx=50, pady=50)

    # enter a default datetime ---------------------
    datetime_entry.delete(0, END)
    datetime_entry.insert(0, '2010-10-01 09:34:23')
    # datetime_entry.insert(1, '2010-14-32 45:34:23')   # test a wrong date!
    
    # datetime_entry.configure(foreground='black')
    datetime_entry.IS_EMPTY = False
    # ----------------------------------------------

    frame.configure(width=len(datetime_entry.format) + 52)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    frame2 = ttk.Frame(root, height = 5, width=frame.cget('width'))
    frame2.grid(sticky='nesw')
    # rules for expansion in frame
    frame2.grid_columnconfigure(0, weight=0)
    frame2.grid_columnconfigure(1, weight=1)
    frame2.grid_rowconfigure(0, weight=1)

    _label = ttk.Label(frame2, text='result:', width=6, anchor='w', justify='right')
    _label.grid(row=0, column=0, padx=(40,10), pady=20, sticky='e')
    result = ttk.Label(frame2, anchor='w', justify='left')
    result.grid(row=0, column=1, padx=(10,40), pady=20, sticky='ew')

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    frame_btn = ttk.Frame(root)
    frame_btn.grid(sticky='nesw')

    button_date=ttk.Button(frame_btn,text='date', command=lambda: result.configure(text=datetime_entry.datetime))
    button_date.grid(padx=40, pady=20)
    button_fmt=ttk.Button(frame_btn,text='format', command=lambda: result.configure(text=datetime_entry.format))
    button_fmt.grid(padx=40, pady=20)

    # to prove we retrieve a real datetime object
    button_s=ttk.Button(frame_btn,text='seconds in 21st century', 
                        command=lambda: result.configure(text=str((datetime_entry.datetime-datetime(2000,1,1)).total_seconds())))
    button_s.grid(row=0, column=0, padx=40, pady=20)

    def change_format():        
        if (datetime_entry.cget('format') == '%Y-%m-%d %H:%M:%S'):            
            datetime_entry.configure(model='YYYY-MM-DD HH:MM:SS.000', format='%Y-%m-%d %H:%M:%S.%f')
            # datetime_entry.refresh(datetime.strftime(datetime_entry.datetime, datetime_entry.format))
        else:
            datetime_entry.configure(model='YYYY-MM-DD HH:MM:SS', format='%Y-%m-%d %H:%M:%S')
            # datetime_entry.refresh(datetime.strftime(datetime_entry.datetime, datetime_entry.format))
        result.configure(text=datetime_entry.format)

    button_date=ttk.Button(frame_btn,text='change format', command=change_format)
    button_date.grid(row=0, column=1, padx=20, pady=20)


    days_of_the_week=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    button_weekday=ttk.Button(frame_btn,text='day of week', 
                             command=lambda: result.configure(text=days_of_the_week[datetime_entry.datetime.weekday()]))
    button_weekday.grid(row=0, column=2, padx=40, pady=20)

    # to check configure
    button_conf=ttk.Button(frame_btn,text='change style', 
                           command=lambda: {datetime_entry.configure(style='black.TEntry') 
                                           if (datetime_entry.cget('style') == 'blue.TEntry') 
                                           else datetime_entry.configure(style='blue.TEntry')})
    button_conf.grid(row=1, column=0, padx=40, pady=20)

    def switch_disabled():
        STATE = datetime_entry.cget("state")
        if str(STATE) == 'normal':
            datetime_entry.configure(state='disabled')
            button_disabled.configure(text='enable')
        else:
            datetime_entry.configure(state='normal')
            button_disabled.configure(text='disable')

    button_disabled=ttk.Button(frame_btn, text='disabled', command=switch_disabled)
    button_disabled.grid(row=1, column=1, padx=40, pady=20)

    button_close=ttk.Button(frame_btn, text='close', command=lambda: root.destroy())
    button_close.grid(row=1, column=2, padx=40, pady=20)

    root.mainloop()

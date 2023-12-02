from tkinter import Tk, ttk, font, END
from entryWithModel import EntryWithModel
from datetime import timedelta
import re


def strptimedelta(time_delta_str: str) -> timedelta:
    """Parse a string into a timedelta."""
    pu = re.compile(r'[hrminsec]+')
    pn = re.compile(r'\d+\.?\d*')
    units = pu.findall(time_delta_str)
    numbers = pn.findall(time_delta_str)

    hours, minutes, seconds = 0, 0, 0
    if len(numbers) >0 and len(numbers) == len(units):
        for number, unit in zip(numbers, units):
            match unit[0]:
                case 'h':
                    hours = float(number)
                case 'm':
                    minutes = float(number)
                case 's':
                    seconds = float(number)
                case _:
                    raise Exception('time delta not recognized')
        return timedelta(hours=hours, minutes=minutes, seconds=seconds)
    else:
        return None  # No match found

def strftimedelta(time_delta: timedelta) -> str:
    """Format a time delta into a string."""
    result = ''
    _TOT_SEC = time_delta.total_seconds()
    if _TOT_SEC >= 3600:
        _HOURS = int(_TOT_SEC // 3600)
        result += f'{_HOURS}h '
        _TOT_SEC -= _HOURS * 3600
    if _TOT_SEC >= 60:
        _MINUTES = int(_TOT_SEC // 60)
        result += f'{_MINUTES}min '
        _TOT_SEC -= _MINUTES * 60
    if _TOT_SEC > 0:
        if _TOT_SEC == int(_TOT_SEC):
            result += f'{int(_TOT_SEC)}s'
        else:
            result += f'{round(_TOT_SEC, 3)}s'
    result = result.rstrip()
    return result
    

class EntryTimedelta(EntryWithModel):
        
    @property
    def timedelta(self):
        return strptimedelta(self.get())


if __name__ == '__main__':
    
    root = Tk()
    root.geometry('1200x500')
    root.attributes('-topmost', 1)  # keep window on top, while checking the code
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=0)
    
    style = ttk.Style()
    style.configure('button.TFrame', background='lightskyblue4')
    style.configure('black.TEntry', fieldbackground='gray99', foreground='black', padding=(50,1,50,1))
    style.configure('gray.TEntry', fieldbackground='gray99', foreground='gray60', padding=(50,1,50,1))
    style.configure('red.TEntry', fieldbackground='yellow', foreground='red', padding=(50,1,50,1))

    # controlling the size of the default font
    default_font = font.nametofont('TkDefaultFont')
    default_font.configure(size=18)
    root.option_add('*Font', default_font)

    frame = ttk.Frame(root)
    frame.grid(row=0, column=0, sticky='nsew')
    frame.rowconfigure(0, weight=0)
    frame.columnconfigure(0, weight=0)
    frame.columnconfigure(1, weight=1)


    def test_values_and_units():
        """First test"""        
        root.title("test values and units.")

        entry_values = EntryWithModel(frame, model='00h 00min 00.0s', width=20,
                                      style='black.TEntry', 
                                      style_model='gray.TEntry',
                                      style_error='red.TEntry')
        entry_values.grid(row=0, column=0, columnspan=2, padx=40, pady=20, sticky='we')
        
        ttk.Label(frame, text='total in seconds:', justify='left', anchor='w').grid(row=1, column=0, padx=(20,10), pady=20)
        total_s = ttk.Label(frame)
        total_s.grid(row=1, column=1, padx=(10,20), pady=20,sticky='we')

        def display_seconds():
            """Detailed step to help debug."""
            nonlocal entry_values
            _timedelta_str = entry_values.get()
            _timedelta = strptimedelta(_timedelta_str)
            _seconds = _timedelta.total_seconds()
            total_s.configure(text = str(_seconds))

        frame_btn = ttk.Frame(root, style='button.TFrame')
        frame_btn.grid(row=1, column=0, sticky='ew')
        frame_btn.rowconfigure(0, weight=1)
        frame_btn.columnconfigure(0, weight=1)
        frame_btn.columnconfigure(1, weight=1)

        ttk.Button(frame_btn, text='analyse', 
                   command=display_seconds).grid(row=0, column=0, padx=40, pady=40)
        ttk.Button(frame_btn, text='close', 
                   command=lambda: root.destroy()).grid(row=0, column=1, padx=40, pady=40)
        
        root.mainloop()

    def test_EntryTimedelta():
        """Second test"""                
        root.title("test EntryTimedelta.")

        entryTimedelta = EntryTimedelta(frame, model='00h 00min 00.0s', width=20,
                                        style='black.TEntry', 
                                        style_model='gray.TEntry',
                                        style_error='red.TEntry')
        entryTimedelta.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky='we')

        ttk.Label(frame, text='result:', justify='left', anchor='e').grid(row=1, column=0, padx=(20,10), pady=20)
        result = ttk.Label(frame, anchor='w', justify='left')
        result.grid(row=1, column=1, padx=(10,20), pady=20)

        frame_btn = ttk.Frame(root, style='button.TFrame')
        frame_btn.grid(row=1, column=0, sticky='ew')
        frame_btn.rowconfigure(0, weight=0)
        frame_btn.columnconfigure(0, weight=1)
        frame_btn.columnconfigure(1, weight=1)

        btn_td = ttk.Button(frame_btn, text='test timedelta', 
                            command=lambda: result.configure(text=entryTimedelta.timedelta))
        btn_td.grid(row=0, column=0, padx=20, pady=20)
        btn_ok = ttk.Button(frame_btn, text='close', command=lambda: root.destroy())
        btn_ok.grid(row=0, column=1, padx=20, pady=20)
        root.mainloop()

    
    def default_case():
        print('Case not defined...')

    # the possible test cases
    tests_cases = {
        'test extraction of values and units': test_values_and_units,
        'test entry of a time delta' : test_EntryTimedelta,
    }

    # test_to_do = "test extraction of values and units"
    test_to_do = 'test entry of a time delta'

    tests_cases.get(test_to_do, default_case)()
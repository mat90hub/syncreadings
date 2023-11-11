import tkinter as tk
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
                    raise Exception("time delta not recognized")
        return timedelta(hours=hours, minutes=minutes, seconds=seconds)
    else:
        return None  # No match found

def strftimedelta(time_delta: timedelta) -> str:
    '''Format a time delta into a string.'''
    result = ""
    _TOT_SEC = time_delta.total_seconds()
    if _TOT_SEC >= 3600:
        _HOURS = int(_TOT_SEC // 3600)
        result += f"{_HOURS}h "
        _TOT_SEC -= _HOURS * 3600
    if _TOT_SEC >= 60:
        _MINUTES = int(_TOT_SEC // 60)
        result += f"{_MINUTES}min "
        _TOT_SEC -= _MINUTES * 60
    if _TOT_SEC > 0:
        if _TOT_SEC == int(_TOT_SEC):
            result += f"{int(_TOT_SEC)}s"
        else:
            result += f"{round(_TOT_SEC, 3)}s"
    result = result.rstrip()
    return result
    

class EntryTimedelta(EntryWithModel):
    def __init__(self, master, **kwargs):

        super().__init__(master, **kwargs)

        if 'model' in kwargs:
            self.MODEL_TEXT = kwargs.pop('model')
        else:
            self.MODEL_TEXT = "00h 00min 00.000s"
        if 'model_color' in kwargs:
            self.MODEL_COLOR = kwargs.pop('model_color')
        else:
            self.MODEL_COLOR = "grey"
        
        if 'width' not in kwargs:
            self.WIDTH = len(self.MODEL_TEXT) + 2
        else:
            self.WIDTH = kwargs['width']
        
        super().configure(foreground=self.MODEL_COLOR)
        super().delete(0, tk.END)
        super().insert(0, self.MODEL_TEXT)

    @property
    def timedelta(self):
        return strptimedelta(self.get())


if __name__ == "__main__":
    
    def test_values_and_units():
        root = tk.Tk()
        root.title("Test value and unit.")
        frame = tk.Frame(root,width=26)
        frame.pack(fill=tk.BOTH, expand=True)

        entry_values = EntryWithModel(frame, 
                                      model="00h 00min 00.0s", 
                                      width=20)
        entry_values.pack(side=tk.LEFT, padx=40, pady=20)

        frame2 = tk.Frame(root, width = 26)
        frame2.pack(expand=True, fill=tk.BOTH)

        tk.Label(frame2, 
                 text='total in seconds:', 
                 width=18).pack(side=tk.LEFT, padx=10, pady=20)
        total_s = tk.Label(frame2, width=20)
        total_s.pack(side=tk.LEFT, padx=20, pady=20)

        def display_seconds():
            """Detailed step to help debug."""
            nonlocal entry_values
            _timedelta_str = entry_values.get()
            _timedelta = strptimedelta(_timedelta_str)
            _seconds = _timedelta.total_seconds()
            total_s.configure(text = str(_seconds))

        frame_btn = tk.Frame(root)
        frame_btn.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        tk.Button(frame_btn, 
                  text='analyse', 
                  command=display_seconds).pack(side=tk.LEFT, padx=40, pady=40)
        tk.Button(frame_btn, 
                  text='close', 
                  command=lambda: root.destroy()).pack(side=tk.RIGHT, padx=40, pady=40)
        root.mainloop()

    def test_EntryTimedelta():
        root = tk.Tk()
        root.title("Test entry of a time delta.")
        frame = tk.Frame(root,width=25, height=6)
        frame.pack()

        entryTimedelta = EntryTimedelta(frame)
        entryTimedelta.pack(side=tk.LEFT, padx=20, pady=20)

        frame2 = tk.Frame(root, width=frame.cget("width"))
        frame2.pack(expand=True, fill=tk.BOTH)

        tk.Label(frame2, text='result:', width=18, anchor="e").pack(side=tk.LEFT, padx=10, pady=20)
        result = tk.Label(frame2, width=entryTimedelta.cget("width"), anchor="w", justify="left")
        result.pack(side=tk.LEFT, padx=10, pady=20)

        frm_btn = tk.Frame(root, width=frame.cget("width"))
        frm_btn.pack(side=tk.BOTTOM)

        btn_td = tk.Button(frm_btn, text='test timedelta', 
                           command=lambda: result.configure(text=entryTimedelta.timedelta))
        btn_td.pack(side=tk.LEFT, padx=20, pady=20)
        btn_ok = tk.Button(frm_btn, text='close', command=lambda: root.destroy())
        btn_ok.pack(side=tk.RIGHT, padx=20, pady=20)
        root.mainloop()

    
    def default_case():
        print("Case not defined...")

    # the possible test cases
    tests_cases = {
        "test extraction of values and units": test_values_and_units,
        "test entry of a time delta" : test_EntryTimedelta,
    }

    # test_to_do = "test extraction of values and units"
    test_to_do = "test entry of a time delta"

    tests_cases.get(test_to_do, default_case)()
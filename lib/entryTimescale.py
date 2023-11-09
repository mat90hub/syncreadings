import tkinter as tk
from tkinter import N, S, W, E
from datetime import datetime, timedelta
from entryDatetime import EntryDatetime
from entryTimedelta import EntryTimedelta, strptimedelta, strftimedelta


class EntryTimeScale(tk.Frame):
    
    def __init__(self, container, 
                 duration="1h",
                 step="1min",
                 **kwargs):
        super().__init__(container, **kwargs)
        self.start_lbl = tk.LabelFrame(container,text="start", padx=5, pady=5)
        self.start_lbl.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.start_entry = EntryDatetime(self.start_lbl)
        self.start_entry.grid()
        self.start_entry.IS_EMPTY = True

        self.end_lbl = tk.LabelFrame(container, text="end", padx=5, pady=5)
        self.end_lbl.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.end_entry = EntryDatetime(self.end_lbl)
        self.end_entry.grid()
        self.end_entry.IS_EMPTY = True
        
        self.DURATION = strptimedelta(duration)
        self.STEP = strptimedelta(step)
        
        self.step_lbl = tk.LabelFrame(container, text="step", padx=5, pady=5)
        self.step_lbl.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        self.step_entry = EntryTimedelta(self.step_lbl, model=step, width=8)
        self.step_entry.grid()

        self.start_entry.bind("<FocusOut>", self.prepare_end)
        
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

    def prepare_end(self, event):
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
            _STATE = kwargs.pop('state')    
            self.start_entry.configure(state=_STATE)
            self.end_entry.configure(state=_STATE)
            self.step_entry.configure(state=_STATE)


if __name__ == "__main__":
    
    root = tk.Tk()
    root.title("Test entry of a time scale.")
    frame = tk.Frame(root,width=15)
    frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    entryTimescale = EntryTimeScale(frame)
    entryTimescale.grid(row=0,column=0)
    
    # Enter a date ---------------------------------
    entryTimescale.start_entry.enter("2022-02-01 09:00:00")
    entryTimescale.end_entry.enter("2022-02-01 11:00:00")
    entryTimescale.step_entry.enter("1min")
    # ----------------------------------------------

    frame2 = tk.Frame(root, height = 5, width=26)
    frame2.grid(row=1,column=0, sticky="nwse", padx=20, pady=0)

    tk.Label(frame2, text='result:', width=6, anchor="w").grid(row=0, column=0)
    result = tk.Label(frame2, width=46, anchor="w", justify="left", bg='white')
    result.grid(row=0,column=1, sticky="ne", padx=20, pady=20)

    frame_btn = tk.Frame(root)
    frame_btn.grid(row=2, column=0, sticky="nesw", padx=20, pady=20)
    button_nb = tk.Button(frame_btn, text='ticks number', height=2,
                          command=lambda: result.configure(text=entryTimescale.ticks_number))
    button_nb.grid(row=0, column=0, padx=20, pady=50, sticky='nesw')

    # tk.Label(frame_btn, width=6).grid(row=0, column=1, sticky='nesw')

    button_lst = tk.Button(frame_btn, text='ticks list', height=2, 
                           command=lambda: result.configure(text=entryTimescale.ticks_list))
    button_lst.grid(row=0, column=2, padx=20, pady=50, sticky='nsw')

    def switch_disabled():
        _STATE = entryTimescale.cget("state")
        if _STATE == "normal":
            entryTimescale.configure(state="disabled")
            button_disabled.configure(text="enable")
        else:
            entryTimescale.configure(state="normal")
            button_disabled.configure(text="disable")

    button_disabled=tk.Button(frame_btn, text="disabled",
                              command=switch_disabled)
    button_disabled.grid(row=0, column=3, padx=20, pady=50, sticky="nsw")

    # tk.Label(frame_btn, width=9).grid(row=0, column=3, sticky='nesw')

    button_close = tk.Button(frame_btn, text='close', height=2, width=7,
                             command=lambda: root.destroy())
    button_close.grid(row=0, column=4, padx=20, pady=50, sticky='w')

    root.resizable(False, False)
    root.mainloop()

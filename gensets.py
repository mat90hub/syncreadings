from tkinter import Tk, ttk
from lib.entryGenerator import EntryGenerator
from lib.buttonFrame import ButtonFrame

class Gensets(ttk.Frame):

    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)
        
    

if __name__ == "__main__":

    root = Tk()
    root.title("Generate the sets for testing.")
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=0)
    root.columnconfigure(0, weight=1)

    frame = ttk.Frame(root, width=2000, height=1500)
    frame.grid(row=0, column=0,padx=20, pady=20, sticky='nesw')
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    

    root.mainloop()



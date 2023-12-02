from tkinter import Tk, ttk

class ButtonFrame():
    ROWS = []
    event_handler = None

    def __init__(self, container, **kwargs):
        self.ROW = kwargs.pop('row', 0)
        self.PLUS_STYLE = kwargs.pop('plus_style', 'TButton')
        self.MINUS_STYLE = kwargs.pop('minus_style', 'TButton')
        self.FRAME1_STYLE = kwargs.pop('frame1_style', 'TFrame')
        self.FRAME2_STYLE = kwargs.pop('frame2_style', 'TFrame')
        self.CONTAINER = container        
        self.BUTTON = ttk.Button(container, text='+', style=self.PLUS_STYLE,
                                 command=self.toggle)
        self.BUTTON.grid(row=self.ROW, column=0, sticky='n', padx=(20,10), pady=10)
        self.FRAME = ttk.Frame(container, padding=10, style=self.FRAME1_STYLE)
        self.FRAME.grid(row=self.ROW, column=1, sticky='news', padx=(10,20), pady=10)
        self.update_color()
        self.FRAME.grid_remove() # initially hidden 

        self.CONTAINER.columnconfigure(0, weight=0)
        self.CONTAINER.columnconfigure(1, weight=1)
        self.CONTAINER.rowconfigure(self.ROW, weight=1)
        
        # self.event_handler = None
        ButtonFrame.ROWS.append(self)        

    def destroy(self):
        """Destroy the couple Button + Frame"""
        self.BUTTON.destroy()
        self.FRAME.destroy()

    def update_color(self):
        """Update the color of the FRAME"""
        if self.ROW % 2 == 0:
            self.FRAME.configure(style=self.FRAME2_STYLE)
        else:
            self.FRAME.configure(style=self.FRAME1_STYLE)

    def update_position(self):
        """After a ROW suppression, update all remaining ones."""
        self.BUTTON.grid(row=self.ROW, column=0)
        self.FRAME.grid(row=self.ROW, column=1)
        self.update_color()
        if self.ROW == len(ButtonFrame.ROWS) - 1:
            self.FRAME.grid_remove()

    def destroy_empty_row(self):
        self.destroy()
        for instance in ButtonFrame.ROWS:
            if instance.ROW > self.ROW:
                instance.ROW -= 1
                instance.update_position()

    def clear(self):
        """Destroy all widget contained in the FRAME"""
        for widget in self.FRAME.winfo_children():
            widget.destroy()

    def toggle(self):
        if self.FRAME.winfo_ismapped():
            # FRAME was visible, we remove the line            
            if ButtonFrame.event_handler is not None:
                self.CONTAINER.event_generate('<<removeLine>>', when='tail')
                ButtonFrame.event_handler('Line removed')            
            ButtonFrame.ROWS.remove(self)
            self.destroy_empty_row()
        else:
            # FRAME not visible, we toggle visibility and add a new ButtonFrame
            if ButtonFrame.event_handler is not None:
                self.CONTAINER.event_generate('<<addLine>>', when='tail')
                ButtonFrame.event_handler('Line added')
            self.FRAME.grid() # make the frame visible
            self.BUTTON.configure(text='-', style=self.MINUS_STYLE)
            ButtonFrame(container=self.CONTAINER, row=self.ROW + 1, 
                        plus_style=self.PLUS_STYLE,
                        minus_style=self.MINUS_STYLE,
                        frame1_style=self.FRAME1_STYLE,
                        frame2_style=self.FRAME2_STYLE)

    def set_event_handler(self, handler):
        ButtonFrame.event_handler = handler


if __name__ == "__main__":

    root = Tk()
    root.title("test ButtonPlus.")
    root.geometry("2000x500")

    style = ttk.Style()
    style.configure('odd.TFrame', background='burlywood1')
    style.configure('pair.TFrame', background='chocolate1')
    style.configure('blue.TFrame', background='blue')
    style.configure('plus.TButton', width=3,
                    background='chartreuse1',
                    highlightcolor=[('focus', 'active', 'aqua')],
                    foreground='chartreuse4',
                    relief=[('pressed', 'groove'),
                            ('!pressed', 'ridge')],
                    font=('Helvetica', 18, 'bold'))
    style.configure('minus.TButton', width=3,
                    background='chocolate1',
                    foreground='chocolate4',
                    relief=[('pressed', 'groove'),
                            ('!pressed', 'ridge')],
                    font=('Helvetica', 18, 'bold'))

    frame = ttk.Frame(root)
    frame.grid(row=0, column=0, padx=10, pady=10, sticky='nesw')
    frame.grid_propagate(False)   # prevent the frame to resize to its content

    button = ButtonFrame(frame, 
                         plus_style='plus.TButton',
                         minus_style='minus.TButton',
                         frame1_style='odd.TFrame',
                         frame2_style='pair.TFrame')
    
    status_bar = ttk.Frame(root, height=20)
    status_bar.grid(row=1, column=0, sticky='nesw')
    status_lbl = ttk.Label(status_bar, text='status: ')
    status_lbl.grid(row=0, column=0, sticky='new', padx=10, pady=10)

    def status_update(event):
        if event == 'Line added':
            status_lbl.configure(text='status: Line added')
        elif event == 'Line removed':
            status_lbl.configure(text='status: Line removed')
        else:
            status_lbl.configure(text='status: ')

    button.set_event_handler(status_update)

    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=0)
    root.grid_columnconfigure(0, weight=1)

    root.mainloop()
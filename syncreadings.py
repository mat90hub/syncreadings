#!/usr/bin/env python3

import os
from tkinter import Tk, font, ttk, Menu, scrolledtext, WORD, DISABLED, NORMAL, END
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox

from lib.setsManagement import read_measures, get_default_choices
from lib.setsManagement import synchronized_sets, report_on_sets
import pandas as pd

from lib.my_dialogs import text_message, about_window, user_manual
from lib.my_dialogs import display_source_plot, display_table


class Application(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.version = '0.1'
        self.title(f'data reformating, v.{self.version}')
        self.settings = get_default_choices()
        self.data_in = {}
        self.data_out = pd.DataFrame()
        self.input_file = ''
        self.adapt_to_screen_size()
        self.create_menu_bar()
        # self.bind("<Configure>", self.adapt_to_screen_size())
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame = ttk.Frame(self)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid(row=0, column=0, sticky='nswe')
        # self.textbox = tk.Text(self.frame, state=tk.DISABLED);
        self.textbox = scrolledtext.ScrolledText(
            self.frame, wrap=WORD, state=DISABLED)
        self.textbox.grid(row=0, column=0, sticky='nswe')

        # add a footer to give general information
        self.footer = ttk.Frame(self, height=20)
        self.footer.grid_columnconfigure(0, weight=1)
        self.footer.grid_rowconfigure(0, weight=1)
        self.footer.grid(row=1, column=0, sticky='nswe')

        self.footer_lbl = ttk.Label(self.footer, text='input file to be loaded...')
        self.footer_lbl.grid(sticky='w', padx=20)

    def adapt_to_screen_size(self):
        """Define font size to adapt to the screen."""
        self.geometry(
            f'{int(self.winfo_screenwidth()*0.3)}x{int(self.winfo_screenheight()*0.2)}'
        )
        # self.winfo_screenwidth() // 3500
        # adapt the font
        self.cmd_font = font.Font(
            family='Helvetica',
            size=12
        )
        self.menu_font = font.Font(
            family='Helvetica',
            size=14,
            weight='bold'
        )

    def create_menu_bar(self):

        menu_bar = Menu(self)

        menu_file = Menu(menu_bar, tearoff=0)
        menu_file.add_command(label='Load File',
                              underline=0,
                              accelerator='CTRL+O',
                              font=self.cmd_font,
                              command=self.load_file)
        menu_file.add_command(label='Close File',
                              underline=0,
                              accelerator='CTRL+C',
                              font=self.cmd_font,
                              command=self.close_file)
        menu_file.add_separator()
        menu_file.add_command(label='Exit',
                              underline=2,
                              accelerator='CTRL+X',
                              font=self.cmd_font,
                              command=lambda: self.destroy())
        menu_bar.add_cascade(label=' Input File ',
                             font=self.menu_font,
                             menu=menu_file)

        self.bind_all('<Control-o>', lambda _: self.load_file())
        self.bind_all('<Control-c>', lambda _: self.close_file())
        self.bind_all('<Control-x>', lambda _: self.destroy())

        menu_sets = Menu(menu_bar, tearoff=0)
        menu_sets.add_command(label='Sets analysis',
                              underline=0,
                              accelerator='CTRL+A',
                              font=self.cmd_font,
                              command=self.sets_analysis)
        menu_sets.add_command(label='Format into table',
                              underline=0,
                              accelerator='CTRL+F',
                              font=self.cmd_font,
                              command=self.format_datasets)
        menu_sets.add_separator()
        menu_sets.add_command(label='Export to CSV',
                              underline=0,
                              accelerator='CTRL+S',
                              font=self.cmd_font,
                              command=self.export_to_csv)
        menu_sets.add_command(label='Export to XLSX',
                              underline=0,
                              accelerator='CTRL+L',
                              font=self.cmd_font,
                              command=self.export_to_xlsx)
        menu_bar.add_cascade(label=' Data Table ',
                             font=self.menu_font,
                             menu=menu_sets)

        self.bind_all('<Control-a>', lambda _: self.sets_analysis())
        self.bind_all('<Control-f>', lambda _: self.format_datasets())
        self.bind_all('<Control-s>', lambda _: self.export_to_csv())
        self.bind_all('<Control-l>', lambda _: self.export_to_xlsx())

        menu_plot = Menu(menu_bar, tearoff=0)
        menu_plot.add_command(label='Plot source measures',
                              font=self.cmd_font,
                              command=self.plot_source)
        menu_plot.add_command(label='Plot resulting table',
                              font=self.cmd_font,
                              command=self.plot_table)

        menu_bar.add_cascade(label=' Graph Plot ',
                             font=self.menu_font,
                             menu=menu_plot)

        menu_help = Menu(menu_bar, tearoff=0)
        menu_help.add_command(label='About',
                              font=self.cmd_font,
                              command=self.about_window)
        menu_help.add_command(label='User manual',
                              font=self.cmd_font,
                              command=self.user_manual)
        menu_bar.add_cascade(label='Help',
                             font=self.menu_font,
                             menu=menu_help)

        self.config(menu=menu_bar)

    def load_file(self):
        self.input_file = askopenfilename(title='Select the file to open',
                                          filetypes=[('CSV', '.csv'),
                                                     ('TXT', '.txt'),
                                                     ('All files', '.*')])
        with open(self.input_file, 'r') as _FILE:
            content = _FILE.read()

        self.footer_lbl.configure(
            text=f"file '{os.path.basename(self.input_file)}' loaded"
        )
        self.textbox.config(state=NORMAL)
        self.textbox.delete('1.0', END)
        self.textbox.insert(END, content)
        self.textbox.config(state=DISABLED)

    def sets_analysis(self):
        if not self.input_file:
            messagebox.showwarning(
                        title='No input file loaded',
                        message='Load first an input file.')
            return
        elif not self.data_in:
            self.data_in = read_measures(self.input_file)
        details = report_on_sets(self.data_in)
        text_message(self, text=details, title='Data Sets Details',
                     width=60, height=12)

    def format_datasets(self):
        if not self.input_file:
            messagebox.showwarning(
                        title='No input file loaded',
                        message='Load first an input file.')
            return
        elif not self.data_in:
            self.data_in = read_measures(self.input_file)
        self.data_out = synchronized_sets(self.data_in, self.settings)
        self.textbox.config(state=NORMAL)
        self.textbox.delete('1.0', END)
        self.textbox.insert(END, self.data_out.to_string(index=True))
        self.textbox.config(state=DISABLED)
        self.footer_lbl.configure(
            text=f"File '{os.path.basename(self.input_file)}' loaded, data tabulated")

    def export_to_csv(self):
        if not self.input_file:
            messagebox.showwarning(
                title='No input file loaded', 
                message='Load first an input file.')
        elif self.data_out.empty:
            messagebox.showwarning(
                title='Data sets no re-formatted', 
                message='Re-format first the sets of data into a table.')
        else:
            _FILE = asksaveasfilename(
                title='Enter file name for saving',
                defaultextension='*.csv',
                filetypes=[('CSV', '*.csv')])
            self.data_out.to_csv(_FILE)
            self.footer_lbl.configure(
                text=f"File '{os.path.basename(_FILE)}' saved")

    def export_to_xlsx(self):
        if not self.input_file:
            messagebox.showwarning(
                title='No input file loaded',
                message='Load first an input file.')
        elif self.data_out.empty:
            messagebox.showwarning(
                title='Data sets no re-formatted',
                message='Re-format first the sets of data into a table.')
        else:
            _FILE = asksaveasfilename(
                        title='Enter file name for saving',
                        defaultextension='*.xlsx',
                        filetypes=[('XLSX', '*.xlsx')])
            self.data_out.to_excel(_FILE)
            self.footer_lbl.configure(
                text=f"File '{os.path.basename(_FILE)}' saved")

    def close_file(self):
        """Closing the file means emptying memories of the input."""
        self.footer_lbl.configure(text='input file to be loaded...')
        self.data_in = {}
        self.data_out = pd.DataFrame()
        self.sets_char = {}
        self.input_file = ''
        self.textbox.config(state=NORMAL)
        self.textbox.delete('1.0', END)
        self.textbox.config(state=DISABLED)

    def plot_source(self):
        """Plot on an independent window the graph of the source measures"""
        if not self.input_file:
            messagebox.showwarning(
                        title='No input file loaded',
                        message='Load first an input file.')
        elif not self.data_in:
            self.data_in = read_measures(self.input_file)
        display_source_plot(self, self.data_in, title='Source measures.')

    def plot_table(self):
        """Plot the synchronized table."""
        if not self.input_file:
            messagebox.showwarning(
                        title='No input file loaded',
                        message='Load first an input file.')
        elif self.data_out.empty:
            messagebox.showwarning(
                title='Data sets no re-formatted',
                message='Re-format first the sets of data into a table.')
        else:
            display_table(self, self.data_out, title='Synchronized measures.')
    
    def plot_compare(self):
        """Plot the source measures with their synchronized versions."""
        if not self.input_file:
            messagebox.showwarning(
                title='No input file loaded',
                message='Load first an input file.')
        elif self.data_out.empty:
            messagebox.showwarning(
                title='Data sets no re-formatted',
                message='Re-format first the sets of data into a table.')
        else:
            display_table(self, self.data_out, title='Synchronized measures.')

    def about_window(self):
        """Window giving general information on the application."""
        text = 'Application for reformating data sets.\n'
        text += 'author: Mathieu Pouit\n'
        text += 'license: MIT\n'
        about_window(self, text=text, 
                     title='About', width=40, height=4,
                     background='lightgrey')

    def user_manual(self):
        """Give user instructions."""
        user_manual(self, title='user instructions',
                    html_file='./lib/html/help.html')

if __name__ == "__main__":
    application = Application()
    application.mainloop()

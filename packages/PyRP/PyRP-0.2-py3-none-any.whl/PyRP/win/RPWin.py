#! python
'''
GUI Application that runs the PyRP module.
'''

from os.path import dirname, join, normpath, realpath, splitext
from os import startfile
from threading import Thread
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror

# Try to import openpyxl
_output_modes = ['csv']
try:
    import openpyxl as xlsx
except ImportError:
    pass
else:
    _output_modes.append('xlsx')

if not __package__:
    # For debugging
    import sys, os
    sys.path.insert(0, join(os.getcwd(), '..'))
    import RP
    from RPLog import RPLog
    from RPWidgets import MethodWidget, OptionsDialog
    from tk.acc import Accelerator
    if 'xlsx' in _output_modes:
        import RPxlsx
else:
    from .. import RP
    from .RPLog import RPLog
    from .RPWidgets import MethodWidget, OptionsDialog
    from ..tk.acc import Accelerator
    if 'xlsx' in _output_modes:
        from .. import RPxlsx


class RPWin(tk.Tk):
    '''
    Main Dialog class that runs the PyRP tie-breaking module.
    '''
    def __init__(self):
        super().__init__()
        self.withdraw()
        self.title('Recursive Performance tie-breaks')
        self.resizable(False, False)
        self._icon_file = normpath(join(
            dirname(realpath(__file__)), 'rp.ico'))
        self.iconbitmap(self._icon_file)
        self._acc = Accelerator(self)
        self._set_variables()
        self._set_styles()
        self._build_widgets()
        self.deiconify()
        self.bind('<Return>', self.on_ok)
        self.bind('<Escape>', self.on_cancel)
        self.update_idletasks()
        self.event_generate('<Alt-f>')

    def _set_variables(self):
        self._output_modes = _output_modes
        # Variables to control widgets
        self.file_name = tk.StringVar()
        self.sort = tk.BooleanVar()
        self.default_elo = tk.IntVar()
        self.headings = tk.BooleanVar()
        # Initial values
        log = RPLog.load()
        for key, value in log['options'].items():
            getattr(self, key).set(value)
        self._algorithm = dict(log['algorithm'])

    @staticmethod
    def _set_styles():
        styles = ttk.Style()
        styles.configure('TButton', width=18)
        styles.configure('Small.TButton', width=15)
        styles.configure('TLabelframe', padding=5)
        
    def _build_widgets(self):
        # Columns
        grid_options = {'row': 0, 'sticky': 'nsew'}
        data_frame = ttk.Frame(master=self, padding=10)
        data_frame.grid(column=0, **grid_options)
        buttons_frame = ttk.Frame(master=self, padding=(10, 18, 10, 10))
        buttons_frame.grid(column=1, **grid_options)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Main blocks
        grid_options = {'column': 0, 'sticky': 'ew'}
        file_frame = ttk.LabelFrame(
            master=data_frame, text='Input file')
        file_frame.grid(row=0, **grid_options)
        methods_frame = ttk.LabelFrame(
            master=data_frame, text='Choose tie-break methods')
        methods_frame.grid(row=1, pady=10, **grid_options)
        others_frame = ttk.LabelFrame(
            master=data_frame, text='Other options')
        others_frame.grid(row=2, **grid_options)
        data_frame.columnconfigure(0, weight=1)

        # Input file
        input_label = ttk.Label(master=file_frame, text='File: ', underline=0)
        input_label.grid(row=0, column=0, sticky='w')
        self._file_entry = ttk.Entry(
            master=file_frame, textvariable=self.file_name, width=62)
        self._file_entry.grid(row=0, column=1, sticky='we', padx=3)
        self._acc.add('<Alt-f>', widget=self._file_entry)
        open_button = ttk.Button(
            master=file_frame, text='Choose...', style='Small.TButton',
            command=self.on_choose, underline=0)
        open_button.grid(row=0, column=2, sticky='e', padx=(10, 5))
        self._acc.add('<Alt-c>', widget=open_button)
        file_frame.columnconfigure(1, weight=1)

        # Methods
        self._methods_chooser = ttk.Frame(master=methods_frame)
        self._methods_chooser.grid(row=0, column=0, sticky='new')
        self._build_method_widgets()

        # Add and remove methods
        separator = ttk.Separator(master=methods_frame, orient=tk.HORIZONTAL)
        separator.grid(row=1, column=0, sticky='ew', pady=10)
        methods_buttons = ttk.Frame(master=methods_frame)
        methods_buttons.grid(row=2, column=0, sticky='ws')
        self._add_button = ttk.Button(
            master=methods_buttons, text='Add method', style='Small.TButton',
            command=self.on_add_method, underline=0)
        self._add_button.grid(row=0, column=0)
        self._acc.add('<Alt-a>', widget=self._add_button)
        self._remove_button = ttk.Button(
            master=methods_buttons, text='Remove method', style='Small.TButton',
            command=self.on_remove_method, underline=0)
        self._remove_button.grid(row=0, column=1, sticky='ws', padx=10)
        self._acc.add('<Alt-r>', widget=self._remove_button)
        self._add_remove_buttons()
        methods_frame.columnconfigure(0, weight=1)

        # Other options
        elo_label = ttk.Label(
            master=others_frame, text='Elo for unrated players: ', underline=0)
        elo_label.grid(row=0, column=0, sticky='w')
        self._elo_spinbox = tk.Spinbox(
            master=others_frame, textvariable=self.default_elo,
            from_=1000, to=3000, increment=50, width=8,
            state='readonly', readonlybackground='white')
        self._elo_spinbox.grid(row=0, column=1, sticky='w', padx=5)
        self._acc.add('<Alt-e>', widget=self._elo_spinbox)
        headings_button = ttk.Checkbutton(
            master=others_frame, text='Include short headings',
            variable=self.headings, underline=14)
        self._acc.add('<Alt-h>', widget=headings_button)
        headings_button.grid(
            row=0, column=3, sticky='e', padx=10)
        others_frame.columnconfigure(2, weight=1)

        # Buttons
        ok_button = ttk.Button(
            master=buttons_frame, text='Ok', default='active',
            command=self.on_ok)
        ok_button.grid(row=0, column=0, sticky='new')
        cancel_button = ttk.Button(
            master=buttons_frame, text='Exit', command=self.on_cancel)
        cancel_button.grid(row=1, column=0, sticky='new', pady=8)
        options_button = ttk.Button(
            master=buttons_frame, text='Options...', command=self.on_options,
            underline=0)
        options_button.grid(row=3, column=0, sticky='sew')
        self._acc.add('<Alt-o>', widget=options_button)
        buttons_frame.rowconfigure(2, weight=1)

    def _build_method_widgets(self):
        log = RPLog.load() # reload log file
        self.method_widgets = []
        for row, options in enumerate(log['methods']):
            method = options['method']
            worst, best = options['worst'], options['best']
            widget = MethodWidget(
                master=self._methods_chooser, accelerator=self._acc,
                method=method, worst=worst, best=best)
            widget.grid(row=row, column=0, sticky='we')
            self.method_widgets.append(widget)
            if row == 0:
                sort_button = ttk.Checkbutton(
                    master=self._methods_chooser,
                    text='Sort using\nthis method',
                    variable=self.sort, underline=0)
                sort_button.grid(row=0, column=1, sticky='e', padx=(20, 5))
                self._acc.add('<Alt-s>', widget=sort_button)
        self._methods_chooser.columnconfigure(0, weight=1)

    def on_choose(self, event=None):
        initial_file = self.file_name.get()
        initial_dir = normpath(dirname(initial_file))
        file_name = askopenfilename(
            parent=self, title='Open Swiss Manager file...',
            initialdir=initial_dir, initialfile=initial_file)
        if file_name:
            self.file_name.set(file_name)

    def on_add_method(self, event=None):
        num = len(self.method_widgets)
        widget = MethodWidget(
            master=self._methods_chooser, accelerator=self._acc)
        widget.grid(row=num, column=0, sticky='we')
        self.method_widgets.append(widget)
        self._add_remove_buttons()

    def on_remove_method(self, event=None):
        widget = self.method_widgets.pop()
        widget.grid_forget()
        widget.destroy()
        self._add_remove_buttons()

    def on_ok(self, event=None):
        Thread(target=self._execute_method).start()
        self.event_generate('<Alt-f>')

    def on_cancel(self, event=None):
        self.destroy()
        self.quit()

    def on_options(self, event=None):
        options_dialog = OptionsDialog(
            master=self, icon=self._icon_file, algorithm=self._algorithm,
            output_modes=self._output_modes)
        options_dialog.do_modal()
        self._algorithm = dict(options_dialog.algorithm)

    def _add_remove_buttons(self):
        num = len(self.method_widgets)
        # Enable or disable buttons depending on number of methods
        state = '!' if num > 1 else ''
        self._remove_button.state([state + 'disabled'])
        state = '!' if num < 6 else ''
        self._add_button.state([state + 'disabled'])
        self.update_idletasks()

    def _execute_method(self):
        file_name = self.file_name.get()
        elo = self.default_elo.get()
        draw = self._algorithm['draw_character']
        epsilon = self._algorithm['epsilon']
        max_iterations = self._algorithm['iterations']
        heading = self.headings.get()
        try:
            module, output_file = self._get_module_file(file_name)
            t = module.Tournament.load(
                file_name, elo_default=elo, draw_character=draw,
                epsilon=epsilon, max_iterations=max_iterations)
        except RP.TournamentError as error:
            showerror(parent=self, title='Tournament error', message=error)
            return
        else:
            methods = [widget.get() for widget in self.method_widgets]
            sort = [methods[0]] if self.sort.get() else []
        try:
            t.run(
                methods_list=[
                    {'method': 'Names'}, {'method': 'Points'}] + methods,
                output_file=normpath(output_file),
                sort_by=[{'method': 'Points'}] + sort,
                comma_separator=self._algorithm['comma_separator'],
                heading=heading)
        except RP.TournamentError as error:
            showerror(parent=self, title='Tournament error', message=error)
        else:
            self._open_output(output_file)
        finally:
            # Save info to a file
            log = RPLog()
            RPLog.save({
                'options': {
                    key: getattr(self, key).get() for key in log['options']},
                'algorithm': self._algorithm,
                'methods': methods,
                'log_info': t.log_info})

    def _get_module_file(self, file_name):
        name, _ = splitext(file_name)
        if self._algorithm['output_mode'] == 'xlsx':
            return RPxlsx, '{}.xlsx'.format(name)
        else:
            return RP, '{}.csv'.format(name)

    def _open_output(self, file_name):
        try:
            startfile(file_name)
        except Exception as error:
            text = error + '\nOutput written on file {}.'.format(file_name)
            showerror(parent=self, title='Tournament error', message=text)

        
###############################################################################
if __name__ == '__main__':
    try:
        root = RPWin()
        root.mainloop()
    except Exception as error:
        showerror(
            parent=root, title='Unknown error', message=error)
    

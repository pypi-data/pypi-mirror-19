'''
RPWidgets is a module that implements the class MethodWidget whose aim is to
be integrated in RPWin as a frame to choose a tie-breaking method.
'''

from contextlib import redirect_stdout
from os.path import dirname, join, normpath, realpath
from functools import partial
import webbrowser
from io import StringIO
import tkinter as tk
from tkinter import ttk

if not __package__:
    # For debugging
    import sys, os
    sys.path.insert(0, join(os.getcwd(), '..'))
    from tk.acc import Accelerator
    from tk.print import RedirectedText
    from RPLog import RPLog
else:
    from ..tk.acc import Accelerator
    from ..tk.print import RedirectedText
    from .RPLog import RPLog


class MethodWidget(ttk.Frame):
    '''
    MethodWidget is a class that contains widgets to specify a tie-breaking
    method together with additional data (number opponents to remove from the
    the average of the tie-breaking rule.
    '''
    _METHODS = ['Recursive Performance', 'ARPO', 'Recursive Bucholz', 'ARBO']
    
    def __init__(
        self, accelerator, *, method='ARPO', worst=1, best=1, **options):
        super().__init__(**options)
        self._acc = accelerator
        self._build_variables()
        self.set({'method': method, 'worst': worst, 'best': best})
        self._build_widgets()
        self._set_state()

    def _build_variables(self):
        self.method = tk.StringVar()
        self.worst = tk.IntVar()
        self.best = tk.IntVar()

    def _build_widgets(self):
        # Common options
        spin_box = {
            'master': self, 'width': 3,
            'state': 'readonly', 'readonlybackground': 'white',
            'from': 0, 'to': 3, 'increment': 1}
        spin_box_grid = {'row': 1, 'sticky': 'w', 'padx': (0, 15)}
        row1 = {'row': 1, 'sticky': 'w'}
        
        # Method
        method_label = ttk.Label(master=self, text='Method: ', underline=0)
        method_label.grid(row=0, column=0, sticky='w')
        self._method_combo = ttk.Combobox(
            master=self, value=self._METHODS,
            textvariable=self.method, width=30)
        self._method_combo.state(['!disabled', 'readonly'])
        self._method_combo.bind('<<ComboboxSelected>>', self._set_state)
        self._method_combo.grid(column=0, **row1)
        self._acc.add('<Alt-m>', widget=self._method_combo)

        # Space
        ttk.Frame(master=self, width=20).grid(
            row=0, column=1, rowspan=2, sticky='we')

        # Modifications
        self._above_label = ttk.Label(
            master=self, text='Calculate average taking out...')
        self._above_label.grid(row=0, column=2, columnspan=4, sticky='w')
        self._worst_label = ttk.Label(
            master=self, text='# worst: ', underline=2)
        self._worst_label.grid(column=2, **row1)
        self._worst_spinbox = tk.Spinbox(textvariable=self.worst, **spin_box)
        self._worst_spinbox.grid(column=3, **spin_box_grid)
        self._acc.add('<Alt-w>', widget=self._worst_spinbox)
        self._best_label = ttk.Label(
            master=self, text='# best: ', underline=2)
        self._best_label.grid(column=4, **row1)
        self._best_spinbox = tk.Spinbox(textvariable=self.best, **spin_box)
        self._best_spinbox.grid(column=5, **spin_box_grid)
        self._acc.add('<Alt-b>', widget=self._best_spinbox)

        # Frame and grid configuration
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, pad=10)
        self.config(pad=5)

    def _set_state(self, event=None):
        method = self.method.get()
        show = 'grid' if method in ('ARPO', 'ARBO') else 'grid_remove'
        for widget in (
            self._above_label, self._worst_label, self._best_label,
            self._worst_spinbox, self._best_spinbox):
            getattr(widget, show)()

    def get(self):
        '''
        Gets the values obtained in the dialog with the same interface as a
        tkinter variable.
        '''
        return {
            key: getattr(self, key).get()
            for key in ('method', 'worst', 'best')}

    def set(self, values):
        '''
        Sets the values obtained in the dialog with the same interface as a
        tkinter variable.  Argument values must be given as a dict.
        '''
        for key, value in values.items():
            getattr(self, key).set(value)


class OptionsDialog(tk.Toplevel):
    '''
    Dialog to introduce some options for the PyRP module.
    '''
    _ALGORITHM_FIELDS = (
        'Draw character', 'Epsilon', 'Iterations', 'Comma separator',
        'Output mode')
    _LINK = 'http://eio.usc.es/pub/julio/Desempate/Performance_Recursiva_en.htm'
    
    def __init__(
        self, master=None, *, icon=None, algorithm=None,
        output_modes=None, **options):
        super().__init__(master=master, **options)
        self._master = master
        self._acc = Accelerator(master=self)
        self.algorithm = dict(algorithm)
        if output_modes is not None:
            self._output_modes = output_modes
        else:
            self._output_modes = ['csv']
        self.withdraw()
        self.title('Options...')
        self.iconbitmap(icon)
        self.resizable(False, False)
        self._create_widgets()
        self.bind('<Return>', self._on_ok)
        self.bind('<Escape>', self._on_cancel)
        self.update_idletasks()

    def _create_widgets(self):
        #Notebook
        self._notebook = ttk.Notebook(master=self, padding=10)
        self._notebook.grid(row=0, column=0)
        self._notebook.enable_traversal()
        self._create_algorithm()
        self._create_help()
        self._create_about()
        self._create_log()

        # Buttons
        grid_opts = {'sticky': 'n', 'pady': 1, 'padx': 10}
        buttons_frame = ttk.Frame(master=self)
        buttons_frame.grid(row=0, column=1, sticky='new', pady=10)
        self._ok_button = ttk.Button(
            master=buttons_frame, text='Ok', command=self._on_ok)
        self._ok_button.grid(row=0, column=0, **grid_opts)
        self._ok_button.event_add('<<Validate>>', '<Map>')
        self._ok_button.bind('<<Validate>>', self._validate_input)
        cancel_button = ttk.Button(
            master=buttons_frame, text='Cancel', command=self._on_cancel)
        cancel_button.grid(row=1, column=0, **grid_opts)

    def _create_algorithm(self):
        algorithm = ttk.Frame(master=self._notebook, padding=10)
        self._notebook.add(algorithm, text='Algorithm', underline=0)
        # Variables and labels
        for row, text in enumerate(self._ALGORITHM_FIELDS):
            var_name = self._to_sentence(text)
            setattr(self, var_name, tk.StringVar())
            getattr(self, var_name).set(self.algorithm[var_name])
            label = ttk.Label(master=algorithm, text=text + ': ', underline=0)
            label.grid(row=row, column=0, sticky='w', pady=5)
            if text != 'Output mode':
                entry = ttk.Entry(
                    master=algorithm, width=8,
                    textvariable=getattr(self, var_name))
            else:
                entry = ttk.Combobox(
                    master=algorithm, width=8,
                    textvariable=getattr(self, var_name))
            entry.grid(row=row, column=1, sticky='we', padx=3)
            setattr(self, '_{}_entry'.format(var_name), entry)
            entry._valid_state_ = True # Duck typing to determine state
            self._acc.add('<Alt-{}>'.format(var_name[0]), widget=entry)
        # Validating input
        positive_float = self.register(
            partial(self._positive_type, float, 'epsilon'))
        self._epsilon_entry.config(
            validate='all', validatecommand=(positive_float, '%P'))
        positive_int = self.register(
            partial(self._positive_type, int, 'iterations'))
        self._iterations_entry.config(
            validate='all', validatecommand=(positive_int, '%P'))
        # Output mode
        self._output_mode_entry.config(value=self._output_modes)
        self._output_mode_entry.state(['!disabled', 'readonly'])

    def _create_help(self):
        frame = ttk.Frame(master=self._notebook)
        self._notebook.add(frame, text='Help', underline=0)
        help_text = RedirectedText(
            master=frame, width=60, height=15, wrap='word')
        help_text.grid(row=0, column=0, sticky='nsew')
        self._print(help_text, 'help.txt')
        text = 'More information on the ARPO methods in the following link:'
        label = ttk.Label(master=frame, text=text)
        label.grid(row=1, column=0, sticky='w', pady=(5, 0))
        button = ttk.Button(
            master=frame, text=self._LINK, underline=22,
            command=lambda: webbrowser.open(self._LINK))
        button.grid(row=2, column=0, sticky='we')
        callback = lambda event=None: button.invoke()
        self._acc.add('<Alt-j>', widget=button, callback=callback)
        
    def _create_about(self):
        about = RedirectedText(
            master=self._notebook, width=60, height=15, wrap='word')
        self._notebook.add(about, text='About', underline=1)
        self._print(about, 'about.txt')

    def _create_log(self):
        log = RedirectedText(master=self._notebook, width=60, height=15)
        self._notebook.add(log, text='Last log', underline=0)
        self._print(log, text=str(RPLog.load())) 

    @staticmethod
    def _print(widget, file_name=None, text=''):
        try:
            if file_name:
                file = normpath(join(dirname(realpath(__file__)), file_name))
                file_object = open(file)
            else:
                file_object = StringIO(text)
        except OSError:
            file_object = StringIO('Missing file.')
        with redirect_stdout(widget):
            for line in file_object:
                print(line, end='')
        file_object.close()
        widget.see('1.0')

    @staticmethod
    def _to_sentence(string):
        return string.lower().replace(' ', '_')

    def _positive_type(self, type_, widget, string):
        entry = getattr(self, '_{}_entry'.format(widget))
        try:
            value = type_(string)
        except ValueError:
            state = False
        else:
            state = value > 0
        entry._valid_state_ = state
        self._ok_button.event_generate('<<Validate>>')
        return True

    def _validate_input(self, event=None):
        names = (self._to_sentence(text) for text in self._ALGORITHM_FIELDS)
        entries = (getattr(self, '_{}_entry'.format(name)) for name in names)
        state = all(entry._valid_state_ for entry in entries)
        self._ok_button.state([('!' if state else '') + 'disabled'])

    def do_modal(self):
        self.transient(self._master)
        self.deiconify()
        self.focus_set()
        self.grab_set()
        self.wait_window()

    def _on_ok(self, event=None):
        for text in self._ALGORITHM_FIELDS:
            var_name = self._to_sentence(text)
            self.algorithm[var_name] = getattr(self, var_name).get()
        self.algorithm['epsilon'] = float(self.algorithm['epsilon'])
        self.algorithm['iterations'] = int(self.algorithm['iterations'])
        return self._on_cancel()

    def _on_cancel(self, event=None):
        self.destroy()
        return 'break'

###############################################################################
if __name__ == '__main__':
    test = 'options'
    if test == 'method':
        root = tk.Tk()
        method = MethodWidget(master=root, accelerator=Accelerator(root))
        method.pack(fill=tk.BOTH, expand=tk.YES)
        root.mainloop()
    elif test == 'options':
        root = tk.Tk()
        opts = OptionsDialog(
            master=root,
            algorithm={
                'draw_character': 'x', 'epsilon': 1.0e-10,
                'iterations': 500, 'comma_separator': ';',
                'output_mode': 'csv'})
        opts.do_modal()

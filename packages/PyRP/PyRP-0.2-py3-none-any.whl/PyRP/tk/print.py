'''
tkPrint is a module that contains a context manager that calls a class whose
purpose is to redirect stdout to a ScrolledText widget.
'''

import sys
from contextlib import contextmanager

import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText


class RedirectedText(ScrolledText):
    '''
    A ScrolledText widget to print text. It works as a
    file-like object where stdout can be redirected.
    '''
    def __init__(self, editable=False, **options):
        super().__init__(**options)
        self._editable = bool(editable)
        if not editable:
            self.config(state='disabled')

    @contextmanager
    def _enable(self):
        self.config(state='normal')
        yield
        if not self._editable:
            self.config(state='disabled')

    def write(self, text):
        with self._enable():
            self.insert('end', str(text))
            self.see('end')
            self.update_idletasks()

    def writelines(self, lines):
        for line in lines:
            self.write(line)


_TOPLEVEL = tk.Tk if __name__ == '__main__' else tk.Toplevel

class Dialog(_TOPLEVEL):
    '''
    A dialog that contains a PrintText object where stdout can be redirected.
    '''
    def __init__(self, editable=False, width=60, height=25, **options):
        super().__init__(**options)
        self.withdraw()
        self._create_widgets(editable, width, height)
        self.bind('<Escape>', self._on_ok)
        self.bind('<Return>', self._on_ok)

    def _create_widgets(self, editable, width, height):
        # PrintText widget
        self.text = RedirectedText(
            master=self, editable=editable, width=width, height=height)
        self.text.grid(row=0, column=0, sticky='nsew')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        # Ok button
        ok_button = ttk.Button(
            master=self, text='OK', command=self._on_ok, width=15)
        ok_button.grid(row=1, column=0, padx=5, pady=5)

    def do_modal(self):
        self.transient(self.winfo_parent())
        self.deiconify()
        self.focus_set()
        self.grab_set()
        self.wait_window()

    def mainloop(self):
        self.deiconify()
        super().mainloop()
        
    def _on_ok(self, event=None):
        self.destroy()
        return 'break'
        

################################################################################
if __name__ == '__main__':
    from contextlib import redirect_stdout
    root = Dialog(height=10)
    root.title('Print dialog')
    with redirect_stdout(root.text):
        print('¿Que din os rumorosos')
        print('na costa verdecente')
        print('ó raio transparente')
        print('de prácido luar?')
    root.mainloop()

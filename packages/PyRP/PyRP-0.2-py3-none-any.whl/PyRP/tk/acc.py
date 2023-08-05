'''
AcceleratorKeys is a module that implements functinality to use acceletator
keys in tkinter.
'''

from collections import defaultdict, namedtuple
from functools import partial
import tkinter as tk
from tkinter import ttk


# Named tuple to hold data of event bindings
bind_data = namedtuple('bind_data', ['widget', 'callback'])

class Accelerator():
    '''
    AcceleratorKeys(master=widget) creates a class to handle accelerator keys
    of a widget.
    '''
    def __init__(self, master):
        self.master = master
        self.__bindings = defaultdict(list)

    def add(self, key_spec, *, widget=None, callback=None, caps=True):
        '''
        AcceleratorKeys.add(key_spec, widget, callback, caps) adds the event
        key_spec as a binding to the master widget with the given callback.
        The binding to the master widget is not compatible with other bindings
        with the same key_spec.
        The widget passed as an argument is the one responsible for the
        accelerator key; In principle this widget takes focus when the
        accelerator key is pressed, and if disabled, the accelerator key
        does not work for it.
        If callback is None, then the accelerator key will automatically be
        binded to some default bindings for the widget: Entry-like widgets
        get focus and select all text, Button-like widgets get pushed,
        Checkbutton-like widgets are toggled.
        If caps is True, then the event is binded to both lower and upper
        letters. Otherwise, the case is respected.
        '''
        spec = self._simplify(key_spec)
        self.__bindings[spec].append(bind_data(widget, callback))
        if caps:
            spec_lower = self._case(spec, 'lower')
            spec_upper = self._case(spec, 'upper')
            self.master.bind(spec_lower, partial(self._callback, spec))
            self.master.bind(spec_upper, partial(self._callback, spec))
        else:
            self.master.bind(spec, partial(self._callback, spec))
        widget.bind('<Destroy>', partial(self._destroy_widget, spec, widget))

    def _callback(self, key_spec, event=None):
        focus = self.master.focus_get()
        bindings = self.__bindings[key_spec]
        widgets = [self._active(widget) for widget, _ in bindings]
        try:
            # Find the widget after the one with focus in the list
            index = (widgets.index(focus) + 1) % len(widgets)
        except ValueError:
            index = 0
        # Choose the first active widget
        for i, widget in enumerate(widgets[index:] + widgets[:index], index):
            if widget != 'disabled':
                index = i  % len(widgets)
                break
        else:
            # No widget is active to handle event
            return
        callback = bindings[index].callback
        if callback is None:
            widget = bindings[index].widget
            callback = self._callback_defaults(widget)
        return callback(event)

    def _destroy_widget(self, key_spec, widget, event=None):
        # Remove this widget from the list of bindings
        bindings = self.__bindings[key_spec]
        widgets = [widget for widget, _ in bindings]
        try:
            index = widgets.index(widget)
            bindings.pop(index)
            if not bindings:
                # If there are no bindings left, unbind from master widget
                self.master.unbind(self._case(key_spec, 'lower'))
                self.master.unbind(self._case(key_spec, 'upper'))
                del self.__bindings[key_spec]
        except ValueError:
            # If widget is not present, just leave
            pass

    def _callback_defaults(self, widget):
        widget.focus_set()
        # default callbacks
        if isinstance(widget, (tk.Entry, ttk.Entry, ttk.Combobox)):
            return partial(self._entry_default, widget)
        elif isinstance(widget, tk.Spinbox):
            return partial(self._spinbox_default, widget)
        elif isinstance(widget, (
            tk.Button, ttk.Button, tk.Checkbutton, ttk.Checkbutton)):
            # Push the button
            return lambda event: widget.invoke()
        else:
            raise TypeError(
                "'NoneType' object is not callable. "
                "Provide a callback function to the accelerator key.")

    @staticmethod
    def _simplify(key_spec):
        # Remove the "KeyPress" specification
        return ''.join(key_spec.split('KeyPress-'))

    @staticmethod
    def _case(spec, to='lower'):
        return '{}{}>'.format(spec[:-2], getattr(spec[-2], to)())
    
    @staticmethod
    def _active(widget):
        if not widget.winfo_ismapped():
            # If it is not visible, don't do anything
            return 'disabled'
        try:
            # This works for ttk widgets
            return widget if widget.instate(['!disabled']) else 'disabled'
        except AttributeError:
            # Fall back to tk widgets (check if there is a better way)
            return widget if not widget['state'] == 'disabled' else 'disabled'

    @staticmethod
    def _entry_default(widget, event=None):
        # Get focus and select
        widget.select_range(0, 'end')
        widget.icursor('end')
        
    @staticmethod
    def _spinbox_default(widget, event=None):
        # Get focus and select
        widget.selection('range', 0, 'end')
        widget.icursor('end')
        

###############################################################################
if __name__ == '__main__':
    # Create a small useless app to check some of the characterisitcs
    root = tk.Tk()
    label1 = ttk.Label(master=root, text='Label 1: ', underline=2)
    label1.grid(row=0, column=0)
    entry1 = ttk.Entry(master=root)
    entry1.grid(row=0, column=1)
    state = '!disabled'
    def toogle_state(event=None):
        global label1, entry1, state
        state = '!disabled' if state == 'disabled' else 'disabled'
        label1.state([state])
        entry1.state([state])
    label2 = ttk.Label(master=root, text='Label 2: ', underline=2)
    label2.grid(row=1, column=0)
    entry2 = ttk.Entry(master=root)
    entry2.grid(row=1, column=1)
    label3 = ttk.Label(master=root, text='Label 3: ', underline=2)
    label3.grid(row=2, column=0)
    entry3 = tk.Spinbox(master=root)
    entry3.grid(row=2, column=1)
    button1 = ttk.Button(
        master=root, text='Button1', underline=1,
        command=toogle_state)
    button1.grid(row=10, column=0)
    button2 = ttk.Button(
        master=root, text='Button2', underline=2,
        command=lambda event=None: button1.destroy())
    button2.grid(row=10, column=1)
    acc = Accelerator(root)
    acc.add('<Alt-b>', widget=entry1)
    acc.add('<Alt-b>', widget=entry2)
    acc.add('<Alt-b>', widget=entry3)
    acc.add('<Alt-u>', widget=button1)
    acc.add('<Alt-t>', widget=button2)
    root.mainloop()

#! python

from tkinter.messagebox import showerror
from PyRP.win.RPWin import RPWin

try:
    root = RPWin()
    root.mainloop()
except Exception as error:
    showerror(
        parent=root, title='Unknown error', message=error)


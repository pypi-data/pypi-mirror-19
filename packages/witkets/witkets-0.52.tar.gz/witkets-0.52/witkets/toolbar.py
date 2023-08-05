from tkinter import *
from tkinter.ttk import *

class Toolbar(Frame):
    """Simple toolbar implementation
      
       Options: All :code:`Frame` widget options
    """

    def __init__(self, master=None, **kw):
        Frame.__init__(self, master, **kw)
        self['style'] = 'Toolbar.TFrame'
        
    def addButton(self, imagepath, command):
        """Adds a button to the toolbar"""
        img = PhotoImage(file=imagepath)
        btn = Button(self, image=img, command=command) #both img needed
        btn.image = img
        btn.pack(side=LEFT, padx=2, pady=2)
        btn['style'] = 'Toolbutton.TButton'
        
if __name__ == '__main__':
    def hello():
        print('hello!!')

    root = Tk()
    toolbar = Toolbar()
    toolbar.addButton('/usr/share/icons/gnome/32x32/actions/add.png', hello)
    toolbar.addButton('/usr/share/icons/gnome/32x32/status/dialog-error.png', hello)
    
    toolbar.pack()
    root.mainloop()

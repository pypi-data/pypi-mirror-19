#!/usr/bin/env python3

"""@OBSOLETE: Use FileChooserEntry instead"""

from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askdirectory

class DirChooserEntry(Frame):
    """Entry and button intended to choose a directory
    
       The chosen path can be accessed either through the :code:`get` method or
       by a Tk StringVar set via the *textvariable* option.
    """
    
    def __init__(self, master, textvariable=None, text='Choose...', **kw):
        Frame.__init__(self, master, **kw)
        #Variables
        self._varEntry = StringVar()
        self._var = textvariable if textvariable else StringVar(value='')
        #Widgets
        self.entry = Entry(self, state='disabled')
        self.entry['state'] = 'disabled'
        self.entry['textvariable'] = self._varEntry
        self.entry['style'] = 'ReadOnlyEntry.TEntry'
        self.entry['width'] = 30
        self.entry.pack(side=LEFT, fill=X, expand=1)
        self.button = Button(self, text=text)
        self.button['command'] = self._chooseDir
        self.button.pack(side=LEFT)
        self._var.trace('w', self._update)
            
    def __setitem__(self, key, val):
        if key == 'textvariable':
            self._var = val
            self._var.trace('w', self._update)
        else:
            Frame.__setitem__(self, key, val)
            
    def __getitem__(self, key):
        if key == 'textvariable':
            return self._var
        else:
            return Frame.__getitem__(self, key)
            
    def config(self, **kw):
        """Tk standard config method"""
        if 'textvariable' in kw:
            self._var = kw['textvariable']
            kw.pop('textvariable', False)
        Frame.config(kw)
        
    def get(self):
        """Gets the current selected directory path"""
        return self._var.get()
        
    def _chooseDir(self):
        """Choose directory button callback"""
        folder = askdirectory(parent=self, title='Escolha um diretório')
        self._var.set(folder)
        self._update()
        
    def _update(self, event=None, *args):
        """Update label"""
        lbl = self._var.get()
        width = self.entry['width']
        lbl = lbl if len(lbl) < width else '...' + lbl[-(width - 4):]
        self.entry['state'] = 'normal'
        self._varEntry.set(lbl)
        self.entry['state'] = 'disabled'
        
if __name__ == '__main__':
    root = Tk()
    Label(root, text='Directory: ').pack()
    chooser = DirChooserEntry(root)
    chooser.pack()
    root.mainloop()

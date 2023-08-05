#!/usr/bin/env python3

from tkinter import *
from tkinter import font
from tkinter.ttk import *
import ast
import configparser
from io import StringIO

#Credits: http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/ttk-map.html
class Theme:
    """Theming widget"""    
    
    def __init__(self, style=None):
        """Initializer

        :param style:
            Tk Style object to manipulate or None for root style
          
        """
        self._style = style if style else Style()

    def setDefaultFonts(self):
        """Set Tk fonts to Witkets default (Helvetica 11)"""
        defaultFont = font.nametofont("TkDefaultFont")
        defaultFont.configure(size=11, family="Helvetica")
        textFont = font.nametofont("TkTextFont")
        textFont.configure(size=11, family="Helvetica")
        fixedFont = font.nametofont("TkFixedFont")
        fixedFont.configure(size=11, family="Helvetica")

    def _parseConfig(self, config):
        """Reads styles from a config structure"""
        self._style.configure('.', background='#FFF')
        for s in config.sections():
            normalValues = {}
            composedValues = {}
            for key in config[s]:
                if '.' in key:
                    parts = key.split('.')
                    #Dictionary keys: foreground=[], background=[], ...
                    baseKey = parts[0]
                    if baseKey not in composedValues:
                        composedValues[baseKey] = []
                    #Constructing list [constraint1, constraint2, ..., value]
                    element = [x.replace('_', '!') for x in parts[1:]]
                    element.append(config[s][key])
                    composedValues[baseKey].append(element)
                else:
                    normalValues[key] = config[s][key]
            self._style.configure(s, **normalValues)
            self._style.map(s, **composedValues)

    def applyFromFile(self, filepath):
        """Applies styles defined in *filepath* (INI-like file)"""
        config = configparser.ConfigParser()
        config.read(filepath)
        self._parseConfig(config)

    def applyFromString(self, rules):
        """Applies styles defined in string *rules* (INI-like string)"""
        config = configparser.ConfigParser()
        config.readfp(StringIO(rules))
        self._parseConfig(config)
        
    def applyDefaultTheme(self):
        """Applies the default theme"""
        self.applyFromString(WITKETS_DEFAULT_THEME)


WITKETS_DEFAULT_THEME = '''\
;Global style
[.]
background=#FFF

;Headers
[Header.TLabel]
font=Helvetica 24 bold italic
foreground=#0000AA

;Blocks
[Blk.TFrame]
borderwidth=4
relief=raised

[BlkTitle.TLabel]
font=Helvetica 16 bold

;Buttons
[TButton]
relief=raised
borderwidth=1
relief.pressed = ridge
relief._pressed = groove

;Special Buttons
[MediumButton.TButton]
relief=raised
borderwidth=1
font=Helvetica 14 bold
relief.pressed = ridge
relief._pressed = groove

[BigButton.TButton]
font=Helvetica 36 bold
borderwidth=0
relief=flat

;Status Label
[StatusOK.TLabel]
foreground=#080

[StatusError.TLabel]
foreground=#800

;Scrollbars
;[TScrollbar]
;relief=raised
;borderwidth=1
;background=#008
;foreground=#FFF

;Entries
[ReadOnlyEntry.TEntry]
borderwidth=0
highlightbackground=#FFF
highlightthickness=0
selectborderwidth=0
foreground.disabled=#000


[Error.TEntry]
fieldbackground=#A00

[Incomplete.TEntry]
fieldbackground=#AA0

[TEntry]
fieldbackground=#FFF

;Frames
[Bordered.TFrame]
borderwidth=5
background=#008

;Toolbar
[Toolbar.TFrame]
relief=flat
background=#CCC

[Toolbutton.TButton]
relief=flat
background=#CCC
'''
         
if __name__ == '__main__':
    root = Tk()
    root.title('Test')
    root.configure(background='#FFF') #not yet supported inside INI-file
    Button(root, text='open').pack(side=LEFT)
    Button(root, text='close').pack(side=LEFT)
    b = Button(root, text='BIG One!')
    b['style'] = 'BigButton.TButton'
    b.pack(side=RIGHT)
    s = Style()
    s.theme_use('clam')
    theme = Theme(s)
    theme.setDefaultFonts()
    theme.applyFromString(WITKETS_DEFAULT_THEME) #that will do the trick!
    root.mainloop()

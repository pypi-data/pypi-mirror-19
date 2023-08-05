#!/usr/bin/env python3

import sys
import xml.etree.ElementTree as ET
from tkinter import *
from tkinter.ttk import *
from tkinter.scrolledtext import ScrolledText
from copy import copy
from witkets.accellabel import AccelLabel
from witkets.led import LED
from witkets.linkbutton import LinkButton
from witkets.logicswitch import LogicSwitch
from witkets.numericlabel import NumericLabel
from witkets.plot import Plot
from witkets.pytext import PyText
from witkets.pyscrolledtext import PyScrolledText
from witkets.scope import Scope
from witkets.tank import Tank
from witkets.theme import Theme
from witkets.toolbar import Toolbar
from witkets.thermometer import Thermometer

tag2tk = {
    #TK Base
    'button': Button,
    'canvas': Canvas,
    'checkbutton': Checkbutton,
    'entry': Entry,
    'frame': Frame,
    'label': Label,
    'labelframe': LabelFrame,
    'listbox': Listbox,
    'menu': Menu,
    'menubutton': Menubutton,
    #'message': Message, #obsolete!
    #'optionmenu': OptionMenu, #not supported!
    #'panedwindow': PanedWindow, #not supported
    'radiobutton': Radiobutton,
    'scale': Scale,
    'scrollbar': Scrollbar,
    'scrolledtext': ScrolledText,
    'spinbox': Spinbox,
    'text': Text,
    #TTK
    'combobox': Combobox,
    'notebook': Notebook,
    'progressbar': Progressbar,
    'separator': Separator,
    'sizegrip': Sizegrip,
    'treeview': Treeview,
    #Witkets (missing some)
    'accellabel': AccelLabel,
    'led': LED,
    'linkbutton': LinkButton,
    'logicswitch': LogicSwitch,
    'numericlabel': NumericLabel,
    'pytext': PyText,
    'pyscrolledtext': PyScrolledText,
    'plot': Plot,
    'scope': Scope,
    'tank': Tank,
    'thermometer': Thermometer,
    'toolbar': Toolbar,
}

containers = [ 'root', 'frame', 'labelframe' ]

class TkBuilder:
    def __init__(self, master):
        """Initializer
        
            :param master:
                Tk root where interface is going to be built
        """
        self._tree = None
        self._root = None
        self._master = master
        #if not hasattr(self._master, 'properties'):
        #    self._master.properties = []
        self.nodes = {}
        self.tkstyle = None
        self.theme = None
        
    def addTag(self, tag, cls, container=False):
        """Maps a tag to a class
        
            :param tag:
                XML tag name
            :type tag:
                str
            :param cls:
                Class to be instantiated when *tag* is found
            :type cls:
                Any subclass of tkinter.Widget
            :param container:
                Whether this Tk widget is a container to other widgets
        """
        tag2tk[tag] = cls
        if container:
            containers.append(tag)
        
    def _handleWidget(self, widgetNode, parent):
        """Handles individual widgets tags"""
        try:
            wid = widgetNode.attrib.pop('wid')
        except KeyError:
            print('Required key "wid" not found in %s' % widgetNode.tag, sys.stderr)
            return
        # Creating widget        
        tkClass = tag2tk[widgetNode.tag]
        if parent == self._root:
            parentNode = self._master
        else:
            parentWid = parent.attrib['wid']
            parentNode = self.nodes[parentWid]        
        self.nodes[wid] = tkClass(parentNode)
        # Mapping attributes
        self._handleAttributes(self.nodes[wid], widgetNode.attrib)
    
    def _handleAttributes(self, widget, attribs):
        """Handles attributes, except TkBuilder related"""
        for key,val in attribs.items():            
            if key.startswith('{editor}'): #skipping editor namespace
                continue
            try:
                widget[key] = val #@FIXME fails for Bool
            except KeyError:
                print('[warning] Invalid key "%s"' % key)
        
    def _handleContainer(self, container, parent):
        """Handles containers (<root>, <frame> and user-defined containers)"""
        if container != self._root:    
            try:
                attribs = copy(container.attrib)
                wid = attribs.pop('wid')
                tkClass = tag2tk[container.tag]
                if parent != self._root:
                    parentWid = parent.attrib['wid']
                    parentNode = self.nodes['wid']
                else:
                    parentNode = self._master
                self.nodes[wid] = tkClass(parentNode)
                self._handleAttributes(self.nodes[wid], attribs)
            except KeyError:
                print('Required key "wid" not found in %s' % container.tag, sys.stderr)
                return
        for child in container:
            if child.tag in containers:
                self._handleContainer(child, container)
            elif child.tag == 'geometry':
                self.currParent = container
                self._handleGeometry(child)
            elif child.tag == 'style':
                self._handleStylesheet(child)
            elif child.tag in tag2tk.keys():
                self._handleWidget(child, container)
            else:
                print('Invalid tag: %s!' % child.tag, sys.stderr)
        if container == self._root:
            attribs = container.attrib
            self._handleAttributes(self._master, attribs)
        
    def _handleGeometry(self, geometry):
        """Handles the special <geometry> tag"""
        for child in geometry:
            attribs = copy(child.attrib)
            if child.tag in ('pack', 'grid', 'place'):
                # Getting widget ID
                try:
                    wid = attribs.pop('for')
                except KeyError:
                    #@TODO emit error
                    print('[geom] Required key "for" not found in %s' % child.tag, sys.stderr)
                    continue
                # Calling appropriate geometry method
                if wid not in self.nodes:
                    print(self.nodes)
                if child.tag == 'pack':
                    self.nodes[wid].pack(**attribs)
                elif child.tag == 'grid':
                    self.nodes[wid].grid(**attribs)
                elif child.tag == 'place':
                    self.nodes[wid].place(**attribs)
            else:
                print('Invalid geometry instruction %s' % child.tag, sys.stderr)    
                #@TODO emit error
                continue
                
    def _handleStylesheet(self, style):
        """Handles the special <style> tag"""
        self.tkstyle = Style()
        self.theme = Theme(self.tkstyle)
        if 'defaultfonts' in style.attrib and \
            style.attrib['defaultfonts'] != '0':
            self.theme.setDefaultFonts()
        if 'fromfile' in style.attrib:
            self.theme.applyFromFile(style.attrib['fromfile'])
        else:
            self.theme.applyFromString(style.text)

    def _parseTree(self):
        """Parses XML and builds interface"""
        if self._root.tag != 'root':
            msg = 'Invalid root tag! Expecting "root", but found %s'
            print(msg % self._root.tag, sys.stderr)
            return False
        self._handleContainer(self._root, self._master)
        return True

    def buildFile(self, filepath):
        """Build user interface from XML file"""
        self._tree = ET.parse(filepath)
        self._root = self._tree.getroot()
        self._parseTree()

    def buildString(self, contents):
        """Build user interface from XML string"""
        self._root = ET.fromstring(contents)
        self._parseTree()
    
if __name__ == '__main__':
    example = '''
        <root>
            <style defaultfonts="1">
                [SpockLabel.TLabel]
                    foreground=#088
                    background=#000
            </style>
            <label wid="lbl1" text="Cap. Kirk" background="red" />
            <frame wid="frm1">
                <label wid="lbl2" text="Bones" width="30" />
                <label wid="lbl3" text="Spock" style="SpockLabel.TLabel" />
                <geometry>
                    <grid for="lbl2" row="0" column="0" sticky="w" />
                    <grid for="lbl3" row="0" column="2" sticky="e"/>
                </geometry>
            </frame>
            <geometry>
                <pack for="lbl1" fill="y" expand="1" />
                <pack for="frm1" />
            </geometry>
        </root>
'''

    root = Tk()
    builder = TkBuilder(root)
    builder.buildString(example)
    root.mainloop()

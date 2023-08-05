# -*- coding: utf-8 -*-

from tkinter import ttk, messagebox
from tkinter.dialog import Dialog

from thonny import tktextext
from thonny.globals import get_workbench
from thonny.misc_utils import running_on_mac_os, running_on_windows, running_on_linux
import tkinter as tk
import traceback


CLAM_BACKGROUND = "#dcdad5"
CALM_WHITE = '#fdfdfd'

_images = set() # for keeping references to tkinter images to avoid garbace colleting them

class AutomaticPanedWindow(tk.PanedWindow):
    """
    Enables inserting panes according to their position_key-s.
    Automatically adds/removes itself to/from its master AutomaticPanedWindow.
    Fixes some style glitches.
    """ 
    def __init__(self, master, position_key=None,
                first_pane_size=1/3, last_pane_size=1/3, **kwargs):
        if not "sashwidth" in kwargs:
            kwargs["sashwidth"]=10
        
        theme = ttk.Style().theme_use()
        
        if not "background" in kwargs:
            if theme == "clam":
                kwargs["background"] = "#DCDAD5"
            elif theme == "aqua":
                kwargs["background"] = "systemSheetBackground"
            else: 
                kwargs["background"] = "SystemButtonFace"
        
        tk.PanedWindow.__init__(self, master, **kwargs)
        
        self.position_key = position_key
        self.visible_panes = set()
        self.first_pane_size = first_pane_size
        self.last_pane_size = last_pane_size
        self._restoring_pane_sizes = False
        
        self._last_window_size = (0,0)
        self._full_size_not_final = True
        self._configure_binding = self.winfo_toplevel().bind("<Configure>", self._on_window_resize, True)
        self.bind("<B1-Motion>", self._on_mouse_dragged, True)
    
    def insert(self, pos, child, **kw):
        if pos == "auto":
            # According to documentation I should use self.panes()
            # but this doesn't return expected widgets
            for sibling in sorted(self.visible_panes, 
                                  key=lambda p:p.position_key 
                                        if hasattr(p, "position_key")
                                        else 0):
                if (not hasattr(sibling, "position_key") 
                    or sibling.position_key == None
                    or sibling.position_key > child.position_key):
                    pos = sibling
                    break
            else:
                pos = "end"
            
        if isinstance(pos, tk.Widget):
            kw["before"] = pos
        self.add(child, **kw)

    def add(self, child, **kw):
        if not "minsize" in kw:
            kw["minsize"]=60
            
        tk.PanedWindow.add(self, child, **kw)
        self.visible_panes.add(child)
        self._update_visibility()
        self._check_restore_pane_sizes()
    
    def remove(self, child):
        tk.PanedWindow.remove(self, child)
        self.visible_panes.remove(child)
        self._update_visibility()
        self._check_restore_pane_sizes()
    
    def forget(self, child):
        tk.PanedWindow.forget(self, child)
        self.visible_panes.remove(child)
        self._update_visibility()
        self._check_restore_pane_sizes()
    
    def destroy(self):
        self.winfo_toplevel().unbind("<Configure>", self._configure_binding)
        tk.PanedWindow.destroy(self)
        
    
    def is_visible(self):
        if not isinstance(self.master, AutomaticPanedWindow):
            return self.winfo_ismapped()
        else:
            return self in self.master.visible_panes
    
    def _on_window_resize(self, event):
        window = self.winfo_toplevel()
        window_size = (window.winfo_width(), window.winfo_height())
        initializing = hasattr(window, "initializing") and window.initializing
        
        if (not initializing
            and not self._restoring_pane_sizes 
            and (window_size != self._last_window_size or self._full_size_not_final)):
            self._check_restore_pane_sizes()
            self._last_window_size = window_size
    
    def _on_mouse_dragged(self, event):
        if event.widget == self and not self._restoring_pane_sizes:
            self._store_pane_sizes()
            
    
    def _store_pane_sizes(self):
        if len(self.panes()) > 1:
            self.last_pane_size = self._get_pane_size("last")
            if len(self.panes()) > 2:
                self.first_pane_size = self._get_pane_size("first")
    
    def _check_restore_pane_sizes(self):
        """last (and maybe first) pane sizes are stored, first (or middle)
        pane changes its size when window is resized"""
        
        window = self.winfo_toplevel()
        if hasattr(window, "initializing") and window.initializing:
            return
        
        try:
            self._restoring_pane_sizes = True
            if len(self.panes()) > 1:
                self._set_pane_size("last", self.last_pane_size)
                if len(self.panes()) > 2:
                    self._set_pane_size("first", self.first_pane_size)
        finally:
            self._restoring_pane_sizes = False
    
    def _get_pane_size(self, which):
        self.update_idletasks()
        
        if which == "first":
            coord = self.sash_coord(0)
        else:
            coord = self.sash_coord(len(self.panes())-2)
            
        if self.cget("orient") == tk.HORIZONTAL:
            full_size = self.winfo_width()
            sash_distance = coord[0]
        else:
            full_size = self.winfo_height()
            sash_distance = coord[1]
        
        if which == "first":
            return sash_distance
        else:
            return full_size - sash_distance 
        
    
    def _set_pane_size(self, which, size):
        #print("setsize", which, size)
        self.update_idletasks()
        
        if self.cget("orient") == tk.HORIZONTAL:
            full_size = self.winfo_width()
        else:
            full_size = self.winfo_height()
        
        self._full_size_not_final = full_size == 1
        
        if self._full_size_not_final:
            return
        
        if isinstance(size, float):
            size = int(full_size * size)
        
        #print("full vs size", full_size, size)
        
        if which == "first":
            sash_index = 0
            sash_distance = size 
        else:
            sash_index = len(self.panes())-2
            sash_distance = full_size - size 
        
        if self.cget("orient") == tk.HORIZONTAL:
            self.sash_place(sash_index, sash_distance, 0)
            #print("PLACE", sash_index, sash_distance, 0)
        else:
            self.sash_place(sash_index, 0, sash_distance)
            #print("PLACE", sash_index, 0, sash_distance)
      
    
    def _update_visibility(self):
        if not isinstance(self.master, AutomaticPanedWindow):
            return
        
        if len(self.visible_panes) == 0 and self.is_visible():
            self.master.forget(self)
            
        if len(self.panes()) > 0 and not self.is_visible():
            self.master.insert("auto", self)
        
    

class AutomaticNotebook(ttk.Notebook):
    """
    Enables inserting views according to their position keys.
    Remember its own position key. Automatically updates its visibility.
    """
    def __init__(self, master, position_key):
        ttk.Notebook.__init__(self, master)
        self.position_key = position_key
    
    def add(self, child, **kw):
        ttk.Notebook.add(self, child, **kw)
        self._update_visibility()
    
    def insert(self, pos, child, **kw):
        if pos == "auto":
            for sibling in map(self.nametowidget, self.tabs()):
                if (not hasattr(sibling, "position_key") 
                    or sibling.position_key == None
                    or sibling.position_key > child.position_key):
                    pos = sibling
                    break
            else:
                pos = "end"
            
        ttk.Notebook.insert(self, pos, child, **kw)
        self._update_visibility()
    
    def hide(self, tab_id):
        ttk.Notebook.hide(self, tab_id)
        self._update_visibility()
    
    def forget(self, tab_id):
        ttk.Notebook.forget(self, tab_id)
        self._update_visibility()
    
    def is_visible(self):
        return self in self.master.visible_panes
        
    def _update_visibility(self):
        if not isinstance(self.master, AutomaticPanedWindow):
            return
        if len(self.tabs()) == 0 and self.is_visible():
            self.master.remove(self)
            
        if len(self.tabs()) > 0 and not self.is_visible():
            self.master.insert("auto", self)
        

class TreeFrame(ttk.Frame):
    def __init__(self, master, columns, displaycolumns='#all', show_scrollbar=True):
        ttk.Frame.__init__(self, master)
        self.vert_scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        if show_scrollbar:
            self.vert_scrollbar.grid(row=0, column=1, sticky=tk.NSEW)
        
        self.tree = ttk.Treeview(self, columns=columns, displaycolumns=displaycolumns, 
                                 yscrollcommand=self.vert_scrollbar.set)
        self.tree['show'] = 'headings'
        self.tree.grid(row=0, column=0, sticky=tk.NSEW)
        self.vert_scrollbar['command'] = self.tree.yview
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.tree.bind("<<TreeviewSelect>>", self.on_select, "+")
        self.tree.bind("<Double-Button-1>", self.on_double_click, "+")
        
    def _clear_tree(self):
        for child_id in self.tree.get_children():
            self.tree.delete(child_id)
    
    def on_select(self, event):
        pass
    
    def on_double_click(self, event):
        pass



def sequence_to_accelerator(sequence):
    """Translates Tk event sequence to customary shortcut string
    for showing in the menu"""
    
    if not sequence:
        return ""
    
    if not sequence.startswith("<"):
        return sequence
    
    accelerator = (sequence
        .strip("<>")
        .replace("Key-", "")
        .replace("KeyPress-", "")
        .replace("Control", "Ctrl")
    )
    
    # Tweaking individual parts
    parts = accelerator.split("-")
    # tkinter shows shift with capital letter, but in shortcuts it's customary to include it explicitly
    if len(parts[-1]) == 1 and parts[-1].isupper() and not "Shift" in parts:
        parts.insert(-1, "Shift")
    
    # even when shift is not required, it's customary to show shortcut with capital letter
    if len(parts[-1]) == 1:
        parts[-1] = parts[-1].upper()
    
    accelerator = "+".join(parts)
    
    # Post processing
    accelerator = (accelerator
        .replace("Minus", "-").replace("minus", "-")
        .replace("Plus", "+").replace("plus", "+"))
    
    return accelerator
    

        
def get_zoomed(toplevel):
    if "-zoomed" in toplevel.wm_attributes(): # Linux
        return bool(toplevel.wm_attributes("-zoomed"))
    else: # Win/Mac
        return toplevel.wm_state() == "zoomed"
          

def set_zoomed(toplevel, value):
    if "-zoomed" in toplevel.wm_attributes(): # Linux
        toplevel.wm_attributes("-zoomed", str(int(value)))
    else: # Win/Mac
        if value:
            toplevel.wm_state("zoomed")
        else:
            toplevel.wm_state("normal")

class EnhancedTextWithLogging(tktextext.EnhancedText):
    def direct_insert(self, index, chars, tags=()):
        try:
            # try removing line numbers
            # TODO: shouldn't it take place only on paste?
            # TODO: does it occur when opening a file with line numbers in it?
            #if self._propose_remove_line_numbers and isinstance(chars, str):
            #    chars = try_remove_linenumbers(chars, self)
            concrete_index = self.index(index)
            return tktextext.EnhancedText.direct_insert(self, index, chars, tags=tags)
        finally:
            get_workbench().event_generate("TextInsert", index=concrete_index, 
                                           text=chars, tags=tags, text_widget=self)

    
    def direct_delete(self, index1, index2=None):
        try:
            # index1 may be eg "sel.first" and it doesn't make sense *after* deletion
            concrete_index1 = self.index(index1)
            if index2 is not None:
                concrete_index2 = self.index(index2)
            else:
                concrete_index2 = None
                
            return tktextext.EnhancedText.direct_delete(self, index1, index2=index2)
        finally:
            get_workbench().event_generate("TextDelete", index1=concrete_index1,
                                           index2=concrete_index2, text_widget=self)
            
    
class SafeScrollbar(ttk.Scrollbar):
    def set(self, first, last):
        try:
            ttk.Scrollbar.set(self, first, last)
        except:
            traceback.print_exc()

class AutoScrollbar(SafeScrollbar):
    # http://effbot.org/zone/tkinter-autoscrollbar.htm
    # a vert_scrollbar that hides itself if it's not needed.  only
    # works if you use the grid geometry manager.
    def set(self, lo, hi):
        # TODO: this can make GUI hang or max out CPU when scrollbar wobbles back and forth
        """
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
        """
        ttk.Scrollbar.set(self, lo, hi)
    def pack(self, **kw):
        raise tk.TclError("cannot use pack with this widget")
    def place(self, **kw):
        raise tk.TclError("cannot use place with this widget")

def update_entry_text(entry, text):
    original_state = entry.cget("state")
    entry.config(state="normal")
    entry.delete(0, "end")
    entry.insert(0, text)
    entry.config(state=original_state)


class ScrollableFrame(tk.Frame):
    # http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame
    
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg=CALM_WHITE)
        
        # set up scrolling with canvas
        vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.canvas = tk.Canvas(self, bg=CALM_WHITE, bd=0, highlightthickness=0,
                           yscrollcommand=vscrollbar.set)
        vscrollbar.config(command=self.canvas.yview)
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)
        self.canvas.grid(row=0, column=0, sticky=tk.NSEW)
        vscrollbar.grid(row=0, column=1, sticky=tk.NSEW)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        self.interior = tk.Frame(self.canvas, bg=CALM_WHITE)
        self.interior.columnconfigure(0, weight=1)
        self.interior.rowconfigure(0, weight=1)
        self.interior_id = self.canvas.create_window(0,0, 
                                                    window=self.interior, 
                                                    anchor=tk.NW)
        self.bind('<Configure>', self._configure_interior, "+")
        self.bind('<Expose>', self._expose, "+")
        
    def _expose(self, event):
        self.update_idletasks()
        self._configure_interior(event)
    
    def _configure_interior(self, event):
        # update the scrollbars to match the size of the inner frame
        size = (self.canvas.winfo_width() , self.interior.winfo_reqheight())
        self.canvas.config(scrollregion="0 0 %s %s" % size)
        if (self.interior.winfo_reqwidth() != self.canvas.winfo_width()
            and self.canvas.winfo_width() > 10):
            # update the interior's width to fit canvas
            #print("CAWI", self.canvas.winfo_width())
            self.canvas.itemconfigure(self.interior_id,
                                      width=self.canvas.winfo_width())

class TtkDialog(Dialog):
    def buttonbox(self):
        '''add standard button box.

        override if you do not want the standard buttons
        '''

        box = ttk.Frame(self)

        w = ttk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = ttk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok, True)
        self.bind("<Escape>", self.cancel, True)

        box.pack()

    

class _QueryDialog(TtkDialog):

    def __init__(self, title, prompt,
                 initialvalue=None,
                 minvalue = None, maxvalue = None,
                 master = None,
                 selection_range=None):

        if not master:
            master = tk._default_root

        self.prompt   = prompt
        self.minvalue = minvalue
        self.maxvalue = maxvalue

        self.initialvalue = initialvalue
        self.selection_range = selection_range

        Dialog.__init__(self, master, title)

    def destroy(self):
        self.entry = None
        Dialog.destroy(self)

    def body(self, master):

        w = ttk.Label(master, text=self.prompt, justify=tk.LEFT)
        w.grid(row=0, padx=5, sticky=tk.W)

        self.entry = ttk.Entry(master, name="entry")
        self.entry.grid(row=1, padx=5, sticky="we")

        if self.initialvalue is not None:
            self.entry.insert(0, self.initialvalue)
            
            if self.selection_range:
                self.entry.icursor(self.selection_range[0])
                self.entry.select_range(self.selection_range[0], self.selection_range[1])
            else:
                self.entry.select_range(0, tk.END)

        return self.entry

    def validate(self):
        try:
            result = self.getresult()
        except ValueError:
            messagebox.showwarning(
                "Illegal value",
                self.errormessage + "\nPlease try again",
                parent = self
            )
            return 0

        if self.minvalue is not None and result < self.minvalue:
            messagebox.showwarning(
                "Too small",
                "The allowed minimum value is %s. "
                "Please try again." % self.minvalue,
                parent = self
            )
            return 0

        if self.maxvalue is not None and result > self.maxvalue:
            messagebox.showwarning(
                "Too large",
                "The allowed maximum value is %s. "
                "Please try again." % self.maxvalue,
                parent = self
            )
            return 0

        self.result = result

        return 1

class _QueryString(_QueryDialog):
    def __init__(self, *args, **kw):
        if "show" in kw:
            self.__show = kw["show"]
            del kw["show"]
        else:
            self.__show = None
        _QueryDialog.__init__(self, *args, **kw)

    def body(self, master):
        entry = _QueryDialog.body(self, master)
        if self.__show is not None:
            entry.configure(show=self.__show)
        return entry

    def getresult(self):
        return self.entry.get()


class ToolTip(object):
    """Taken from http://www.voidspace.org.uk/python/weblog/arch_d7_2006_07_01.shtml"""

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, _, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 27
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        try:
            # For Mac OS
            tw.tk.call("::tk::unsupported::MacWindowStyle",
                       "style", tw._w,
                       "help", "noActivates")
        except tk.TclError:
            pass
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                      background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def create_tooltip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

def askstring(title, prompt, **kw):
    '''get a string from the user

    Arguments:

        title -- the dialog title
        prompt -- the label text
        **kw -- see SimpleDialog class

    Return value is a string
    '''
    d = _QueryString(title, prompt, **kw)
    return d.result


def get_current_notebook_tab_widget(notebook):    
    for child in notebook.winfo_children():
        if str(child) == str(notebook.select()):
            return child
        
    return None

def create_string_var(value, modification_listener=None):
    """Creates a tk.StringVar with "modified" attribute
    showing whether the variable has been modified after creation"""
    return _create_var(tk.StringVar, value, modification_listener)

def create_int_var(value, modification_listener=None):
    """See create_string_var"""
    return _create_var(tk.IntVar, value, modification_listener)

def create_double_var(value, modification_listener=None):
    """See create_string_var"""
    return _create_var(tk.DoubleVar, value, modification_listener)

def create_boolean_var(value, modification_listener=None):
    """See create_string_var"""
    return _create_var(tk.BooleanVar, value, modification_listener)

def _create_var(class_, value, modification_listener):
    var = class_(value=value)
    var.modified = False
    
    def on_write(*args):
        var.modified = True
        if modification_listener:
            try:
                modification_listener()
            except:
                # Otherwise whole process will be brought down
                # because for some reason Tk tries to call non-existing method
                # on variable
                get_workbench().report_exception()
    
    # TODO: https://bugs.python.org/issue22115 (deprecation warning)
    var.trace("w", on_write)
    return var

def shift_is_pressed(event_state):
    # http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/event-handlers.html
    # http://stackoverflow.com/q/32426250/261181
    return event_state & 0x0001

def control_is_pressed(event_state):
    # http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/event-handlers.html
    # http://stackoverflow.com/q/32426250/261181
    return event_state & 0x0004

def select_sequence(win_version, mac_version, linux_version=None):
    if running_on_windows():
        return win_version
    elif running_on_mac_os():
        return mac_version
    elif running_on_linux() and linux_version:
        return linux_version
    else:
        return win_version
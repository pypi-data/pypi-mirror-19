# -*- coding: utf-8 -*-

from distutils.version import StrictVersion
import importlib
from logging import exception, warning, debug
import os.path
import sys
from tkinter import ttk, messagebox
import traceback

from thonny import ui_utils
from thonny.code import EditorNotebook
from thonny.common import Record, ToplevelCommand, UserError
from thonny.config import ConfigurationManager
from thonny.misc_utils import running_on_mac_os
from thonny.ui_utils import sequence_to_accelerator, AutomaticPanedWindow, AutomaticNotebook,\
    create_tooltip, get_current_notebook_tab_widget, select_sequence
import tkinter as tk
import tkinter.font as tk_font
import tkinter.messagebox as tk_messagebox
from thonny.running import Runner
import thonny.globals
import logging
from thonny.globals import register_runner, get_runner
from thonny.config_ui import ConfigurationDialog
import pkgutil
import configparser
import socket
import queue
from _thread import start_new_thread
import ast
from thonny.exersys import init_exercise_system
from thonny import THONNY_USER_DIR

THONNY_PORT = 4957
SERVER_SUCCESS = "OK"
CONFIGURATION_FILE_NAME = os.path.join(THONNY_USER_DIR, "configuration.ini")
SINGLE_INSTANCE_DEFAULT = True

class Workbench(tk.Tk):
    """
    Thonny's main window and communication hub.
    
    Is responsible for:
    
        * creating the main window
        * maintaining layout (_init_containers)
        * loading plugins (_init_plugins, add_view, add_command)        
        * providing references to main components (editor_notebook and runner)
        * communication between other components (see event_generate and bind)
        * configuration services (get_option, set_option, add_defaults)
        * loading translations
        * maintaining fonts (get_font, increasing and decreasing font size)
    
    After workbench and plugins get loaded, 3 kinds of events start happening:
        
        * User events (keypresses, mouse clicks, menu selections, ...)
        * Virtual events (mostly via get_workbench().event_generate). These include:
          events reported via and dispatched by Tk event system;
          WorkbenchEvent-s, reported via and dispatched by enhanced get_workbench().event_generate.
        * Events from the background process (program output notifications, input requests,
          notifications about debugger's progress)
          
    """
    def __init__(self, server_socket=None):
        self._destroying = False
        self.initializing = True
        
        tk.Tk.__init__(self)
        tk.Tk.report_callback_exception = self._on_tk_exception
        self._event_handlers = {}
        self._select_theme()
        self._editor_notebook = None
        thonny.globals.register_workbench(self)
        
        self._init_configuration()
        self._init_diagnostic_logging()
        self._init_fonts()
        self._init_window()
        self._images = set() # to avoid Python garbage collecting them
        self._init_menu()
        
        self.title("Thonny")
        self.bind("BackendMessage", self._update_title, True)
        
        self._init_containers()
        
        self._init_runner()
            
        self._init_commands()
        init_exercise_system()
        self._load_plugins()
        
        self._update_toolbar()
        self._editor_notebook.load_startup_files()
        self._editor_notebook.focus_set()
        
        if server_socket is not None:
            self._init_server_loop(server_socket)
        
        self.initializing = False

        
    def _init_configuration(self):
        try: 
            self._configuration_manager = ConfigurationManager(CONFIGURATION_FILE_NAME)
        except configparser.Error:
            if (os.path.exists(CONFIGURATION_FILE_NAME) 
                and messagebox.askyesno("Problem", 
                    "Thonny's configuration file can't be read. It may be corrupt.\n\n"
                    + "Do you want to discard the file and open Thonny with default settings?")):
                os.remove(CONFIGURATION_FILE_NAME)
                self._configuration_manager = ConfigurationManager(CONFIGURATION_FILE_NAME)
            else:
                raise
                
        self._configuration_pages = {}

        self.add_option("general.single_instance", SINGLE_INSTANCE_DEFAULT)
        self.add_option("general.expert_mode", False)
        self.add_option("debug_mode", False)

    
    def _init_diagnostic_logging(self):
        logging.basicConfig(format='%(levelname)s:%(message)s',
            level=logging.DEBUG if self.get_option("debug_mode") else logging.INFO)
    
    def _init_window(self):
        
        self.add_option("layout.zoomed", False)
        self.add_option("layout.top", 15)
        self.add_option("layout.left", 150)
        self.add_option("layout.width", 700)
        self.add_option("layout.height", 650)
        self.add_option("layout.w_width", 200)
        self.add_option("layout.e_width", 200)
        self.add_option("layout.s_height", 200)
        
        # I don't actually need saved options for Full screen/maximize view,
        # but it's easier to create menu items, if I use configuration manager's variables
        self.add_option("view.full_screen", False)  
        self.add_option("view.maximize_view", False)
        
        # In order to avoid confusion set these settings to False 
        # even if they were True when Thonny was last run
        self.set_option("view.full_screen", False)
        self.set_option("view.maximize_view", False)
        
        
        self.geometry("{0}x{1}+{2}+{3}".format(self.get_option("layout.width"),
                                            self.get_option("layout.height"),
                                            self.get_option("layout.left"),
                                            self.get_option("layout.top")))
        
        if self.get_option("layout.zoomed"):
            ui_utils.set_zoomed(self, True)
        
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        
        icon_file = os.path.join(self.get_package_dir(), "res", "thonny.ico")
        try:
            self.iconbitmap(icon_file, default=icon_file)
        except:
            try:
                # seems to work in mac
                self.iconbitmap(icon_file)
            except:
                pass # TODO: try to get working in Ubuntu  
        
        self.bind("<Configure>", self._on_configure, True)
        
    def _init_menu(self):
        self.option_add('*tearOff', tk.FALSE)
        self._menubar = tk.Menu(self)
        self["menu"] = self._menubar
        self._menus = {}
        self._menu_item_groups = {} # key is pair (menu_name, command_label)
        self._menu_item_testers = {} # key is pair (menu_name, command_label)
        
        # create standard menus in correct order
        self.get_menu("file", "File")
        self.get_menu("edit", "Edit")
        self.get_menu("view", "View")
        self.get_menu("run", "Run")
        self.get_menu("tools", "Tools")
        self.get_menu("help", "Help")
    
    def _load_plugins(self):
        import thonny.plugins
        self._load_plugins_from_path(thonny.plugins.__path__, "thonny.plugins.")
        
        user_plugins_path = os.path.join(THONNY_USER_DIR, "plugins")
        sys.path.append(user_plugins_path)
        self._load_plugins_from_path([user_plugins_path])
        
    def _load_plugins_from_path(self, path, prefix=""):
        for _, module_name, _ in pkgutil.iter_modules(path, prefix):
            try:
                m = importlib.import_module(module_name)
                if hasattr(m, "load_plugin"):
                    m.load_plugin()
            except:
                exception("Failed loading plugin '" + module_name + "'")
    
                                
    def _init_fonts(self):
        self.add_option("view.io_font_family", 
                        "Courier" if running_on_mac_os() else "Courier New")
        
        default_editor_family = "Courier New"
        families = tk_font.families()
        
        for family in ["Consolas", "Ubuntu Mono", "Menlo", "DejaVu Sans Mono"]:
            if family in families:
                default_editor_family = family
                break
        
        self.add_option("view.editor_font_family", default_editor_family)
        self.add_option("view.editor_font_size", 
                        14 if running_on_mac_os() else 11)

        default_font = tk_font.nametofont("TkDefaultFont")

        self._fonts = {
            'IOFont' : tk_font.Font(family=self.get_option("view.io_font_family")),
            'EditorFont' : tk_font.Font(family=self.get_option("view.editor_font_family")),
            'BoldEditorFont' : tk_font.Font(family=self.get_option("view.editor_font_family"),
                                            weight="bold"),
            'ItalicEditorFont' : tk_font.Font(family=self.get_option("view.editor_font_family"),
                                            slant="italic"),
            'BoldItalicEditorFont' : tk_font.Font(family=self.get_option("view.editor_font_family"),
                                            weight="bold", slant="italic"),
            'TreeviewFont' : tk_font.Font(family=default_font.cget("family"),
                                          size=default_font.cget("size"))
        }
        
        self.update_fonts()
        
    def _init_runner(self):
        try:
            register_runner(Runner())
            get_runner().send_command(ToplevelCommand(command="Reset"))
        except:
            self.report_exception("Error when initializing backend")
    
    def _init_server_loop(self, server_socket):
        """Socket will listen requests from newer Thonny instances,
        which try to delegate opening files to older instance"""
        self._requests_from_socket = queue.Queue()
        
        def server_loop():
            while True:
                debug("Waiting for next client")
                (client_socket, _) = server_socket.accept()
                try:
                    self._handle_socket_request(client_socket)
                except:
                    traceback.print_exc()
        
        start_new_thread(server_loop, ())
        self._poll_socket_requests()

    def _init_commands(self):
        
        self.add_command("exit", "file", "Exit",
            self._on_close, 
            default_sequence=select_sequence("<Alt-F4>", "<Command-q>"))
        
        
        self.add_command("show_options", "tools", "Options ...", self._cmd_show_options)
        self.createcommand("::tk::mac::ShowPreferences", self._cmd_show_options)
        
        self.add_command("increase_font_size", "view", "Increase font size",
            lambda: self._change_font_size(1),
            default_sequence=select_sequence("<Control-plus>", "<Command-Shift-plus>"),
            group=60)
                
        self.add_command("decrease_font_size", "view", "Decrease font size",
            lambda: self._change_font_size(-1),
            default_sequence=select_sequence("<Control-minus>", "<Command-minus>"),
            group=60)
        
        self.bind("<Control-MouseWheel>", self._cmd_zoom_with_mouse, True)
        
        self.add_command("focus_editor", "view", "Focus editor",
            self._cmd_focus_editor,
            default_sequence="<Alt-e>",
            group=70)
        
                
        self.add_command("focus_shell", "view", "Focus shell",
            self._cmd_focus_shell,
            default_sequence="<Alt-s>",
            group=70)
        
        if self.get_option("general.expert_mode"):
            
            self.add_command("toggle_maximize_view", "view", "Maximize view",
                self._cmd_toggle_maximize_view,
                flag_name="view.maximize_view",
                default_sequence=None,
                group=80)
            self.bind_class("TNotebook", "<Double-Button-1>", self._maximize_view, True)
            self.bind("<Escape>", self._unmaximize_view, True)
            
            if not running_on_mac_os():
                # TODO: approach working in Win/Linux doesn't work in mac as it should and only confuses
                self.add_command("toggle_maximize_view", "view", "Full screen",
                    self._cmd_toggle_full_screen,
                    flag_name="view.full_screen",
                    default_sequence=select_sequence("<F11>", "<Command-Shift-F>"),
                    group=80)
        
            
    def _init_containers(self):
        
        # Main frame functions as
        # - a backgroud behind padding of main_pw, without this OS X leaves white border
        # - a container to be hidden, when a view is maximized and restored when view is back home
        main_frame= ttk.Frame(self) # 
        self._main_frame = main_frame
        main_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self._maximized_view = None
        
        self._toolbar = ttk.Frame(main_frame, padding=0) # TODO: height=30 ?
        self._toolbar.grid(column=0, row=0, sticky=tk.NSEW, padx=10, pady=(5,0))
        
        self.add_option("layout.main_pw_first_pane_size", 1/3)
        self.add_option("layout.main_pw_last_pane_size", 1/3)
        self._main_pw = AutomaticPanedWindow(main_frame, orient=tk.HORIZONTAL,
            first_pane_size=self.get_option("layout.main_pw_first_pane_size"),
            last_pane_size=self.get_option("layout.main_pw_last_pane_size")
        )
        
        self._main_pw.grid(column=0, row=1, sticky=tk.NSEW, padx=10, pady=10)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        self.add_option("layout.west_pw_first_pane_size", 1/3)
        self.add_option("layout.west_pw_last_pane_size", 1/3)
        self.add_option("layout.center_pw_first_pane_size", 1/3)
        self.add_option("layout.center_pw_last_pane_size", 1/3)
        self.add_option("layout.east_pw_first_pane_size", 1/3)
        self.add_option("layout.east_pw_last_pane_size", 1/3)
        
        self._west_pw = AutomaticPanedWindow(self._main_pw, 1, orient=tk.VERTICAL,
            first_pane_size=self.get_option("layout.west_pw_first_pane_size"),
            last_pane_size=self.get_option("layout.west_pw_last_pane_size")
        )
        self._center_pw = AutomaticPanedWindow(self._main_pw, 2, orient=tk.VERTICAL,
            first_pane_size=self.get_option("layout.center_pw_first_pane_size"),
            last_pane_size=self.get_option("layout.center_pw_last_pane_size")
        )
        self._east_pw = AutomaticPanedWindow(self._main_pw, 3, orient=tk.VERTICAL,
            first_pane_size=self.get_option("layout.east_pw_first_pane_size"),
            last_pane_size=self.get_option("layout.east_pw_last_pane_size")
        )
        
        self._view_records = {}
        self._view_notebooks = {
            'nw' : AutomaticNotebook(self._west_pw, 1),
            'w'  : AutomaticNotebook(self._west_pw, 2),
            'sw' : AutomaticNotebook(self._west_pw, 3),
            
            's'  : AutomaticNotebook(self._center_pw, 3),
            
            'ne' : AutomaticNotebook(self._east_pw, 1),
            'e'  : AutomaticNotebook(self._east_pw, 2),
            'se' : AutomaticNotebook(self._east_pw, 3),
        }

        self._editor_notebook = EditorNotebook(self._center_pw)
        self._editor_notebook.position_key = 1
        self._center_pw.insert("auto", self._editor_notebook)

    def _select_theme(self):
        style = ttk.Style()
        
        if 'xpnative' in style.theme_names():
            # in Win7 'xpnative' gives better scrollbars than 'vista'
            style.theme_use('xpnative') 
        elif 'vista' in style.theme_names():
            style.theme_use('vista')
        elif 'clam' in style.theme_names():
            style.theme_use('clam')

        
    def add_command(self, command_id, menu_name, command_label, handler,
                    tester=None,
                    default_sequence=None,
                    flag_name=None,
                    skip_sequence_binding=False,
                    accelerator=None,
                    group=99,
                    position_in_group="end",
                    image_filename=None,
                    include_in_toolbar=False):
        """Adds an item to specified menu.
        
        Args:
            menu_name: Name of the menu the command should appear in.
                Standard menu names are "file", "edit", "run", "view", "help".
                If a menu with given name doesn't exist, then new menu is created
                (with label=name).
            command_label: Label for this command
            handler: Function to be called when the command is invoked. 
                Should be callable with one argument (the event or None).
            tester: Function to be called for determining if command is available or not.
                Should be callable with one argument (the event or None).
                Should return True or False.
                If None then command is assumed to be always available.
            default_sequence: Default shortcut (Tk style)
            flag_name: Used for toggle commands. Indicates the name of the boolean option.
            group: Used for grouping related commands together. Value should be int. 
                Groups with smaller numbers appear before.
        
        Returns:
            None
        """     
        
        def dispatch(event=None):
            if not tester or tester():
                denied = False
                handler()
            else:
                denied = True
                debug("Command '" + command_id + "' execution denied")
                self.bell()
                
            self.event_generate("Command", command_id=command_id, denied=denied)
        
        sequence_option_name = "shortcuts." + command_id
        self.add_option(sequence_option_name, default_sequence)
        sequence = self.get_option(sequence_option_name) 
        
        if sequence and not skip_sequence_binding:
            self.bind_all(sequence, dispatch, True)
        
        
        def dispatch_from_menu():
            # I don't like that Tk menu toggles checbutton variable
            # automatically before calling the handler.
            # So I revert the toggle before calling the actual handler.
            # This way the handler doesn't have to worry whether it
            # needs to toggle the variable or not, and it can choose to 
            # decline the toggle.
            if flag_name is not None:
                var = self.get_variable(flag_name)
                var.set(not var.get())
                
            dispatch(None)
        
        if image_filename:
            image = self.get_image(image_filename)
        else:
            image = None
        
        if not accelerator and sequence:
            accelerator = sequence_to_accelerator(sequence)
            
        menu = self.get_menu(menu_name)
        menu.insert(
            self._find_location_for_menu_item(menu_name, command_label, group, position_in_group),
            "checkbutton" if flag_name else "command",
            label=command_label,
            accelerator=accelerator,
            image=image,
            compound=tk.LEFT,
            variable=self.get_variable(flag_name) if flag_name else None,
            command=dispatch_from_menu)
        
        # remember the details that can't be stored in Tkinter objects
        self._menu_item_groups[(menu_name, command_label)] = group
        self._menu_item_testers[(menu_name, command_label)] = tester
        
        if include_in_toolbar:
            toolbar_group = self._get_menu_index(menu) * 100 + group
            self._add_toolbar_button(image, command_label, accelerator, handler, tester,
                toolbar_group)
        
    
    def add_view(self, class_, label, default_location,
                visible_by_default=False,
                default_position_key=None):
        """Adds item to "View" menu for showing/hiding given view. 
        
        Args:
            view_class: Class or constructor for view. Should be callable with single
                argument (the master of the view)
            label: Label of the view tab
            location: Location descriptor. Can be "nw", "sw", "s", "se", "ne"
        
        Returns: None        
        """
        view_id = class_.__name__
        if default_position_key == None:
            default_position_key = label
        
        self.add_option("view." + view_id + ".visible" , visible_by_default)
        self.add_option("view." + view_id + ".location", default_location)
        self.add_option("view." + view_id + ".position_key", default_position_key)
        
        self._view_records[view_id] = {
            "class" : class_,
            "label" : label,
            "location" : self.get_option("view." + view_id + ".location"),
            "position_key" : self.get_option("view." + view_id + ".position_key")
        }
        
        visibility_flag = self.get_variable("view." + view_id + ".visible")
        
        # handler
        def toggle_view_visibility():
            if visibility_flag.get():
                self.hide_view(view_id)
            else:
                self.show_view(view_id, True)
        
        self.add_command("toggle_" + view_id,
            menu_name="view",
            command_label=label,
            handler=toggle_view_visibility,
            flag_name="view." + view_id + ".visible",
            group=10,
            position_in_group="aplhabetic")
        
        if visibility_flag.get():
            self.show_view(view_id, False)
    
    def add_configuration_page(self, title, page_class):
        self._configuration_pages[title] = page_class
        
    def get_option(self, name):
        return self._configuration_manager.get_option(name)
    
    def set_option(self, name, value):
        self._configuration_manager.set_option(name, value)
        
    def add_option(self, name, default_value):
        """Registers a new option.
        
        If the name contains a period, then the part left to the (first) period
        will become the section of the option and rest will become name under that 
        section.
        
        If the name doesn't contain a period, then it will be added under section 
        "general".
         
        Don't confuse this method with Tkinter's option_add!
        """
        self._configuration_manager.add_option(name, default_value)
    
    def get_variable(self, name):
        return self._configuration_manager.get_variable(name)
    
    def get_font(self, name):
        """
        Supported names are EditorFont and BoldEditorFont
        """
        return self._fonts[name]
    
    
    def get_menu(self, name, label=None):
        """Gives the menu with given name. Creates if not created yet.
        
        Args:
            name: meant to be used as not translatable menu name
            label: translated label, used only when menu with given name doesn't exist yet
        """
        if name not in self._menus:
            menu = tk.Menu(self._menubar)
            menu["postcommand"] = lambda: self._update_menu(menu, name)
            self._menubar.add_cascade(label=label if label else name, menu=menu)
            
            self._menus[name] = menu
            if label:
                self._menus[label] = menu
                
        return self._menus[name]
    
    def get_view(self, view_id, create=True):
        if "instance" not in self._view_records[view_id]:
            if not create:
                return None
            
            class_ = self._view_records[view_id]["class"]
            location = self._view_records[view_id]["location"]
            master = self._view_notebooks[location]
            
            # create the view
            view = class_(self) # View's master is workbench to allow making it maximized
            view.position_key = self._view_records[view_id]["position_key"]
            self._view_records[view_id]["instance"] = view

            # create the view home_widget to be added into notebook
            view.home_widget = ttk.Frame(master) 
            view.home_widget.columnconfigure(0, weight=1)
            view.home_widget.rowconfigure(0, weight=1)
            view.home_widget.maximizable_widget = view
            
            # initially the view will be in it's home_widget
            view.grid(row=0, column=0, sticky=tk.NSEW, in_=view.home_widget)
            
            
        return self._view_records[view_id]["instance"]
    
    def get_current_editor(self):
        return self._editor_notebook.get_current_editor()
    
    def get_editor_notebook(self):
        return self._editor_notebook
    
    def get_package_dir(self):
        """Returns thonny package directory"""
        return os.path.dirname(sys.modules["thonny"].__file__)
    
    def get_image(self, filename, tk_name=None):
        # if path is relative then interpret it as living in res folder
        if not os.path.isabs(filename):
            filename = os.path.join(self.get_package_dir(), "res", filename)
            
        img = tk.PhotoImage(tk_name, file=filename)
        self._images.add(img)
        return img
                      
    def show_view(self, view_id, set_focus=True):
        """View must be already registered.
        
        Args:
            view_id: View class name 
            without package name (eg. 'ShellView') """

        # NB! Don't forget that view.home_widget is added to notebook, not view directly
        # get or create
        view = self.get_view(view_id)
        notebook = view.home_widget.master
        
        if hasattr(view, "before_show") and view.before_show() == False:
            return False
            
        if not view.winfo_ismapped():
            notebook.insert("auto", view.home_widget, text=self._view_records[view_id]["label"])
        
        # switch to the tab
        notebook.select(view.home_widget)
        
        # add focus
        if set_focus:
            view.focus_set()
        
        self.set_option("view." + view_id + ".visible", True)
        self.event_generate("ShowView", view=view, view_id=view_id)
    
    def hide_view(self, view_id):
        # NB! Don't forget that view.home_widget is added to notebook, not view directly
        
        if "instance" in self._view_records[view_id]:
            # TODO: handle the case, when view is maximized
            view = self._view_records[view_id]["instance"]
            
            if hasattr(view, "before_hide") and view.before_hide() == False:
                return False
            
            view.home_widget.master.forget(view.home_widget)
            
            self.set_option("view." + view_id + ".visible", False)
            
            self.event_generate("HideView", view=view, view_id=view_id)

        

    def event_generate(self, sequence, **kwargs):
        """Uses custom event handling when sequence doesn't start with <.
        In this case arbitrary attributes can be added to the event.
        Otherwise forwards the call to Tk's event_generate"""
        if sequence.startswith("<"):
            tk.Tk.event_generate(self, sequence, **kwargs)
        else:
            if sequence in self._event_handlers:
                for handler in self._event_handlers[sequence]:
                    try:
                        # Yes, I'm creating separate event object for each handler
                        # so that they can't misuse the mutabilty
                        event = WorkbenchEvent(sequence, **kwargs)
                        handler(event)
                    except:
                        self.report_exception("Problem when handling '" + sequence + "'")
                
    def bind(self, sequence, func, add=None):
        """Uses custom event handling when sequence doesn't start with <.
        Otherwise forwards the call to Tk's bind"""
        
        if not add:
            warning("Workbench.bind({}, ..., add={}) -- did you really want to replace existing bindings?".format(sequence, add))
        
        if sequence.startswith("<"):
            tk.Tk.bind(self, sequence, func, add)
        else:
            if sequence not in self._event_handlers or not add:
                self._event_handlers[sequence] = set()
                
            self._event_handlers[sequence].add(func)

    def unbind(self, sequence, funcid=None):
        if sequence.startswith("<"):
            tk.Tk.unbind(self, sequence, funcid=funcid)
        else:
            if (sequence in self._event_handlers 
                and funcid in self._event_handlers[sequence]):
                self._event_handlers[sequence].remove(funcid)
                

    def get_version(self):
        try:
            with open(os.path.join(self.get_package_dir(), "VERSION"), encoding="ASCII") as fp:
                version_str = fp.read().strip()
            return StrictVersion(version_str)
        except:
            return StrictVersion("0.0")
      
    
    def in_heap_mode(self):
        # TODO: add a separate command for enabling the heap mode 
        # untie the mode from HeapView
        
        return (self._configuration_manager.has_option("view.HeapView.visible")
            and self.get_option("view.HeapView.visible"))
    
    def update_fonts(self):
        editor_font_size = self._guard_font_size(self.get_option("view.editor_font_size"))
        editor_font_family = self.get_option("view.editor_font_family")
        io_font_family = self.get_option("view.io_font_family")
        
        self.get_font("IOFont").configure(family=io_font_family,
                                          size=min(editor_font_size - 2,
                                                   int(editor_font_size * 0.8 + 3)))
        self.get_font("EditorFont").configure(family=editor_font_family,
                                              size=editor_font_size)
        self.get_font("BoldEditorFont").configure(family=editor_font_family,
                                                  size=editor_font_size)
        self.get_font("ItalicEditorFont").configure(family=editor_font_family,
                                                  size=editor_font_size)
        self.get_font("BoldItalicEditorFont").configure(family=editor_font_family,
                                                  size=editor_font_size)
        
        
        style = ttk.Style()
        if running_on_mac_os():
            treeview_font_size = int(editor_font_size * 0.7 + 4)
            rowheight = int(treeview_font_size*1.2 + 4 )
        else:
            treeview_font_size = int(editor_font_size * 0.7 + 2)
            rowheight = int(treeview_font_size * 2.0 + 6)
            
        self.get_font("TreeviewFont").configure(size=treeview_font_size)
        style.configure("Treeview", rowheight=rowheight)
        
        if self._editor_notebook is not None:
            self._editor_notebook.update_appearance()
        
    
    def _get_menu_index(self, menu):
        for i in range(len(self._menubar.winfo_children())):
            if menu == self._menubar.winfo_children()[i]:
                return i
        else:
            return None
    
    def _add_toolbar_button(self, image, command_label, accelerator, handler, 
                            tester, toolbar_group):
        
        slaves = self._toolbar.grid_slaves(0, toolbar_group)
        if len(slaves) == 0:
            group_frame = ttk.Frame(self._toolbar)
            group_frame.grid(row=0, column=toolbar_group, padx=(0, 10))
        else:
            group_frame = slaves[0]
        
        button = ttk.Button(group_frame, 
                         command=handler, 
                         image=image, 
                         style="Toolbutton", # TODO: does this cause problems in some Macs?
                         state=tk.NORMAL
                         )
        button.pack(side=tk.LEFT)
        button.tester = tester 
        create_tooltip(button, command_label 
                       + (" (" + accelerator + ")" if accelerator else ""))
        
    def _update_toolbar(self):
        for group_frame in self._toolbar.grid_slaves(0):
            for button in group_frame.pack_slaves():
                if button.tester and not button.tester():
                    button["state"] = tk.DISABLED
                else:
                    button["state"] = tk.NORMAL
        
        self.after(300, self._update_toolbar)
            
    
    def _cmd_zoom_with_mouse(self, event):
        if event.delta > 0:
            self._change_font_size(1)
        else:
            self._change_font_size(-1)
    
    def _change_font_size(self, delta):
        
        if delta != 0:
            editor_font_size = self.get_option("view.editor_font_size")
            editor_font_size += delta
            self.set_option("view.editor_font_size", self._guard_font_size(editor_font_size))
            self.update_fonts()
    
    def _guard_font_size(self, size):
        # https://bitbucket.org/plas/thonny/issues/164/negative-font-size-crashes-thonny
        MIN_SIZE = 4
        MAX_SIZE = 200
        if size < MIN_SIZE:
            return MIN_SIZE
        elif size > MAX_SIZE:
            return MAX_SIZE
        else:
            return size
        
        
    
    def _check_update_window_width(self, delta):
        if not ui_utils.get_zoomed(self):
            self.update_idletasks()
            # TODO: shift to left if right edge goes away from screen
            # TODO: check with screen width
            new_geometry = "{0}x{1}+{2}+{3}".format(self.winfo_width() + delta,
                                                   self.winfo_height(),
                                                   self.winfo_x(), self.winfo_y())
            
            self.geometry(new_geometry)
            
    
    def _maximize_view(self, event=None):
        if self._maximized_view is not None:
            return
        
        # find the widget that can be relocated
        widget = self.focus_get()
        if isinstance(widget, EditorNotebook) or isinstance(widget, AutomaticNotebook):
            current_tab = get_current_notebook_tab_widget(widget)
            if current_tab is None:
                return
            
            if not hasattr(current_tab, "maximizable_widget"):
                return
            
            widget = current_tab.maximizable_widget
        
        while widget is not None:
            if hasattr(widget, "home_widget"):
                # if widget is view, then widget.master is workbench
                widget.grid(row=0, column=0, sticky=tk.NSEW, in_=widget.master)
                # hide main_frame
                self._main_frame.grid_forget()
                self._maximized_view = widget
                self.get_variable("view.maximize_view").set(True)
                break
            else:
                widget = widget.master
    
    def _unmaximize_view(self, event=None):
        if self._maximized_view is None:
            return
        
        # restore main_frame
        self._main_frame.grid(row=0, column=0, sticky=tk.NSEW, in_=self)
        # put the maximized view back to its home_widget
        self._maximized_view.grid(row=0, column=0, sticky=tk.NSEW, in_=self._maximized_view.home_widget)
        self._maximized_view = None
        self.get_variable("view.maximize_view").set(False)
    
    def _cmd_show_options(self):
        dlg = ConfigurationDialog(self, self._configuration_pages)
        dlg.focus_set()
        dlg.transient(self)
        dlg.grab_set()
        self.wait_window(dlg)
    
    def _cmd_focus_editor(self):
        self._editor_notebook.focus_set()
    
    def _cmd_focus_shell(self):
        self.show_view("ShellView", True)
    
    def _cmd_toggle_full_screen(self):
        var = self.get_variable("view.full_screen")
        var.set(not var.get())
        self.attributes("-fullscreen", var.get())
    
    def _cmd_toggle_maximize_view(self):
        if self._maximized_view is not None:
            self._unmaximize_view()
        else:
            self._maximize_view()
            
            
    
    def _update_menu(self, menu, menu_name):
        if menu.index("end") == None:
            return
        
        for i in range(menu.index("end")+1):
            item_data = menu.entryconfigure(i)
            if "label" in item_data:
                command_label = menu.entrycget(i, "label")
                tester = self._menu_item_testers[(menu_name, command_label)]

                if tester and not tester():
                    menu.entryconfigure(i, state=tk.DISABLED)
                else:
                    menu.entryconfigure(i, state=tk.ACTIVE)   
                    
                    
        
    
    def _find_location_for_menu_item(self, menu_name, command_label, group,
            position_in_group="end"):        
        
        menu = self.get_menu(menu_name)
        
        if menu.index("end") == None: # menu is empty
            return "end"
        
        this_group_exists = False
        for i in range(0, menu.index("end")+1):
            data = menu.entryconfigure(i)
            if "label" in data:
                # it's a command, not separator
                sibling_label = menu.entrycget(i, "label")
                sibling_group = self._menu_item_groups[(menu_name, sibling_label)]

                if sibling_group == group:
                    this_group_exists = True
                    if position_in_group == "aplhabetic" and sibling_label > command_label:
                        return i
                    
                if sibling_group > group:
                    assert not this_group_exists # otherwise we would have found the ending separator
                    menu.insert_separator(i)
                    return i
            else:
                # We found a separator
                if this_group_exists: 
                    # it must be the ending separator for this group
                    return i
                
        else:
            # no group was bigger, ie. this should go to the end
            if not this_group_exists:
                menu.add_separator()
                
            return "end"

    def _handle_socket_request(self, client_socket):
        """runs in separate thread"""
        # read the request
        data = bytes()
        while True:
            new_data = client_socket.recv(1024)
            if len(new_data) > 0:
                data += new_data
            else:
                break
        
        self._requests_from_socket.put(data)
        
        # respond OK
        client_socket.sendall(SERVER_SUCCESS.encode(encoding='utf-8'))
        client_socket.shutdown(socket.SHUT_WR)
        print("AFTER NEW REQUEST", client_socket)
    
    def _poll_socket_requests(self):
        """runs in gui thread"""
        try:
            while not self._requests_from_socket.empty():
                data = self._requests_from_socket.get()
                args = ast.literal_eval(data.decode("UTF-8"))
                assert isinstance(args, list)
                for filename in args:
                    if os.path.exists(filename):
                        self._editor_notebook.show_file(filename)
                        
                self.become_topmost_window()
        finally:
            self.after(50, self._poll_socket_requests)

    def _on_close(self):
        if not self._editor_notebook.check_allow_closing():
            return
        
        try:
            self._save_layout()
            #ui_utils.delete_images()
            self.event_generate("WorkbenchClose")
        except:
            self.report_exception()

        self.destroy()
    
    def focus_get(self):
        try:
            return tk.Tk.focus_get(self)
        except:
            # This may give error in Ubuntu
            return None
    
    def destroy(self):
        try:
            self._destroying = True
            tk.Tk.destroy(self)
        except tk.TclError:
            exception("Error while destroying workbench")
        finally:
            runner = get_runner()
            if runner != None:
                runner.kill_backend()
    
    def _on_configure(self, event):
        # called when window is moved or resized
        if (hasattr(self, "_maximized_view") # configure may happen before the attribute is defined 
            and self._maximized_view):
            # grid again, otherwise it acts weird
            self._maximized_view.grid(row=0, column=0, sticky=tk.NSEW, in_=self._maximized_view.master)
    
    def _on_tk_exception(self, exc, val, tb):
        # copied from tkinter.Tk.report_callback_exception with modifications
        # see http://bugs.python.org/issue22384
        sys.last_type = exc
        sys.last_value = val
        sys.last_traceback = tb
        self.report_exception()
    
    def report_exception(self, title="Internal error"):
        exception(title)
        if tk._default_root and not self._destroying:
            (typ, value, _) = sys.exc_info()
            if issubclass(typ, UserError):
                msg = str(value)
            else:
                msg = traceback.format_exc()
            tk_messagebox.showerror(title, msg)
    
        
    def _save_layout(self):
        self.update_idletasks()
        
        self.set_option("layout.zoomed", ui_utils.get_zoomed(self))
        
        # each AutomaticPanedWindow remember it's splits for both 2 and 3 panes
        self.set_option("layout.main_pw_first_pane_size", self._main_pw.first_pane_size)
        self.set_option("layout.main_pw_last_pane_size", self._main_pw.last_pane_size)
        self.set_option("layout.east_pw_first_pane_size", self._east_pw.first_pane_size)
        self.set_option("layout.east_pw_last_pane_size", self._east_pw.last_pane_size)
        self.set_option("layout.center_pw_last_pane_size", self._center_pw.last_pane_size)
        self.set_option("layout.west_pw_first_pane_size", self._west_pw.first_pane_size)
        self.set_option("layout.west_pw_last_pane_size", self._west_pw.last_pane_size)
                
        if not ui_utils.get_zoomed(self):
            self.set_option("layout.top", self.winfo_y())
            self.set_option("layout.left", self.winfo_x())
            self.set_option("layout.width", self.winfo_width())
            self.set_option("layout.height", self.winfo_height())
        
        self._configuration_manager.save()
    
    #def focus_set(self):
    #    tk.Tk.focus_set(self)
    #    self._editor_notebook.focus_set()
    
    def _update_title(self, event):
        self.title("Thonny  -  Python {1}.{2}.{3}  -  {0}".format(self._runner.get_cwd(), *sys.version_info))
    
    def become_topmost_window(self):
        self.deiconify()
        self.attributes('-topmost', True)
        self.after_idle(self.attributes, '-topmost', False)
        self.focus_set()
        self.lift()
    

class WorkbenchEvent(Record):
    def __init__(self, sequence, **kwargs):
        Record.__init__(self, **kwargs)
        self.sequence = sequence


import tkinter as tk
from jedi import Script
from jedi.parser import tree
from thonny.globals import get_workbench
from jedi.parser.tree import Function
import logging

class LocalsHighlighter:

    def __init__(self, text, local_variable_font=None):
        self.text = text
        
        if local_variable_font:
            self.local_variable_font=local_variable_font
        else:
            self.local_variable_font = self.text["font"]
        
        self._configure_tags()
        self._update_scheduled = False
        
    def get_positions(self):

        locs = []

        def process_scope(scope):
            if isinstance(scope, Function):
                # process all children after name node,
                # (otherwise name of global function will be marked as local def)
                local_names = set() 
                global_names = set()
                for child in scope.children[2:]:
                    process_node(child, local_names, global_names)
            else:
                for child in scope.subscopes:
                    process_scope(child)
        
        def process_node(node, local_names, global_names):
            if isinstance(node, tree.GlobalStmt):
                global_names.update([n.value for n in node.get_global_names()])
                
            elif isinstance(node, tree.Name):
                if node.value in global_names:
                    return
                
                if node.is_definition(): # local def
                    locs.append(node)
                    local_names.add(node.value)
                elif node.value in local_names: # use of local 
                    locs.append(node)
                    
            elif isinstance(node, tree.BaseNode):
                # ref: jedi/parser/grammar*.txt
                if node.type == "trailer" and node.children[0].value == ".":
                    # this is attribute
                    return
                
                if isinstance(node, tree.Function):
                    global_names = set() # outer global statement doesn't have effect anymore
                
                for child in node.children:
                    process_node(child, local_names, global_names)

        def process_module():
            for child in module.children:
                if isinstance(child, tree.BaseNode) and child.is_scope():
                    process_scope(child)

        index = self.text.index("insert").split(".")
        line, column = int(index[0]), int(index[1])
        script = Script(self.text.get('1.0', 'end'), line, column)
        module = script._parser.module()

        process_module()

        loc_pos = set(("%d.%d" % (usage.start_pos[0], usage.start_pos[1]),
                "%d.%d" % (usage.start_pos[0], usage.start_pos[1] + len(usage.value)))
                for usage in locs)

        return loc_pos

    def _configure_tags(self):
        self.text.tag_configure("LOCAL_NAME",
                                font=self.local_variable_font, 
                                foreground="#000055")
        self.text.tag_raise("sel")
        
    def _highlight(self, pos_info):
        for pos in pos_info:
            start_index, end_index = pos[0], pos[1]
            self.text.tag_add("LOCAL_NAME", start_index, end_index)

    def schedule_update(self):
        def perform_update():
            try:
                self.update()
            finally:
                self._update_scheduled = False
        
        if not self._update_scheduled:
            self._update_scheduled = True
            self.text.after_idle(perform_update)
            
    def update(self):
        self.text.tag_remove("LOCAL_NAME", "1.0", "end")
        
        if get_workbench().get_option("view.locals_highlighting"):
            try:
                highlight_positions = self.get_positions()
                self._highlight(highlight_positions)
            except:
                logging.exception("Problem when updating local variable tags")


def update_highlighting(event):
    assert isinstance(event.widget, tk.Text)
    text = event.widget
    
    if not hasattr(text, "local_highlighter"):
        text.local_highlighter = LocalsHighlighter(text,
            get_workbench().get_font("ItalicEditorFont"))
        
    text.local_highlighter.schedule_update()


def load_plugin():
    wb = get_workbench()
    wb.add_option("view.locals_highlighting", True)
    wb.bind_class("CodeViewText", "<<TextChange>>", update_highlighting, True)
    wb.bind("<<UpdateAppearance>>", update_highlighting, True)
    

def _experiment_with_jedi():
    prog = """
def fun():
    pass
"""
    script = Script(prog, 1, 0)
    module = script._parser.module()
    
    def print_node(node, level):
        print("  "  * level, type(node), node.type,
              node.value if hasattr(node, "value") else "")
        
        if isinstance(node, tree.BaseNode):
            for child in node.children:
                print_node(child, level+1)
            
    print_node(module, 0)

if __name__ == "__main__":
    _experiment_with_jedi()
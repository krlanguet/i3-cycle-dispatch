#!/usr/bin/env python3

# Module imports
from sys import argv                # Generating command line interface
from neovim import attach           # Sending focus commands to nvim
from i3ipc import Connection        # Identifying focused window and context, and sending focus commands

# Local imports
from i3 import *
#from nvim import *

#
# Logging
#
'''
from os import path, getenv         # Creating log file
from logging import getLogger, FileHandler, INFO, DEBUG
'''
#import traceback
#import psutil

#log = getLogger(__name__)
#log.setLevel(DEBUG)
#log.setLevel(INFO)
#log.addHandler(FileHandler(path.join(getenv("HOME","") , "i3cd.log"), delay=False))
#
# End of Logging
#


# Main function : Determines appropriate dispatch function given context
def i3cd(command = argv[1],     # focus|move
         target = argv[2],      # container|tab
         direction = argv[3]    # left|right|up|down
    ):
    print(command, target, direction)
    

    focus_name = get_focused_window_name()
    if command == 'focus':
        if target == 'container':
            if focus_name.startswith('nvim'):
                print('neovim!')



#################################### ^ Refactored Code ^ ########################################

'''


connection = Connection()
root = connection.get_tree()
focus_con = root.find_focused()

if command == 'focus' and target == 'container':
    if regex_nvim.match():
        success = change_focus_nvim(direction)

        if not success:
            tree = i3tree(root)
            change_focus_container_i3(tree, direction)

"""
Sup <l | ;> command.
    If current focus is qutebrowser,
        
    Else if current focus is descendent of tab-container,
        Focus ancestor that is direct child of tab-container
        If ancestor has sibling in <direction>,
            Focus sibling
        Else,
            Cycle sibling


Exit value:
0 => success
1 => failure
"""
directions = {
        'left' : 'h',
        'right' : "l",
        'up': 'k',
        'down': 'j',
}



def get_dispatcher():
        name = get_focused_window_name()
        #log.debug("Window name=%s" % name)
# if we are focusing neovim
        if name.endswith("NVIM"):
                return nvim_dispatcher
        return i3_dispatcher


'''

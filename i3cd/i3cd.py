#!/usr/bin/env python3

# Module imports
from sys import argv                # Generating command line interface

# Local imports
from i3cd.i3 import get_focused_window_name, i3_focus_container_dispatcher, i3_focus_tab_dispatcher
from i3cd.i3 import i3_move_container_dispatcher, i3_move_tab_dispatcher
from i3cd.nvim import nvim_focus_dispatcher, nvim_move_dispatcher

#
# Logging
#
'''
from os import path, getenv         # Creating log file
from logging import getLogger, FileHandler, INFO, DEBUG
'''
#import traceback

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

    focus_name, focus_con, i3_root, i3_connection = get_focused_window_name()
    if command == 'focus':
        if target == 'container':
            if focus_name.startswith('nvim'):
                success = nvim_focus_dispatcher(direction)

                if not success:
                    i3_focus_container_dispatcher(i3_connection, i3_root, focus_con, direction)

            else:
                i3_focus_container_dispatcher(i3_connection, i3_root, focus_con, direction)

        elif target == 'tab':
            i3_focus_tab_dispatcher(i3_connection, i3_root, focus_con, direction)

        else:
            raise Exception('target value: ' + target + ' is invalid')

    elif command == 'move':
        raise Exception('Command move is currently unimplemented')
        '''
        Sup <l | ;> command.
            If current focus is qutebrowser,
                
            Else if current focus is descendent of tab-container,
                Focus ancestor that is direct child of tab-container
                If ancestor has sibling in <direction>,
                    Focus sibling
                Else,
                    Cycle sibling
        '''

    else:
        raise Exception('command: ' + command + '{} is invalid')


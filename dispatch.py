
from sys import argv
from re import compile
from i3ipc import Connection


command = argv[1]    # focus|move
target = argv[2]     # container|tab
direction = argv[3]  # left|right|up|down




connection = Connection()
root = connection.get_tree()
focus_con = root.find_focused()

if command == 'focus' and target == 'container':
    if regex_nvim.match():
        success = change_focus_nvim(direction)

        if not success:
            tree = i3tree(root)
            change_focus_container_i3(tree, direction)

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

#!/usr/bin/env python
from neovim import attach
import argparse
import subprocess
import os
import traceback
import logging
import psutil


log = logging.getLogger(__name__)
# log.setLevel(logging.INFO)
log.setLevel(logging.DEBUG)

log.addHandler(logging.FileHandler(os.path.join(os.getenv("HOME","") , "i3dispatch.log"), delay=False))

"""
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

regex_nvim = compile('^nvim')
regex_qutebrowser = compile('^.') # TODO


def get_dispatcher():
        name = get_focused_window_name()
        log.debug("Window name=%s" % name)
# if we are focusing neovim
        if name.endswith("NVIM"):
                return nvim_dispatcher
        return i3_dispatcher

def get_focused_window_name():
        try:
                out = subprocess.check_output("xdotool getwindowfocus getwindowname", shell=True).decode('utf-8').rstrip()
                return out
        except Exception as e:
                log.error(e)
        return ""


"""
Program starts here
"""
# TODO we can set NVIM_LISTEN_ADDRESS before hand
parser = argparse.ArgumentParser(description="parameter to send to wincmd")
parser.add_argument("direction", choices=directions.keys())
parser.add_argument("--test", action="store_const", const=True)

args = parser.parse_args()

"""
get dispatcher function
"""
dispatcher = get_dispatcher()

log.info("Calling dispatcher %r with direction %s" % (dispatcher, args.direction))
# dispatcher("toto")
# if anything failed or nvim didn't change buffer focus, we forward the command o i3
if not dispatcher(args.direction):
        i3_dispatcher(args.direction)
exit(0)

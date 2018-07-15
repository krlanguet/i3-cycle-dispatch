#!/usr/bin/env python3
                                    # Generating command line interface
from click import group, option, argument, Choice, pass_context, make_pass_decorator
from re import compile              # Identifying focused window
from neovim import attach           # Sending focus commands to nvim
from i3ipc import Connection        # Identifying focused window and context, and sending focus commands
from subprocess import check_output # Spawining xdotool process to ID focused window

#
# Logging
#
from os import path, getenv         # Creating log file
from logging import getLogger, FileHandler, INFO, DEBUG
#import traceback
#import psutil

# Might be better handled with inheritance
class Log():
    def __init__(self, debug, debug_level):
        if debug:
            self.log = getLogger(__name__)
            levels = {'Info': INFO, 'Verbose': DEBUG}
            self.log.setLevel(levels[debug_level])
            self.log.addHandler(FileHandler(path.join(getenv("HOME","") , "i3cd.log"), delay=False))
        else:
            self.log = None

    def info(message):
        if self.log:
            self.log.info(message)

    def debug(message):
        if self.log:
            self.log.debug(message)
pass_log = make_pass_decorator(Log)


@group()
@option('--debug', is_flag=True, default=False)
@option('--debug-level', type=Choice(['Info', 'Verbose']), default='Info', help='Note: Is ignored without explicit --debug.')
@pass_context
def i3cd(ctx, debug, debug_level):
    log = Log(debug, debug_level)
    ctx.obj = log

@i3cd.group()
@pass_log
def focus(log):
    pass

@focus.command()
@argument('direction')
@pass_log
def container(log, direction):
    pass

@focus.command()
@argument('direction')
@pass_log
def tab(log, direction):
    pass

@i3cd.group()
@pass_log
def move(log):
    pass

@move.command()
@argument('direction')
@pass_log
def container(log, direction):
    pass

@move.command()
@argument('direction')
@pass_log
def tab(log, direction):
    pass
#################################### ^ Refactored Code ^ ########################################

'''


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

'''

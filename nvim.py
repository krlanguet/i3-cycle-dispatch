
# Keys used internally by nvim for direction
nvim_d = {'left': 'h', 'right': 'l', 'up': 'k', 'down': 'j'}

def change_focus_nvim(direction):
    con_nvim = ''
    cur_nvim_window_num = '' #con_nvim.command('winnr')
    #con_nvim.command('wincmd ' + nvim_d[direction])
    return not True #cur_nvim_window_num == con_nvim.command('winnr')

def nvim_dispatcher(direction):
        print("TRIDI")
        log.info("NVIM detected")
        res, socket = get_nvim_socket()

        if not res:
                log.error("Could not find vim socket")
        elif send_nvim_wincmd(socket, directions[direction]):
                log.debug("nvim changed its focus")
                # if neovim succeeded changing buffer 
                return True
        else:
                log.debug("nvim did not change focus")
        return False

def get_nvim_socket():
        """
        1/ get pid of focused window
        2/ look for nvim processes in its children
        3/ search for socket name in the nvim child process
        """
        try:
                pid = subprocess.check_output("xdotool getwindowfocus getwindowpid", shell=True).decode()
                pid = pid.rstrip()
                pid = int(pid)
                log.debug("Retreived terminal pid %d, nvim should be one of its children" % pid)
                proc = psutil.Process( pid)
                log.debug( "proc name %s with %d children" % (proc.name(), len(proc.children(recursive=True))))
                for child in proc.children(recursive=True):
                        log.debug("child name & pid %s/%d" % (child.name(), child.pid))
                        if child.name() == "nvim":
                                unix_sockets = child.connections(kind="unix")
                                log.debug("Found an nvim subprocess with %d " % len(unix_sockets))
                                # look for socket 
                                # for filename, fd in child.open_files():
                                # log.debug("Open file %s " % filename)
                                for con in unix_sockets:
                                        filename = con.laddr
                                        log.debug("Socket %s " % filename)
                                        if "/tmp/nvim" in filename:
                                                log.debug("Found a match: %s" % filename) 
                                                return True, filename
                                return False, ""
        except Exception as e:
                log.error('Could not find neovim socket %s' % e)
                log.error(traceback.format_exc())
                return False, ""

        # instead of using psutil one could do sthg like:
        # lsof -a -U -p 15684 -F n | grep /tmp/nvim |head -n1

def send_nvim_wincmd(path_to_socket, direction):
        log.info("Sending %s to socket %s" % (direction, path_to_socket))
        try:
                # path=os.environ["NVIM_LISTEN_ADDRESS"]
                # https://github.com/neovim/python-client/issues/124
                nvim = attach('socket', path=path_to_socket)
                log.debug("nvim attached")
                nvim.command('let oldwin = winnr()') 
                nvim.command('wincmd ' + direction)
                res = nvim.eval('oldwin != winnr()')
                log.debug("Result of command %d" % res)
                return res
        except Exception as e:
                log.error("Exception %s" % e)
                return False

        return False

from i3ipc import Connection        # Identifying context and sending focus commands

# Uses i3ipcs to get name of currently focused window. Slower than xdotool, but saves time in the case that
#  i3_focus_dispatcher gets called anyways.
def get_focused_window_name():
    connection = Connection()
    root = connection.get_tree()
    focus_con = root.find_focused()

    return focus_con.name, focus_con, root, connection

def i3_focus_container_dispatcher(i3_connection, i3_root, focus_con, direction):
    tree = i3tree(i3_root)
    focus_node = tree.id_table[focus_con.id]

    ancestor, ancestral_degree = find_tab_ancestor(focus_node)

    # If current focus is somewhere inside a tab-container
    if ancestor:
        # If current focus is direct child of tab-container,
        if ancestral_degree == 0:
            i3_connection.command('focus parent; focus ' + direction)

        # Current focus is descendent but not child of tab-container
        else:
            
            # If has neighbor within current tab, focus it
            if not check_against_boundary(focus_node, ancestor, direction):
                i3_connection.command('focus ' + direction)

            elif check_against_boundary(focus_node, tree.root, direction):
                pass
                # TODO : cycle through containers in current tab

            # Next container in direction is outside tab-container
            else:
                ancestor.parent.raw_node.command('focus; focus ' + direction)

    # Current focus is not inside a tab-container
    else:
        i3_connection.command('focus ' + direction)
    
    return True


def i3_focus_tab_dispatcher(i3_connection, i3_root, focus_con, direction):
    if direction not in ['left', 'right']:
        raise Exception('direction: ' + direction + ' is not a valid focus tab  direction')

    tree = i3tree(i3_root)
    focus_node = tree.id_table[focus_con.id]

    ancestor, ancestral_degree = find_tab_ancestor(focus_node)

    if ancestor:
        ancestor.raw_node.command('focus; focus ' + direction)
        # TODO : cycle through tabs


def i3_move_container_dispatcher():
    pass
def i3_move_tab_dispatcher():
    pass
            
class i3tree:
    # self.id_table : dictionary of id: node pairs
    # self.root     : root node

    def __init__(self, raw_tree):
        self.id_table = {}
        self.root = i3tree.Node(self, raw_tree)

    class Node:
        # self.id
        # self.parent
        # self.children
        # self.raw_node

        def __init__(self, i3tree, raw_node, parent=None):
            self.id = raw_node.id
            self.layout = raw_node.layout
            self.parent = parent
            self.children = []
            for child in raw_node.nodes:
                self.children.append(i3tree.Node(i3tree, child, self))
            self.raw_node = raw_node

            i3tree.id_table[self.id] = self


def find_tab_ancestor(node):
    ancestral_degree = 0
    while node.parent: # I don't think this is an off-by-one because the root is not interesting
        if node.parent.layout == 'tabbed':
            return node, ancestral_degree
        node = node.parent
        ancestral_degree += 1

    return False, False

def check_against_boundary(node, ancestor, direction):
    # Checks difference between currently focused node and boundary of ancestor in desired direction
    # small gap between node and boundary => no neighbor in desired direction
    # TODO make more robust, factoring in size of gaps
    # TODO Probably won't work with multi monitor setup => need to look into actual current screen size, like current workspace
    too_small = 20

    # !! Remember that in graphics, the upper left corner is (0,0)
    if direction == 'left':
        relevant_difference = node.raw_node.rect.x - ancestor.raw_node.rect.x
    elif direction == 'right':
        relevant_difference = (ancestor.raw_node.rect.x + ancestor.raw_node.rect.width) - (node.raw_node.rect.x + node.raw_node.rect.width)
    elif direction == 'up':
        relevant_difference = node.raw_node.rect.y - ancestor.raw_node.rect.y
    elif direction == 'down':
        relevant_difference = (ancestor.raw_node.rect.y + ancestor.raw_node.rect.height) - (node.raw_node.rect.y + node.raw_node.rect.height)

    return relevant_difference <= too_small



def i3_dispatcher(direction):
        cmd = "i3-msg focus %s" % (direction)
        log.info("running command: %s" % cmd)
        os.system(cmd)
        return True

            
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

        def __init__(self, i3tree, raw_node, parent=None):
            self.id = raw_node.id
            self.layout = raw_node.layout
            self.parent = parent
            self.children = []
            for child in raw_node.descendents():
                self.children.append(i3tree.Node(i3tree, child, self))

            i3tree.id_table[self.id] = self


def find_tabbed_ancestor(tree, con):
    node = tree.id_table[con.id]

    ancestral_degree = 0
    while node.parent: # I don't think this is an off-by-one because the root is not interesting
        if node.layout == 'tabbed':
            return node, ancestral_degree
        node = node.parent
        ancestral_degree += 1

    return False, False

def find_aunt_in_direction(tree, con, direction):
    pass

def change_focus_container_i3(tree, direction):
    ancestor, ancestral_degree = find_tabbed_ancestor(tree, focus_con)
    if ancestor:
        # If current focus is direct child of tab-container,
        if ancestral_degree == 1:
            pass # (Focus parent, then focus <direction>)
        
        aunt = find_tabbed_aunt(tree, focus_con, direction)
        if aunt:
            pass # Focus aunt (by id)

        # Focus ancestor, then focus <direction>
    else:
        #connection.command() # Focus <direction>
        pass

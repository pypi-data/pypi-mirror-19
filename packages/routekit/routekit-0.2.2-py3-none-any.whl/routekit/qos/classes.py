import collections


class Node(object):
    """
    Origin type for every node in the qos tree
    """
    def __init__(self):
        self._parent = None

        self.ratepct = None
        self.rate = None

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        if not isinstance(value, ClassfulNode):
            raise NodeException("Parent argument {} is not a classful node".format(value))

        if self not in value.classes:
            raise NodeException("Add node as child before establishing parent relationship")

        if value == self:
            raise NodeException("Node cannot hold itself as a parent")

        # All checks passed and we have a valid ClassfulNode target

        # Delete this node from its previous parent
        if self._parent is not None:
            self._parent._classes.remove(self)

        self._parent = value


class ClassfulNode(Node, collections.Set):
    """
    Specific class for nodes with subclasses in the tree
    """
    def __init__(self, value=None):
        super(ClassfulNode, self).__init__()

        self._classes = []

        if value is not None:
            self.append(value)

    def __iter__(self):
        return iter(self.classes)

    def __contains__(self, value):
        return value in self.classes

    def __len__(self):
        return len(self.classes)

    @property
    def classes(self):
        return self._classes

    def append(self, value):

        # Wrap standalone objects in a list
        if not isinstance(value, list):
            value = [value]

        for c in value:
            # Only allow Branch or Leaf
            if not isinstance(c, (Branch, Leaf)):
                raise NodeException("Only Branch or Leaf allowed in ClassfulNode")

            if c not in self.classes:
                # Insert parent reference into node
                self._classes.append(c)
                c.parent = self

    def remove(self, value):

        # Wrap standalone objects in a list
        if not isinstance(value, list):
            value = [value]

        for c in value:
            try:
                self._classes.remove(c)
                c._parent = None
            except ValueError:
                break


class Root(ClassfulNode):

    def __init__(self, value=None):
        super(Root, self).__init__(value)

        self.ifname = ''
        self.ifrate = None

        self.qdisc = 'hfsc'
        self.qdisc_leaf = None

    @ClassfulNode.parent.setter
    def parent(self, value):
        raise NodeException('Cannot set parent of a root node')


class Branch(ClassfulNode):

    def __init__(self, value=None):
        super(Branch, self).__init__(value)


class Leaf(Node):

    def __init__(self):
        super(Leaf, self).__init__()


class QOSException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class NodeException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

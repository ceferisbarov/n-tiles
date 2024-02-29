class Domain(list):
    """Class used to control possible values for variables."""

    def __init__(self, set):
        list.__init__(self, set)
        self._hidden = []
        self._states = []

    def resetState(self):
        self.extend(self._hidden)
        del self._hidden[:]
        del self._states[:]

    def pushState(self):
        self._states.append(len(self))

    def popState(self):
        diff = self._states.pop() - len(self)
        if diff:
            self.extend(self._hidden[-diff:])
            del self._hidden[-diff:]

    def hideValue(self, value):
        list.remove(self, value)
        self._hidden.append(value)
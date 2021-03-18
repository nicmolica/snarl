class Turnorder:
    def __init__(self, init_order):
        """ Creates a Turnorder object, which is used by the Gamemanager to handle
        the logic behind ensuring turn orders are correct.
        """
        self.init_order = init_order
        self.order = init_order.copy()
        # The first call to next should return the 0th element of init_order, and next
        # increments current, so this should be set to -1 at first.
        self.current = -1

    def eject(self, entity):
        """ Eject the entity from the turn order and modify the order to match.
        """
        if not entity in self.order:
            raise RuntimeError("Cannot eject nonexistent entity from the turn order.")
        entity_index = self.order.index(entity)
        self.order.remove(entity)
        if entity_index <= self.current:
            self._decrement()

    def add(self, entity, position = -1):
        """ Add the entity to the turn order at the given position and motify the order to match.
        """
        if position < -1:
            raise ValueError("Cannot add an entity to the turn order in a negative position.")
        if position == -1:
            self.order.append(entity)
            # perhaps change this in the future, but for now assume that added entities will need
            # to be added to future levels as well, so store them here
            self.init_order.append(entity)
        else:
            self.order.insert(position, entity)
            self.init_order.insert(position, entity)
            if position < self.current:
                self._increment()

    def _increment(self):
        """ Move to the next entity's turn.
        """
        if len(self.order) == 0:
            raise RuntimeError("You can't move to the next turn when there are no turns yet.")
        self.current = (self.current + 1) % (len(self.order))

    def _decrement(self):
        """ Move to the previous entity's turn.
        """
        if len(self.order) == 0:
            raise RuntimeError("You can't move to the previous turn when there are no turns yet.")
        self.current = (self.current - 1) % (len(self.order))

    def next(self):
        """ Jump to the next turn and return the entity whose turn it now is.
        """
        self._increment()
        return self.order[self.current]
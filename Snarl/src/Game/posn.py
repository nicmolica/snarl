class Posn:
    """ This class is used simply to reference x-y coordinates on a grid. It is a lightweight
    version of the Tile class, meant to be referential and read-only.
    """
    def __init__(self, x, y):
        """ Initialize a Posn with an x and a y coord. The only requirement is that x and y be
        non-negative.
        """
        if x < 0 or y < 0:
            raise ValueError("You cannot have a grid position with negative indices.")
        self.x = x
        self.y = y
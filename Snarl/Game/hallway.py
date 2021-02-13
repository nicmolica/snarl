from tile import Tile

class Hallway:
    """Represents a hallway that connects two rooms. Hallways are composed of
    vertical and horizontal segments.
    """
    def __init__(self, waypoints, start, end):
        """Create a new hallway that follows the given waypoints to connect door1 to door2.

        Arguments:
            waypoints(list[Tile]): the list of corners in the hallway.

        Returns:
            None
        """ 
        if type(waypoints) is not list:
            raise TypeError("Waypoints must be a list!")
        if not all([type(waypoint) is Tile for waypoint in waypoints]):
            raise TypeError("Waypoints must be a list of Posns!")
        if not type(start) == Tile and type(end) == Tile:
            raise TypeError("Doors must be Posns!")
        
        self.start = start
        self.end = end
        self.waypoints = waypoints
        self.waypoints.insert(0, self.start)
        self.waypoints.append(self.end)

        if not self.are_waypoints_valid():
            raise ValueError("Waypoints must form a sequence of horizontal and vertical segments!")

    def __eq__(self, other):
        """ Overwrite == for Hallways to enable directly checking equality.
        """
        return type(other) is Hallway and self.waypoints == other.waypoints

    def __hash__(self):
        """ Overwriting hash for Hallways because we overwrote ==.
        """
        return hash((self.waypoints, self.start, self.end))

    def are_waypoints_valid(self):
        """Determines if the waypoints will form a series of horizontal and vertical
        segments. If not, returns False.
        """
        for i in range(0, len(self.waypoints) - 1):
            this_waypoint = self.waypoints[i]
            next_waypoint = self.waypoints[i + 1]
            if not self.do_waypoints_share_axis(this_waypoint, next_waypoint):
                return False
        return True

    def do_waypoints_share_axis(self, waypoint1, waypoint2):
        """Do the given waypoints have at least one axis that is equal?
        """
        return waypoint1.x == waypoint2.x or waypoint1.y == waypoint2.y
    
    def does_it_intersect(self, other):
        """ Does this hallway intersect with the other provided hallway?
        """
        for i in range(0, len(self.waypoints) - 1):
            this_w = self.waypoints[i]
            next_w = self.waypoints[i + 1]
            print(this_w.x)
            for j in range(0, len(other.waypoints) - 1):
                this_p = other.waypoints[j]
                next_p = other.waypoints[j + 1]
                if self.does_segment_intersect(this_w, next_w, this_p, next_p):
                    return True
        return False
    
    def does_segment_intersect(self, w1, w2, p1, p2):
        """ Does the row of tiles between w1 and w2 intersect with the row of tiles
        between p1 and p2?
        """
        w_x = range(min(w1.x, w2.x), max(w1.x, w2.x) + 1)
        w_y = range(min(w1.y, w2.y), max(w1.y, w2.y) + 1)
        p_x = range(min(p1.x, p2.x), max(p1.x, p2.x) + 1)
        p_y = range(min(p1.y, p2.y), max(p1.y, p2.y) + 1)
        xflag = set(w_x).intersection(set(p_x)) != set()
        yflag = set(w_y).intersection(set(p_y)) != set()
        return xflag and yflag
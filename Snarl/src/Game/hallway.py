from .tile import Tile

class Hallway:
    """Represents a hallway that connects two rooms. Hallways are composed of
    vertical and horizontal segments.
    """
    def __init__(self, waypoints: list, door1: Tile, door2: Tile):
        """Create a new hallway that follows the given waypoints to connect door1 to door2.

        Arguments:
            waypoints(list[Tile]): the list of corners in the hallway.

        Returns:
            None
        """ 
        if type(waypoints) is not list:
            raise TypeError("Waypoints must be a list!")
        if not all([isinstance(waypoint, Tile) for waypoint in waypoints]):
            raise TypeError("Waypoints must be a list of Tiles!")
        if not (isinstance(door1, Tile) and isinstance(door2, Tile)):
            raise TypeError("Doors must be Tiles!")
        
        self.door1 = door1
        self.door2 = door2
        self.waypoints = waypoints
        self._assign_start_end_waypoints(door1, door2)

        if not self._are_waypoints_valid():
            raise ValueError("Waypoints must form a sequence of horizontal and vertical segments connecting two rooms!")

    def __eq__(self, other):
        """ Overwrite == for Hallways to enable directly checking equality.
        """
        return type(other) is Hallway and self.waypoints == other.waypoints and \
            self.door1 == other.door1 and self.door2 == other.door2

    def __hash__(self):
        """ Overwriting hash for Hallways because we overwrote ==.
        """
        return hash((str(self.waypoints), self.door1, self.door2))

    def _assign_start_end_waypoints(self, door1: Tile, door2: Tile):
        """ Place start and end waypoints inside the hallway and adjacent to the
        entrance doors, allowing duplicate waypoints to exist. If doors are
        adjacent, ensure list of waypoints is empty.
        """
        if abs(door1.x - door2.x) <= 1 and abs(door1.y - door2.y) <= 1:
            if self.waypoints != []:
                raise ValueError("Cannot have waypoints in a zero-length hallway!")
            else:
                pass
        elif self.waypoints == []:
            start_x = door1.x + (0 if door2.x == door1.x else ((door2.x - door1.x) / abs(door2.x - door1.x)))
            start_y = door1.y + (0 if door2.y == door1.y else ((door2.y - door1.y) / abs(door2.y - door1.y)))
            end_x = door2.x + (0 if door2.x == door1.x else ((door1.x - door2.x) / abs(door1.x - door2.x)))
            end_y = door2.y + (0 if door2.y == door1.y else ((door1.y - door2.y) / abs(door1.y - door2.y)))
            start = Tile(int(start_x), int(start_y))
            end = Tile(int(end_x), int(end_y))
            self.waypoints.insert(0, start)
            self.waypoints.append(end)
        else:
            first_wp = self.waypoints[0]
            last_wp = self.waypoints[len(self.waypoints) - 1]
            start_x = door1.x + (0 if first_wp.x == door1.x else ((first_wp.x - door1.x) / abs(first_wp.x - door1.x)))
            start_y = door1.y + (0 if first_wp.y == door1.y else ((first_wp.y - door1.y) / abs(first_wp.y - door1.y)))
            end_x = door2.x + (0 if last_wp.x == door2.x else ((last_wp.x - door2.x) / abs(last_wp.x - door2.x)))
            end_y = door2.y + (0 if last_wp.y == door2.y else ((last_wp.y - door2.y) / abs(last_wp.y - door2.y)))
            start = Tile(int(start_x), int(start_y))
            end = Tile(int(end_x), int(end_y))
            self.waypoints.insert(0, start)
            self.waypoints.append(end)

    def _are_waypoints_valid(self) -> bool:
        """Determines if the waypoints will form a series of horizontal and vertical
        segments. If not, returns False.
        """
        if len(self.waypoints) < 2 and not self._do_waypoints_share_axis(self.door1, self.door2):
            return False
        
        for i in range(0, len(self.waypoints) - 1):
            this_waypoint = self.waypoints[i]
            next_waypoint = self.waypoints[i + 1]
            if not self._do_waypoints_share_axis(this_waypoint, next_waypoint):
                return False
        return True

    def _do_waypoints_share_axis(self, waypoint1: Tile, waypoint2: Tile) -> bool:
        """Do the given waypoints have at least one axis that is equal?
        """
        return waypoint1.x == waypoint2.x or waypoint1.y == waypoint2.y
    
    def does_it_intersect(self, other) -> bool:
        """ Does this hallway intersect with the other provided hallway?
        """
        for i in range(0, len(self.waypoints) - 1):
            this_w = self.waypoints[i]
            next_w = self.waypoints[i + 1]
            for j in range(0, len(other.waypoints) - 1):
                this_p = other.waypoints[j]
                next_p = other.waypoints[j + 1]
                if self._does_segment_intersect(this_w, next_w, this_p, next_p):
                    return True
        return False
    
    def _does_segment_intersect(self, w1: Tile, w2: Tile, p1: Tile, p2: Tile) -> bool:
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

    def contains(self, tile: Tile) -> bool:
        """Does this hallway contain the given tile?
        """
        for i in range(0, len(self.waypoints) - 1):
            this_w = self.waypoints[i]
            next_w = self.waypoints[i + 1]
            if self._does_segment_intersect(this_w, next_w, tile, tile):
                return True
                
        return False
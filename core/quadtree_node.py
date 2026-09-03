import numpy as np

class QuadTreeNode:
    """
    QuadTree spatial subdivision node for adaptive resolution 2.5D mapping.
    """
    def __init__(self, x_min, x_max, y_min, y_max, depth=0, max_depth=6, min_size=0.5):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.depth = depth
        self.max_depth = max_depth
        self.min_size = min_size

        self.children = []
        self.is_leaf = True

        # Statistics
        self.mean_z = 0.0
        self.min_z = 0.0
        self.max_z = 0.0
        self.variance_z = 0.0
        self.point_count = 0
        self.water_depth = 0.0
        self.is_flooded = False

    @property
    def width(self):
        return self.x_max - self.x_min

    @property
    def height(self):
        return self.y_max - self.y_min

    @property
    def center(self):
        return ((self.x_min + self.x_max) / 2.0, (self.y_min + self.y_max) / 2.0)

    def contains(self, x, y):
        return (self.x_min <= x < self.x_max) and (self.y_min <= y < self.y_max)

    def subdivide(self):
        if not self.is_leaf:
            return

        mid_x = (self.x_min + self.x_max) / 2.0
        mid_y = (self.y_min + self.y_max) / 2.0
        next_depth = self.depth + 1

        self.children = [
            QuadTreeNode(self.x_min, mid_x, self.y_min, mid_y, next_depth, self.max_depth, self.min_size), # SW
            QuadTreeNode(mid_x, self.x_max, self.y_min, mid_y, next_depth, self.max_depth, self.min_size), # SE
            QuadTreeNode(self.x_min, mid_x, mid_y, self.y_max, next_depth, self.max_depth, self.min_size), # NW
            QuadTreeNode(mid_x, self.x_max, mid_y, self.y_max, next_depth, self.max_depth, self.min_size)  # NE
        ]
        self.is_leaf = False

    def build_adaptive(self, points, var_threshold=0.15):
        """
        Recursively subdivide quadtree node based on elevation variance.
        """
        self.point_count = len(points)
        if self.point_count == 0:
            self.mean_z = 0.0
            self.min_z = 0.0
            self.max_z = 0.0
            self.variance_z = 0.0
            return

        z_vals = points[:, 2]
        self.mean_z = float(np.mean(z_vals))
        self.min_z = float(np.min(z_vals))
        self.max_z = float(np.max(z_vals))
        self.variance_z = float(np.var(z_vals))

        should_split = (
            self.variance_z > var_threshold and
            self.depth < self.max_depth and
            self.width > self.min_size and
            self.point_count >= 4
        )

        if should_split:
            self.subdivide()
            mid_x = (self.x_min + self.x_max) / 2.0
            mid_y = (self.y_min + self.y_max) / 2.0

            sw_mask = (points[:, 0] < mid_x) & (points[:, 1] < mid_y)
            se_mask = (points[:, 0] >= mid_x) & (points[:, 1] < mid_y)
            nw_mask = (points[:, 0] < mid_x) & (points[:, 1] >= mid_y)
            ne_mask = (points[:, 0] >= mid_x) & (points[:, 1] >= mid_y)

            self.children[0].build_adaptive(points[sw_mask], var_threshold)
            self.children[1].build_adaptive(points[se_mask], var_threshold)
            self.children[2].build_adaptive(points[nw_mask], var_threshold)
            self.children[3].build_adaptive(points[ne_mask], var_threshold)

    def get_leaves(self):
        if self.is_leaf:
            return [self]
        leaves = []
        for child in self.children:
            leaves.extend(child.get_leaves())
        return leaves

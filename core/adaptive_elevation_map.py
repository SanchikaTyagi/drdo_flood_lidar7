import numpy as np
from core.quadtree_node import QuadTreeNode
import config

class AdaptiveElevationMap:
    """
    Manages variable-resolution 2.5D elevation mesh generated via QuadTree subdivision.
    """
    def __init__(self, x_bounds=(config.X_MIN, config.X_MAX), y_bounds=(config.Y_MIN, config.Y_MAX)):
        self.x_min, self.x_max = x_bounds
        self.y_min, self.y_max = y_bounds
        self.root = None
        self.leaves = []

    def update(self, point_cloud, var_threshold=config.ELEVATION_VARIANCE_THRESHOLD):
        self.root = QuadTreeNode(
            self.x_min, self.x_max, self.y_min, self.y_max,
            depth=0, max_depth=config.MAX_QUADTREE_DEPTH, min_size=config.MIN_CELL_SIZE
        )
        if len(point_cloud) > 0:
            self.root.build_adaptive(point_cloud.points, var_threshold=var_threshold)
        self.leaves = self.root.get_leaves()

    def update_flood_depths(self, water_surface_level):
        """
        Calculates depth = water_level - mean_elevation per leaf node.
        """
        for leaf in self.leaves:
            if leaf.point_count > 0:
                leaf.water_depth = max(0.0, water_surface_level - leaf.mean_z)
                leaf.is_flooded = leaf.water_depth > 0.05
            else:
                leaf.water_depth = 0.0
                leaf.is_flooded = False

    def get_metrics(self):
        active_cells = len(self.leaves)
        # Uniform equivalent at finest leaf resolution
        min_size = config.MIN_CELL_SIZE
        num_cols = int((self.x_max - self.x_min) / min_size)
        num_rows = int((self.y_max - self.y_min) / min_size)
        equivalent_uniform_cells = num_cols * num_rows

        reduction_pct = 0.0
        if equivalent_uniform_cells > 0:
            reduction_pct = (1.0 - (active_cells / float(equivalent_uniform_cells))) * 100.0

        return {
            "active_cells": active_cells,
            "equivalent_uniform": equivalent_uniform_cells,
            "reduction_pct": max(0.0, reduction_pct)
        }

import numpy as np

class FloodDetector:
    """
    Performs robust water-surface estimation and flood depth computation.
    """
    def __init__(self):
        self.current_water_level = 0.0

    def estimate_water_surface(self, point_cloud, nominal_water_level):
        """
        Estimates planar water surface using spatial height distribution statistics.
        """
        if len(point_cloud) == 0:
            self.current_water_level = nominal_water_level
            return nominal_water_level

        pts = point_cloud.points
        # Filter near estimated water plane level
        near_water = pts[(pts[:, 2] >= nominal_water_level - 0.5) & (pts[:, 2] <= nominal_water_level + 0.5)]
        
        if len(near_water) > 10:
            self.current_water_level = float(np.median(near_water[:, 2]))
        else:
            self.current_water_level = float(nominal_water_level)

        return self.current_water_level

    def compute_statistics(self, adaptive_map):
        leaves = adaptive_map.leaves
        if not leaves:
            return {"max_depth": 0.0, "avg_depth": 0.0, "inundated_pct": 0.0}

        depths = [leaf.water_depth for leaf in leaves if leaf.point_count > 0]
        flooded_leaves = [leaf for leaf in leaves if leaf.is_flooded and leaf.point_count > 0]

        max_depth = max(depths) if depths else 0.0
        avg_depth = sum(depths) / len(depths) if depths else 0.0
        inundated_pct = (len(flooded_leaves) / float(len(leaves))) * 100.0 if leaves else 0.0

        return {
            "max_depth": max_depth,
            "avg_depth": avg_depth,
            "inundated_pct": inundated_pct
        }

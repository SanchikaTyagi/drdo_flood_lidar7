import numpy as np

class SafeZone:
    def __init__(self, zone_id, center, elevation, area):
        self.zone_id = zone_id
        self.center = center  # (x, y)
        self.elevation = elevation
        self.area = area

class SafeZoneDetector:
    """
    Identifies dry, stable high-ground evacuation zones from the adaptive 2.5D map.
    """
    @staticmethod
    def detect_safe_zones(adaptive_map, min_area=10.0):
        dry_leaves = [
            leaf for leaf in adaptive_map.leaves
            if leaf.point_count > 0 and leaf.water_depth <= 0.01 and leaf.mean_z > 2.0
        ]

        if not dry_leaves:
            return [], 0.0

        total_dry_area = sum([leaf.width * leaf.height for leaf in dry_leaves])
        total_map_area = (adaptive_map.x_max - adaptive_map.x_min) * (adaptive_map.y_max - adaptive_map.y_min)
        high_ground_pct = (total_dry_area / float(total_map_area)) * 100.0

        # Cluster adjacent dry leaves into distinct zones
        zones = []
        zone_id = 1
        for leaf in dry_leaves:
            area = leaf.width * leaf.height
            if area >= min_area or leaf.width * leaf.height >= 1.0:
                zones.append(SafeZone(
                    zone_id=f"Zone-{zone_id:02d}",
                    center=leaf.center,
                    elevation=leaf.mean_z,
                    area=area
                ))
                zone_id += 1

        return zones[:6], high_ground_pct  # Top safe zones

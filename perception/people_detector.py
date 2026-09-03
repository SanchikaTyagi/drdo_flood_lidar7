import numpy as np
from scipy.spatial import cKDTree
import config

class DetectedSurvivor:
    def __init__(self, survivor_id, position, height, confidence):
        self.id = survivor_id
        self.position = position  # [x, y, z]
        self.height = height
        self.confidence = confidence
        self.triage_priority = "SAFE"
        self.surrounding_water_depth = 0.0
        self.dist_to_boat = 999.0

class PeopleDetector:
    """
    3D Point-Cloud perception for human survivor detection using height filtering,
    density clustering, and anthropometric constraints.
    """
    def __init__(self):
        pass

    def detect_survivors(self, non_ground_pc, water_level):
        if len(non_ground_pc) == 0:
            return []

        pts = non_ground_pc.points
        # Filter point height relative to water level
        height_above_water = pts[:, 2] - water_level
        cand_mask = (height_above_water >= 0.2) & (height_above_water <= config.SURVIVOR_MAX_HEIGHT + 0.5)
        cand_pts = pts[cand_mask]

        if len(cand_pts) == 0:
            return []

        # Euclidean 2D Spatial Clustering
        tree = cKDTree(cand_pts[:, :2])
        visited = np.zeros(len(cand_pts), dtype=bool)
        survivors = []
        survivor_counter = 1

        for i in range(len(cand_pts)):
            if visited[i]:
                continue

            indices = tree.query_ball_point(cand_pts[i, :2], r=config.SURVIVOR_CLUSTER_RADIUS)
            visited[indices] = True

            if len(indices) < config.SURVIVOR_MIN_POINTS:
                continue

            cluster = cand_pts[indices]
            x_span = np.ptp(cluster[:, 0])
            y_span = np.ptp(cluster[:, 1])
            z_span = np.ptp(cluster[:, 2])

            # Anthropometric shape verification: compact horizontal, vertical extent
            if x_span < 1.8 and y_span < 1.8 and (config.SURVIVOR_MIN_HEIGHT <= z_span <= config.SURVIVOR_MAX_HEIGHT):
                center_x = float(np.mean(cluster[:, 0]))
                center_y = float(np.mean(cluster[:, 1]))
                center_z = float(np.max(cluster[:, 2]))
                confidence = min(0.99, 0.75 + (len(indices) * 0.01))

                survivor = DetectedSurvivor(
                    survivor_id=f"P{survivor_counter:02d}",
                    position=(center_x, center_y, center_z),
                    height=float(z_span),
                    confidence=float(confidence)
                )
                survivors.append(survivor)
                survivor_counter += 1

        return survivors

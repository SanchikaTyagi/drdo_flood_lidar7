import numpy as np
from scipy.spatial import cKDTree
import config

class TrackedObject:
    def __init__(self, track_id, position, obj_type="BOAT"):
        self.track_id = track_id
        self.position = np.array(position, dtype=np.float64) # [x, y, z]
        self.previous_position = np.array(position, dtype=np.float64)
        self.velocity = np.zeros(3, dtype=np.float64)
        self.speed = 0.0
        self.heading_deg = 0.0
        self.obj_type = obj_type
        self.history = [self.position.copy()]
        self.age = 1

    def update(self, new_pos, dt=0.1):
        self.previous_position = self.position.copy()
        self.position = np.array(new_pos, dtype=np.float64)
        disp = self.position - self.previous_position
        self.velocity = disp / max(dt, 1e-5)
        self.speed = float(np.linalg.norm(self.velocity[:2]))
        if self.speed > 0.05:
            self.heading_deg = float(np.degrees(np.arctan2(disp[1], disp[0]))) % 360.0
        self.history.append(self.position.copy())
        if len(self.history) > 30:
            self.history.pop(0)
        self.age += 1

class DynamicFilter:
    """
    Frame-to-frame dynamic motion object segmentation and tracking engine.
    """
    def __init__(self):
        self.tracks = {}
        self.next_track_id = 100

    def process_frames(self, current_pc, previous_pc, dt=0.1):
        if previous_pc is None or len(previous_pc) == 0 or len(current_pc) == 0:
            return self.tracks

        tree_prev = cKDTree(previous_pc.points[:, :2])
        dists, _ = tree_prev.query(current_pc.points[:, :2])

        # Points moving faster than threshold
        moving_mask = dists > config.DYNAMIC_MOTION_THRESHOLD
        moving_pts = current_pc.points[moving_mask]

        if len(moving_pts) == 0:
            return self.tracks

        # Cluster dynamic points
        clusters = self._cluster_points(moving_pts, radius=2.5)
        
        detected_centers = []
        for cluster in clusters:
            if len(cluster) >= 3:
                center = np.mean(cluster, axis=0)
                detected_centers.append(center)

        # Track association
        unmatched_centers = list(detected_centers)
        for track_id, track in list(self.tracks.items()):
            if not unmatched_centers:
                break
            dists = [np.linalg.norm(track.position[:2] - c[:2]) for c in unmatched_centers]
            min_idx = int(np.argmin(dists))
            if dists[min_idx] < config.TRACK_ASSOCIATION_DIST:
                track.update(unmatched_centers[min_idx], dt)
                unmatched_centers.pop(min_idx)

        # Create new tracks for unassociated clusters
        for center in unmatched_centers:
            self.tracks[self.next_track_id] = TrackedObject(self.next_track_id, center, "BOAT")
            self.next_track_id += 1

        return self.tracks

    def _cluster_points(self, points, radius=2.5):
        if len(points) == 0:
            return []
        tree = cKDTree(points[:, :2])
        visited = np.zeros(len(points), dtype=bool)
        clusters = []

        for i in range(len(points)):
            if visited[i]:
                continue
            indices = tree.query_ball_point(points[i, :2], r=radius)
            visited[indices] = True
            clusters.append(points[indices])
        return clusters

    def get_boat_track(self):
        for track in self.tracks.values():
            if track.obj_type == "BOAT":
                return track
        return None

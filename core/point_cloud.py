import numpy as np

class PointCloud:
    """
    3D LiDAR Point Cloud container supporting attributes, spatial filtering, 
    bounding box extraction, and terrain separation.
    """
    def __init__(self, points=None, intensities=None, frame_id=0, timestamp=0.0):
        if points is not None and len(points) > 0:
            self.points = np.asarray(points, dtype=np.float64)
            if intensities is not None:
                self.intensities = np.asarray(intensities, dtype=np.float64)
            else:
                self.intensities = np.ones(len(self.points), dtype=np.float64) * 255.0
        else:
            self.points = np.empty((0, 3), dtype=np.float64)
            self.intensities = np.empty((0,), dtype=np.float64)

        self.frame_id = frame_id
        self.timestamp = timestamp

    def __len__(self):
        return len(self.points)

    def get_bbox(self):
        if len(self.points) == 0:
            return (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        min_p = np.min(self.points, axis=0)
        max_p = np.max(self.points, axis=0)
        return (min_p[0], max_p[0], min_p[1], max_p[1], min_p[2], max_p[2])

    def filter_by_bounds(self, x_min, x_max, y_min, y_max, z_min=-np.inf, z_max=np.inf):
        if len(self.points) == 0:
            return PointCloud([], [], self.frame_id, self.timestamp)
        mask = (
            (self.points[:, 0] >= x_min) & (self.points[:, 0] <= x_max) &
            (self.points[:, 1] >= y_min) & (self.points[:, 1] <= y_max) &
            (self.points[:, 2] >= z_min) & (self.points[:, 2] <= z_max)
        )
        return PointCloud(self.points[mask], self.intensities[mask], self.frame_id, self.timestamp)

    def separate_ground_ransac(self, max_iterations=50, distance_threshold=0.15):
        """
        RANSAC implementation for robust ground surface plane estimation.
        Returns ground PointCloud and non-ground PointCloud.
        """
        if len(self.points) < 3:
            return self, PointCloud([], [], self.frame_id, self.timestamp)

        best_inliers = []
        n_pts = len(self.points)

        for _ in range(max_iterations):
            idx = np.random.choice(n_pts, 3, replace=False)
            p1, p2, p3 = self.points[idx]
            
            v1 = p2 - p1
            v2 = p3 - p1
            normal = np.cross(v1, v2)
            norm = np.linalg.norm(normal)
            if norm < 1e-6:
                continue
            normal = normal / norm

            # Force upward orientation
            if normal[2] < 0:
                normal = -normal

            d = -np.dot(normal, p1)
            distances = np.abs(np.dot(self.points, normal) + d)
            inliers = np.where(distances < distance_threshold)[0]

            if len(inliers) > len(best_inliers):
                best_inliers = inliers

        if len(best_inliers) == 0:
            return PointCloud([], [], self.frame_id, self.timestamp), self

        mask = np.zeros(n_pts, dtype=bool)
        mask[best_inliers] = True

        ground_pc = PointCloud(self.points[mask], self.intensities[mask], self.frame_id, self.timestamp)
        non_ground_pc = PointCloud(self.points[~mask], self.intensities[~mask], self.frame_id, self.timestamp)
        return ground_pc, non_ground_pc

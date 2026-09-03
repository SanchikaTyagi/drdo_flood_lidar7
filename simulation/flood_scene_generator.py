import numpy as np

class FloodSceneGenerator:
    """
    Simulates dynamic flood disaster LiDAR point cloud frames featuring synthetic terrain,
    rising water table, buildings, stranded survivors, and moving rescue vessels.
    """
    def __init__(self, seed=42):
        np.random.seed(seed)
        self.frame_id = 0
        self.time = 0.0
        self.water_level = 0.5

        # Static Terrain Grid
        x = np.linspace(-50, 50, 110)
        y = np.linspace(-50, 50, 110)
        self.X, self.Y = np.meshgrid(x, y)
        
        # Synthetic Terrain Profile (rolling hills + central depression)
        self.Z_terrain = (
            2.5 * np.sin(self.X / 12.0) * np.cos(self.Y / 12.0) +
            0.05 * (self.X + 20)**2 / 50.0 +
            1.5
        )

        # Static Building Structures: [x_min, x_max, y_min, y_max, height]
        self.buildings = [
            (-30, -20, 15, 30, 8.0),
            (10, 25, 20, 35, 6.0),
            (-35, -20, -30, -15, 7.5),
            (15, 30, -30, -15, 9.0)
        ]

        # Stranded Survivors (Static positions on rooftops / high points)
        self.survivor_positions = [
            (-25.0, 22.0, 8.0),   # On Building 1 roof
            (18.0, -22.0, 9.0),   # On Building 4 roof
            (-10.0, -5.0, 2.1),   # Low ground survivor (flooding soon)
            (32.0, 10.0, 4.5)     # Moderate hill survivor
        ]

        # Rescue Boat Trajectory (Moving dynamic object)
        self.boat_x = -40.0
        self.boat_y = -40.0

    def step(self):
        """
        Advance simulation time step, update water level, and synthesize LiDAR frame.
        """
        self.frame_id += 1
        self.time += 0.5
        self.water_level += 0.04  # Rising water level

        # Update Boat Trajectory
        self.boat_x += 0.6
        self.boat_y += 0.45

        pts = []
        intensities = []

        # 1. Terrain Sampling
        n_pts = self.X.size
        sample_indices = np.random.choice(n_pts, size=10000, replace=False)
        terrain_x = self.X.flat[sample_indices]
        terrain_y = self.Y.flat[sample_indices]
        terrain_z = self.Z_terrain.flat[sample_indices]

        # Apply water clipping (LiDAR absorption on water surface)
        submerged = terrain_z < self.water_level
        terrain_z[submerged] = self.water_level + np.random.normal(0, 0.01, np.sum(submerged))

        for x, y, z in zip(terrain_x, terrain_y, terrain_z):
            pts.append([x, y, z])
            intensities.append(120.0 if z > self.water_level else 40.0)

        # 2. Building Point Cloud Synthesis
        for x1, x2, y1, y2, h in self.buildings:
            bx = np.random.uniform(x1, x2, 400)
            by = np.random.uniform(y1, y2, 400)
            bz = np.random.uniform(self.water_level, h, 400)
            for x, y, z in zip(bx, by, bz):
                pts.append([x, y, z])
                intensities.append(220.0)

        # 3. Stranded Survivor Point Cloud Synthesis
        for sx, sy, sz in self.survivor_positions:
            # Human profile points (approx 1.7m height)
            hx = np.random.normal(sx, 0.2, 25)
            hy = np.random.normal(sy, 0.2, 25)
            hz = np.random.uniform(sz, sz + 1.7, 25)
            for x, y, z in zip(hx, hy, hz):
                pts.append([x, y, z])
                intensities.append(180.0)

        # 4. Moving Rescue Boat Point Cloud Synthesis
        boat_pts_x = np.random.normal(self.boat_x, 1.2, 60)
        boat_pts_y = np.random.normal(self.boat_y, 0.6, 60)
        boat_pts_z = np.random.uniform(self.water_level, self.water_level + 0.8, 60)
        for x, y, z in zip(boat_pts_x, boat_pts_y, boat_pts_z):
            pts.append([x, y, z])
            intensities.append(250.0)

        # Add Gaussian LiDAR sensor noise
        pts_arr = np.array(pts, dtype=np.float64)
        pts_arr += np.random.normal(0, 0.02, pts_arr.shape)

        return pts_arr, np.array(intensities, dtype=np.float64), self.water_level

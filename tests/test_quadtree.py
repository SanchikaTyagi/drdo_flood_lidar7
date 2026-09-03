import unittest
import numpy as np
from core.quadtree_node import QuadTreeNode
from core.adaptive_elevation_map import AdaptiveElevationMap
from core.point_cloud import PointCloud

class TestQuadTree(unittest.TestCase):
    def test_quadtree_subdivision(self):
        # Generate non-uniform height points
        pts = []
        for x in np.linspace(-10, 10, 20):
            for y in np.linspace(-10, 10, 20):
                z = 5.0 if (x > 0 and y > 0) else 0.0
                pts.append([x, y, z])

        pc = PointCloud(pts)
        map_25d = AdaptiveElevationMap(x_bounds=(-20, 20), y_bounds=(-20, 20))
        map_25d.update(pc, var_threshold=0.05)

        metrics = map_25d.get_metrics()
        self.assertGreater(metrics["active_cells"], 1)
        self.assertGreater(metrics["reduction_pct"], 0.0)

if __name__ == "__main__":
    unittest.main()

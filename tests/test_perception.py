import unittest
import numpy as np
from core.point_cloud import PointCloud
from perception.people_detector import PeopleDetector
from perception.flood_detector import FloodDetector

class TestPerception(unittest.TestCase):
    def test_flood_detector(self):
        pts = np.random.normal(0, 1, (100, 3))
        pts[:, 2] = 1.25  # Simulated water plane at z=1.25
        pc = PointCloud(pts)
        detector = FloodDetector()
        water_z = detector.estimate_water_surface(pc, nominal_water_level=1.2)
        self.assertAlmostEqual(water_z, 1.25, delta=0.1)

    def test_people_detector(self):
        # Cluster of points mimicking a standing human
        human_pts = np.random.uniform(-0.2, 0.2, (20, 3))
        human_pts[:, 2] = np.linspace(1.0, 2.6, 20)  # Height span ~1.6m
        pc = PointCloud(human_pts)

        detector = PeopleDetector()
        survivors = detector.detect_survivors(pc, water_level=1.0)
        self.assertEqual(len(survivors), 1)
        self.assertGreaterEqual(survivors[0].confidence, 0.70)

if __name__ == "__main__":
    unittest.main()

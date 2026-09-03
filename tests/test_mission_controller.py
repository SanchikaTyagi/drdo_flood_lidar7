import unittest
from mission.mission_controller import MissionController

class TestMissionController(unittest.TestCase):
    def test_controller_stepping_and_reset(self):
        mc = MissionController()
        self.assertEqual(mc.simulator.frame_id, 0)

        # Step 3 frames
        for _ in range(3):
            mc.step_frame()

        self.assertEqual(mc.simulator.frame_id, 3)
        self.assertIsNotNone(mc.current_pc)
        self.assertGreater(len(mc.adaptive_map.leaves), 0)

        # Reset verification
        mc.reset()
        self.assertEqual(mc.simulator.frame_id, 0)
        self.assertEqual(len(mc.survivors), 0)

if __name__ == "__main__":
    unittest.main()

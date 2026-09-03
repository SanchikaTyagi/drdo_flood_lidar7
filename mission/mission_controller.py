from core.point_cloud import PointCloud
from core.adaptive_elevation_map import AdaptiveElevationMap
from perception.flood_detector import FloodDetector
from perception.dynamic_filter import DynamicFilter
from perception.people_detector import PeopleDetector
from perception.triage import SurvivorTriage
from perception.safe_zones import SafeZoneDetector
from simulation.flood_scene_generator import FloodSceneGenerator

class MissionController:
    """
    Central orchestration engine processing raw LiDAR sweeps through perception pipelines
    and providing synchronized system state for the command dashboard.
    """
    def __init__(self):
        self.simulator = FloodSceneGenerator()
        self.adaptive_map = AdaptiveElevationMap()
        self.flood_detector = FloodDetector()
        self.dynamic_filter = DynamicFilter()
        self.people_detector = PeopleDetector()

        self.previous_pc = None
        self.current_pc = None
        
        self.is_running = False
        self.simulation_speed = 1
        
        self.survivors = []
        self.dynamic_tracks = {}
        self.safe_zones = []
        self.high_ground_pct = 0.0
        self.water_level = 0.5
        self.event_log = []

        self.log_event("DRDO System Initialized. Sensors Operational.")

    def log_event(self, text):
        time_str = f"[{int(self.simulator.time // 60):02d}:{int(self.simulator.time % 60):02d}]"
        self.event_log.append(f"{time_str} {text}")
        if len(self.event_log) > 20:
            self.event_log.pop(0)

    def step_frame(self):
        """
        Execute full perception step pipeline for one frame.
        """
        pts, intensities, sim_water = self.simulator.step()
        
        self.previous_pc = self.current_pc
        self.current_pc = PointCloud(pts, intensities, self.simulator.frame_id, self.simulator.time)

        # 1. Update Adaptive QuadTree Map
        self.adaptive_map.update(self.current_pc)

        # 2. Estimate Water Plane & Depth Map
        self.water_level = self.flood_detector.estimate_water_surface(self.current_pc, sim_water)
        self.adaptive_map.update_flood_depths(self.water_level)

        # 3. Separate Ground & Non-Ground
        ground_pc, non_ground_pc = self.current_pc.separate_ground_ransac()

        # 4. Dynamic Object Tracking
        self.dynamic_tracks = self.dynamic_filter.process_frames(self.current_pc, self.previous_pc)

        # 5. Survivor Detection & Triage
        raw_survivors = self.people_detector.detect_survivors(non_ground_pc, self.water_level)
        boat_track = self.dynamic_filter.get_boat_track()
        self.survivors = SurvivorTriage.evaluate_triage(raw_survivors, self.adaptive_map, boat_track)

        # 6. Safe Evacuation Zone Analysis
        self.safe_zones, self.high_ground_pct = SafeZoneDetector.detect_safe_zones(self.adaptive_map)

        # Periodic Event Logging
        if self.simulator.frame_id % 3 == 0:
            self.log_event(f"Frame {self.simulator.frame_id:03d}: Adaptive QuadTree updated ({len(self.adaptive_map.leaves)} cells).")
        if boat_track and boat_track.age == 2:
            self.log_event(f"DYNAMIC TARGET #{boat_track.track_id} (RESCUE BOAT) DETECTED!")
        if self.survivors and self.simulator.frame_id == 1:
            self.log_event(f"SURVIVOR ALERT: {len(self.survivors)} personnel identified.")

    def reset(self):
        self.simulator = FloodSceneGenerator()
        self.adaptive_map = AdaptiveElevationMap()
        self.flood_detector = FloodDetector()
        self.dynamic_filter = DynamicFilter()
        self.people_detector = PeopleDetector()
        self.previous_pc = None
        self.current_pc = None
        self.survivors = []
        self.dynamic_tracks = {}
        self.safe_zones = []
        self.event_log = []
        self.log_event("MISSION RESET PERFORMED. System Ready.")

"""
Configuration parameters for DRDO Defense & Disaster Perception System.
"""

# Map Extents (Meters)
X_MIN = -50.0
X_MAX = 50.0
Y_MIN = -50.0
Y_MAX = 50.0

# QuadTree Configuration
MAX_QUADTREE_DEPTH = 6
MIN_CELL_SIZE = 0.5  # meters
ELEVATION_VARIANCE_THRESHOLD = 0.15  # meters^2 to trigger split

# LiDAR Simulator Settings
NUM_TERRAIN_POINTS = 12000
POINT_NOISE_STD = 0.03
LIDAR_SWEEP_RATE_HZ = 10.0

# Water & Flood Parameters
INITIAL_WATER_LEVEL = 0.5  # meters
WATER_RISING_RATE = 0.05    # meters per frame

# Perception Thresholds
SURVIVOR_MIN_HEIGHT = 1.2   # meters above terrain/water
SURVIVOR_MAX_HEIGHT = 2.2   # meters above terrain/water
SURVIVOR_CLUSTER_RADIUS = 1.2
SURVIVOR_MIN_POINTS = 5

DYNAMIC_MOTION_THRESHOLD = 0.35 # meters minimum displacement for motion tracking
TRACK_ASSOCIATION_DIST = 3.0    # meters max distance to associate dynamic tracks

# UI Colors & Theme (Tactical Command Theme)
COLOR_BG_DARK = "#0A0E14"
COLOR_PANEL_BG = "#131922"
COLOR_PANEL_BORDER = "#1E2836"
COLOR_ACCENT_GREEN = "#00FF66"
COLOR_ACCENT_CYAN = "#00E5FF"
COLOR_ACCENT_ORANGE = "#FF9900"
COLOR_ACCENT_RED = "#FF3344"
COLOR_TEXT_LIGHT = "#E2E8F0"
COLOR_TEXT_MUTED = "#64748B"

# DRDO Defense & Disaster Perception: Adaptive Variable-Resolution 2.5D LiDAR Mapping

A real-time disaster perception and tactical decision-support application built for flood scenarios, survivor search-and-rescue, dynamic target tracking, and high-ground evacuation analysis.

---

## 1. Installation Instructions (Windows & VS Code)

1. Open *PowerShell* in VS Code inside the project folder drdo_flood_lidar.
2. Ensure Python 3.14+ is installed.
3. Install dependencies:
   powershell
   py -m pip install -r requirements.txt

2. Run Automated Verification Tests
Verify the spatial algorithms and perception pipelines:
py -m unittest discover -s tests -v

3. Launch the Tactical Dashboard
Launch the GUI software window:
py app.py

4. Key Architectural Modules
 * core/quadtree_node.py: Spatial QuadTree node structure supporting recursive variance-driven subdivision.
 * core/adaptive_elevation_map.py: Generates variable-resolution 2.5D elevation maps where high variance areas split into fine cells.
 * perception/flood_detector.py: Robust RANSAC-inspired water plane estimation and dynamic inundation computing.
 * perception/people_detector.py: 3D spatial point-cloud clustering and anthropometric bounding constraints for survivor localization.
 * perception/dynamic_filter.py: Multi-frame point displacement tracking for moving vessels and vehicles.
 * perception/triage.py: Priority assignment (CRITICAL, URGENT, SAFE) based on depth, isolation, and rescue proximity.

---

### Verification & Windows Execution Commands

Run these exact commands in your PowerShell terminal to install requirements, verify the test suite, and run the live command dashboard:

powershell
py -m pip install -r requirements.txt
py -m unittest discover -s tests -v
py app.py

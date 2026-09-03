class SurvivorTriage:
    """
    Assigns medical/tactical rescue triage priority (CRITICAL, URGENT, SAFE)
    based on water inundation depth, isolation, and access distance.
    """
    @staticmethod
    def evaluate_triage(survivors, adaptive_map, boat_track=None):
        for s in survivors:
            x, y, z = s.position
            
            # Find water depth at survivor location
            water_depth = 0.0
            for leaf in adaptive_map.leaves:
                if leaf.contains(x, y):
                    water_depth = leaf.water_depth
                    break

            s.surrounding_water_depth = water_depth

            if boat_track is not None:
                bx, by, _ = boat_track.position
                s.dist_to_boat = float((((x - bx) ** 2 + (y - by) ** 2) ** 0.5))
            else:
                s.dist_to_boat = 999.0

            # Categorize Triage Priority
            if water_depth > 1.0 or (water_depth > 0.5 and s.dist_to_boat > 20.0):
                s.triage_priority = "CRITICAL"
            elif water_depth > 0.3 or s.dist_to_boat > 30.0:
                s.triage_priority = "URGENT"
            else:
                s.triage_priority = "SAFE"

        # Rank survivors for rescue order
        triage_weights = {"CRITICAL": 0, "URGENT": 1, "SAFE": 2}
        ranked_survivors = sorted(
            survivors,
            key=lambda item: (triage_weights[item.triage_priority], -item.surrounding_water_depth, item.dist_to_boat)
        )
        return ranked_survivors

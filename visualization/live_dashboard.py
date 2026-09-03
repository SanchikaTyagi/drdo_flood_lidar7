import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

import config

class LiveTacticalDashboard:
    """
    Professional DRDO Tactical Desktop Command Dashboard implemented with Tkinter and Matplotlib.
    """
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        self.root.title("DRDO Defense & Disaster Perception System")
        self.root.geometry("1400x900")
        self.root.configure(bg=config.COLOR_BG_DARK)

        # Layer Toggles
        self.layer_terrain = tk.BooleanVar(value=True)
        self.layer_water = tk.BooleanVar(value=True)
        self.layer_survivors = tk.BooleanVar(value=True)
        self.layer_dynamic = tk.BooleanVar(value=True)
        self.layer_safe_zones = tk.BooleanVar(value=True)

        self._setup_styles()
        self._build_header()
        self._build_main_layout()

        # Start Tkinter Animation Loop
        self.root.after(200, self._animation_loop)

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", background=config.COLOR_BG_DARK, foreground=config.COLOR_TEXT_LIGHT)
        style.configure("TFrame", background=config.COLOR_BG_DARK)
        style.configure("Panel.TFrame", background=config.COLOR_PANEL_BG, relief="solid", borderwidth=1)
        style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"), foreground=config.COLOR_ACCENT_CYAN, background=config.COLOR_BG_DARK)
        style.configure("Title.TLabel", font=("Segoe UI", 10, "bold"), foreground=config.COLOR_ACCENT_GREEN, background=config.COLOR_PANEL_BG)

    def _build_header(self):
        header_frame = tk.Frame(self.root, bg=config.COLOR_PANEL_BG, height=50, bd=1, relief="solid")
        header_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        title = tk.Label(
            header_frame, 
            text="DRDO DEFENSE & DISASTER PERCEPTION SYSTEM\nADAPTIVE VARIABLE-RESOLUTION 2.5D LiDAR MAPPING",
            font=("Segoe UI", 11, "bold"), fg=config.COLOR_ACCENT_CYAN, bg=config.COLOR_PANEL_BG, justify=tk.LEFT
        )
        title.pack(side=tk.LEFT, padx=10, pady=5)

        # Header Status Indicators
        self.lbl_water = tk.Label(header_frame, text="WATER LEVEL: 0.50 m", font=("Segoe UI", 10, "bold"), fg=config.COLOR_ACCENT_ORANGE, bg=config.COLOR_PANEL_BG)
        self.lbl_water.pack(side=tk.RIGHT, padx=15)

        self.lbl_frame = tk.Label(header_frame, text="FRAME: 0000", font=("Segoe UI", 10, "bold"), fg=config.COLOR_TEXT_LIGHT, bg=config.COLOR_PANEL_BG)
        self.lbl_frame.pack(side=tk.RIGHT, padx=15)

        self.lbl_status = tk.Label(header_frame, text="● LIVE", font=("Segoe UI", 11, "bold"), fg=config.COLOR_ACCENT_GREEN, bg=config.COLOR_PANEL_BG)
        self.lbl_status.pack(side=tk.RIGHT, padx=15)

    def _build_main_layout(self):
        main_frame = tk.Frame(self.root, bg=config.COLOR_BG_DARK)
        main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # LEFT SIDEBAR
        sidebar = tk.Frame(main_frame, bg=config.COLOR_PANEL_BG, width=220, bd=1, relief="solid")
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=2, pady=2)
        sidebar.pack_propagate(False)

        # CENTER MAP AREA
        center_area = tk.Frame(main_frame, bg=config.COLOR_BG_DARK)
        center_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)

        # RIGHT DATA PANELS
        right_panel = tk.Frame(main_frame, bg=config.COLOR_PANEL_BG, width=320, bd=1, relief="solid")
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=2, pady=2)
        right_panel.pack_propagate(False)

        self._build_sidebar(sidebar)
        self._build_center_maps(center_area)
        self._build_right_panel(right_panel)
        self._build_bottom_bar()

    def _build_sidebar(self, parent):
        tk.Label(parent, text="MISSION CONTROLS", font=("Segoe UI", 10, "bold"), fg=config.COLOR_ACCENT_GREEN, bg=config.COLOR_PANEL_BG).pack(anchor="w", padx=10, pady=8)

        btn_start = tk.Button(parent, text="START MISSION", bg="#1E3A2B", fg=config.COLOR_ACCENT_GREEN, font=("Segoe UI", 9, "bold"), command=self._cmd_start)
        btn_start.pack(fill=tk.X, padx=10, pady=3)

        btn_pause = tk.Button(parent, text="PAUSE", bg="#3A2E1E", fg=config.COLOR_ACCENT_ORANGE, font=("Segoe UI", 9, "bold"), command=self._cmd_pause)
        btn_pause.pack(fill=tk.X, padx=10, pady=3)

        btn_step = tk.Button(parent, text="STEP FRAME", bg="#1E2836", fg=config.COLOR_TEXT_LIGHT, font=("Segoe UI", 9, "bold"), command=self._cmd_step)
        btn_step.pack(fill=tk.X, padx=10, pady=3)

        btn_reset = tk.Button(parent, text="RESET", bg="#3A1E1E", fg=config.COLOR_ACCENT_RED, font=("Segoe UI", 9, "bold"), command=self._cmd_reset)
        btn_reset.pack(fill=tk.X, padx=10, pady=3)

        ttk.Separator(parent, orient="horizontal").pack(fill=tk.X, padx=10, pady=10)

        tk.Label(parent, text="DISPLAY LAYERS", font=("Segoe UI", 10, "bold"), fg=config.COLOR_ACCENT_GREEN, bg=config.COLOR_PANEL_BG).pack(anchor="w", padx=10, pady=5)

        tk.Checkbutton(parent, text="Terrain / Elevation", variable=self.layer_terrain, bg=config.COLOR_PANEL_BG, fg=config.COLOR_TEXT_LIGHT, selectcolor=config.COLOR_BG_DARK).pack(anchor="w", padx=15, pady=2)
        tk.Checkbutton(parent, text="Water / Flood", variable=self.layer_water, bg=config.COLOR_PANEL_BG, fg=config.COLOR_TEXT_LIGHT, selectcolor=config.COLOR_BG_DARK).pack(anchor="w", padx=15, pady=2)
        tk.Checkbutton(parent, text="Survivors", variable=self.layer_survivors, bg=config.COLOR_PANEL_BG, fg=config.COLOR_TEXT_LIGHT, selectcolor=config.COLOR_BG_DARK).pack(anchor="w", padx=15, pady=2)
        tk.Checkbutton(parent, text="Dynamic Objects", variable=self.layer_dynamic, bg=config.COLOR_PANEL_BG, fg=config.COLOR_TEXT_LIGHT, selectcolor=config.COLOR_BG_DARK).pack(anchor="w", padx=15, pady=2)
        tk.Checkbutton(parent, text="Safe Zones", variable=self.layer_safe_zones, bg=config.COLOR_PANEL_BG, fg=config.COLOR_TEXT_LIGHT, selectcolor=config.COLOR_BG_DARK).pack(anchor="w", padx=15, pady=2)

        ttk.Separator(parent, orient="horizontal").pack(fill=tk.X, padx=10, pady=10)

        # ADAPTIVE RESOLUTION METRICS
        tk.Label(parent, text="ADAPTIVE MAPPING", font=("Segoe UI", 10, "bold"), fg=config.COLOR_ACCENT_GREEN, bg=config.COLOR_PANEL_BG).pack(anchor="w", padx=10, pady=5)
        self.lbl_active_cells = tk.Label(parent, text="Active Cells: 0", font=("Consolas", 9), fg=config.COLOR_ACCENT_CYAN, bg=config.COLOR_PANEL_BG)
        self.lbl_active_cells.pack(anchor="w", padx=15, pady=1)
        self.lbl_uniform_cells = tk.Label(parent, text="Uniform Grid: 40,000", font=("Consolas", 9), fg=config.COLOR_TEXT_MUTED, bg=config.COLOR_PANEL_BG)
        self.lbl_uniform_cells.pack(anchor="w", padx=15, pady=1)
        self.lbl_reduction = tk.Label(parent, text="Reduction: 0.0%", font=("Consolas", 9, "bold"), fg=config.COLOR_ACCENT_GREEN, bg=config.COLOR_PANEL_BG)
        self.lbl_reduction.pack(anchor="w", padx=15, pady=1)

    def _build_center_maps(self, parent):
        # Matplotlib Multi-Panel Figure setup
        self.fig = plt.Figure(figsize=(8, 7), facecolor=config.COLOR_BG_DARK)
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # GridSpec Layout: Top Large 2.5D Map, Bottom Two QuadTree & Flood Depth Maps
        gs = self.fig.add_gridspec(2, 2, height_ratios=[1.8, 1.0])

        self.ax_main = self.fig.add_subplot(gs[0, :], facecolor="#0B121B")
        self.ax_quadtree = self.fig.add_subplot(gs[1, 0], facecolor="#0B121B")
        self.ax_depth = self.fig.add_subplot(gs[1, 1], facecolor="#0B121B")

        self.fig.tight_layout(pad=2.0)

    def _build_right_panel(self, parent):
        # SURVIVOR & TRIAGE TABLE
        tk.Label(parent, text="SURVIVOR TRIAGE PRIORITY", font=("Segoe UI", 10, "bold"), fg=config.COLOR_ACCENT_GREEN, bg=config.COLOR_PANEL_BG).pack(anchor="w", padx=10, pady=5)
        
        columns = ("id", "priority", "depth", "dist")
        self.tree_survivors = ttk.Treeview(parent, columns=columns, show="headings", height=5)
        self.tree_survivors.heading("id", text="ID")
        self.tree_survivors.heading("priority", text="TRIAGE")
        self.tree_survivors.heading("depth", text="DEPTH")
        self.tree_survivors.heading("dist", text="BOAT DIST")

        self.tree_survivors.column("id", width=40, anchor="center")
        self.tree_survivors.column("priority", width=80, anchor="center")
        self.tree_survivors.column("depth", width=70, anchor="center")
        self.tree_survivors.column("dist", width=80, anchor="center")
        self.tree_survivors.pack(fill=tk.X, padx=5, pady=2)

        ttk.Separator(parent, orient="horizontal").pack(fill=tk.X, padx=10, pady=8)

        # DYNAMIC TARGET TRACKING
        tk.Label(parent, text="DYNAMIC OBJECT TRACKING", font=("Segoe UI", 10, "bold"), fg=config.COLOR_ACCENT_GREEN, bg=config.COLOR_PANEL_BG).pack(anchor="w", padx=10, pady=2)
        self.lbl_boat_status = tk.Label(parent, text="BOAT TRACK: WAITING FOR DETECTION", font=("Consolas", 8, "bold"), fg=config.COLOR_ACCENT_ORANGE, bg=config.COLOR_PANEL_BG)
        self.lbl_boat_status.pack(anchor="w", padx=10, pady=2)

        ttk.Separator(parent, orient="horizontal").pack(fill=tk.X, padx=10, pady=8)

        # EVENT LOG
        tk.Label(parent, text="TACTICAL EVENT LOG", font=("Segoe UI", 10, "bold"), fg=config.COLOR_ACCENT_GREEN, bg=config.COLOR_PANEL_BG).pack(anchor="w", padx=10, pady=2)
        self.txt_log = tk.Text(parent, bg=config.COLOR_BG_DARK, fg=config.COLOR_TEXT_LIGHT, font=("Consolas", 8), height=14, bd=1, relief="solid")
        self.txt_log.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def _build_bottom_bar(self):
        bottom_bar = tk.Frame(self.root, bg=config.COLOR_PANEL_BG, height=25, bd=1, relief="solid")
        bottom_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=2)

        self.lbl_metrics = tk.Label(
            bottom_bar, 
            text="POINTS: 0 | ACTIVE CELLS: 0 | REDUCTION: 0% | INUNDATED: 0% | SURVIVORS: 0", 
            font=("Consolas", 9, "bold"), fg=config.COLOR_ACCENT_CYAN, bg=config.COLOR_PANEL_BG
        )
        self.lbl_metrics.pack(side=tk.LEFT, padx=10)

    def _cmd_start(self):
        self.controller.is_running = True
        self.lbl_status.config(text="● LIVE", fg=config.COLOR_ACCENT_GREEN)

    def _cmd_pause(self):
        self.controller.is_running = False
        self.lbl_status.config(text="PAUSED", fg=config.COLOR_ACCENT_ORANGE)

    def _cmd_step(self):
        self.controller.is_running = False
        self.lbl_status.config(text="STEP", fg=config.COLOR_ACCENT_CYAN)
        self.controller.step_frame()
        self._update_render()

    def _cmd_reset(self):
        self.controller.is_running = False
        self.controller.reset()
        self.lbl_status.config(text="RESET", fg=config.COLOR_ACCENT_RED)
        self._update_render()

    def _animation_loop(self):
        if self.controller.is_running:
            self.controller.step_frame()
            self._update_render()
        self.root.after(300, self._animation_loop)

    def _update_render(self):
        # Update Header Labels
        self.lbl_frame.config(text=f"FRAME: {self.controller.simulator.frame_id:04d}")
        self.lbl_water.config(text=f"WATER LEVEL: {self.controller.water_level:.2f} m")

        # Update QuadTree Metric Labels
        map_metrics = self.controller.adaptive_map.get_metrics()
        self.lbl_active_cells.config(text=f"Active Cells: {map_metrics['active_cells']:,}")
        self.lbl_uniform_cells.config(text=f"Uniform Grid: {map_metrics['equivalent_uniform']:,}")
        self.lbl_reduction.config(text=f"Reduction: {map_metrics['reduction_pct']:.1f}%")

        # Update Main 2.5D Map
        self.ax_main.clear()
        self.ax_main.set_title("2.5D TACTICAL DISASTER MAP", color=config.COLOR_TEXT_LIGHT, fontsize=9, fontweight="bold")
        self.ax_main.set_xlim(config.X_MIN, config.X_MAX)
        self.ax_main.set_ylim(config.Y_MIN, config.Y_MAX)
        self.ax_main.tick_params(colors=config.COLOR_TEXT_MUTED, labelsize=7)

        pc = self.controller.current_pc
        if pc is not None and len(pc) > 0 and self.layer_terrain.get():
            pts = pc.points
            # Color points by elevation
            scatter = self.ax_main.scatter(pts[:, 0], pts[:, 1], c=pts[:, 2], s=2, cmap="terrain", alpha=0.6)

        # Plot Safe Zones
        if self.layer_safe_zones.get():
            for zone in self.controller.safe_zones:
                rect = patches.Rectangle((zone.center[0]-3, zone.center[1]-3), 6, 6, linewidth=1.5, edgecolor=config.COLOR_ACCENT_GREEN, facecolor="none", linestyle="--")
                self.ax_main.add_patch(rect)
                self.ax_main.text(zone.center[0], zone.center[1], f"SAFE ZONE\n{zone.zone_id}", color=config.COLOR_ACCENT_GREEN, fontsize=6, fontweight="bold", ha="center")

        # Plot Survivors
        if self.layer_survivors.get():
            for s in self.controller.survivors:
                color = config.COLOR_ACCENT_RED if s.triage_priority == "CRITICAL" else (config.COLOR_ACCENT_ORANGE if s.triage_priority == "URGENT" else config.COLOR_ACCENT_GREEN)
                self.ax_main.plot(s.position[0], s.position[1], "^", color=color, markersize=8)
                self.ax_main.text(s.position[0] + 1, s.position[1] + 1, f"{s.id} ({s.triage_priority})", color=color, fontsize=7, fontweight="bold")

        # Plot Dynamic Boat Track
        if self.layer_dynamic.get():
            boat_track = self.controller.dynamic_filter.get_boat_track()
            if boat_track:
                hist = np.array(boat_track.history)
                self.ax_main.plot(hist[:, 0], hist[:, 1], "-", color=config.COLOR_ACCENT_CYAN, linewidth=2, label="Boat Track")
                self.ax_main.plot(boat_track.position[0], boat_track.position[1], "s", color=config.COLOR_ACCENT_CYAN, markersize=8)
                self.ax_main.text(boat_track.position[0] + 1, boat_track.position[1] + 1, f"RESCUE BOAT #{boat_track.track_id}\n{boat_track.speed:.1f} m/s", color=config.COLOR_ACCENT_CYAN, fontsize=7, fontweight="bold")
                self.lbl_boat_status.config(text=f"BOAT #{boat_track.track_id} | SPEED: {boat_track.speed:.2f} m/s | HEADING: {boat_track.heading_deg:.0f}°", fg=config.COLOR_ACCENT_CYAN)
            else:
                self.lbl_boat_status.config(text="BOAT TRACK: WAITING FOR DETECTION", fg=config.COLOR_ACCENT_ORANGE)

        # Update QuadTree Mesh Subdivisions
        self.ax_quadtree.clear()
        self.ax_quadtree.set_title("ADAPTIVE QUADTREE MESH", color=config.COLOR_TEXT_LIGHT, fontsize=8, fontweight="bold")
        self.ax_quadtree.set_xlim(config.X_MIN, config.X_MAX)
        self.ax_quadtree.set_ylim(config.Y_MIN, config.Y_MAX)
        self.ax_quadtree.tick_params(colors=config.COLOR_TEXT_MUTED, labelsize=6)

        for leaf in self.controller.adaptive_map.leaves:
            edge_color = config.COLOR_ACCENT_CYAN if leaf.depth >= 4 else "#1E2836"
            rect = patches.Rectangle((leaf.x_min, leaf.y_min), leaf.width, leaf.height, linewidth=0.5, edgecolor=edge_color, facecolor="none")
            self.ax_quadtree.add_patch(rect)

        # Update Flood Depth Map Heatmap
        self.ax_depth.clear()
        self.ax_depth.set_title("FLOOD INUNDATION DEPTH (m)", color=config.COLOR_TEXT_LIGHT, fontsize=8, fontweight="bold")
        self.ax_depth.set_xlim(config.X_MIN, config.X_MAX)
        self.ax_depth.set_ylim(config.Y_MIN, config.Y_MAX)
        self.ax_depth.tick_params(colors=config.COLOR_TEXT_MUTED, labelsize=6)

        leaves = self.controller.adaptive_map.leaves
        if leaves:
            for leaf in leaves:
                if leaf.is_flooded:
                    rect = patches.Rectangle((leaf.x_min, leaf.y_min), leaf.width, leaf.height, linewidth=0, facecolor="#0066FF", alpha=min(0.8, leaf.water_depth / 2.0))
                    self.ax_depth.add_patch(rect)

        self.canvas.draw_idle()

        # Update Survivor Triage Table
        for item in self.tree_survivors.get_children():
            self.tree_survivors.delete(item)
        for s in self.controller.survivors:
            self.tree_survivors.insert("", tk.END, values=(s.id, s.triage_priority, f"{s.surrounding_water_depth:.2f}m", f"{s.dist_to_boat:.1f}m"))

        # Update Event Log Text Box
        self.txt_log.delete("1.0", tk.END)
        for log in self.controller.event_log:
            self.txt_log.insert(tk.END, log + "\n")
        self.txt_log.see(tk.END)

        # Update Bottom Metrics Bar
        flood_stats = self.controller.flood_detector.compute_statistics(self.controller.adaptive_map)
        n_pts = len(pc) if pc else 0
        self.lbl_metrics.config(
            text=f"POINTS: {n_pts:,} | ACTIVE CELLS: {map_metrics['active_cells']:,} | REDUCTION: {map_metrics['reduction_pct']:.1f}% | INUNDATED: {flood_stats['inundated_pct']:.1f}% | SURVIVORS: {len(self.controller.survivors)}"
        )

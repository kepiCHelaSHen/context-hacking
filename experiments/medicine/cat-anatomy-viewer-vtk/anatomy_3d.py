"""
CHP Anatomy Viewer v2 — VTK 3D Renderer
Medically-accurate 3D anatomy viewer using VTK.
All organ positions from Gray's Anatomy 41st Edition via frozen constants.

Run:   python anatomy_3d.py
Test:  python anatomy_3d.py --test
Keys:  1-7 toggle systems, A all, S screenshot, R reset, Q quit
"""

import math
import os
import sys
from pathlib import Path

import numpy as np

# ---------------------------------------------------------------------------
# Frozen constants — imported from the canonical source
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).parent.parent / "anatomy-viewer" / "frozen"))
from anatomy_constants import (
    # Segment ratios
    HEAD_HEIGHT_RATIO, NECK_HEIGHT_RATIO, TORSO_HEIGHT_RATIO,
    UPPER_ARM_RATIO, FOREARM_RATIO, HAND_RATIO,
    PELVIS_HEIGHT_RATIO, THIGH_RATIO, LOWER_LEG_RATIO, FOOT_HEIGHT_RATIO,
    SHOULDER_WIDTH_RATIO, HIP_WIDTH_RATIO, HEAD_WIDTH_RATIO, WAIST_WIDTH_RATIO,
    BILATERAL_SYMMETRY_TOL,
    # Organs
    HEART_CENTER_Y, HEART_CENTER_X_OFF, HEART_HEIGHT, HEART_WIDTH,
    LEFT_LUNG_CENTER_Y, LEFT_LUNG_CENTER_X, LEFT_LUNG_HEIGHT, LEFT_LUNG_WIDTH,
    RIGHT_LUNG_CENTER_Y, RIGHT_LUNG_CENTER_X, RIGHT_LUNG_HEIGHT, RIGHT_LUNG_WIDTH,
    LIVER_CENTER_Y, LIVER_CENTER_X, LIVER_HEIGHT, LIVER_WIDTH,
    STOMACH_CENTER_Y, STOMACH_CENTER_X, STOMACH_HEIGHT, STOMACH_WIDTH,
    SPLEEN_CENTER_Y, SPLEEN_CENTER_X, SPLEEN_HEIGHT, SPLEEN_WIDTH,
    BRAIN_CENTER_Y, BRAIN_HEIGHT, BRAIN_WIDTH,
    DIAPHRAGM_Y, DIAPHRAGM_RIGHT_HIGHER,
    # Aorta
    AORTA_ARCH_Y, AORTA_DESCENDING_Y, AORTA_BIFURCATION_Y,
    # Vertebral
    C1_Y, T1_Y, T12_Y, L5_Y, S1_Y,
    STERNUM_TOP_Y, STERNUM_BOTTOM_Y, STERNUM_WIDTH,
    # Colors
    COLORS,
)

import vtk

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
H = 1.80  # canonical figure height in metres

SYSTEM_NAMES = [
    "skeletal", "muscular", "nervous", "circulatory",
    "respiratory", "digestive", "lymphatic",
]


def hex_to_rgb(hex_color: str) -> tuple:
    """Convert '#RRGGBB' to (r, g, b) floats in [0,1]."""
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


SYSTEM_COLORS = {name: hex_to_rgb(COLORS[name]) for name in SYSTEM_NAMES}

# ---------------------------------------------------------------------------
# Coordinate conversion — THE single conversion function
# ---------------------------------------------------------------------------


def ratio_to_vtk(ratio_y: float, offset_x: float = 0.0, depth_y: float = 0.0):
    """Convert frozen-spec ratios to VTK world coordinates.

    ratio_y: fraction of total height from TOP (0=top of head, 1=feet)
    offset_x: fraction of height for left-right offset
    depth_y: absolute depth in metres (anterior-posterior)

    Returns (x, y, z) in VTK coords where:
      x = left-right
      y = anterior-posterior
      z = inferior-superior (0=feet, 1.80=top of head)
    """
    z = (1.0 - ratio_y) * H
    x = offset_x * H
    y = depth_y
    return (x, y, z)


# ---------------------------------------------------------------------------
# Utility: create a positioned actor from a VTK source
# ---------------------------------------------------------------------------


def _make_actor(source, position, color, opacity=1.0, orientation=None, scale=None):
    """Create a VTK actor from source, position it, color it."""
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(source.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.SetPosition(*position)
    actor.GetProperty().SetColor(*color)
    actor.GetProperty().SetOpacity(opacity)
    actor.GetProperty().SetSpecular(0.3)
    actor.GetProperty().SetSpecularPower(20)
    if orientation is not None:
        actor.SetOrientation(*orientation)
    if scale is not None:
        actor.SetScale(*scale)
    return actor


def _make_tube(points, radius, color, opacity=1.0):
    """Create a tube actor along a polyline of (x,y,z) points."""
    vtk_points = vtk.vtkPoints()
    for p in points:
        vtk_points.InsertNextPoint(*p)
    line = vtk.vtkPolyLine()
    line.GetPointIds().SetNumberOfIds(len(points))
    for i in range(len(points)):
        line.GetPointIds().SetId(i, i)
    cells = vtk.vtkCellArray()
    cells.InsertNextCell(line)
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(vtk_points)
    polydata.SetLines(cells)
    tube_filter = vtk.vtkTubeFilter()
    tube_filter.SetInputData(polydata)
    tube_filter.SetRadius(radius)
    tube_filter.SetNumberOfSides(12)
    tube_filter.CappingOn()
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(tube_filter.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(*color)
    actor.GetProperty().SetOpacity(opacity)
    actor.GetProperty().SetSpecular(0.3)
    actor.GetProperty().SetSpecularPower(20)
    return actor


def _make_ellipsoid(position, radii, color, opacity=1.0):
    """Create an ellipsoid (scaled sphere) actor."""
    sphere = vtk.vtkSphereSource()
    sphere.SetThetaResolution(24)
    sphere.SetPhiResolution(24)
    sphere.SetRadius(1.0)
    actor = _make_actor(sphere, position, color, opacity,
                        scale=(radii[0], radii[1], radii[2]))
    return actor


# ===========================================================================
# BUILD FUNCTIONS — one per system
# ===========================================================================


def build_body_surface(renderer):
    """Semi-transparent skin mesh. Returns list of actors."""
    actors = []
    skin_color = (0.94, 0.82, 0.72)
    skin_opacity = 0.08

    # Head
    head = vtk.vtkSphereSource()
    head.SetRadius(HEAD_WIDTH_RATIO * H / 2)
    head.SetThetaResolution(24)
    head.SetPhiResolution(24)
    pos = ratio_to_vtk(0.072, 0, 0.02)
    actors.append(_make_actor(head, pos, skin_color, skin_opacity))

    # Torso — cylinder along Z axis
    torso = vtk.vtkCylinderSource()
    torso.SetHeight(TORSO_HEIGHT_RATIO * H)
    torso.SetRadius(SHOULDER_WIDTH_RATIO * H / 2 * 0.85)
    torso.SetResolution(24)
    pos = ratio_to_vtk(0.42, 0, 0)
    # VTK cylinder default axis is Y — rotate 90 deg around X to align with Z
    actors.append(_make_actor(torso, pos, skin_color, skin_opacity,
                              orientation=(90, 0, 0)))

    # Pelvis
    pelvis = vtk.vtkSphereSource()
    pelvis.SetRadius(1.0)
    pelvis.SetThetaResolution(20)
    pelvis.SetPhiResolution(20)
    pos = ratio_to_vtk(0.54, 0, 0)
    actors.append(_make_actor(pelvis, pos, skin_color, skin_opacity,
                              scale=(HIP_WIDTH_RATIO * H / 2, 0.08, 0.07)))

    # Thighs (bilateral)
    for sign in [-1, 1]:
        thigh = vtk.vtkCylinderSource()
        thigh.SetHeight(THIGH_RATIO * H)
        thigh.SetRadius(0.055)
        thigh.SetResolution(16)
        pos = ratio_to_vtk(0.67, sign * 0.055, 0)
        actors.append(_make_actor(thigh, pos, skin_color, skin_opacity,
                                  orientation=(90, 0, 0)))

    # Lower legs (bilateral)
    for sign in [-1, 1]:
        leg = vtk.vtkCylinderSource()
        leg.SetHeight(LOWER_LEG_RATIO * H)
        leg.SetRadius(0.040)
        leg.SetResolution(16)
        pos = ratio_to_vtk(0.88, sign * 0.055, 0)
        actors.append(_make_actor(leg, pos, skin_color, skin_opacity,
                                  orientation=(90, 0, 0)))

    # Upper arms (bilateral)
    for sign in [-1, 1]:
        arm = vtk.vtkCylinderSource()
        arm.SetHeight(UPPER_ARM_RATIO * H)
        arm.SetRadius(0.032)
        arm.SetResolution(16)
        pos = ratio_to_vtk(0.40, sign * SHOULDER_WIDTH_RATIO / 2, 0)
        actors.append(_make_actor(arm, pos, skin_color, skin_opacity,
                                  orientation=(90, 0, 0)))

    # Forearms (bilateral)
    for sign in [-1, 1]:
        forearm = vtk.vtkCylinderSource()
        forearm.SetHeight(FOREARM_RATIO * H)
        forearm.SetRadius(0.025)
        forearm.SetResolution(16)
        pos = ratio_to_vtk(0.55, sign * SHOULDER_WIDTH_RATIO / 2, 0)
        actors.append(_make_actor(forearm, pos, skin_color, skin_opacity,
                                  orientation=(90, 0, 0)))

    for a in actors:
        renderer.AddActor(a)
    return actors


# ---------------------------------------------------------------------------
# SKELETAL
# ---------------------------------------------------------------------------

def _spinal_bezier_points(n_points=60):
    """Generate spinal column path with cervical lordosis, thoracic kyphosis,
    lumbar lordosis. Returns list of (x, y, z)."""
    points = []
    c1_z = ratio_to_vtk(C1_Y)[2]
    t1_z = ratio_to_vtk(T1_Y)[2]
    t12_z = ratio_to_vtk(T12_Y)[2]
    l5_z = ratio_to_vtk(L5_Y)[2]

    # Cervical: C1 to T1 — lordosis (anterior curve)
    for i in range(n_points // 3):
        t = i / (n_points // 3)
        z = c1_z + t * (t1_z - c1_z)
        # Lordosis: anterior bulge
        depth = -0.08 + 0.015 * math.sin(t * math.pi)
        points.append((0.0, depth, z))

    # Thoracic: T1 to T12 — kyphosis (posterior curve)
    for i in range(n_points // 3):
        t = i / (n_points // 3)
        z = t1_z + t * (t12_z - t1_z)
        # Kyphosis: posterior bulge
        depth = -0.08 - 0.020 * math.sin(t * math.pi)
        points.append((0.0, depth, z))

    # Lumbar: T12 to L5 — lordosis (anterior curve)
    for i in range(n_points // 3):
        t = i / (n_points // 3)
        z = t12_z + t * (l5_z - t12_z)
        # Lordosis: anterior bulge
        depth = -0.08 + 0.015 * math.sin(t * math.pi)
        points.append((0.0, depth, z))

    return points


def build_skeletal(renderer, active_systems):
    """Full skeletal system. Returns list of actors."""
    actors = []
    color = SYSTEM_COLORS["skeletal"]
    visible = "skeletal" in active_systems

    # Skull
    skull = vtk.vtkSphereSource()
    skull.SetRadius(HEAD_WIDTH_RATIO * H / 2 * 0.95)
    skull.SetThetaResolution(24)
    skull.SetPhiResolution(24)
    pos = ratio_to_vtk(BRAIN_CENTER_Y, 0, 0.01)
    a = _make_actor(skull, pos, color, 0.7)
    a.SetVisibility(visible)
    actors.append(a)

    # Vertebral column — individual vertebrae along bezier path
    spine_path = _spinal_bezier_points()

    # Cervical: 7 vertebrae
    c1_z = ratio_to_vtk(C1_Y)[2]
    t1_z = ratio_to_vtk(T1_Y)[2]
    for i in range(7):
        t = i / 6
        z = c1_z + t * (t1_z - c1_z)
        depth = -0.08 + 0.015 * math.sin(t * math.pi)
        cube = vtk.vtkCubeSource()
        cube.SetXLength(0.025)
        cube.SetYLength(0.025)
        cube.SetZLength(0.015)
        a = _make_actor(cube, (0, depth, z), color, 0.8)
        a.SetVisibility(visible)
        actors.append(a)

    # Thoracic: 12 vertebrae
    t12_z = ratio_to_vtk(T12_Y)[2]
    for i in range(12):
        t = i / 11
        z = t1_z + t * (t12_z - t1_z)
        depth = -0.08 - 0.020 * math.sin(t * math.pi)
        cube = vtk.vtkCubeSource()
        cube.SetXLength(0.028)
        cube.SetYLength(0.028)
        cube.SetZLength(0.014)
        a = _make_actor(cube, (0, depth, z), color, 0.8)
        a.SetVisibility(visible)
        actors.append(a)

    # Lumbar: 5 vertebrae
    l5_z = ratio_to_vtk(L5_Y)[2]
    for i in range(5):
        t = i / 4
        z = t12_z + t * (l5_z - t12_z)
        depth = -0.08 + 0.015 * math.sin(t * math.pi)
        cube = vtk.vtkCubeSource()
        cube.SetXLength(0.035)
        cube.SetYLength(0.035)
        cube.SetZLength(0.016)
        a = _make_actor(cube, (0, depth, z), color, 0.8)
        a.SetVisibility(visible)
        actors.append(a)

    # Ribcage: 12 pairs of arcs
    for rib_idx in range(12):
        t = rib_idx / 11
        rib_z = t1_z + t * (t12_z - t1_z)
        # Radius decreases from rib 1 (0.14m) to rib 12 (0.09m)
        rib_radius = 0.14 - 0.05 * t
        # True ribs (0-6) extend further anterior, false/floating shorter
        is_true = rib_idx < 7
        is_floating = rib_idx >= 10
        arc_angle = 160 if is_true else (120 if not is_floating else 90)

        for sign in [-1, 1]:
            # Create arc as a series of points
            n_arc = 16
            arc_points = []
            for j in range(n_arc):
                angle = (j / (n_arc - 1)) * math.radians(arc_angle)
                x = sign * rib_radius * math.sin(angle)
                y = rib_radius * math.cos(angle) * 0.6 - 0.02
                z_off = rib_z - 0.01 * math.sin(angle)  # slight downward slope
                arc_points.append((x, y, z_off))

            a = _make_tube(arc_points, 0.006, color, 0.7)
            a.SetVisibility(visible)
            actors.append(a)

    # Sternum
    sternum_top_z = ratio_to_vtk(STERNUM_TOP_Y)[2]
    sternum_bot_z = ratio_to_vtk(STERNUM_BOTTOM_Y)[2]
    sternum_height = abs(sternum_top_z - sternum_bot_z)
    sternum = vtk.vtkCylinderSource()
    sternum.SetHeight(sternum_height)
    sternum.SetRadius(STERNUM_WIDTH * H / 2)
    sternum.SetResolution(12)
    sternum_mid_z = (sternum_top_z + sternum_bot_z) / 2
    a = _make_actor(sternum, (0, 0.10, sternum_mid_z), color, 0.8,
                    orientation=(90, 0, 0))
    a.SetVisibility(visible)
    actors.append(a)

    # Femur (bilateral)
    for sign in [-1, 1]:
        femur = vtk.vtkCylinderSource()
        femur.SetHeight(THIGH_RATIO * H)
        femur.SetRadius(0.018)
        femur.SetResolution(12)
        pos = ratio_to_vtk(0.67, sign * 0.055, 0)
        a = _make_actor(femur, pos, color, 0.8, orientation=(90, 0, 0))
        a.SetVisibility(visible)
        actors.append(a)

    # Tibia (bilateral)
    for sign in [-1, 1]:
        tibia = vtk.vtkCylinderSource()
        tibia.SetHeight(LOWER_LEG_RATIO * H * 0.8)
        tibia.SetRadius(0.014)
        tibia.SetResolution(12)
        pos = ratio_to_vtk(0.88, sign * 0.055, 0.01)
        a = _make_actor(tibia, pos, color, 0.8, orientation=(90, 0, 0))
        a.SetVisibility(visible)
        actors.append(a)

    # Fibula (bilateral)
    for sign in [-1, 1]:
        fibula = vtk.vtkCylinderSource()
        fibula.SetHeight(LOWER_LEG_RATIO * H * 0.8)
        fibula.SetRadius(0.006)
        fibula.SetResolution(12)
        pos = ratio_to_vtk(0.88, sign * 0.055 + sign * 0.015 / H, -0.01)
        a = _make_actor(fibula, pos, color, 0.8, orientation=(90, 0, 0))
        a.SetVisibility(visible)
        actors.append(a)

    # Humerus (bilateral)
    for sign in [-1, 1]:
        humerus = vtk.vtkCylinderSource()
        humerus.SetHeight(UPPER_ARM_RATIO * H)
        humerus.SetRadius(0.012)
        humerus.SetResolution(12)
        pos = ratio_to_vtk(0.40, sign * SHOULDER_WIDTH_RATIO / 2, 0)
        a = _make_actor(humerus, pos, color, 0.8, orientation=(90, 0, 0))
        a.SetVisibility(visible)
        actors.append(a)

    # Radius/Ulna (bilateral)
    for sign in [-1, 1]:
        radius_bone = vtk.vtkCylinderSource()
        radius_bone.SetHeight(FOREARM_RATIO * H)
        radius_bone.SetRadius(0.009)
        radius_bone.SetResolution(12)
        pos = ratio_to_vtk(0.55, sign * SHOULDER_WIDTH_RATIO / 2, 0.005)
        a = _make_actor(radius_bone, pos, color, 0.8, orientation=(90, 0, 0))
        a.SetVisibility(visible)
        actors.append(a)

        ulna = vtk.vtkCylinderSource()
        ulna.SetHeight(FOREARM_RATIO * H)
        ulna.SetRadius(0.007)
        ulna.SetResolution(12)
        pos = ratio_to_vtk(0.55, sign * SHOULDER_WIDTH_RATIO / 2, -0.005)
        a = _make_actor(ulna, pos, color, 0.8, orientation=(90, 0, 0))
        a.SetVisibility(visible)
        actors.append(a)

    # Pelvis
    pelvis_pos = ratio_to_vtk(0.54, 0, 0)
    a = _make_ellipsoid(pelvis_pos, (0.12, 0.08, 0.07), color, 0.6)
    a.SetVisibility(visible)
    actors.append(a)

    for a in actors:
        renderer.AddActor(a)
    return actors


# ---------------------------------------------------------------------------
# CIRCULATORY
# ---------------------------------------------------------------------------

def build_circulatory(renderer, active_systems):
    """Heart, aorta, major vessels. Returns list of actors."""
    actors = []
    color = SYSTEM_COLORS["circulatory"]
    visible = "circulatory" in active_systems

    # Heart — positioned via frozen constants
    heart_pos = ratio_to_vtk(HEART_CENTER_Y, HEART_CENTER_X_OFF, 0.04)
    heart_rx = HEART_WIDTH * H / 2
    heart_ry = HEART_WIDTH * H / 2
    heart_rz = HEART_HEIGHT * H / 2
    a = _make_ellipsoid(heart_pos, (heart_rx, heart_ry, heart_rz),
                        (0.85, 0.10, 0.10), 0.85)
    a.SetVisibility(visible)
    actors.append(a)

    # Aortic arch: heart -> arch apex -> descending -> bifurcation
    arch_pos = ratio_to_vtk(AORTA_ARCH_Y, -0.015, 0.02)
    desc_pos = ratio_to_vtk(AORTA_DESCENDING_Y, 0, -0.06)
    bif_pos = ratio_to_vtk(AORTA_BIFURCATION_Y, 0, -0.04)

    # Ascending aorta
    aorta_pts = [
        heart_pos,
        ratio_to_vtk(AORTA_ARCH_Y, -0.01, 0.03),
        arch_pos,
        ratio_to_vtk(AORTA_DESCENDING_Y, 0.005, -0.04),
        desc_pos,
    ]
    a = _make_tube(aorta_pts, 0.015, color, 0.8)
    a.SetVisibility(visible)
    actors.append(a)

    # Descending aorta to bifurcation
    desc_pts = [desc_pos, bif_pos]
    a = _make_tube(desc_pts, 0.013, color, 0.8)
    a.SetVisibility(visible)
    actors.append(a)

    # Iliac arteries from bifurcation to each leg
    for sign in [-1, 1]:
        iliac_pts = [
            bif_pos,
            ratio_to_vtk(0.58, sign * 0.04, -0.02),
            ratio_to_vtk(0.62, sign * 0.055, 0.0),
        ]
        a = _make_tube(iliac_pts, 0.010, color, 0.7)
        a.SetVisibility(visible)
        actors.append(a)

    # Femoral arteries
    for sign in [-1, 1]:
        femoral_pts = [
            ratio_to_vtk(0.62, sign * 0.055, 0.0),
            ratio_to_vtk(0.75, sign * 0.055, 0.01),
            ratio_to_vtk(0.85, sign * 0.055, 0.01),
        ]
        a = _make_tube(femoral_pts, 0.007, color, 0.6)
        a.SetVisibility(visible)
        actors.append(a)

    for a in actors:
        renderer.AddActor(a)
    return actors


# ---------------------------------------------------------------------------
# RESPIRATORY
# ---------------------------------------------------------------------------

def build_respiratory(renderer, active_systems):
    """Lungs, trachea, diaphragm. Returns list of actors."""
    actors = []
    color = SYSTEM_COLORS["respiratory"]
    lung_color = (0.60, 0.75, 0.90)
    visible = "respiratory" in active_systems

    # Left lung — smaller (cardiac notch)
    left_pos = ratio_to_vtk(LEFT_LUNG_CENTER_Y, LEFT_LUNG_CENTER_X, 0.00)
    left_rx = LEFT_LUNG_WIDTH * H / 2
    left_ry = 0.07
    left_rz = LEFT_LUNG_HEIGHT * H / 2
    a = _make_ellipsoid(left_pos, (left_rx, left_ry, left_rz), lung_color, 0.55)
    a.SetVisibility(visible)
    actors.append(a)

    # Right lung — LARGER (no cardiac notch)
    right_pos = ratio_to_vtk(RIGHT_LUNG_CENTER_Y, RIGHT_LUNG_CENTER_X, 0.00)
    right_rx = RIGHT_LUNG_WIDTH * H / 2
    right_ry = 0.07
    right_rz = RIGHT_LUNG_HEIGHT * H / 2
    a = _make_ellipsoid(right_pos, (right_rx, right_ry, right_rz), lung_color, 0.55)
    a.SetVisibility(visible)
    actors.append(a)

    # Trachea: from ~z=1.50 down to T4 level
    trachea = vtk.vtkCylinderSource()
    trachea.SetHeight(0.24)
    trachea.SetRadius(0.009)
    trachea.SetResolution(12)
    trachea_pos = ratio_to_vtk(0.200, 0, 0.02)
    a = _make_actor(trachea, trachea_pos, color, 0.7, orientation=(90, 0, 0))
    a.SetVisibility(visible)
    actors.append(a)

    # Diaphragm — two domes, right higher than left
    diaphragm_z = ratio_to_vtk(DIAPHRAGM_Y)[2]
    # Right dome (higher by ~0.02m because of liver below)
    right_dome = vtk.vtkSphereSource()
    right_dome.SetRadius(0.08)
    right_dome.SetThetaResolution(20)
    right_dome.SetPhiResolution(20)
    right_dome_z = diaphragm_z + 0.02  # right higher
    a = _make_actor(right_dome, (0.06, 0, right_dome_z), color, 0.3,
                    scale=(1.0, 0.8, 0.4))
    a.SetVisibility(visible)
    actors.append(a)

    # Left dome (lower)
    left_dome = vtk.vtkSphereSource()
    left_dome.SetRadius(0.08)
    left_dome.SetThetaResolution(20)
    left_dome.SetPhiResolution(20)
    left_dome_z = diaphragm_z  # left at baseline
    a = _make_actor(left_dome, (-0.06, 0, left_dome_z), color, 0.3,
                    scale=(1.0, 0.8, 0.4))
    a.SetVisibility(visible)
    actors.append(a)

    for a in actors:
        renderer.AddActor(a)
    return actors


# ---------------------------------------------------------------------------
# DIGESTIVE
# ---------------------------------------------------------------------------

def build_digestive(renderer, active_systems):
    """Liver, stomach, intestines. Returns list of actors."""
    actors = []
    color = SYSTEM_COLORS["digestive"]
    visible = "digestive" in active_systems

    # Liver — RIGHT side (positive x)
    liver_pos = ratio_to_vtk(LIVER_CENTER_Y, LIVER_CENTER_X, 0.02)
    liver_rx = LIVER_WIDTH * H / 2
    liver_ry = 0.06
    liver_rz = LIVER_HEIGHT * H / 2
    a = _make_ellipsoid(liver_pos, (liver_rx, liver_ry, liver_rz),
                        (0.60, 0.25, 0.15), 0.7)
    a.SetVisibility(visible)
    actors.append(a)

    # Stomach — left side
    stomach_pos = ratio_to_vtk(STOMACH_CENTER_Y, STOMACH_CENTER_X, 0.03)
    stomach_rx = STOMACH_WIDTH * H / 2
    stomach_ry = 0.04
    stomach_rz = STOMACH_HEIGHT * H / 2
    a = _make_ellipsoid(stomach_pos, (stomach_rx, stomach_ry, stomach_rz),
                        color, 0.65)
    a.SetVisibility(visible)
    actors.append(a)

    # Small intestine — coiled tube segments
    si_center = ratio_to_vtk(0.50, 0, 0.03)
    si_points = []
    for i in range(30):
        angle = i * 0.7
        r = 0.02 + 0.015 * (i / 30)
        x = si_center[0] + r * math.cos(angle)
        y = si_center[1] + r * math.sin(angle) * 0.5
        z = si_center[2] - i * 0.003
        si_points.append((x, y, z))
    a = _make_tube(si_points, 0.008, color, 0.5)
    a.SetVisibility(visible)
    actors.append(a)

    # Large intestine — rectangular frame
    li_base_z = ratio_to_vtk(0.52)[2]
    li_top_z = ratio_to_vtk(0.44)[2]
    li_points = [
        (0.10, 0.02, li_base_z - 0.05),  # cecum (right, low)
        (0.10, 0.02, li_top_z),            # ascending (right, up)
        (-0.00, 0.02, li_top_z + 0.01),    # transverse mid
        (-0.10, 0.02, li_top_z),            # transverse left
        (-0.10, 0.02, li_base_z - 0.03),   # descending
        (-0.06, 0.02, li_base_z - 0.08),   # sigmoid
    ]
    a = _make_tube(li_points, 0.014, color, 0.5)
    a.SetVisibility(visible)
    actors.append(a)

    for a in actors:
        renderer.AddActor(a)
    return actors


# ---------------------------------------------------------------------------
# NERVOUS
# ---------------------------------------------------------------------------

def build_nervous(renderer, active_systems):
    """Brain, spinal cord. Returns list of actors."""
    actors = []
    color = SYSTEM_COLORS["nervous"]
    brain_color = (0.85, 0.80, 0.92)
    visible = "nervous" in active_systems

    # Brain
    brain_pos = ratio_to_vtk(BRAIN_CENTER_Y, 0, 0.01)
    brain_rx = BRAIN_WIDTH * H / 2
    brain_ry = BRAIN_WIDTH * H / 2 * 0.85
    brain_rz = BRAIN_HEIGHT * H / 2
    a = _make_ellipsoid(brain_pos, (brain_rx, brain_ry, brain_rz),
                        brain_color, 0.8)
    a.SetVisibility(visible)
    actors.append(a)

    # Spinal cord — thin tube following vertebral path
    spine_pts = _spinal_bezier_points(40)
    a = _make_tube(spine_pts, 0.007, color, 0.7)
    a.SetVisibility(visible)
    actors.append(a)

    # Major nerves from spinal cord to limbs (brachial plexus, lumbar plexus)
    # Brachial plexus (bilateral)
    t1_z = ratio_to_vtk(T1_Y)[2]
    for sign in [-1, 1]:
        brachial_pts = [
            (0, -0.08, t1_z),
            (sign * 0.08, -0.04, t1_z - 0.02),
            (sign * SHOULDER_WIDTH_RATIO * H / 2, 0, t1_z - 0.05),
        ]
        a = _make_tube(brachial_pts, 0.004, color, 0.5)
        a.SetVisibility(visible)
        actors.append(a)

    # Sciatic nerves (bilateral)
    l5_z = ratio_to_vtk(L5_Y)[2]
    for sign in [-1, 1]:
        sciatic_pts = [
            (0, -0.08, l5_z),
            (sign * 0.04, -0.06, l5_z - 0.05),
            (sign * 0.055, -0.02, ratio_to_vtk(0.70)[2]),
            (sign * 0.055, -0.01, ratio_to_vtk(0.85)[2]),
        ]
        a = _make_tube(sciatic_pts, 0.005, color, 0.5)
        a.SetVisibility(visible)
        actors.append(a)

    for a in actors:
        renderer.AddActor(a)
    return actors


# ---------------------------------------------------------------------------
# MUSCULAR
# ---------------------------------------------------------------------------

def build_muscular(renderer, active_systems):
    """Major muscle groups. Returns list of actors."""
    actors = []
    color = SYSTEM_COLORS["muscular"]
    visible = "muscular" in active_systems

    # Pectoralis major (bilateral)
    for sign in [-1, 1]:
        pec_pos = ratio_to_vtk(0.30, sign * 0.05, 0.08)
        a = _make_ellipsoid(pec_pos, (0.07, 0.025, 0.04), color, 0.45)
        a.SetVisibility(visible)
        actors.append(a)

    # Deltoids (bilateral)
    for sign in [-1, 1]:
        delt_pos = ratio_to_vtk(0.26, sign * SHOULDER_WIDTH_RATIO / 2 * 0.95, 0.02)
        a = _make_ellipsoid(delt_pos, (0.035, 0.035, 0.04), color, 0.45)
        a.SetVisibility(visible)
        actors.append(a)

    # Rectus abdominis — 6-pack
    for i in range(6):
        for sign in [-1, 1]:
            ab_z = ratio_to_vtk(0.36 + i * 0.025)[2]
            a = _make_ellipsoid((sign * 0.025, 0.09, ab_z),
                                (0.022, 0.015, 0.012), color, 0.40)
            a.SetVisibility(visible)
            actors.append(a)

    # Trapezius (posterior)
    trap_pos = ratio_to_vtk(0.26, 0, -0.10)
    a = _make_ellipsoid(trap_pos, (0.10, 0.02, 0.08), color, 0.35)
    a.SetVisibility(visible)
    actors.append(a)

    # Latissimus dorsi (bilateral posterior)
    for sign in [-1, 1]:
        lat_pos = ratio_to_vtk(0.38, sign * 0.08, -0.09)
        a = _make_ellipsoid(lat_pos, (0.06, 0.015, 0.08), color, 0.35)
        a.SetVisibility(visible)
        actors.append(a)

    # Gluteus maximus (bilateral posterior)
    for sign in [-1, 1]:
        glute_pos = ratio_to_vtk(0.56, sign * 0.06, -0.06)
        a = _make_ellipsoid(glute_pos, (0.06, 0.05, 0.05), color, 0.45)
        a.SetVisibility(visible)
        actors.append(a)

    # Quadriceps (bilateral)
    for sign in [-1, 1]:
        quad_pos = ratio_to_vtk(0.65, sign * 0.055, 0.03)
        quad = vtk.vtkCylinderSource()
        quad.SetHeight(THIGH_RATIO * H * 0.7)
        quad.SetRadius(0.04)
        quad.SetResolution(16)
        a = _make_actor(quad, quad_pos, color, 0.40, orientation=(90, 0, 0))
        a.SetVisibility(visible)
        actors.append(a)

    # Hamstrings (bilateral posterior)
    for sign in [-1, 1]:
        ham_pos = ratio_to_vtk(0.67, sign * 0.055, -0.03)
        ham = vtk.vtkCylinderSource()
        ham.SetHeight(THIGH_RATIO * H * 0.6)
        ham.SetRadius(0.035)
        ham.SetResolution(16)
        a = _make_actor(ham, ham_pos, color, 0.35, orientation=(90, 0, 0))
        a.SetVisibility(visible)
        actors.append(a)

    for a in actors:
        renderer.AddActor(a)
    return actors


# ---------------------------------------------------------------------------
# LYMPHATIC
# ---------------------------------------------------------------------------

def build_lymphatic(renderer, active_systems):
    """Thymus, spleen, thoracic duct, lymph nodes. Returns list of actors."""
    actors = []
    color = SYSTEM_COLORS["lymphatic"]
    visible = "lymphatic" in active_systems

    # Thymus
    thymus_pos = ratio_to_vtk(0.250, 0, 0.05)
    a = _make_ellipsoid(thymus_pos, (0.03, 0.02, 0.025), color, 0.7)
    a.SetVisibility(visible)
    actors.append(a)

    # Spleen
    spleen_pos = ratio_to_vtk(SPLEEN_CENTER_Y, SPLEEN_CENTER_X, -0.02)
    spleen_rx = SPLEEN_WIDTH * H / 2
    spleen_ry = 0.025
    spleen_rz = SPLEEN_HEIGHT * H / 2
    a = _make_ellipsoid(spleen_pos, (spleen_rx, spleen_ry, spleen_rz),
                        color, 0.7)
    a.SetVisibility(visible)
    actors.append(a)

    # Thoracic duct — thin tube from abdomen to left subclavian
    td_points = [
        ratio_to_vtk(0.50, 0.01, -0.06),
        ratio_to_vtk(0.40, 0.005, -0.06),
        ratio_to_vtk(0.30, -0.01, -0.05),
        ratio_to_vtk(0.24, -0.03, -0.03),
    ]
    a = _make_tube(td_points, 0.004, color, 0.6)
    a.SetVisibility(visible)
    actors.append(a)

    # Lymph nodes — small spheres at key locations
    node_positions = [
        # Cervical nodes (bilateral)
        ratio_to_vtk(0.18, -0.04, 0.02),
        ratio_to_vtk(0.18, 0.04, 0.02),
        # Axillary nodes (bilateral)
        ratio_to_vtk(0.28, -0.14, 0.01),
        ratio_to_vtk(0.28, 0.14, 0.01),
        # Inguinal nodes (bilateral)
        ratio_to_vtk(0.57, -0.05, 0.03),
        ratio_to_vtk(0.57, 0.05, 0.03),
    ]
    for npos in node_positions:
        node = vtk.vtkSphereSource()
        node.SetRadius(0.012)
        node.SetThetaResolution(12)
        node.SetPhiResolution(12)
        a = _make_actor(node, npos, color, 0.7)
        a.SetVisibility(visible)
        actors.append(a)

    for a in actors:
        renderer.AddActor(a)
    return actors


# ===========================================================================
# SELF-CHECK: Prior error detection (Milestone 3 false positive protocol)
# ===========================================================================

def run_self_checks():
    """Print self-check values. Returns True if all pass."""
    all_pass = True

    # 1. Heart Z position
    heart_z = ratio_to_vtk(HEART_CENTER_Y, HEART_CENTER_X_OFF, 0.04)[2]
    expected_heart_z = (1.0 - 0.355) * H  # = 1.161m
    print(f"SELF-CHECK: heart z = {heart_z:.3f}m (should be ~1.161m for T5)")
    if heart_z > 1.20:
        print("  BLOCKING: heart at T3 level, not T5!")
        all_pass = False

    # 2. Liver X position
    liver_x = ratio_to_vtk(LIVER_CENTER_Y, LIVER_CENTER_X, 0.02)[0]
    print(f"SELF-CHECK: liver x = {liver_x:.3f}m (should be +0.108m, right side)")
    if liver_x < 0:
        print("  BLOCKING: liver on wrong side!")
        all_pass = False

    # 3. Lung asymmetry
    right_rz = RIGHT_LUNG_HEIGHT * H / 2
    left_rz = LEFT_LUNG_HEIGHT * H / 2
    print(f"SELF-CHECK: right_lung_rz = {right_rz:.3f}m > left_lung_rz = {left_rz:.3f}m: {right_rz > left_rz}")
    if right_rz <= left_rz:
        print("  BLOCKING: equal or smaller right lung!")
        all_pass = False

    # 4. Aorta bifurcation
    bif_z = ratio_to_vtk(AORTA_BIFURCATION_Y)[2]
    print(f"SELF-CHECK: bifurcation z = {bif_z:.3f}m (should be ~0.837m for L4)")
    if bif_z > 0.86:
        print("  BLOCKING: bifurcation at L3, not L4!")
        all_pass = False

    # 5. Diaphragm asymmetry
    print(f"SELF-CHECK: DIAPHRAGM_RIGHT_HIGHER = {DIAPHRAGM_RIGHT_HIGHER}")
    if not DIAPHRAGM_RIGHT_HIGHER:
        print("  BLOCKING: symmetric diaphragm!")
        all_pass = False

    return all_pass


# ===========================================================================
# KEYBOARD HANDLER
# ===========================================================================

class AnatomyInteractor(vtk.vtkInteractorStyleTrackballCamera):
    """Custom keyboard handler for toggling systems and saving screenshots."""

    def __init__(self, system_actors, render_window, renderer):
        self.system_actors = system_actors  # dict: system_name -> [actors]
        self.active_systems = set(SYSTEM_NAMES)
        self.render_window = render_window
        self.renderer = renderer
        self.AddObserver("KeyPressEvent", self._on_key)

    def _on_key(self, obj, event):
        key = self.GetInteractor().GetKeySym()

        key_map = {
            "1": "skeletal", "2": "muscular", "3": "nervous",
            "4": "circulatory", "5": "respiratory", "6": "digestive",
            "7": "lymphatic",
        }

        if key in key_map:
            system = key_map[key]
            if system in self.active_systems:
                self.active_systems.discard(system)
                for a in self.system_actors.get(system, []):
                    a.SetVisibility(False)
            else:
                self.active_systems.add(system)
                for a in self.system_actors.get(system, []):
                    a.SetVisibility(True)
            self.render_window.Render()

        elif key == "a":
            if len(self.active_systems) == len(SYSTEM_NAMES):
                # All on -> turn all off
                self.active_systems.clear()
                for sys_actors in self.system_actors.values():
                    for a in sys_actors:
                        a.SetVisibility(False)
            else:
                # Some off -> turn all on
                self.active_systems = set(SYSTEM_NAMES)
                for sys_actors in self.system_actors.values():
                    for a in sys_actors:
                        a.SetVisibility(True)
            self.render_window.Render()

        elif key == "s":
            save_screenshot(self.render_window, "figures/vtk_screenshot.png")
            print("Screenshot saved to figures/vtk_screenshot.png")

        elif key == "r":
            # Reset to anterior view
            camera = self.renderer.GetActiveCamera()
            camera.SetPosition(0, 4, 0.9)
            camera.SetFocalPoint(0, 0, 0.9)
            camera.SetViewUp(0, 0, 1)
            self.renderer.ResetCameraClippingRange()
            self.render_window.Render()

        elif key in ("q", "Escape"):
            self.render_window.Finalize()
            self.GetInteractor().TerminateApp()


# ===========================================================================
# SCREENSHOT
# ===========================================================================

def save_screenshot(render_window, filepath):
    """Save current VTK render to PNG."""
    figures_dir = Path(filepath).parent
    figures_dir.mkdir(parents=True, exist_ok=True)

    w2i = vtk.vtkWindowToImageFilter()
    w2i.SetInput(render_window)
    w2i.SetScale(1)
    w2i.SetInputBufferTypeToRGBA()
    w2i.ReadFrontBufferOff()
    w2i.Update()

    writer = vtk.vtkPNGWriter()
    writer.SetFileName(str(filepath))
    writer.SetInputConnection(w2i.GetOutputPort())
    writer.Write()


# ===========================================================================
# PUBLICATION FIGURES (Milestone 4)
# ===========================================================================

def generate_publication_figures(renderer, render_window, system_actors):
    """Generate static publication-quality PNG renders."""
    figures_dir = Path(__file__).parent / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    camera = renderer.GetActiveCamera()

    # White background for publication
    renderer.SetBackground(1.0, 1.0, 1.0)
    renderer.SetBackground2(0.95, 0.95, 0.97)
    renderer.GradientBackgroundOn()

    # --- Anterior view ---
    camera.SetPosition(0, 4, 0.9)
    camera.SetFocalPoint(0, 0, 0.9)
    camera.SetViewUp(0, 0, 1)
    renderer.ResetCameraClippingRange()
    # Show all systems
    for sys_actors in system_actors.values():
        for a in sys_actors:
            a.SetVisibility(True)
    render_window.Render()
    save_screenshot(render_window, str(figures_dir / "vtk_anterior.png"))
    print(f"Saved {figures_dir / 'vtk_anterior.png'}")

    # --- Lateral view ---
    camera.SetPosition(4, 0, 0.9)
    camera.SetFocalPoint(0, 0, 0.9)
    camera.SetViewUp(0, 0, 1)
    renderer.ResetCameraClippingRange()
    render_window.Render()
    save_screenshot(render_window, str(figures_dir / "vtk_lateral.png"))
    print(f"Saved {figures_dir / 'vtk_lateral.png'}")

    # --- Systems grid (7 panels) ---
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.image import imread

    panels = []
    for sys_name in SYSTEM_NAMES:
        # Hide all, show only this system + body surface
        for name, sys_actors_list in system_actors.items():
            vis = (name == sys_name)
            for a in sys_actors_list:
                a.SetVisibility(vis)
        # Reset camera to anterior
        camera.SetPosition(0, 4, 0.9)
        camera.SetFocalPoint(0, 0, 0.9)
        camera.SetViewUp(0, 0, 1)
        renderer.ResetCameraClippingRange()
        render_window.Render()

        # Save temp panel to figures dir (avoid Windows temp file locking)
        panel_path = str(figures_dir / f"_panel_{sys_name}.png")
        save_screenshot(render_window, panel_path)
        panels.append((sys_name, panel_path))

    # Compose grid with matplotlib
    fig, axes = plt.subplots(1, 7, figsize=(20, 4), dpi=100)
    for ax, (sys_name, panel_path) in zip(axes, panels):
        img = imread(panel_path)
        ax.imshow(img)
        ax.set_title(sys_name.capitalize(),
                     color=f"#{COLORS[sys_name].lstrip('#')}",
                     fontweight="bold", fontsize=10)
        ax.axis("off")
    plt.tight_layout()
    grid_path = str(figures_dir / "vtk_systems_grid.png")
    plt.savefig(grid_path, dpi=160, bbox_inches="tight")
    plt.close()
    print(f"Saved {grid_path}")

    # Clean up panel files
    for _, panel_path in panels:
        try:
            os.unlink(panel_path)
        except OSError:
            pass

    # Restore all systems visible and dark background
    for sys_actors_list in system_actors.values():
        for a in sys_actors_list:
            a.SetVisibility(True)
    renderer.SetBackground(0.05, 0.05, 0.08)
    renderer.GradientBackgroundOff()


# ===========================================================================
# MAIN
# ===========================================================================

def main():
    headless = "--test" in sys.argv
    pub_figures = "--figures" in sys.argv or headless

    # --- Renderer ---
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(0.05, 0.05, 0.08)

    # --- Render window ---
    render_window = vtk.vtkRenderWindow()
    render_window.SetSize(800, 900)
    render_window.SetWindowName("CHP Anatomy Viewer — VTK 3D")
    render_window.AddRenderer(renderer)

    if headless:
        render_window.OffScreenRenderingOn()

    # --- 3-point lighting ---
    renderer.RemoveAllLights()
    renderer.AutomaticLightCreationOff()

    key_light = vtk.vtkLight()
    key_light.SetPosition(2, 3, 4)
    key_light.SetIntensity(1.0)
    key_light.SetColor(1.0, 0.98, 0.90)
    renderer.AddLight(key_light)

    fill_light = vtk.vtkLight()
    fill_light.SetPosition(-2, 1, 2)
    fill_light.SetIntensity(0.4)
    fill_light.SetColor(0.85, 0.90, 1.0)
    renderer.AddLight(fill_light)

    back_light = vtk.vtkLight()
    back_light.SetPosition(0, -3, 1)
    back_light.SetIntensity(0.3)
    back_light.SetColor(1.0, 1.0, 1.0)
    renderer.AddLight(back_light)

    # --- Build all systems ---
    active_systems = set(SYSTEM_NAMES)

    body_actors = build_body_surface(renderer)

    system_actors = {}
    system_actors["skeletal"] = build_skeletal(renderer, active_systems)
    system_actors["muscular"] = build_muscular(renderer, active_systems)
    system_actors["nervous"] = build_nervous(renderer, active_systems)
    system_actors["circulatory"] = build_circulatory(renderer, active_systems)
    system_actors["respiratory"] = build_respiratory(renderer, active_systems)
    system_actors["digestive"] = build_digestive(renderer, active_systems)
    system_actors["lymphatic"] = build_lymphatic(renderer, active_systems)

    # --- Camera: anterior view, Z-up ---
    camera = renderer.GetActiveCamera()
    camera.SetPosition(0, 4, 0.9)
    camera.SetFocalPoint(0, 0, 0.9)
    camera.SetViewUp(0, 0, 1)
    renderer.ResetCameraClippingRange()

    # --- Run self-checks (Milestone 3 protocol) ---
    print("\n" + "=" * 60)
    print("CHP ANATOMY VIEWER v2 — SELF-CHECK (Prior Error Detection)")
    print("=" * 60)
    checks_pass = run_self_checks()
    print("=" * 60)
    if checks_pass:
        print("All self-checks PASSED.")
    else:
        print("BLOCKING: One or more self-checks FAILED!")
    print("=" * 60 + "\n")

    if headless:
        # Render one frame, save test figure, generate publication figures
        render_window.Render()
        figures_dir = Path(__file__).parent / "figures"
        figures_dir.mkdir(parents=True, exist_ok=True)
        save_screenshot(render_window, str(figures_dir / "vtk_test.png"))
        print(f"Test screenshot saved: {figures_dir / 'vtk_test.png'}")

        generate_publication_figures(renderer, render_window, system_actors)
        print("\nAll publication figures generated.")
        sys.exit(0)

    if pub_figures:
        render_window.Render()
        generate_publication_figures(renderer, render_window, system_actors)

    # --- Interactor ---
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)

    style = AnatomyInteractor(system_actors, render_window, renderer)
    interactor.SetInteractorStyle(style)

    # --- Show controls ---
    print("Controls:")
    print("  1-7: Toggle body systems (skeletal, muscular, nervous, etc.)")
    print("  A:   Toggle all systems on/off")
    print("  S:   Save screenshot to figures/")
    print("  R:   Reset to anterior view")
    print("  Q:   Quit")
    print("  Mouse: Rotate, zoom, pan")

    render_window.Render()
    interactor.Start()


if __name__ == "__main__":
    main()

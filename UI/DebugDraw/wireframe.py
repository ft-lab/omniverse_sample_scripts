from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import omni.ui
import omni.kit.app
import carb
import carb.events
import math
from omni.debugdraw import _debugDraw

_debugDraw = _debugDraw.acquire_debug_draw_interface()

# --------------------------------------------.
# Draw arrow.
# --------------------------------------------.
def drawArrow (p1, p2, color):
    _debugDraw.draw_line(carb.Float3(p1[0], p1[1], p1[2]), color, carb.Float3(p2[0], p2[1], p2[2]), color)
    P1 = Gf.Vec3f(p1[0], p1[1], p1[2])
    P2 = Gf.Vec3f(p2[0], p2[1], p2[2])
    vDir = P2 - P1
    lenV = vDir.GetLength()
    vDir /= lenV

    v1_2 = Gf.Vec4f(vDir[0], vDir[1], vDir[2], 1.0)
    v2_2 = Gf.Vec4f(0, 1, 0, 1.0)
    v3_2 = Gf.HomogeneousCross(v1_2, v2_2)

    vDirX = Gf.Vec3f(v3_2[0], v3_2[1], v3_2[2]).GetNormalized()
    vD1 = (vDir + vDirX).GetNormalized() * (lenV * 0.1)
    vD2 = (vDir - vDirX).GetNormalized() * (lenV * 0.1)

    pp = P1 + vD1
    _debugDraw.draw_line(carb.Float3(pp[0], pp[1], pp[2]), color, carb.Float3(P1[0], P1[1], P1[2]), color)
    pp = P1 + vD2
    _debugDraw.draw_line(carb.Float3(pp[0], pp[1], pp[2]), color, carb.Float3(P1[0], P1[1], P1[2]), color)

    pp = P2 - vD1
    _debugDraw.draw_line(carb.Float3(pp[0], pp[1], pp[2]), color, carb.Float3(P2[0], P2[1], P2[2]), color)
    pp = P2 - vD2
    _debugDraw.draw_line(carb.Float3(pp[0], pp[1], pp[2]), color, carb.Float3(P2[0], P2[1], P2[2]), color)

# ------------------------------------------.
# Update event.
# ------------------------------------------.
def on_update(e: carb.events.IEvent):
    color = 0xffffc000  # AARRGGBB

    r = 100.0
    angleD = 10.0
    angleV = 0.0
    px1 = 0.0
    pz1 = 0.0
    py1 = 0.0
    for i in range(200):
        px2 = math.cos(angleV * math.pi / 180.0) * r
        pz2 = math.sin(angleV * math.pi / 180.0) * r
        py2 = py1 + 0.1
        if i == 0:
            px1 = px2
            pz1 = pz2
        
        _debugDraw.draw_line(carb.Float3(px1, py1, pz1), color, carb.Float3(px2, py2, pz2), color)
        r -= 0.5

        angleV += angleD
        px1 = px2
        py1 = py2
        pz1 = pz2

    #_debugDraw.draw_point(carb.Float3(0, 30, 0), 0xffff0000)
    color2 = 0xffff0000
    drawArrow((-100.0, 5.0, -100.0), (-100.0, 5.0, 100.0), color2)

# ------------------------------------------.
# Register for update events.
# To clear the event, specify "subs=None".
subs = omni.kit.app.get_app().get_update_event_stream().create_subscription_to_pop(on_update, name="draw update")

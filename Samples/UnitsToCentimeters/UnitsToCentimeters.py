from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get metersPerUnit (default : 0.01).
metersPerUnit = UsdGeom.GetStageMetersPerUnit(stage)

# ----------------------------------------------------------------------.
# Convert the scale of Mesh and Xform so that metersPerUnit is 0.01.
# ----------------------------------------------------------------------.
def ConvPrimScale (_metersPerUnit, path):
    prim = stage.GetPrimAtPath(path)
    if prim.IsValid() == False:
        return False

    # Set xformOpOrder (Xform/Mesh).
    transformOrder = prim.GetAttribute('xformOpOrder')
    typeName = prim.GetTypeName()
    if typeName == 'Xform' or typeName == 'Mesh':
        tV = prim.GetAttribute('xformOp:scale')
        if tV.IsValid() == False:
            if prim.GetAttribute('xformOp:translate').IsValid() == False:
                prim.CreateAttribute("xformOp:translate", Sdf.ValueTypeNames.Float3, False).Set(Gf.Vec3f(0, 0, 0))
            if prim.GetAttribute('xformOp:scale').IsValid() == False:
                prim.CreateAttribute("xformOp:scale", Sdf.ValueTypeNames.Float3, False).Set(Gf.Vec3f(1, 1, 1))
            if prim.GetAttribute('xformOp:rotateXYZ').IsValid() == False:
                prim.CreateAttribute("xformOp:rotateXYZ", Sdf.ValueTypeNames.Float3, False).Set(Gf.Vec3f(0, 0, 0))

            transformOrder = prim.CreateAttribute("xformOpOrder", Sdf.ValueTypeNames.String, False)
            transformOrder.Set(["xformOp:translate", "xformOp:rotateXYZ", "xformOp:scale"])

    if transformOrder.IsValid() and transformOrder.Get() != None:
        tV = prim.GetAttribute('xformOp:scale')
        if tV.IsValid():
            scaleV = tV.Get()
            scale = _metersPerUnit / 0.01
            tV.Set(scaleV * scale)
            return True
    return False
    
# ----------------------------------------------------------------------.

if abs(metersPerUnit - 0.01) < 1e-5:
    print("The units of Stage are already centimeters.")
else:
    # Get default prim.
    defaultPrim = stage.GetDefaultPrim()
    if defaultPrim == None or defaultPrim.IsValid() == False:
        print("DefaultPrim does not exist.")
    else:
        path = defaultPrim.GetPath().pathString
        if ConvPrimScale(metersPerUnit, path) == False:
            print("Failed to change DefaultPrim.")
        else:
            # Set metersPerUnit.
            try:
                UsdGeom.SetStageMetersPerUnit(stage, 0.01)
                print("DefaultPrim has been successfully changed.")
            except Exception as e:
                print(e)


"""
This requires that Extension "omni.syntheticdata" be enabled.

Synthetic Data Sensor

"""
from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import omni.ui
import omni.kit.app
import omni.syntheticdata  # Use omni.syntheticdata extension.
import numpy as np
from PIL import Image
import OpenEXR

# Get main window viewport.
window = omni.ui.Window('Viewport')
viewportI = omni.kit.viewport.acquire_viewport_interface()
vWindow = viewportI.get_viewport_window(None)

iface = omni.syntheticdata._syntheticdata.acquire_syntheticdata_interface()
sensor_list = iface.get_sensor_list(vWindow)

#iface.create_sensor(omni.syntheticdata._syntheticdata.SensorType.DepthLinear, vWindow)

for sensorD in sensor_list:
    if iface.get_sensor_type(sensorD) == omni.syntheticdata._syntheticdata.SensorType.DepthLinear:
        # Get viewport image.
        data = iface.get_sensor_host_float_texture_array(sensorD)

        # Get size.
        hei, wid = data.shape[:2]

        # Store data (buff[hei][wid]).
        buff = np.frombuffer(data, np.float32).reshape(hei, wid, -1)

        print(str(wid) + " " + str(hei))

        # Save the Viewport image as a file.
        # The path should be rewritten to match your environment.
        filePath = "K:/temp/output_depth.png"

        # Create new image (with PIL).
        #im = Image.new("RGBA", (wid, hei), (0, 0, 0, 0))
        #im.save(filePath, quality=95)


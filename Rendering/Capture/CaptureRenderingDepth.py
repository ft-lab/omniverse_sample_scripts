"""
Use "Synthetic Data Sensor".

This requires that Extension "omni.syntheticdata" be enabled.
Set "Depth" of "Synthetic Data Sensor" to On.
"""
from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import omni.ui
import omni.kit.app
import omni.syntheticdata  # Use omni.syntheticdata extension.
import numpy as np
from PIL import Image
import itertools

# Colorize Helpers (ref : omni.syntheticdata)
def colorize_depth(depth_image):
    height, width = depth_image.shape[:2]
    colorized_image = np.zeros((height, width, 4))
    depth_image[depth_image == 0.0] = 1e-5
    depth_image = np.clip(depth_image, 0, 255)
    depth_image -= np.min(depth_image)
    depth_image /= np.max(depth_image) + 1e-8
    colorized_image[:, :, 0] = depth_image
    colorized_image[:, :, 1] = depth_image
    colorized_image[:, :, 2] = depth_image
    colorized_image[:, :, 3] = 1
    colorized_image = (colorized_image * 255).astype(int)
    return colorized_image

# Get main window viewport.
window = omni.ui.Window('Viewport')
viewportI = omni.kit.viewport.acquire_viewport_interface()
vWindow = viewportI.get_viewport_window(None)

iface = omni.syntheticdata._syntheticdata.acquire_syntheticdata_interface()
sensor_list = iface.get_sensor_list(vWindow)

for sensorD in sensor_list:
    if iface.get_sensor_type(sensorD) == omni.syntheticdata._syntheticdata.SensorType.DepthLinear:
        # Get viewport image.
        data = iface.get_sensor_host_float_texture_array(sensorD)

        # Get size.
        hei, wid = data.shape[:2]

        # Store data (buff[hei][wid]).
        buff = np.frombuffer(data, np.float32).reshape(hei, wid, -1)
        buff[buff == buff.max()] = 0

        # Save the Viewport image as a file.
        # The path should be rewritten to match your environment.
        filePath = "K:/temp/output_depth.png"

        # Convert float32 to RGBA.
        rgbaBuff  = colorize_depth(buff.squeeze())
        rgbaBuff2 = list(itertools.chain.from_iterable(rgbaBuff))

        rgbaBuff3 = []
        for item in rgbaBuff2:
            rgbaBuff3.append((item[0], item[1], item[2], item[3]))

        # Create new image (with PIL).
        im = Image.new("RGBA", (wid, hei), (0, 0, 0, 0))
        im.putdata(rgbaBuff3)   # store rgba.

        im.save(filePath, quality=95)


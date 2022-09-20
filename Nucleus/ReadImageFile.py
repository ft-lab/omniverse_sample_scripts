# See : https://docs.omniverse.nvidia.com/py/kit/source/extensions/omni.client/docs/index.html

import io
import omni.client
from PIL import Image

result, vers, content = omni.client.read_file("omniverse://localhost/Users/test/xxx.png")
if result != omni.client.Result.ERROR_NOT_FOUND:
    image_data = memoryview(content).tobytes()
    image = Image.open(io.BytesIO(image_data))

    # Show Image.
    image.show()

    # Save Image.
    #image.save("C:\\temp\\xxx.png")


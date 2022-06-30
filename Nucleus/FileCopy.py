# See : https://docs.omniverse.nvidia.com/py/kit/source/extensions/omni.client/docs/index.html

import asyncio
import omni.client

# The following should be rewritten for your environment.
srcURL = "K:\\NVIDIA_omniverse\\images\\tile_image.png"
dstURL = "omniverse://localhost/test/tile_image.png"

# Copy a file or folder.
# When copying is complete, proceed.
result = omni.client.copy(srcURL, dstURL)
if result == omni.client.Result.OK:
    print("success !")
else:
    print("failed ...")


# See : https://docs.omniverse.nvidia.com/py/kit/source/extensions/omni.client/docs/index.html

import asyncio
import omni.client

# The following should be rewritten for your environment.
url = "omniverse://localhost/test/new_folder"

result = omni.client.create_folder(url)
if result == omni.client.Result.OK:
    print("success !")
else:
    print("failed ...")


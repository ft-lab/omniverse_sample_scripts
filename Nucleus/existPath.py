# See : https://docs.omniverse.nvidia.com/py/kit/source/extensions/omni.client/docs/index.html

import asyncio
import omni.client

# Check for the existence of the specified path.
async def existPath (path : str):
    (result, entry) = await omni.client.stat_async(path)
    if result == omni.client.Result.ERROR_NOT_FOUND:
        print("Does not exist : " + path)
        return

    print("Exist : " + path)

# ------------------------------------------.
path1 = "omniverse://localhost/Users/test"
asyncio.ensure_future(existPath(path1))

path2 = "omniverse://localhost/Users/test/xxx.usd"
asyncio.ensure_future(existPath(path2))


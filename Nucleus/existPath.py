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

# Awaiting results.
async def _ocl_existPath (path : str):
    (result, entry) = await omni.client.stat_async(path)
    if result == omni.client.Result.ERROR_NOT_FOUND:
        return False
    return True

def ocl_existPath (path : str):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(_ocl_existPath(path))

# ------------------------------------------.
path1 = "omniverse://localhost/Users/test"
asyncio.ensure_future(existPath(path1))

path2 = "omniverse://localhost/Users/test/xxx.usd"
asyncio.ensure_future(existPath(path2))


if ocl_existPath(path1):
    print("Exist : " + path1)
else:
    print("Does not exist : " + path1)

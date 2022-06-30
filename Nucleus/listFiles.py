# See : https://docs.omniverse.nvidia.com/py/kit/source/extensions/omni.client/docs/index.html

import asyncio
import omni.client

# Lists files in the specified path.
async def listFiles (_depth : int, _path : str):
    (result, entries) = await omni.client.list_async(_path)
    if result != omni.client.Result.OK:
        return

    for entry in entries:
        # Skip for Channel file.
        if (entry.flags & omni.client.ItemFlags.IS_CHANNEL) != 0:
            continue

        name = entry.relative_path
        if name == "" or name.find(".") == 0:
            continue

        path = _path + "/" + name

        isFolder = (entry.flags & omni.client.ItemFlags.CAN_HAVE_CHILDREN) != 0

        msg = ""
        for i in range(_depth):
            msg += "  "

        if isFolder:
            msg += "[" + name + "]"
        else:
            msg += name
        
        msg += "   "
        if (entry.flags & omni.client.ItemFlags.READABLE_FILE) != 0:
            msg += " [R]"
        if (entry.flags & omni.client.ItemFlags.WRITEABLE_FILE) != 0:
            msg += " [W]"
        if (entry.flags & omni.client.ItemFlags.CAN_LIVE_UPDATE) != 0:
            msg += " [LiveUpdate]"

        if not isFolder:
            msg += f" {entry.size} bytes"

        print(msg)

        if isFolder:
            await listFiles(_depth + 1, path)

# -----------------------------------------------.

path1 = "omniverse://localhost/Users/test"
asyncio.ensure_future(listFiles(0, path1))


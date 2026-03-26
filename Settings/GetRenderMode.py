import carb.settings
import omni.kit

import asyncio

def get_rendering_mode() -> str:
    """
    Get the current rendering mode from Omniverse settings.

    Returns:
        A string representing the current rendering mode.
        "iray", "pxr", "PathTracing", "RealTimePathTracing" or other custom modes.
    """

    # Get Render Mode.
    settings = carb.settings.get_settings()
    renderMode = settings.get("/rtx/rendermode")

    # rtx, iray, pxr
    activeRender = settings.get("/renderer/active")

    if activeRender == "rtx":
        # "PathTracing", "RealTimePathTracing"
        return renderMode
    else:
        return activeRender

async def set_rendering_mode(mode: str):
    """
    Set the rendering mode in Omniverse.

    Args:
        mode (RenderingMode): The rendering mode to set. Options include "iray", "pxr", "PathTracing", "RealTimePathTracing".
    """
    settings = carb.settings.get_settings()
    await omni.kit.app.get_app().next_update_async()

    if mode == "iray":
        settings.set("/renderer/active", "iray")
    elif mode == "pxr":
        settings.set("/renderer/active", "pxr")
    else:
        settings.set("/renderer/active", "rtx")
        settings.set("/rtx/rendermode", mode)

print(f"Current Render Mode: {get_rendering_mode()}")


# Set "RTX-Real-Time 2.0"
asyncio.ensure_future(set_rendering_mode("RealTimePathTracing"))

# Set "RTX-Interactive"
asyncio.ensure_future(set_rendering_mode("PathTracing"))


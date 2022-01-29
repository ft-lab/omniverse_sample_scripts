import carb.settings

# Get Render Mode.
# However, it seems that iray cannot be identified.
settings = carb.settings.get_settings()
renderMode = settings.get('/rtx/rendermode')

if renderMode == 'RaytracedLighting':
    print("Render Mode : RTX Real-time")
else:
    if renderMode == 'PathTracing':
        print("Render Mode : RTX Path-traced")
    else:
        print("Render Mode : " + renderMode)

# Set "RTX Real-time"
settings.set('/rtx/rendermode', 'RaytracedLighting')

# Set "RTX Path-traced"
settings.set('/rtx/rendermode', 'PathTracing')

import carb
import omni
import asyncio
import omni.kit.asset_converter

# Progress of processing.
def progress_callback (current_step: int, total: int):
   # Show progress
   print(f"{current_step} of {total}")

# Convert asset file(obj/fbx/glTF, etc) to usd.
async def convert_asset_to_usd (input_asset: str, output_usd: str):
   # Input options are defaults.
   converter_context = omni.kit.asset_converter.AssetConverterContext()
   instance = omni.kit.asset_converter.get_instance()
   task = instance.create_converter_task(input_asset, output_usd, progress_callback, converter_context)

   # Wait for completion.
   success = await task.wait_until_finished()
   if not success:
       carb.log_error(task.get_status(), task.get_detailed_error())
   print("converting done")

# Rewrite it to suit your environment.
input_obj  = "K:/Modeling/obj/simple_obj2/simple_obj.obj"
output_usd = "K:/Modeling/obj/simple_obj2/simple_obj/simple_obj.usd"

# Convert to USD (obj to USD).
asyncio.ensure_future(
   convert_asset_to_usd(input_obj, output_usd)
)

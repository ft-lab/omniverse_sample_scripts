# --------------------------------------------------.
# obj to usd conversion.
# See : https://docs.omniverse.nvidia.com/app_create/prod_extensions/ext_asset-converter.html
# --------------------------------------------------.
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
   converter_context.ignore_materials = False
   converter_context.ignore_camera = False
   converter_context.ignore_animations = False
   converter_context.ignore_light = False
   converter_context.export_preview_surface = False
   converter_context.use_meter_as_world_unit = False
   converter_context.create_world_as_default_root_prim = True
   converter_context.embed_textures = True
   converter_context.convert_fbx_to_y_up = False
   converter_context.convert_fbx_to_z_up = False
   converter_context.merge_all_meshes = False
   converter_context.use_double_precision_to_usd_transform_op = False 
   converter_context.ignore_pivots = False 
   converter_context.keep_all_materials = True
   converter_context.smooth_normals = True
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

import os.path
import carb.tokens

kitPath = os.path.abspath(carb.tokens.get_tokens_interface().resolve("${kit}"))
print(kitPath)

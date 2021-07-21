import sys
import os

# Append path.
def appendSysPath (newPath):
    existF = False
    for path in sys.path:
      if path == newPath:
        existF = True
        break

    if existF:
      return

    sys.path.append(newPath)

for path in sys.path:
    print(path)



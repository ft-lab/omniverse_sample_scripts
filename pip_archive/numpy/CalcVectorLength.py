import numpy

val = numpy.array([2.5, 1.0, 3.0])
lenV = numpy.linalg.norm(val)

print(f"{val} : Length = {lenV}")

# Normalized.
lenV = numpy.linalg.norm(val)
val2 = val
if lenV != 0.0:
  val2 = val / lenV

print(f"Normalized {val} ==> {val2}")

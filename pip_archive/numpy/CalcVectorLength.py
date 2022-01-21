import numpy

val = numpy.array([2.5, 1.0, 3.0])
lenV = numpy.linalg.norm(val)

print(str(val) + " : Length = " + str(lenV))

# Normalized.
lenV = numpy.linalg.norm(val)
val2 = val
if lenV != 0.0:
  val2 = val / lenV

print("Normalized " + str(val) + " ==> " + str(val2))

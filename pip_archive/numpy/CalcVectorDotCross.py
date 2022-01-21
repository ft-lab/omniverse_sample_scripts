import numpy

v1 = numpy.array([0.0, 1.0, 2.0])
v2 = numpy.array([1.2, 1.5, 2.3])

# Calculating the Inner Product.
v = numpy.dot(v1, v2)
print("Inner product : " + str(v))

# Calculating the Outer Product.
v = numpy.cross(v1, v2)
print("Outer product : " + str(v))

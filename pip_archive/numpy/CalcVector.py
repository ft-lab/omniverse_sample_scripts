import numpy

v1 = numpy.array([0.0, 1.0, 2.0])
v2 = numpy.array([1.2, 1.5, 2.3])

v3 = v1 + v2
print(v3)

v3 = v1 * v2
print(v3)

v2[0] += 0.5
print(v2[0])
print(v2[1])
print(v2[2])


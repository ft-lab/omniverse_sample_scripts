import numpy

# Create Vector3.
v1 = numpy.array([0.0, 1.0, 2.0])

# Create 4x4 matrix.
m1 = numpy.matrix(numpy.identity(4))
m1[3] = [22.3, 15.5, 3.0, 1.0]

# Make sure that the vector to be multiplied has four elements.
vec4 = numpy.array(v1)
if v1.size == 3:
  vec4 = numpy.array([v1[0], v1[1], v1[2], 1.0])

# Vector and matrix multiplication.
retM = numpy.dot(vec4, m1)
print(retM)

# Replace the result with Vector3.
retV = numpy.array([retM[0,0], retM[0,1], retM[0,2]])
print(retV)

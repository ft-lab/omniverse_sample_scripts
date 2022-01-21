import numpy

# Create 4x4 matrix (identity matrix).
m1 = numpy.matrix(numpy.identity(4))
m2 = numpy.matrix(numpy.identity(4))

m1[3] = [22.3, 15.5, 3.0, 1.0]
m2[3] = [50.0, 100.0, -20.0, 1.0]

# Multiply matrix.
# (Same result for mA and mB)
mA = m1 * m2
mB = numpy.dot(m1, m2)
print(mA)
print(mB)


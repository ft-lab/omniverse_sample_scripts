import numpy

# Create 4x4 matrix (identity matrix).
m = numpy.matrix(numpy.identity(4))
print(m)

# Set a value to a matrix.
m[3,0] = 2.0
m[2] = [50.0, 100.0, -20.0, 1.0]
print(m)

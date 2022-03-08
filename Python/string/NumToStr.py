v = 0.25364

# number to string.
# ==> "0.25364"
print("Value = " + str(v))

# Digit number specification.
# ==> "0000.25364"
print("Value : {:#010}".format(v))
print("Value : " + format(v, '#010'))

# Specify the number of decimal places.
# ==> "0.254"
print("Value : {:.3f}".format(v))
print("Value : " + format(v, '.3f'))

# Replaced by hexadecimal.
# ==> "0x7fff"
v2 = 32767
print(hex(v2))

# Replaced by a binary number.
# ==> "0b101"
v2 = 5
print(bin(v2))


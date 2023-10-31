"""
A file consisting of functions to convert between binary and decimal numbers.
"""
from common import *
LOWER_LIMIT = -2147483648
UPPER_LIMIT = 2147483648

def int_to_bin(number):
    """
    Convert an integer to a binary string.
    """
    return format(number, 'b')

def int_to_32bin(number):
    """
    Convert an integer to a 32-bit binary string.
    """
    return format(number, '032b')

def bin_to_int(number):
    """
    Convert a binary string to an integer.
    """
    return int(number, 2)


#  https://stackoverflow.com/questions/1604464/twos-complement-in-python
"""def twos_comp(val, bits):
    # compute the 2's complement of int value val
    if (val & (1 << (bits - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)         # compute negative value
    return val                          # return positive value as is
"""


# made by co-pilot
def twos_comp(binary, bits=32):
    """
    Compute the 2's complement of binary string.
    """
    if binary[0] == '1':
        return bin_to_int(binary) - (1 << bits)
    else:
        return bin_to_int(binary)

if __name__ == '__main__':
    # test if implemented correctly
    print(int_to_bin(-1))
    print(int_to_32bin(10))
    print(bin_to_int('1010'))
    print(bin_to_int('00000000000000000000000000001010'))
    print(twos_comp('101', 0))
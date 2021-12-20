import struct


def real_convert(value: bytearray) -> float:
    # print(value)
    real = struct.unpack('>f', struct.pack('4B', *value))[0]
    # print(round(real, 5))
    return round(real, 5)

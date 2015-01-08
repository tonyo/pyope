

def byte_to_bitstring(byte):
    """Convert one byte to a list of bits"""
    assert 0 <= byte <= 0xff
    bits = [int(x) for x in list(bin(byte + 0x100)[3:])]
    return bits


def str_to_bitstring(data):
    """Convert a string to a list of bits"""
    byte_list = list(bytearray(data))
    bit_list = [bit for data_byte in byte_list for bit in byte_to_bitstring(data_byte)]
    return bit_list
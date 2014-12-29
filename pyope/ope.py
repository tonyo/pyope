import math
from .hgd import gen_hgd

DEFAULT_IN_START = 0
DEFAULT_IN_END = 2**16
DEFAULT_OUT_START = 0
DEFAULT_OUT_END = 2**32


class ValueRange(object):

    def __init__(self, start, end):
        start, end = int(start), int(end)
        if start > end:
            raise Exception("Invalid range: start is larger than end")
        self.start = start
        self.end = end

    def size(self):
        return self.end - self.start + 1


class OPE(object):

    def __init__(self, key, in_range=None, out_range=None):
        self.key = key
        if in_range is None:
            in_range = ValueRange(DEFAULT_IN_START, DEFAULT_IN_END)
        self.in_range = in_range

        if out_range is None:
            out_range = ValueRange(DEFAULT_OUT_START, DEFAULT_OUT_END)
        self.out_range = out_range

    def encrypt(self, plaintext):
        return self.encrypt_rec(plaintext, self.in_range, self.out_range)

    def encrypt_rec(self, plaintext, in_range, out_range):
        assert in_range.size() <= out_range.size()
        in_size = in_range.size()       # M
        out_size = out_range.size()     # N
        in_edge = in_range.start - 1    # d
        out_edge = out_range.start - 1  # r
        mid = out_edge + int(math.ceil(out_size / 2.0))  # y
        if in_range.size() == 1:
            pass
        cc = self.tape_gen()
        x = gen_hgd()
        if plaintext <= x:
            in_range = ValueRange(in_edge + 1, x)
            out_range = ValueRange(out_edge + 1, mid)
        else:
            in_range = ValueRange(x + 1, in_edge + in_size)
            out_range = ValueRange(mid + 1, out_edge + out_size)
        return self.encrypt_rec(plaintext, in_range, out_range)

    def decrypt(self, ciphertext):
        return None

    def tape_gen(self):
        return 0
from hmac import HMAC
from math import ceil, log
import random
import stat

DEFAULT_IN_START = 0
DEFAULT_IN_END = 2**15 - 1
DEFAULT_OUT_START = 0
DEFAULT_OUT_END = 2**31 - 1


class ValueRange(object):

    def __init__(self, start, end):
        start, end = int(start), int(end)
        if start > end:
            raise Exception("Invalid range: start is greater than end")
        self.start = start
        self.end = end

    def size(self):
        return self.end - self.start + 1

    def range_bit_size(self):
        return int(ceil(log(self.size(), 2)))

    def contains(self, number):
        return self.start <= number <= self.end


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
        return self.encrypt_recursive(plaintext, self.in_range, self.out_range)

    def encrypt_recursive(self, plaintext, in_range, out_range):
        assert in_range.size() <= out_range.size()
        in_size = in_range.size()       # M
        out_size = out_range.size()     # N
        in_edge = in_range.start - 1    # d
        out_edge = out_range.start - 1  # r
        mid = out_edge + int(ceil(out_size / 2.0))  # y
        if in_range.size() == 1:
            coins = self.tape_gen(plaintext, out_range.range_bit_size())
            ciphertext = stat.sample_uniform(out_range, coins)
            return ciphertext
        coins = self.tape_gen(mid, in_range.range_bit_size())
        x = stat.sample_hgd(in_range, out_range, mid, coins)

        if plaintext <= x:
            in_range = ValueRange(in_edge + 1, x)
            out_range = ValueRange(out_edge + 1, mid)
        else:
            in_range = ValueRange(x + 1, in_edge + in_size)
            out_range = ValueRange(mid + 1, out_edge + out_size)
        return self.encrypt_recursive(plaintext, in_range, out_range)

    def decrypt(self, ciphertext):
        return self.decrypt_recursive(ciphertext, self.in_range, self.out_range)

    def decrypt_recursive(self, ciphertext, in_range, out_range):
        assert in_range.size() <= out_range.size()
        in_size = in_range.size()       # M
        out_size = out_range.size()     # N
        in_edge = in_range.start - 1    # d
        out_edge = out_range.start - 1  # r
        mid = out_edge + int(ceil(out_size / 2.0))  # y
        if in_range.size() == 1:
            in_range_min = in_range.start
            coins = self.tape_gen(in_range_min, out_range.range_bit_size())
            sampled_ciphertext = stat.sample_uniform(out_range, coins)
            if sampled_ciphertext == ciphertext:
                return in_range_min
            else:
                raise Exception('Invalid ciphertext')
        coins = self.tape_gen(mid, in_range.range_bit_size())
        x = stat.sample_hgd(in_range, out_range, mid, coins)

        if ciphertext <= mid:
            in_range = ValueRange(in_edge + 1, x)
            out_range = ValueRange(out_edge + 1, mid)
        else:
            in_range = ValueRange(x + 1, in_edge + in_size)
            out_range = ValueRange(mid + 1, out_edge + out_size)
        return self.decrypt_recursive(ciphertext, in_range, out_range)

    def tape_gen(self, data, bits_needed):
        """Returns a bit string as a long integer"""
        assert(bits_needed >= 0)
        if bits_needed == 0:
            return [0]
        # TODO proper pack?
        data = bytes(data)
        hmac_obj = HMAC(self.key)
        hmac_obj.update(data)
        digest = hmac_obj.digest()
        random.seed(digest)
        bits = [random.randint(0, 1) for _ in range(bits_needed)]
        return bits

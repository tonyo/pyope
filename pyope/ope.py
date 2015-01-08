import hmac
import math
import random
from Crypto.Cipher import AES
from Crypto.Util import Counter
from pyope.util import str_to_bitstring
import stat
import hashlib

from pyope.errors import InvalidCiphertextError, InvalidRangeLimitsError, OutOfRangeError


DEFAULT_IN_RANGE_START = 0
DEFAULT_IN_RANGE_END = 2**15 - 1
DEFAULT_OUT_RANGE_START = 0
DEFAULT_OUT_RANGE_END = 2**31 - 1


class ValueRange(object):

    def __init__(self, start, end):
        start, end = int(start), int(end)
        if start > end:
            raise InvalidRangeLimitsError("Invalid range: the start of the range is greater than the end")
        self.start = start
        self.end = end

    def size(self):
        return self.end - self.start + 1

    def range_bit_size(self):
        """Return a number of bits required to encode any value within the range"""
        return int(math.ceil(math.log(self.size(), 2)))

    def contains(self, number):
        return self.start <= number <= self.end

    def copy(self):
        return ValueRange(self.start, self.end)


class OPE(object):

    def __init__(self, key, in_range=None, out_range=None):
        self.key = key
        if in_range is None:
            in_range = ValueRange(DEFAULT_IN_RANGE_START, DEFAULT_IN_RANGE_END)
        self.in_range = in_range

        if out_range is None:
            out_range = ValueRange(DEFAULT_OUT_RANGE_START, DEFAULT_OUT_RANGE_END)
        self.out_range = out_range

    def encrypt(self, plaintext):
        if not self.in_range.contains(plaintext):
            raise OutOfRangeError('Plaintext is not within the input range')
        return self.encrypt_recursive(plaintext, self.in_range, self.out_range)

    def encrypt_recursive(self, plaintext, in_range, out_range):
        in_size = in_range.size()       # M
        out_size = out_range.size()     # N
        in_edge = in_range.start - 1    # d
        out_edge = out_range.start - 1  # r
        mid = out_edge + int(math.ceil(out_size / 2.0))  # y
        assert in_size <= out_size
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
        if not self.out_range.contains(ciphertext):
            raise OutOfRangeError('Plaintext is not within the output range')
        return self.decrypt_recursive(ciphertext, self.in_range, self.out_range)

    def decrypt_recursive(self, ciphertext, in_range, out_range):
        in_size = in_range.size()       # M
        out_size = out_range.size()     # N
        in_edge = in_range.start - 1    # d
        out_edge = out_range.start - 1  # r
        mid = out_edge + int(math.ceil(out_size / 2.0))  # y
        assert in_size <= out_size
        if in_range.size() == 1:
            in_range_min = in_range.start
            coins = self.tape_gen(in_range_min, out_range.range_bit_size())
            sampled_ciphertext = stat.sample_uniform(out_range, coins)
            if sampled_ciphertext == ciphertext:
                return in_range_min
            else:
                raise InvalidCiphertextError('Invalid ciphertext')
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
        bits_needed = int(bits_needed)
        assert(bits_needed >= 0)
        if bits_needed == 0:
            return []
        data = bytes(data)
        # Derive a key
        hmac_obj = hmac.HMAC(self.key, digestmod=hashlib.sha256)
        hmac_obj.update(data)
        assert hmac_obj.digest_size == 32
        digest = hmac_obj.digest()

        # Use AES-CTR cipher to generate a pseudo-random bit string
        aes_cipher = AES.new(digest, AES.MODE_CTR, counter=Counter.new(nbits=128))
        bytes_needed = (bits_needed + 7) / 8
        encrypted_data = aes_cipher.encrypt('\x00' * bytes_needed)

        # Convert the data to a list of bits
        bits = str_to_bitstring(encrypted_data)[:bits_needed]
        return bits

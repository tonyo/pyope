from pyope.ope import OPE, ValueRange


def test_order_guarantees():
    values = [0, 1, 2, 10, 28, 42, 1000, 1001]
    key = 'key'
    cipher = OPE(key)
    encrypted_values = [cipher.encrypt(value) for value in values]
    assert encrypted_values == sorted(set(encrypted_values)), "Order is not preserved"


def test_ope_encrypt_decrypt():
    values = [0, 10, 100, 314, 1337, 1338, 10000]
    key = 'key'
    cipher = OPE(key)
    encrypted_values = [cipher.encrypt(value) for value in values]

    cipher_dec = OPE(key)
    for value, encrypted in zip(values, encrypted_values):
        decrypted = cipher_dec.decrypt(encrypted)
        assert value == decrypted, "Dec(Enc(P)) != P"

def test_dense_range():
    range_start = 0
    range_end = 2**15
    in_range = ValueRange(range_start, range_end)
    out_range = ValueRange(range_start, range_end)
    key = '123'
    cipher = OPE(key, in_range, out_range)
    values = [0, 10, 20, 50, 100, 1000, 2**10, 2**15]
    for v in values:
        assert cipher.encrypt(v) == v
        assert cipher.decrypt(v) == v


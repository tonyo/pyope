from pyope.ope import OPE, ValueRange


def test_order_guarantees():
    """Test that encryption is order-preserving"""
    values = [0, 1, 2, 10, 28, 42, 1000, 1001, 2**15 - 1]
    key = 'key'
    cipher = OPE(key)
    encrypted_values = [cipher.encrypt(value) for value in values]
    assert encrypted_values == sorted(set(encrypted_values)), "Order is not preserved"


def test_ope_encrypt_decrypt():
    """Encrypt and then decrypt"""
    values = [0, 10, 100, 314, 1337, 1338, 10000]
    key = 'key'
    # Client encrypts values
    cipher = OPE(key)
    encrypted_values = [cipher.encrypt(value) for value in values]

    # Decryption at the peer side
    cipher_dec = OPE(key)
    for value, encrypted in zip(values, encrypted_values):
        decrypted = cipher_dec.decrypt(encrypted)
        assert value == decrypted, "Dec(Enc(P)) != P"


def test_dense_range():
    """Equal ranges must yield 1-to-1 mapping"""
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


def test_long_different_keys():
    """Test that different keys yield different ciphertexts"""
    key1 = '\x12\x23\x34\x45\x56\x67\x78\x89\x90\x0A\xAB\xBC\xCD\xDE\xEF\F0\x13\x14\x15\x16'
    key2 = '\x0A\xAB\xBC\xCD\xDE\xEF\F0\x13\x14\x15\x16\x12\x23\x34\x45\x56\x67\x78\x89\x90\x12\x13'
    ope1, ope2 = OPE(key1), OPE(key2)
    values = [0, 1, 10, 100, 1000, 2000, 3000, 4000, 5000]
    for v in values:
        assert ope1.encrypt(v) != ope2.encrypt(v)

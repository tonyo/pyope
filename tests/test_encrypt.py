from pyope.ope import OPE


def test_order_guarantees():
    values = [0, 1, 2, 42, 1000, 1001]
    key = 'key'
    cipher = OPE(key)
    encrypted_values = [cipher.encrypt(value) for value in values]
    assert encrypted_values == sorted(set(encrypted_values))


def test_ope_encrypt_decrypt():
    values = [0, 10, 100, 314, 1337]
    key = 'key'
    cipher = OPE(key)
    for value in values:
        encrypted = cipher.encrypt(value)
        assert value == cipher.decrypt(encrypted)

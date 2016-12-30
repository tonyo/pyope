class InvalidCiphertextError(ValueError):
    pass


class InvalidRangeLimitsError(ValueError):
    pass


class OutOfRangeError(ValueError):
    pass


class NotEnoughCoinsError(Exception):
    pass


class InvalidCoinError(Exception):
    pass

import string

keyspace = (string.digits + string.ascii_letters)


def encode_int(value, keyspace=keyspace):
    """
    Encode a positive integer into a variable-length string.

    By default, the keyspace is ascii-compatible.

    :param value: The integer to encode.
    :type value: int
    :param keyspace: The keyspace string to use.
    :type keyspace: str
    :return: Encoded string.
    """
    if value < 0:
        raise ValueError('value must be positive')
    value = int(value)
    out = []
    while value:
        value, digit = divmod(value, len(keyspace))
        out.append(keyspace[digit])
    return ''.join(out[::-1])


def decode_int(str, keyspace=keyspace):
    """
    Decode an integer previously encoded by `decode_int`.

    :param str: The encoded string.
    :type str: str
    :param keyspace: The encoding keyspace. This will naturally
                     have to be the same used while encoding for
                     correct results.
    :type keyspace: str
    :return: an integer
    :rtype: int
    """
    out = 0
    n = len(keyspace)
    for char in str:
        out = out * n + keyspace.index(char)
    return out

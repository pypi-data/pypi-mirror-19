"""
Some helpers for the internal ClickHouse protocol via :9000.
"""


def varint_length(x):
    return sum(x >= r for r in (0, 1 << 7, 1 << 14, 1 << 21, 1 << 28, 1 << 35, 1 << 42, 1 << 49, 1 << 56))


def int2varint(x):
    y = x
    result = []

    for _ in range(8):
        b = y & 0x7f
        if y > 0x7f:
            b = b | 0x80

        result.append(b)

        y = y >> 7

        if not y:
            return ''.join(map(chr, result))


def varint2int(x):
    result = 0

    for i, b in enumerate(x):
        result = result | (ord(b) & 0x7f) << (7 * i)

        if not (ord(b) & 0x80):
            return result


def to_string(value):
    return int2varint(len(value)) + value


"""
See dbms/include/DB/Core/Protocol.h for detailed info.

Client commands:
0 HELLO
1 QUERY
2 DATA
3 CANCEL
4 PING

Server commands:
0 HELLO
1 DATA
2 EXCEPTION
3 PROGRESS
4 PONG
5 END_OF_STREAM
6 PROFILE_INFO
7 TOTALS
8 EXTREMES
"""

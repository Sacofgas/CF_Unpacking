#!/usr/bin/env python3

import argparse
from datetime import datetime

def decode_cf61(data: bytes):
    idx = 0
    chunk_len = 17
    res = [data[idx:idx + chunk_len].hex()]

    idx += chunk_len
    chunk_len = 2
    res.append(data[idx:idx + chunk_len].hex())

    idx += chunk_len
    chunk_len = 1
    res.append(data[idx:idx + chunk_len].hex())

    idx += chunk_len
    chunk_len = 4
    res.append(f"{data[idx:idx + chunk_len].hex()} {datetime.fromtimestamp(int.from_bytes(data[idx:idx + chunk_len], 'big')).strftime('%Y/%m/%d %H:%M:%S')}")

    idx += chunk_len
    chunk_len = 2
    res.append(data[idx:idx + chunk_len].hex())

    idx += chunk_len
    chunk_len = 4
    for _ in range(3):
        res.append(data[idx:idx + chunk_len].hex())
        idx += chunk_len

    chunk_len = 2
    res.append(data[idx:idx + chunk_len].hex())

    idx += chunk_len
    res.append(data[idx:].hex())

    return res

def decode_cf62(data: bytes):
    res = decode_cf61(data[:-25] + data[-5:])[:-1]
    res += decode_cf61(data[:20] + data[40:])[3:]
    return res

def decode_cf63(data: bytes):
    idx = 0
    chunk_len = 17
    res = [data[idx:idx + chunk_len].hex()]

    idx += chunk_len
    chunk_len = 2
    res.append(data[idx:idx + chunk_len].hex())

    idx += chunk_len
    chunk_len = 1
    res.append(data[idx:idx + chunk_len].hex())

    idx += chunk_len
    chunk_len = 20
    res.append(data[idx:idx + chunk_len].hex())

    idx += chunk_len
    chunk_len = 1
    res.append(data[idx:idx + chunk_len].hex())

    idx += chunk_len
    chunk_len = 4
    hour = 6
    while idx + 5 < len(data):
        res.append(f"{data[idx:idx + chunk_len].hex(sep=',', bytes_per_sep=2)} {hour}->")
        hour = (hour + 1) % 24
        res[-1] += str(hour)
        idx += chunk_len

    res.append(data[idx:].hex())

    return res

def decode_cf64(data: bytes):
    res = decode_cf63(data[:40] + data[60:-101] + data[-5:])[:-1]
    second_part = decode_cf63(data[:20] + data[40:61] + data[-101:])
    res.insert(4, second_part[3])
    res += second_part[-25:]
    return res

def bytesfromhex(s: str) -> bytes:
    return bytes.fromhex(s)

def main():
    CF_FUNCTION_TABLE = {
        61: decode_cf61,
        62: decode_cf62,
        63: decode_cf63,
        64: decode_cf64,
    }

    parser = argparse.ArgumentParser()
    parser.add_argument('data', type=bytesfromhex, help='Input hex data string')
    args = parser.parse_args()

    for s in CF_FUNCTION_TABLE[args.data[0]](args.data):
        print(s.upper())

if __name__ == "__main__":
    main()

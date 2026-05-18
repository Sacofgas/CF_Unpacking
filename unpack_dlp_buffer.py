from argparse import ArgumentParser, Namespace
from collections.abc import Iterator
from ctypes import (
    BigEndianStructure,
    c_uint16,
    c_uint32,
    sizeof,
    Structure,
)
from datetime import datetime
from json import dumps as json_dumps
from typing import Any, Self


###################
#    FUNCTIONS    #
###################

class IterUnpackableBigEndianStructure(BigEndianStructure):

    @classmethod
    def iter_unpack(cls, data: bytes) -> Iterator[Self]:
        # this method is intended to be like `struct.Struct.iter_unpack()`
        size = sizeof(cls)
        if len(data) % size != 0:
            raise ValueError(f'Iterative unpacking requires a buffer of a multiple of {size} bytes.')
        num_elems = len(data) // size
        for i_elem in range(num_elems):
            i_byte_start = size * i_elem
            i_byte_end = i_byte_start + size
            bytes_of_elem = data[i_byte_start:i_byte_end]
            yield cls.from_buffer_copy(bytes_of_elem)


class DLPBufferEntry(IterUnpackableBigEndianStructure):
    # UNI/TS 11291-13-2 (UNI1610630) 5.4.11.4.2
    _pack_ = 1
    _fields_ = [
        ('unix_time', c_uint32),
        ('daily_diagnostic', c_uint16),
        ('curr_index_of_converted_vol', c_uint32),
        ('curr_index_of_converted_vol_under_alarm', c_uint32),
        ('max_conventional_converted_gas_flow_value', c_uint32),
        ('max_conventional_converted_gas_flow_status', c_uint16),
    ]


def ctypes_struct_2_dict(struct: Structure) -> dict[str, Any]:
    return {f: getattr(struct, f) for f, *_ in struct._fields_}


def unpack_dlp_buffer(dlp_buffer: bytes) -> None:
    _DATETIME_FMT = '%Y-%m-%d %H:%M:%S'
    _dd_num_bits = DLPBufferEntry.daily_diagnostic.size * 8
    elems = DLPBufferEntry.iter_unpack(dlp_buffer)
    expanded_elems = [
        {
            'index': i,
            'datetime': datetime.fromtimestamp(elem.unix_time).strftime(_DATETIME_FMT),
            'bitwise_daily_diagnostic': f'{elem.daily_diagnostic:0{_dd_num_bits}b}',
            'data': ctypes_struct_2_dict(elem),
        } for i, elem in enumerate(elems)
    ]
    json_str = json_dumps(expanded_elems, indent=4)
    print(json_str)


###################
#    SCRIPTING    #
###################

def create_argparser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument('data', type=bytes.fromhex, help='input hex data string')
    return parser


def parse_args() -> Namespace:
    parser = create_argparser()
    args = parser.parse_args()
    return args


def main() -> None:
    args = parse_args()
    unpack_dlp_buffer(args.data)


if __name__ == '__main__':
    main()

# Unpacking of UNI/TS 11291-13 Structures



## Compact Buffer of Compact Frame (CF)

Usage:

```sh cf.py [-h] data

positional arguments:
  data        Input hex data string

options:
  -h, --help  show this help message and exit
```

Example
```sh
python .\cf.py 3d6a1c6ec200016363020001e604a25888fe0e016a1bb240588800000000000000000000000000000000000000
```



## Buffer of Daily Load Profile

Usage:
```sh
python unpack_dlp_buffer.py [-h] data

positional arguments:
  data        input hex data string

options:
  -h, --help  show this help message and exit
```

Example:
```sh
python unpack_dlp_buffer.py 69F96B400800000000000000000000000000000069FABCC008000000000000000000000000000000
```

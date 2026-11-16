"""Minimal dependency-free PNG I/O for indexed images (Orchid graphics tools).

read_indexed(path)  -> (width, height, pixels[list of rows of ints], palette[list of (r,g,b)])
write_indexed(path, width, height, pixels, palette)
read_jasc(path)     -> palette list
"""
import struct
import zlib


def _chunks(data):
    pos = 8
    while pos < len(data):
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        ctype = data[pos + 4:pos + 8]
        yield ctype, data[pos + 8:pos + 8 + length]
        pos += 12 + length


def _unfilter(raw, width_bytes, height, bpp):
    rows = []
    prev = bytearray(width_bytes)
    pos = 0
    for _ in range(height):
        ftype = raw[pos]
        line = bytearray(raw[pos + 1:pos + 1 + width_bytes])
        pos += 1 + width_bytes
        for i in range(width_bytes):
            a = line[i - bpp] if i >= bpp else 0
            b = prev[i]
            c = prev[i - bpp] if i >= bpp else 0
            if ftype == 1:
                line[i] = (line[i] + a) & 0xFF
            elif ftype == 2:
                line[i] = (line[i] + b) & 0xFF
            elif ftype == 3:
                line[i] = (line[i] + ((a + b) >> 1)) & 0xFF
            elif ftype == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pred = a if pa <= pb and pa <= pc else (b if pb <= pc else c)
                line[i] = (line[i] + pred) & 0xFF
        rows.append(line)
        prev = line
    return rows


def read_indexed(path):
    data = open(path, "rb").read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path}: not a PNG")
    idat = b""
    palette = []
    for ctype, body in _chunks(data):
        if ctype == b"IHDR":
            width, height, depth, ctype_, _, _, interlace = struct.unpack(">IIBBBBB", body)
            if interlace:
                raise ValueError(f"{path}: interlaced PNG not supported")
        elif ctype == b"PLTE":
            palette = [tuple(body[i:i + 3]) for i in range(0, len(body), 3)]
        elif ctype == b"IDAT":
            idat += body
    if ctype_ not in (0, 3):
        raise ValueError(f"{path}: must be indexed or greyscale (colour type {ctype_})")
    raw = zlib.decompress(idat)
    width_bytes = (width * depth + 7) // 8
    rows = _unfilter(raw, width_bytes, height, 1)
    pixels = []
    per_byte = 8 // depth
    mask = (1 << depth) - 1
    for line in rows:
        row = []
        for x in range(width):
            byte = line[x // per_byte]
            shift = 8 - depth * (x % per_byte + 1)
            row.append((byte >> shift) & mask)
        pixels.append(row)
    return width, height, pixels, palette


def write_indexed(path, width, height, pixels, palette):
    def chunk(ctype, body):
        return (struct.pack(">I", len(body)) + ctype + body
                + struct.pack(">I", zlib.crc32(ctype + body) & 0xFFFFFFFF))
    raw = bytearray()
    for row in pixels:
        raw.append(0)
        raw.extend(bytes(row))
    pal = list(palette) + [(0, 0, 0)] * (256 - len(palette))
    out = b"\x89PNG\r\n\x1a\n"
    out += chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 3, 0, 0, 0))
    out += chunk(b"PLTE", b"".join(bytes(c) for c in pal[:256]))
    out += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    out += chunk(b"IEND", b"")
    open(path, "wb").write(out)


def read_jasc(path):
    lines = open(path).read().split()
    if lines[0] != "JASC-PAL":
        raise ValueError(f"{path}: not a JASC palette")
    count = int(lines[2])
    vals = list(map(int, lines[3:3 + count * 3]))
    return [tuple(vals[i:i + 3]) for i in range(0, count * 3, 3)]

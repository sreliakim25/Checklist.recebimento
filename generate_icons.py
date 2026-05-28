"""
Generate icon-192.png and icon-512.png using only Python stdlib.
Dark red (#5C1A2E) background, white "UDE" text, white border ring.
No PIL required — writes raw PNG via struct/zlib.
"""
import math
import struct
import zlib
import os

# ── Colour constants ──────────────────────────────────────────────
BG_R, BG_G, BG_B = 0x5C, 0x1A, 0x2E   # #5C1A2E  bordeaux
FG_R, FG_G, FG_B = 0xFF, 0xFF, 0xFF   # #FFFFFF  white


# ── PNG helpers ───────────────────────────────────────────────────
def _png_chunk(chunk_type: bytes, data: bytes) -> bytes:
    c = chunk_type + data
    return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xFFFFFFFF)


def _png_bytes(pixels: list[list[tuple[int, int, int]]]) -> bytes:
    """pixels[y][x] = (R, G, B)  →  PNG bytes (8-bit RGB, no alpha)."""
    h = len(pixels)
    w = len(pixels[0])
    # IHDR
    ihdr = struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)
    # Raw scanlines: filter byte 0 (none) + RGB triplets
    raw_rows = []
    for row in pixels:
        line = bytearray([0])  # filter type None
        for (r, g, b) in row:
            line += bytes([r, g, b])
        raw_rows.append(bytes(line))
    idat_data = zlib.compress(b''.join(raw_rows), 9)
    return (
        b'\x89PNG\r\n\x1a\n'
        + _png_chunk(b'IHDR', ihdr)
        + _png_chunk(b'IDAT', idat_data)
        + _png_chunk(b'IEND', b'')
    )


# ── Drawing primitives ────────────────────────────────────────────
def _draw_filled_circle(pixels, cx, cy, r, r_col, g_col, b_col):
    for y in range(max(0, cy - r - 1), min(len(pixels), cy + r + 2)):
        for x in range(max(0, cx - r - 1), min(len(pixels[0]), cx + r + 2)):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                pixels[y][x] = (r_col, g_col, b_col)


def _draw_ring(pixels, cx, cy, r_outer, r_inner, r_col, g_col, b_col):
    for y in range(max(0, cy - r_outer - 1), min(len(pixels), cy + r_outer + 2)):
        for x in range(max(0, cx - r_outer - 1), min(len(pixels[0]), cx + r_outer + 2)):
            d2 = (x - cx) ** 2 + (y - cy) ** 2
            if r_inner * r_inner <= d2 <= r_outer * r_outer:
                pixels[y][x] = (r_col, g_col, b_col)


def _lerp(a, b, t):
    return a + (b - a) * t


# ── Simple bitmap font (9×13 bitmaps for U D E) ──────────────────
# Each glyph is a list of row-bitmasks (MSB = leftmost pixel), 9 px wide.
# Drawn at whatever scale we want via nearest-neighbour.

# 9-wide glyphs (rows top→bottom, big-endian 9-bit)
GLYPHS = {
    'U': [
        0b111111111,
        0b110000110,
        0b110000110,
        0b110000110,
        0b110000110,
        0b110000110,
        0b110000110,
        0b110000110,
        0b011000110,
        0b011001100,
        0b001111000,
        0b000110000,
        0b000000000,
    ],
    'D': [
        0b111110000,
        0b110011000,
        0b110001100,
        0b110000110,
        0b110000110,
        0b110000110,
        0b110000110,
        0b110000110,
        0b110001100,
        0b110011000,
        0b111110000,
        0b000000000,
        0b000000000,
    ],
    'E': [
        0b111111111,
        0b110000000,
        0b110000000,
        0b110000000,
        0b110000000,
        0b111111110,
        0b110000000,
        0b110000000,
        0b110000000,
        0b110000000,
        0b111111111,
        0b000000000,
        0b000000000,
    ],
}
GLYPH_W = 9
GLYPH_H = 13


def _draw_text_ude(pixels, size):
    """Draw "UDE" centred in a square image of `size` pixels."""
    # Scale: choose glyph pixel size so "UDE" fits in ~50% of icon width
    # 3 letters × 9px + 2 gaps × 2px = 31px source width
    letter_gap = 2  # source pixels between letters
    total_src_w = 3 * GLYPH_W + 2 * letter_gap
    scale = max(1, int(size * 0.46 / total_src_w))

    scaled_w = total_src_w * scale
    scaled_h = GLYPH_H * scale

    start_x = (size - scaled_w) // 2
    start_y = (size - scaled_h) // 2

    text = ['U', 'D', 'E']
    for i, ch in enumerate(text):
        glyph = GLYPHS[ch]
        ox = start_x + i * (GLYPH_W + letter_gap) * scale
        for gy, row_mask in enumerate(glyph):
            for gx in range(GLYPH_W):
                bit = (row_mask >> (GLYPH_W - 1 - gx)) & 1
                if bit:
                    for sy in range(scale):
                        for sx in range(scale):
                            py = start_y + gy * scale + sy
                            px = ox + gx * scale + sx
                            if 0 <= py < size and 0 <= px < size:
                                pixels[py][px] = (FG_R, FG_G, FG_B)


def generate_icon(size: int, output_path: str):
    pixels = [[(BG_R, BG_G, BG_B)] * size for _ in range(size)]

    cx = cy = size // 2
    radius = size // 2 - 1  # full circle

    # 1. Fill background with bordeaux circle (anti-alias edges via bg square is fine)
    _draw_filled_circle(pixels, cx, cy, radius, BG_R, BG_G, BG_B)

    # 2. White border ring (thickness = ~3.5% of size)
    ring_thick = max(2, int(size * 0.035))
    _draw_ring(pixels, cx, cy, radius, radius - ring_thick, FG_R, FG_G, FG_B)

    # 3. "UDE" letters centred
    _draw_text_ude(pixels, size)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'wb') as f:
        f.write(_png_bytes(pixels))
    print(f'  Generated: {output_path}  ({size}×{size})')


if __name__ == '__main__':
    base = os.path.join(os.path.dirname(__file__), 'static', 'icons')
    generate_icon(192, os.path.join(base, 'icon-192.png'))
    generate_icon(512, os.path.join(base, 'icon-512.png'))
    print('Done.')

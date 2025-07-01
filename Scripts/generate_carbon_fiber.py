import math
import random

import image_generator

SIZE = 4096
WEAVE_COUNT = 128 # 128: small (recommended), 64: large

BASE_COLOR = 0.1
REFLECTION_COLOR = 0.5
BRUSH_INTENSITY = 0.05 # 0.05: recommended, 0.1: very shiny
NORMAL_BEND = 0.05 # 0.05: recommended, 0.02: a more flat look

NOISE1_SIZE = 256
NOISE2_SIZE = 512

WEAVE_SIZE_PIXEL = math.ceil(SIZE / WEAVE_COUNT)
WEAVE_SIZE_NORMALIZED = 1.0 / WEAVE_COUNT

# noise generation

noise1: list[list[float]] = []
noise2: list[list[float]] = []

for i in range(NOISE1_SIZE):
    noise1.append([])
    for j in range(NOISE1_SIZE):
        noise1[i].append(random.random() * 2.0 - 1.0)
for i in range(NOISE2_SIZE):
    noise2.append([])
    for j in range(NOISE2_SIZE):
        noise2[i].append(random.random() * 2.0 - 1.0)

# tile generator

brush_tiles: list[list[list[(float, float, float)]]] = []
normal_tiles: list[list[list[(float, float, float)]]] = []

def get_tile_type(x, y) -> int:
    # types:
    # 0: bottom half of vertical   weave
    # 1: top    half of vertical   weave
    # 2: left   half of horizontal weave
    # 3: right  half of horizontal weave
    return (int(x / WEAVE_SIZE_NORMALIZED) + int(y / WEAVE_SIZE_NORMALIZED)) % 4

def transform_tile_coord(x, y) -> tuple[float, float]:
    return (x % WEAVE_SIZE_NORMALIZED / WEAVE_SIZE_NORMALIZED, y % WEAVE_SIZE_NORMALIZED / WEAVE_SIZE_NORMALIZED)

def convert_tile_input(x, y, tile_type):
    if tile_type > 1:
        temp = x
        x = y
        y = temp
    if tile_type % 2 == 1:
        y = 1 - y
    return (x, y)

def convert_tile_output(output, tile_type, enable_reverse = True):
    x, y, z = output
    if tile_type % 2 == 1 and enable_reverse:
        y = 1 - y
    if tile_type > 1:
        temp = x
        x = y
        y = temp
    return (x, y, z)

def generate_brush_tile(x, y, tile_type):
    # generate
    return convert_tile_output((0.5, 0.5 + 0.5 * BRUSH_INTENSITY, 0.5), tile_type, enable_reverse=False)

def generate_normal_tile(x, y, tile_type):
    # transform input to type 0
    x, y = convert_tile_input(x, y, tile_type)
    # generate
    vbend = 1 - y
    vbend = 0.5 * NORMAL_BEND * vbend * vbend
    hbend = 2 * x - 0.5
    hbend = 0.125 * NORMAL_BEND * hbend * hbend
    if x < 0.5:
        hbend = -hbend
    return convert_tile_output((0.5 + hbend, 0.5 - vbend, 1), tile_type)

# generators

def normalize_normal(result):
    result = (result[0] * 2 - 1, result[1] * 2 - 1, result[2] * 2 - 1)
    m = math.sqrt(result[0] * result[0] + result[1] * result[1] + result[2] * result[2])
    result = (result[0] / m, result[1] / m, result[2] / m)
    result = (result[0] * 0.5 + 0.5, result[1] * 0.5 + 0.5, result[2] * 0.5 + 0.5)
    return result

def base_generator(x, y):
    return BASE_COLOR

def reflection_generator(x, y):
    return REFLECTION_COLOR

def normal_generator(x, y):
    tile_coord = transform_tile_coord(x, y)
    tile_type = get_tile_type(x, y)
    base = generate_normal_tile(tile_coord[0], tile_coord[1], tile_type)
    result = base
    # TODO: Maybe add imperfections by sampling and using the generated noise1 and noise2
    # normalize for more precision
    return normalize_normal(result)

def brush_generator(x, y):
    tile_coord = transform_tile_coord(x, y)
    tile_type = get_tile_type(x, y)
    base = generate_brush_tile(tile_coord[0], tile_coord[1], tile_type)
    return base

# render

image_generator.generate_grayscale_image(
    (16, 16), base_generator, "base.png"
)

image_generator.generate_grayscale_image(
    (16, 16), reflection_generator, "reflection.png"
)

image_generator.generate_image(
    (SIZE, SIZE), normal_generator, "normal.png"
)

image_generator.generate_image(
    (SIZE, SIZE), brush_generator, "brush.png"
)

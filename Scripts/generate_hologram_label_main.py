import math
from PIL import Image


Size = 4096

TilesCountPerDimension = 16
TilesSizePerTile = 0.8

CircularOffsetPerLayer = 0.1
NormalOffsetPerLayer = 0.04


# progress display

progress_step = 0.0625 # (0.0001)b
progress_character = "#"
progress_milestones = [
    (0, "0%"),
    (0.25, "25%"),
    (0.5, "50%"),
    (0.75, "75%"),
    (1, "100%")
]

def progress_reset():
    global progress_threshold
    global progress_milestones
    global progress_remaining_milestones
    progress_threshold = 0
    progress_remaining_milestones = progress_milestones.copy()

def progress_update(progress):
    global progress_threshold
    global progress_step
    global progress_character
    global progress_remaining_milestones
    if progress >= progress_threshold:
        if progress_threshold != 0:
            print(progress_character, end="", flush=True)
        if len(progress_remaining_milestones) > 0 and progress >= progress_remaining_milestones[0][0]:
            print(progress_remaining_milestones[0][1], end="", flush=True)
            progress_remaining_milestones.pop(0)
        progress_threshold += progress_step

# render

size_center = float(Size) / 2 - 0.5
half_pixel_amount = 1.0 / Size
pixel_amount = half_pixel_amount * 2
tiles_per_uv_one = TilesCountPerDimension / 2
tiles_1_size = (1 / tiles_per_uv_one)
tiles_thickness = tiles_1_size * TilesSizePerTile
tiles_gap = tiles_1_size - tiles_thickness
tiles_gap_per_tile = 1 - TilesSizePerTile
tiles_gap_per_tile_half = tiles_gap_per_tile / 2

for layer_number in range(0, 5):
    if layer_number == 0:
        num = ""
    else:
        num = str(layer_number)

    if layer_number == 0:
        reflections = Image.new('L', (Size, Size))
    else:
        reflections = Image.new('RGB', (Size, Size))
        brush = Image.new('RGB', (Size, Size))
        normal = Image.new('RGB', (Size, Size))

    print("Layer " + str(layer_number) + ":")
    progress_reset()
    print("Progress: ", end="", flush=True)

    circular_offset = (layer_number - 2) * CircularOffsetPerLayer
    normal_offset = (layer_number - 2) * NormalOffsetPerLayer
    for y in range(0, Size):
        progress_update(float(y) / Size)
        for x in range(0, Size):
            u = float(x) / size_center - 1
            v = -float(y) / size_center + 1
            l = math.sqrt(u * u + v * v)

            # calculate presence
            if l < 0.5 - half_pixel_amount:
                center_brush_presence = 1.0
                tiles_presence = 0.0
            elif l < 0.5 + half_pixel_amount:
                center_brush_presence = ((0.5 + half_pixel_amount) - l) / pixel_amount
                tiles_presence = 0.0
            elif l < 0.5 + tiles_gap - half_pixel_amount:
                center_brush_presence = 0.0
                tiles_presence = 0.0
            else:
                center_brush_presence = 0.0
                tile_x_f = (u + 1) * tiles_per_uv_one - tiles_gap_per_tile_half
                tile_y_f = (v + 1) * tiles_per_uv_one - tiles_gap_per_tile_half
                tile_x = int(tile_x_f)
                tile_y = int(tile_y_f)
                if tile_x_f >= 0 and tile_y_f >= 0 and tile_x_f - tile_x < TilesSizePerTile and tile_y_f - tile_y < TilesSizePerTile:
                    if l < 0.5 + tiles_gap + half_pixel_amount:
                        tiles_presence = (l - (0.5 + tiles_gap - half_pixel_amount)) / pixel_amount
                    else:
                        tiles_presence = 1.0
                else:
                    tiles_presence = 0.0

            # calculate colors
            if layer_number == 0:
                reflections_color = 144 - int(144 * (center_brush_presence + tiles_presence))
                reflections.putpixel((x, y), (reflections_color))
            else:
                if layer_number == 1:
                    reflections.putpixel((x, y), (int(144 * (center_brush_presence + tiles_presence)), 0, 0))
                elif layer_number == 2:
                    reflections.putpixel((x, y), (0, int(144 * (center_brush_presence + tiles_presence)), 0))
                elif layer_number == 3:
                    reflections.putpixel((x, y), (0, 0, int(144 * (center_brush_presence + tiles_presence))))
                elif layer_number == 4:
                    reflections.putpixel((x, y), (int(112 * (center_brush_presence + tiles_presence)), 0, 0))

                if center_brush_presence != 0.0:
                    u_n = u / l
                    v_n = v / l
                    if circular_offset != 0.0:
                        # apply offset
                        offset = (v_n, -u_n)
                        u_n -= offset[0] * circular_offset
                        v_n -= offset[1] * circular_offset
                        # normalize
                        l_n = math.sqrt(u_n * u_n + v_n * v_n)
                        u_n /= l_n
                        v_n /= l_n
                    brush.putpixel((x, y), (int(128 + v_n * 127), int(128 - u_n * 127), 128))
                    normal.putpixel((x, y), (128, 128, 255))
                elif tiles_presence != 0.0:
                    brush_type = (tile_x + tile_y) % 4
                    if brush_type == 0:
                        brush_x = 255
                        brush_y = 128
                        normal_x = int(127.5 + 127.5 * normal_offset)
                        normal_y = 128
                    elif brush_type == 1:
                        brush_x = 128
                        brush_y = 255
                        normal_x = 128
                        normal_y = int(127.5 + 127.5 * normal_offset)
                    elif brush_type == 2:
                        brush_x = 255
                        brush_y = 128
                        normal_x = int(127.5 - 127.5 * normal_offset)
                        normal_y = 128
                    elif brush_type == 3:
                        brush_x = 128
                        brush_y = 255
                        normal_x = 128
                        normal_y = int(127.5 - 127.5 * normal_offset)
                    brush.putpixel((x, y), (brush_x, brush_y, 128))
                    normal.putpixel((x, y), (normal_x, normal_y, 255))
                else:
                    brush.putpixel((x, y), (128, 128, 128))
                    normal.putpixel((x, y), (128, 128, 255))
    progress_update(1)
    print()
    reflections.save("reflections" + num + ".png")
    if layer_number != 0:
        brush.save("brush" + num + ".png")
        normal.save("normal" + num + ".png")

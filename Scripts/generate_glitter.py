import math
from PIL import Image
import random


Size = 512

NormalRangeMaxOffset = 1
NormalXRange = (-NormalRangeMaxOffset, NormalRangeMaxOffset)
NormalYRange = (-NormalRangeMaxOffset, NormalRangeMaxOffset)

Shininess = 0.25

ReflectionLayersCount = 4

# Applied to the first layer only (layer 0)
BaseStaticColor = (0.25, 0.25, 0.25)

# Only renders a 16x16 base filled with BaseStaticColor for the first layer without normal or reflections
EnableFlatStaticBase = True

# Whether to render a base for each reflection layer at all
EnableBaseColorFraction = True

# For the random colors:

ReflectionColorFraction = 1
# Doesn't matter if EnableBaseColorFraction is set to False
BaseColorFraction = 0.1 / ReflectionLayersCount

LayersCount = ReflectionLayersCount
if EnableFlatStaticBase:
    LayersCount += 1

RGBColors = [
    (1.0, 1.0, 1.0),
    (1.0, 0.5, 0.5),
    (0.5, 1.0, 0.5),
    (0.5, 0.5, 1.0)
]
ReminimalismColors = [
    (1.0, 1.0,  1.0 ),
    (1.0, 0.0,  0.39),
    (0.0, 0.86, 0.78)
]
Colors = RGBColors


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

base_cf = BaseColorFraction * 255
refl_cf = ReflectionColorFraction * 255
base_sc = (int(BaseStaticColor[0] * 255), int(BaseStaticColor[1] * 255), int(BaseStaticColor[2] * 255))

for layer_number in range(0, LayersCount):

    if layer_number == 0:
        num = ""
    else:
        num = str(layer_number)

    if (layer_number == 0 and EnableFlatStaticBase):
        base = Image.new('RGB', (16, 16))
        for y in range(0, 16):
            for x in range(0, 16):
                base.putpixel((x, y), base_sc)
        base.save("base.png")
        continue

    shininess_color = int(Shininess * 255)
    shininess = Image.new('L', (16, 16))
    for y in range(0, 16):
        for x in range(0, 16):
            shininess.putpixel((x, y), shininess_color)
    shininess.save("shininess" + num + ".png")


    print("Layer " + str(layer_number) + ":")
    progress_reset()


    if EnableBaseColorFraction:
        base = Image.new('RGB', (Size, Size))
    reflections = Image.new('RGB', (Size, Size))
    normal = Image.new('RGB', (Size, Size))
    print("Progress: ", end="", flush=True)
    for y in range(0, Size):
        progress_update(float(y) / Size)
        for x in range(0, Size):
            nx = NormalXRange[0] + random.random() * (NormalXRange[1] - NormalXRange[0])
            ny = NormalYRange[0] + random.random() * (NormalYRange[1] - NormalYRange[0])
            nx = int(127.5 + nx * 127.5)
            ny = int(127.5 + ny * 127.5)

            color = random.choice(Colors)

            if EnableBaseColorFraction:
                if (layer_number == 0):
                    base_color = base_sc
                else:
                    base_color = (0, 0, 0)

                base_color = (
                    int(base_color[0] + color[0] * base_cf),
                    int(base_color[1] + color[1] * base_cf),
                    int(base_color[2] + color[2] * base_cf)
                )
                base.putpixel((x, y), base_color)

            reflections_color = (
                int(color[0] * refl_cf),
                int(color[1] * refl_cf),
                int(color[2] * refl_cf)
            )
            reflections.putpixel((x, y), reflections_color)
            normal.putpixel((x, y), (nx, ny, 255))
    progress_update(1)
    print()
    if EnableBaseColorFraction:
        base.save("base" + num + ".png")
    reflections.save("reflections" + num + ".png")
    normal.save("normal" + num + ".png")

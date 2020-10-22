import math
from PIL import Image
import random


Size = 4096

WavesCount = 4
ReverseCosine = True
MaxSlope = 0.5
BrushLinesWidthInPixels = 4

BaseDeepColor = 120
BaseHighColor = 128
ReflectionsDeepColor = 128
ReflectionsHighColor = 128

BrushIntensity = 16
NormalIntensity = 0.1 # Can be even 0!


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

pixel_amount = 1.0 / Size

wave_cos_t_c = math.pi * 2 * WavesCount
wave_cos_c = (1.0 / wave_cos_t_c) * MaxSlope
if ReverseCosine:
    wave_cos_c = -wave_cos_c
    wave_sin_c = MaxSlope
else:
    wave_sin_c = -MaxSlope

lines_cos_t_c = (Size * math.pi * 2) / BrushLinesWidthInPixels

base_high_color_offset = BaseHighColor - BaseDeepColor
refl_high_color_offset = ReflectionsHighColor - ReflectionsDeepColor

base = Image.new('L', (Size, Size))
reflections = Image.new('L', (Size, Size))
normal = Image.new('RGB', (Size, Size))
brush = Image.new('RGB', (Size, Size))
brush_intensity = Image.new('L', (16, 16))
for x in range(16):
    for y in range(16):
        brush_intensity.putpixel((x, y), (BrushIntensity))

progress_reset()
print("Progress: ", end="", flush=True)

for x in range(0, Size):
    progress_update(float(x) / Size)

    u = float(x) / Size

    w = math.cos(u * wave_cos_t_c) * wave_cos_c

    dw = math.sin(u * wave_cos_t_c) * wave_sin_c

    bx = 1.0
    by = bx * dw
    bm = math.sqrt(bx * bx + by * by)
    brush_vector = (bx / bm, by / bm)
    brush_color = (
        round(128 + brush_vector[0] * 127),
        round(128 + brush_vector[1] * 127),
        128
    )

    normal_offset = (-brush_vector[1], brush_vector[0])

    for y in range(0, Size):

        v = float((Size - 1) - y) / Size

        v_w = v - w

        h = math.cos(v_w * lines_cos_t_c)
        dh_for_normal = math.sin(v_w * lines_cos_t_c)

        base.putpixel((x, y), (round(BaseDeepColor + h * base_high_color_offset)))
        reflections.putpixel((x, y), (round(ReflectionsDeepColor + h * refl_high_color_offset)))
        brush.putpixel((x, y), brush_color)

        normal.putpixel((x, y), (
            round(127.5 + 127.5 * normal_offset[0] * dh_for_normal * NormalIntensity),
            round(127.5 + 127.5 * normal_offset[1] * dh_for_normal * NormalIntensity),
            255
        ))
progress_update(1)
print()

base.save("base.png")
reflections.save("reflections.png")
normal.save("normal.png")
brush.save("brush.png")
brush_intensity.save("brush_intensity.png")

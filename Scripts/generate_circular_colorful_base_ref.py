import math
from PIL import Image
import random


Size = 4096
NoiseRadius = 8
NoiseCountPerPixel = 1

max_color = 255 - NoiseRadius

RGBBaseColors = [
    (96, 32, 64),
    (32, 96, 64),
    (32, 64, 96),
    (96, 96, 96)
]

RGBReflectionsColors = [
    (max_color, 32, 64),
    (32, max_color, 64),
    (32, 64, max_color),
    (max_color, max_color, max_color)
]

BaseColors = RGBBaseColors
ReflectionsColors = RGBReflectionsColors


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

# process

noise = []

for i in range(int(Size * NoiseCountPerPixel)):
    noise.append(random.random() * NoiseRadius * 2 - NoiseRadius)

half_pixel_amount = 1.0 / Size
pixel_amount = half_pixel_amount * 2

phase_size = 0.25
last_phase = 3
phase_aa_ranges = [
    (0.25 - half_pixel_amount, 0.25 + half_pixel_amount),
    (0.5 - half_pixel_amount, 0.5 + half_pixel_amount),
    (0.75 - half_pixel_amount, 0.75 + half_pixel_amount)
]
phase_fix_points = [
    0,
    phase_aa_ranges[0][1],
    phase_aa_ranges[1][1],
    phase_aa_ranges[2][1],

    phase_aa_ranges[2][1],
    phase_aa_ranges[2][1]
]

def lerp(color_a : tuple, color_b : tuple, t : float):
    return (
        color_a[0] + (color_b[0] - color_a[0]) * t,
        color_a[1] + (color_b[1] - color_a[1]) * t,
        color_a[2] + (color_b[2] - color_a[2]) * t
    )

def add_color_num(color : tuple, number : float):
    return (color[0] + number, color[1] + number, color[2] + number)

size_center = float(Size) / 2 - 0.5
base = Image.new('RGB', (Size, Size))
reflections = Image.new('RGB', (Size, Size))
print("Progress: ", end="", flush=True)
for y in range(0, Size):
    progress_update(float(y) / Size)
    for x in range(0, Size):
        u = float(x) / size_center - 1
        v = -float(y) / size_center + 1
        l = math.sqrt(u * u + v * v)
        offset_index_f = abs(l) * (Size / 2) * NoiseCountPerPixel
        offset_index = int(offset_index_f)
        offset = noise[offset_index] + (offset_index_f - offset_index) * (noise[offset_index + 1] - noise[offset_index])

        phase_index = int(l / phase_size)
        if l < phase_fix_points[phase_index]:
            phase_index -= 1

        if phase_index >= last_phase:
            phase_index = last_phase
            phase_aa = 0
        elif phase_aa_ranges[phase_index][0] <= l < phase_aa_ranges[phase_index][1]:
            phase_aa = (l - phase_aa_ranges[phase_index][0]) / pixel_amount
        else:
            phase_aa = 0

        if phase_aa == 0:
            base_color = BaseColors[phase_index]
            refl_color = ReflectionsColors[phase_index]
        else:
            base_color = lerp(BaseColors[phase_index], BaseColors[phase_index + 1], phase_aa)
            refl_color = lerp(ReflectionsColors[phase_index], ReflectionsColors[phase_index + 1], phase_aa)

        base_color = add_color_num(base_color, offset)
        refl_color = add_color_num(refl_color, offset)

        base_color = (int(base_color[0]), int(base_color[1]), int(base_color[2]), )
        refl_color = (int(refl_color[0]), int(refl_color[1]), int(refl_color[2]), )

        base       .putpixel((x, y), base_color)
        reflections.putpixel((x, y), refl_color)
progress_update(1)
print()
base.save("base.png")
reflections.save("reflections.png")

import math
from PIL import Image
import random


Size = 4096
NoiseRadius = 8


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

for i in range(Size):
    noise.append(random.random() * NoiseRadius * 2 - NoiseRadius)

max_color = 255 - NoiseRadius
half_pixel_amount = 1.0 / Size
pixel_amount = half_pixel_amount * 2

phase1 = 0.25 - half_pixel_amount
phase1aa = 0.25 + half_pixel_amount
phase2 = 0.5 - half_pixel_amount
phase2aa = 0.5 + half_pixel_amount
phase3 = 0.75 - half_pixel_amount
phase3aa = 0.75 + half_pixel_amount

def aa(prev_phase, l, prev_color, next_color):
    global pixel_amount
    return prev_color + ((l - prev_phase) / pixel_amount) * (next_color - prev_color)

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
        offset_index_f = abs(l) * (Size / 2)
        offset_index = int(offset_index_f)
        offset = noise[offset_index] + (offset_index_f - offset_index) * (noise[offset_index + 1] - noise[offset_index])
        if l < phase1:
            b_r = 96 + offset; r_r = max_color + offset
            b_g = r_g = 32 + offset
            b_b = r_b = 64 + offset
        elif l < phase1aa:
            b_r = aa(phase1, l, 96, 32) + offset; r_r = aa(phase1, l, max_color, 32) + offset
            b_g = aa(phase1, l, 32, 96) + offset; r_g = aa(phase1, l, 32, max_color) + offset
            b_b = r_b = 64 + offset
        elif l < phase2:
            b_r = r_r = 32 + offset
            b_g = 96 + offset; r_g = max_color + offset
            b_b = r_b = 64 + offset
        elif l < phase2aa:
            b_r = r_r = 32 + offset
            b_g = aa(phase2, l, 96, 64) + offset; r_g = aa(phase2, l, max_color, 64) + offset
            b_b = aa(phase2, l, 64, 96) + offset; r_b = aa(phase2, l, 64, max_color) + offset
        elif l < phase3:
            b_r = r_r = 32 + offset
            b_g = r_g = 64 + offset
            b_b = 96 + offset; r_b = max_color + offset
        elif l < phase3aa:
            b_r = r_r = aa(phase3, l, 32, 128) + offset
            b_g = r_g = aa(phase3, l, 64, 128) + offset
            b_b = aa(phase3, l, 96, 128) + offset; r_b = aa(phase3, l, max_color, 128) + offset
        else:
            b_r = b_g = b_b = r_r = r_g = r_b = 128 + offset

        base       .putpixel((x, y), (int(b_r), int(b_g), int(b_b)))
        reflections.putpixel((x, y), (int(r_r), int(r_g), int(r_b)))
progress_update(1)
print()
base.save("base.png")
reflections.save("reflections.png")

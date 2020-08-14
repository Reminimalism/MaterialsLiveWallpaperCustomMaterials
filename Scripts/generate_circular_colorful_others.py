import math
from PIL import Image
import random


Size = 4096
LineThickness = 2.0 / 1024
NormalRadius = 32
BrushIntensities = [ 32, 16, 24, 16 ]


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

half_pixel_amount = 1.0 / Size
pixel_amount = half_pixel_amount * 2

phases = []

for i in range(3):
    if i == 0:
        pos = 0.25
    elif i == 1:
        pos = 0.5
    elif i == 2:
        pos = 0.75
    phases.append(
        (
            pos - LineThickness - half_pixel_amount, # phase      i
            pos - LineThickness + half_pixel_amount, # phase      i   aa line outer i
            pos                 - half_pixel_amount, # line outer i
            pos                 + half_pixel_amount, # line outer i   aa line inner i+1
            pos + LineThickness - half_pixel_amount, # line inner i+1
            pos + LineThickness + half_pixel_amount  # line inner i+1 aa phase      i+1
        )
    )

def aa_mono(prev_phase, l, prev_color, next_color):
    global pixel_amount
    return prev_color + ((l - prev_phase) / pixel_amount) * (next_color - prev_color)

def aa(prev_phase, l, prev_color, next_color):
    global pixel_amount
    r = prev_color[0] + ((l - prev_phase) / pixel_amount) * (next_color[0] - prev_color[0])
    g = prev_color[1] + ((l - prev_phase) / pixel_amount) * (next_color[1] - prev_color[1])
    b = prev_color[2] + ((l - prev_phase) / pixel_amount) * (next_color[2] - prev_color[2])
    return (r, g, b)

size_center = float(Size) / 2 - 0.5
normal = Image.new('RGB', (Size, Size))
brush_intensity = Image.new('L', (Size, Size))
print("Progress: ", end="", flush=True)
for y in range(0, Size):
    progress_update(float(y) / Size)
    for x in range(0, Size):
        u = float(x) / size_center - 1
        v = -float(y) / size_center + 1
        l = math.sqrt(u * u + v * v)
        for i in range(4):
            if i == 3: # phase 3
                n = (128, 128, 255)
                bi = BrushIntensities[3]
                break
            if l < phases[i][0]: # phase i
                n = (128, 128, 255)
                bi = BrushIntensities[i]
                break
            if l < phases[i][1]: # phase i aa line outer i
                n = aa(
                    phases[i][0], l,
                    (128, 128, 255),
                    (127.5 + NormalRadius * u / l, 127.5 + NormalRadius * v / l, 255)
                )
                bi = BrushIntensities[i]
                break
            if l < phases[i][2]: # line outer i
                n = (127.5 + NormalRadius * u / l, 127.5 + NormalRadius * v / l, 255)
                bi = BrushIntensities[i]
                break
            if l < phases[i][3]: # line outer i aa line inner i+1
                n = aa(
                    phases[i][2], l,
                    (127.5 + NormalRadius * u / l, 127.5 + NormalRadius * v / l, 255),
                    (127.5 - NormalRadius * u / l, 127.5 - NormalRadius * v / l, 255)
                )
                bi = aa_mono(phases[i][2], l, BrushIntensities[i], BrushIntensities[i + 1])
                break
            if l < phases[i][4]: # line inner i+1
                n = (127.5 - NormalRadius * u / l, 127.5 - NormalRadius * v / l, 255)
                bi = BrushIntensities[i + 1]
                break
            if l < phases[i][5]: # line inner i+1 aa phase i+1
                n = aa(
                    phases[i][4], l,
                    (127.5 - NormalRadius * u / l, 127.5 - NormalRadius * v / l, 255),
                    (128, 128, 255)
                )
                bi = BrushIntensities[i + 1]
                break
        n = (int(n[0]), int(n[1]), int(n[2]))
        bi = int(bi)
        normal.putpixel((x, y), n)
        brush_intensity.putpixel((x, y), bi)
progress_update(1)
print()
normal.save("normal.png")
brush_intensity.save("brush_intensity.png")

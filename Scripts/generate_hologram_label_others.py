import math
from PIL import Image


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

base = Image.new('L', (16, 16))
shininess = Image.new('L', (16, 16))
brush_intensity = Image.new('L', (16, 16))
progress_reset()
print("Progress: ", end="", flush=True)

for y in range(0, 16):
    progress_update(float(y) / 16)
    for x in range(0, 16):
        base.putpixel((x, y), (112))
        shininess.putpixel((x, y), (16))
        brush_intensity.putpixel((x, y), (16))
progress_update(1)
print()
base.save("base.png")
shininess.save("shininess.png")
brush_intensity.save("brush_intensity1.png")
brush_intensity.save("brush_intensity2.png")
brush_intensity.save("brush_intensity3.png")
brush_intensity.save("brush_intensity4.png")

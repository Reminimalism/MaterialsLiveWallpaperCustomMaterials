import math
from PIL import Image


Size = 4096


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
            print(progress_character, end="")
        if len(progress_remaining_milestones) > 0 and progress >= progress_remaining_milestones[0][0]:
            print(progress_remaining_milestones[0][1], end="")
            progress_remaining_milestones.pop(0)
        progress_threshold += progress_step

# render

size_center = float(Size) / 2 - 0.5
img = Image.new('RGB', (Size, Size))
print("Progress: ", end="")
for y in range(0, Size):
    progress_update(float(y) / Size)
    for x in range(0, Size):
        u = float(x) / size_center - 1
        v = -float(y) / size_center + 1
        l = math.sqrt(u * u + v * v)
        u /= l
        v /= l
        r = int(128 + v * 127)
        g = int(128 - u * 127)
        b = 128
        img.putpixel((x, y), (r, g, b))
progress_update(1)
print()
img.save("circular_brush.png")

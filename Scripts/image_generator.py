from PIL import Image


class ProgressPrinter:
    def __init__(self):
        self.progress_step = 0.0625 # (0.0001)b
        self.progress_character = "#"
        self.progress_milestones = [
            (0, "0%"),
            (0.25, "25%"),
            (0.5, "50%"),
            (0.75, "75%"),
            (1, "100%")
        ]
        self.reset()

    def reset(self):
        self.progress_threshold = 0
        self.progress_remaining_milestones = self.progress_milestones.copy()
        print("Progress: ", end="", flush=True)

    def update(self, progress):
        if progress >= self.progress_threshold:
            if len(self.progress_remaining_milestones) != 0:
                if self.progress_threshold != 0:
                    print(self.progress_character, end="", flush=True)
                if progress >= self.progress_remaining_milestones[0][0]:
                    print(self.progress_remaining_milestones[0][1], end="", flush=True)
                    self.progress_remaining_milestones.pop(0)
                    if len(self.progress_remaining_milestones) == 0:
                        print()
            self.progress_threshold += self.progress_step


def generate_image(resolution: 'tuple[float, float]', generation_function, output_filename: str = None, aa_level: int = 1):
    output = Image.new('RGB', resolution)

    progress = ProgressPrinter()

    aa_count = aa_level * aa_level
    aa_offset_x = 1.0 / resolution[0] / aa_level
    aa_offset_y = 1.0 / resolution[1] / aa_level
    base_offset_x = 0.5 * aa_offset_x
    base_offset_y = 0.5 * aa_offset_y

    for x in range(0, resolution[0]):
        progress.update(float(x) / resolution[0])
        u = float(x) / resolution[0] + base_offset_x

        for y in range(0, resolution[1]):
            v = float((resolution[1] - 1) - y) / resolution[1] + base_offset_y

            color = [0, 0, 0]
            for i in range(0, aa_level):
                for j in range(0, aa_level):
                    temp = generation_function(u + i * aa_offset_x, v + j * aa_offset_y)
                    for k in range (0, 3):
                        color[k] += temp[k] / aa_count
            color = (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))
            output.putpixel((x, y), color)

    progress.update(1)

    if output_filename is None:
        output_filename = "output.png"
    output.save(output_filename)

def generate_grayscale_image(resolution: 'tuple[float, float]', generation_function, output_filename: str = None, aa_level: int = 1):
    output = Image.new('L', resolution)

    progress = ProgressPrinter()

    aa_count = aa_level * aa_level
    aa_offset_x = 1.0 / resolution[0] / aa_level
    aa_offset_y = 1.0 / resolution[1] / aa_level
    base_offset_x = 0.5 * aa_offset_x
    base_offset_y = 0.5 * aa_offset_y

    for x in range(0, resolution[0]):
        progress.update(float(x) / resolution[0])
        u = float(x) / resolution[0] + base_offset_x

        for y in range(0, resolution[1]):
            v = float((resolution[1] - 1) - y) / resolution[1] + base_offset_y

            color = 0
            for i in range(0, aa_level):
                for j in range(0, aa_level):
                    temp = generation_function(u + i * aa_offset_x, v + j * aa_offset_y)
                    color += temp / aa_count
            color = int(color * 255)
            output.putpixel((x, y), color)

    progress.update(1)

    if output_filename is None:
        output_filename = "output.png"
    output.save(output_filename)

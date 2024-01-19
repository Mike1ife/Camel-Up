from PIL import Image
from itertools import permutations

red = Image.open("Red.png").convert("RGBA")
blue = Image.open("Blue.png").convert("RGBA")
yellow = Image.open("Yellow.png").convert("RGBA")
purple = Image.open("Purple.png").convert("RGBA")
green = Image.open("Green.png").convert("RGBA")

names = ["Red", "Blue", "Yello", "Purple", "Green"]
camels = [red, blue, yellow, purple, green]
camel_width, camel_height = red.width, red.height - 33

for i in range(1, 6):
    for indice in permutations(range(0, 5), i):
        new_img = Image.new(
            "RGBA",
            (camel_width, red.height + camel_height * (len(indice) - 1)),
            (0, 0, 0, 0),
        )
        for i, img in enumerate([camels[index] for index in indice]):
            new_img.paste(img, (0, camel_height * (len(indice) - i - 1)), mask=img)
        # index: 0=the first camel
        file_name = "./images/"
        for name in [names[index] for index in indice]:
            file_name += f"{name}_"
        file_name = f"{file_name[:-1]}.png"
        print(file_name)
        new_img.save(file_name)

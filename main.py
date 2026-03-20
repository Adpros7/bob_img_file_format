import lzma
import re
from typing import Counter
import zlib

from PIL import Image


def find_repeated(s, threshold=5, size=7):
    matches = re.findall(rf"\d{{{size}}}", s) + re.findall(rf"\w{{{size}}}", s)
    counts = Counter(matches)
    return {k: v for k, v in counts.items() if v > threshold}


def main(image: str):
    img = Image.open(image).convert("RGBA")
    rgb_to_hex = lambda r, g, b, a: f"{"#" if a < 255 else ""}{r:02x}{g:02x}{b:02x}" + (f"{a:02x}" if a < 255 else "")
    final = ""
    for i in range(img.width):
        for j in range(img.height):
            final += rgb_to_hex(*img.getpixel((i, j))) # type: ignore
            # print(img.getpixel((i, j)))


    for i, v in enumerate(find_repeated(final).items()):
        final = f"{chr(i + 122)}={v[0]}{final}"

    final = lzma.compress(final.encode("utf-8"))

    with open("new.bob", "wb") as f:
        f.write(final)

    # with open("newtxt.bob", "w", encoding="utf-8") as f:
    #     f.write(final)
if __name__ == "__main__":
    # main("examples/pngwing.com.png")
    main("img.jpg")

import os
import json
import ffmpeg
import argparse
import subprocess

from PIL import Image, ImageDraw
from util import get_output


MARKER_COLORS = {
    'boat': (255, 255, 0),
    'bird': (255, 0, 255),
    'default': (255, 255, 255),
}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, help='path to detection metadata')
    parser.add_argument('--input', type=str, help='path to frames')
    parser.add_argument('--output', type=str, help='path to sequence of frames with detection markers')
    kwargs = parser.parse_args()

    if not kwargs.input:
        exit('Please pass required "--input" argument')

    if not kwargs.data:
        exit('Please pass required "--data" argument')

    output = get_output(kwargs)

    with open(kwargs.data, 'r') as fp:
        metadata = json.load(fp)

    for (ix, file) in enumerate(os.listdir(kwargs.input)):
        img = Image.open(os.path.join(kwargs.input, file))
        draw = ImageDraw.Draw(img)

        width, height = img.size
        # stream = ffmpeg.input(':pipe', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(width, height))

        for item in metadata:
            if item['file'] == file:
                for obj in item['objects']:
                    x1, y1, x2, y2 = obj['bbox']
                    color = MARKER_COLORS.get(obj['type']) or MARKER_COLORS['default']
                    draw.rectangle(
                        (
                            x1 * width,
                            y1 * height,
                            x2 * width,
                            y2 * height,
                        ),
                        outline=color,
                        width=3
                    )

                break

        img.save(os.path.join(output, f'{ix}.jpg'), 'jpeg')

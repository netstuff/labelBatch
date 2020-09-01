import os
import pdb
import ffmpeg
import argparse

from util import get_output


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, help='path to file/stream')
    parser.add_argument('-o', '--output', type=str, help='path to sequence of frames')
    parser.add_argument('-f', '--format', type=str, default='jpg', help='frame image format')
    parser.add_argument('-s', '--period', type=float, default=0.25, help='time period between frames')
    kwargs = parser.parse_args()

    if not kwargs.input:
        exit('Please pass required "--input" argument')

    output = get_output(kwargs)

    ix = 0
    ss = 0
    err = None
    info = ffmpeg.probe(kwargs.input)
    duration = float(info['format']['duration'])

    while ix < int(duration):
        name = str(ix).zfill(3) + f'.{kwargs.format.lower()}'
        out, err = (
            ffmpeg
                .input(kwargs.input, ss=ss)
                .output(os.path.join(output, name), vframes=1, vcodec='mjpeg')
                .run(capture_stdout=True) # capture_stderr=True
        )

        ss += kwargs.period
        ix += 1

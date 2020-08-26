import os
import pdb
import ffmpeg
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, help='path to file/stream')
    parser.add_argument('-o', '--output', type=str, help='path to sequence of frames')
    parser.add_argument('-f', '--format', type=str, default='jpg', help='frame image format')
    kwargs = parser.parse_args()

    if not kwargs.input:
        exit('Please pass required "--input" argument')

    output = kwargs.output or os.path.join(
        os.path.dirname(kwargs.input),
        os.path.splitext(kwargs.input)[0] + '_frames',
    )

    if not os.path.exists(output):
        os.mkdir(output)

    ix = 0
    err = None
    info = ffmpeg.probe(kwargs.input)
    duration = float(info['format']['duration'])

    while ix < int(duration):
        name = str(ix).zfill(3) + f'.{kwargs.format.lower()}'
        out, err = (
            ffmpeg
                .input(kwargs.input, ss=ix)
                .output(os.path.join(output, name), vframes=1, vcodec='mjpeg')
                .run(capture_stdout=True) # capture_stderr=True
        )

        ix += 1

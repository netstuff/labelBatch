import os
import pdb
import ffmpeg
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, help='path to file/stream')
    kwargs = parser.parse_args()

    if not kwargs.input:
        exit('Please pass required "--input" argument')

    ix = 0
    err = None
    info = ffmpeg.probe(kwargs.input)
    duration = float(info['format']['duration'])

    while ix < int(duration):
        out, err = (
            ffmpeg
                .input(kwargs.input, ss=ix)
                .output(f'input/frame_{ix + 1}.jpg', vframes=1, vcodec='mjpeg')
                .run(capture_stdout=True) # capture_stderr=True
        )

        ix += 1

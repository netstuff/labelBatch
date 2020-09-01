import os
import json
import argparse
import xml.etree.ElementTree as ET

from util import get_output


def voc_to_json(path, output=None):
    """Covert VOC to JSON."""
    result = []

    for voc in os.listdir(path):
        with open(os.path.join(path, voc), 'r') as fp:
            _, ext = os.path.splitext(voc)

            if ext != '.xml':
                continue

            tree = ET.fromstring(fp.read())
            elem = {
                'file': tree.find('filename').text,
                'objects': [],
            }

            width, height, _ = [int(child.text) for child in tree.find('size')]

            for obj in tree.findall('object'):
                x1, y1, x2, y2 = [int(child.text) for child in obj.find('bndbox')]
                elem['objects'].append({
                    'type': obj.find('name').text,
                    'prob': 1,
                    'bbox': [
                        round(x1 / width, 3),
                        round(y1 / height, 3),
                        round(x2 / width, 3),
                        round(y2 / height, 3),
                    ]
                })

            result.append(elem)

    with open(os.path.join(output), 'w') as fp:
        json.dump(result, fp)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, help='path to source voc-files')
    parser.add_argument('-o', '--output', type=str, help='path to result json-file')
    kwargs = parser.parse_args()

    if not kwargs.input:
        exit('Please pass required "--input" argument')

    output = get_output(kwargs, os.path.join(kwargs.input, 'output.json'))
    voc_to_json(kwargs.input, output)

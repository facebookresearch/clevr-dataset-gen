# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

import argparse, json, os

"""
During rendering, each CLEVR scene file is dumped to disk as a separate JSON
file; this is convenient for distributing rendering across multiple machines.
This script collects all CLEVR scene files stored in a directory and combines
them into a single JSON file. This script also adds the version number, date,
and license to the output file.
"""

parser = argparse.ArgumentParser()
parser.add_argument('--input_dir', default='output/scenes')
parser.add_argument('--output_file', default='output/CLEVR_misc_scenes.json')
parser.add_argument('--version', default='1.0')
parser.add_argument('--date', default='7/8/2017')
parser.add_argument('--license',
           default='Creative Commons Attribution (CC-BY 4.0')


def main(args):
  input_files = os.listdir(args.input_dir)
  scenes = []
  split = None
  for filename in os.listdir(args.input_dir):
    if not filename.endswith('.json'):
      continue
    path = os.path.join(args.input_dir, filename)
    with open(path, 'r') as f:
      scene = json.load(f)
    scenes.append(scene)
    if split is not None:
      msg = 'Input directory contains scenes from multiple splits'
      assert scene['split'] == split, msg
    else:
      split = scene['split']
  scenes.sort(key=lambda s: s['image_index'])
  for s in scenes:
    print(s['image_filename'])
  output = {
    'info': {
      'date': args.date,
      'version': args.version,
      'split': split,
      'license': args.license,
    },
    'scenes': scenes
  }
  with open(args.output_file, 'w') as f:
    json.dump(output, f)


if __name__ == '__main__':
  args = parser.parse_args()
  main(args)


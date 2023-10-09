import os
import re
import struct
import sys
from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize

norm = Normalize(vmin=-1.0, vmax=1.0)
CMAP = LinearSegmentedColormap.from_list("custom_cmap",
                                         [
                                         [norm(-1.0), "0"],
                                         [norm(1.0), "yellow"]
                                         ]
                                         )

"""Source buffer cls"""


class Buffer:
    def __init__(self, buf_path: Path, CF=0):
        """Init numpy array from path to SO dat file"""
        buffer = []
        dat_file = open(buf_path, "rb").read()

        for i in range(0, len(dat_file), 2):
            buffer.append(struct.unpack("<H", dat_file[i: i + 2]))

        self.matrix = np.reshape(np.array(buffer), (2048, 1200)).T
        if str(CF).isdigit() and int(CF) > 0:
            max_matrix = self.matrix.max()
            convert = np.vectorize(lambda x: min(x * int(CF), max_matrix))
            self.matrix = convert(self.matrix)

    def save_jpg(self, jpg_fname: Path) -> None:
        plt.imsave(fname=jpg_fname,
                   arr=self.matrix,
                   cmap=CMAP,
                   format='jpg')

def mkdir_images_from_dat_path(dat_path: Path, CF:int=0) -> str | None:
    """
    creating directory with jpg files by path with dat files
    """
    try:
        buffers = list(dat_path.iterdir())
    except FileNotFoundError as err:
        return str(err)

    image_path = Path('dataset') / 'images'
    os.makedirs(image_path, exist_ok=True)

    for buf in sorted(buffers):
        if not re.search("^SO.*dat$", buf.name):
            continue

        jpg_fname = image_path / (buf.stem + '.jpg')
        if jpg_fname.exists():
            continue

        Buffer(buf_path=buf, CF=CF).save_jpg(jpg_fname=jpg_fname)

def main():
    dat_path = Path('Buffers')
    args = sys.argv[1:]
    CF = args[0] if len(args) > 0 else 0
    mkdir_images_from_dat_path(dat_path=dat_path, CF=int(CF))
    

if __name__ == "__main__":
    main()

import os
from pathlib import Path

def mk_classes(source_path):
    os.makedirs(source_path / 'images', exist_ok=True)
    with open (source_path / 'images' / 'classes.txt', 'w') as f:
        f.write('target\n')

def main():
    mk_classes(Path('dataset'))
    os.system('labelImg dataset/images')


if __name__ == "__main__":
    main()

import re
from pathlib import Path

IMAGES_PATH = Path("dataset") / "images"


def parse_line(source_line: str):
    A, D = 0, 0

    for coord_string in source_line.split(","):
        if len(coord_string.split("=")) >= 2:
            if coord_string.split("=")[0].strip() == "Az":
                A = float(coord_string.split("=")[-1])

            elif coord_string.split("=")[0].strip() == "D":
                D = float(coord_string.split("=")[-1])

    return {"azimuth": A, "distance": D}


def parse_so_txt(source_path):
    row_coordinates_dict = {}
    buf_files_list = list(source_path.iterdir())
    for buf_file in sorted(buf_files_list):
        if not re.search("^SO.*txt$", buf_file.name):
            continue

        with open(buf_file) as f:
            cur_coord_list = []
            for line in f.readlines():
                cur_coord_list.append(parse_line(line))

        for stem in [f.stem for f in list(IMAGES_PATH.iterdir()) if buf_file.stem in f.name]:
            row_coordinates_dict[stem] = cur_coord_list

    return row_coordinates_dict


def create_layout_files(raw_coords_dict):
    for so_name, coord_list in raw_coords_dict.items():
        if len(coord_list) == 0:
            pass
            # os.remove(source_path / 'images' / f"{so_name}.jpg")
        else:
            with open(IMAGES_PATH / f"{so_name}.txt", "a") as f:
                for coord_pair in coord_list:
                    f.write(
                        f"0 {round(coord_pair['azimuth'] / 360, 6)} {round(coord_pair['distance'] /1000 / 360, 6)} {round(10 / 360, 6)} {round(5 / 360, 6)}"
                    )
                    f.write("\n")


if __name__ == "__main__":
    raw_coords_dict = parse_so_txt(Path("Buffers"))
    create_layout_files(raw_coords_dict)
